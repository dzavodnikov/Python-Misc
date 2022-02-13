from http.server import SimpleHTTPRequestHandler
import socketserver


SEPARATOR_LEN = 32


class CustomRequestHandler(SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        request_path = self.path
        request_headers = self.headers

        print(f'GET {request_path}')
        print("-" * SEPARATOR_LEN)
        print(request_headers)

        print("=" * SEPARATOR_LEN)

        self.send_response(200)

    def do_POST(self):
        request_path = self.path
        request_headers = self.headers

        print(f'POST {request_path}')
        print("-" * SEPARATOR_LEN)
        print(request_headers)

        length_str = request_headers.get('Content-Length')
        length = int(length_str) if length_str else 0
        body = self.rfile.read(length) if length > 0 else None
        if body: print(body)
        print("=" * SEPARATOR_LEN)

        self.send_response(200)


def run(host, port):
    with socketserver.TCPServer((host, port), CustomRequestHandler) as httpd:
        print(f'Listening on {host}:{port}')
        print("=" * SEPARATOR_LEN)
        httpd.serve_forever()


if __name__ == "__main__":
    run("0.0.0.0", 8080)
