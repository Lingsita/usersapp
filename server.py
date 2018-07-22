from http.server import SimpleHTTPRequestHandler
import re


class RequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, request, client_address, server):

        self.__router = Router(self)

        super(RequestHandler, self).__init__(request, client_address, server)

    def do_GET(self):
        print(self.path)
        route_response = self.__router.route(self.request, self.path)
        if not route_response == 404:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Hello world', encoding='utf-8'))
        else:
            self.__server.send_response(404)
            self.__server.end_headers()


    def do_POST(self):
        request_path = self.path

        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0

        print(self.rfile.read(length))

        self.send_response(200)


class BaseRouter(object):

    def __init__(self, server):
        self.__routes = []

    def register(self, regexp, controller, name):
        self.__routes.append({'regexp': regexp, 'controller': controller, 'name': name})

    def route(self, request, path):
        for route in self.__routes:
            if re.search(route['regexp'], path):
                cls = globals()[route['controller']]
                func = cls.__dict__[route['controller']]
                func(request)
                return
        return "404"


class Router(object):
    def register(self, regexp, controller, name):
        super(Router, self).register( regexp, controller, name)
