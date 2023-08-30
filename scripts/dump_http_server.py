#!/usr/bin/env python

import argparse
import json
import os
from datetime import datetime
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


class DebugRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, out: Path, *args, **kwargs) -> None:
        self.out = out

        super(DebugRequestHandler, self).__init__(*args, **kwargs)

    def log_message(self, *args, **kwargs) -> None:
        pass

    def _html(self, data: str) -> None:
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(data.encode("utf-8"))

    def _json(self, data: str | dict) -> None:
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _process_action(self, action: str) -> Path:
        print(f"{action} {self.path}")
        holder_name = datetime.now().strftime("%Y.%m.%d_%H-%M-%S")
        holder_dir = Path(self.out, holder_name)
        os.makedirs(holder_dir, exist_ok=True)

        # Headers
        headers_path = Path(holder_dir, "headers.json")
        print(f"    Headers saved at {headers_path}")
        with open(headers_path, "w", encoding="UTF-8") as f:
            json.dump(dict(self.headers), f, indent=4)

        # Body
        if content_len := self.headers.get("Content-Length"):
            body_path = Path(holder_dir, "body")
            print(f"    Body saved at {body_path}")
            body = self.rfile.read(int(content_len))
            with open(body_path, "bw") as f:
                f.write(body)
        else:
            print("    No body")

        # Response.
        self.send_response(200)
        # self._html(f"<h3>Request data saved at {holder_dir}</h1>")
        self._json({"saved_at": holder_dir.as_posix()})

    def do_GET(self) -> None:
        self._process_action("GET")

    def do_HEAD(self) -> None:
        self._process_action("HEAD")

    def do_POST(self) -> None:
        self._process_action("POST")

    def do_PUT(self) -> None:
        self._process_action("PUT")

    def do_DELETE(self) -> None:
        self._process_action("DELETE")

    def do_CONNECT(self) -> None:
        self._process_action("CONNECT")

    def do_OPTIONS(self) -> None:
        self._process_action("OPTIONS")

    def do_TRACE(self) -> None:
        self._process_action("TRACE")

    def do_PATCH(self) -> None:
        self._process_action("PATCH")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Dump HTTP Server",
        description="Dump all requests that came to the server",
    )
    parser.add_argument("--host", nargs="?", type=str, default="0.0.0.0")
    parser.add_argument("--port", nargs="?", type=int, default=8001)
    parser.add_argument("--out", nargs="?", type=Path, default="tmp")
    args = parser.parse_args()

    print(f"Start Dump HTTP Server at {args.host}:{args.port}")

    custom_handler = partial(DebugRequestHandler, args.out)
    server = HTTPServer((args.host, args.port), custom_handler)
    server.serve_forever()
