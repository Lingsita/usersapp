import re
import cgi
import base64
from urllib.parse import parse_qs
from http.server import CGIHTTPRequestHandler


class Router:

    def __init__(self):
        self.__routes = []

    def register(self, regexp, controller):
        self.__routes.append({'regexp': regexp, 'controller': controller})

    def route(self, path, *args, **kwargs):
        for route in self.__routes:
            if re.search(r'^'+route['regexp']+'$', path):
                func = route['controller']
                return func(*args, **kwargs)
        return 404


class RequestHandler(CGIHTTPRequestHandler):
    '''
    Handler for HTTP Requests, search for routes and redirect
    '''
    __router = Router()

    def __init__(self, request, client_address, server):

        super(RequestHandler, self).__init__(request, client_address, server)

    @classmethod
    def get_router(cls):
        return cls.__router

    def do_GET(self):
        status_code, route_response = self.__router.route(self.path)
        if status_code == 404:
            self.send_response(status_code)
            self.end_headers()
        elif status_code == 301:
            self.send_response(status_code)
            new_path = (route_response)
            self.send_header('Location', new_path)
            self.end_headers()
        else:
            self.send_response(status_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(route_response, encoding='utf-8'))


    def do_POST(self):
        request_headers = self.headers
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        status_code, route_response = self.__router.route(self.path, postvars=postvars, method='POST')

        if status_code == 404:
            self.send_response(status_code)
            self.end_headers()
        elif status_code == 301:
            self.send_response(status_code)
            new_path = (route_response)
            self.send_header('Location', new_path)
            self.end_headers()
        else:
            self.send_response(status_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(route_response, encoding='utf-8'))

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    @staticmethod
    def generate_key(username, password):
        return base64.b64encode('%s:%s' % (username, password))

    def is_authenticated(self):
        auth_header = self.headers.get('Authorization')
        return auth_header and auth_header == 'Basic ' + self.generate_key()

    def try_authenticate(self):
        if not self.is_authenticated():
            self.do_AUTHHEAD()
            self.wfile.write('not authenticated')
            return False
        return True