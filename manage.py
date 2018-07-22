import http.server
import socketserver
import argparse

from server import RequestHandler

DEFAULT_PORT = 8000

Handler = RequestHandler


def run(port=8000):
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print("serving at port", port)
            httpd.serve_forever()
    except:
        print("Shutting down...")
        httpd.socket.close()


def get_port():
    parser = argparse.ArgumentParser()
   
    parser.add_argument(
        '-p', '--port', type=int, help='Port number, default 8000', required=False, nargs='+')
    
    args = parser.parse_args()
    port = int(args.port[0]) if args.port else DEFAULT_PORT
    return port


if __name__ == "__main__":
    run(get_port())
