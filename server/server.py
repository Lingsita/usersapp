import re
import cgi
import base64
from http import cookies
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
        return 404, None, False


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
        (status_code, route_response, do_logout) = self.__router.route(self.path)
        if status_code == 404:
            self.send_response(status_code)
            self.end_headers()
        elif status_code == 301:
            self.send_response(status_code)
            if do_logout:
                self.set_cookie()
            self.send_header('Location', route_response)
            self.end_headers()
        else:
            self.send_response(status_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(route_response, encoding='utf-8'))


    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        (status_code, route_response, do_login) = self.__router.route(self.path, postvars=postvars, method='POST')

        if status_code == 404:
            self.send_response(status_code)
            self.end_headers()
        elif status_code == 301:
            self.send_response(status_code)
            if do_login:
                self.set_cookie(user_credentials=postvars)
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
        return base64.b64encode(username + password)

    def set_cookie(self, user_credentials=None):
        if user_credentials:
            username = user_credentials.get(b'username')[0]
            password = user_credentials.get(b'password')[0]
            key = self.generate_key(username, password)
            self.send_header('Set-Cookie', 'session_key='+key.decode("utf-8"))
        else:
            self.send_header('Set-Cookie', 'session_key=deleted')