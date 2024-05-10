#!/usr/bin/env python

import re
from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen

REQUEST_TIMEOUT_SEC = 5

REQUEST = re.compile(r"^/?([^/]+)(/.*)$")


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        m = REQUEST.match(self.path)
        if not m:
            print("Use format /host:port/path")
            return

        host_port = m.group(1)
        path = m.group(2)
        url = f"http://{host_port}{path}"

        try:
            with urlopen(url, timeout=REQUEST_TIMEOUT_SEC) as resp:
                self.send_response(resp.status)
                self.end_headers()

                data_bin = resp.read()
                self.wfile.write(data_bin)
        except Exception as e:
            self.send_response(200)
            self.end_headers()

            self.wfile.write(str(e).encode("utf-8"))


if __name__ == "__main__":
    parser = ArgumentParser(prog="Proxy GET HTTP Server", description="Make proxy GET requests to another hosts")
    parser.add_argument("--host", nargs="?", type=str, default="0.0.0.0")
    parser.add_argument("--port", nargs="?", type=int, default=8002)
    args = parser.parse_args()

    print(f"Start Proxy GET HTTP Server at {args.host}:{args.port}")

    httpd = HTTPServer((args.host, args.port), RequestHandler)
    httpd.serve_forever()
