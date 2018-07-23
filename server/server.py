from http.server import SimpleHTTPRequestHandler
import re


class Router:

    def __init__(self):
        self.__routes = []

    def register(self, regexp, controller):
        self.__routes.append({'regexp': regexp, 'controller': controller})
        print(self.__routes)

    def route(self, request, path):
        for route in self.__routes:
            if re.search(r'^'+route['regexp']+'$', path):
                func = route['controller']
                return func(request)
        return 404


class RequestHandler(SimpleHTTPRequestHandler):
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
        print(self.path)
        route_response = self.__router.route(self.request, self.path)
        if not route_response == 404:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Hello world', encoding='utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


    def do_POST(self):
        request_path = self.path

        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0

        print(self.rfile.read(length))

        self.send_response(200)




