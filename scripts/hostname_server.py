#!/usr/bin/env python

from argparse import ArgumentParser
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from socket import gethostname


class HostnameHandler(BaseHTTPRequestHandler):

    def __init__(self, name: str, *args, **kwargs) -> None:
        self.name = name

        super(HostnameHandler, self).__init__(*args, **kwargs)

    def log_message(self, *args, **kwargs) -> None:
        pass

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(f"Current hostname is '{self.name}'\n".encode("utf-8"))


if __name__ == "__main__":
    parser = ArgumentParser(prog="Hostname HTTP Server", description="Return current hostname")
    parser.add_argument("--host", nargs="?", type=str, default="0.0.0.0")
    parser.add_argument("--port", nargs="?", type=int, default=8000)
    parser.add_argument("--name", nargs="?", type=str, default=gethostname())
    args = parser.parse_args()

    print(f"Start Hostname HTTP Server at {args.host}:{args.port}")

    custom_handler = partial(HostnameHandler, args.name)
    server = HTTPServer((args.host, args.port), custom_handler)
    server.serve_forever()
