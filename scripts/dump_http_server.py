#!/usr/bin/env python

import json
import os
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


class Type(str, Enum):
    HTML = "html"
    JSON = "json"


@dataclass
class State:
    requests_counter: int


class StoppableHTTPServer(HTTPServer):
    def run(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print("\nStopping server...")
            # Clean-up the server: close socket, etc.
            self.server_close()


class DebugRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, response: Type, out: Path, state: State, *args, **kwargs) -> None:
        self.response = response
        self.out = out
        self.state = state

        super(DebugRequestHandler, self).__init__(*args, **kwargs)

    def log_message(self, *args, **kwargs) -> None:
        pass

    def _html(self, data: str) -> None:
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(data.encode("UTF-8"))

    def _json(self, data: str | dict) -> None:
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(data).encode("UTF-8"))

    def _process_action(self, action: str) -> None:
        print(f"{action} {self.path}")

        self.state.requests_counter += 1
        suffix = f"{self.state.requests_counter:03d}"

        # Headers.
        self.out.mkdir(parents=True, exist_ok=True)
        headers_path = Path(self.out, f"headers_{suffix}.json")
        with open(headers_path, "w", encoding="UTF-8") as f:
            json.dump(dict(self.headers), f, indent=4)
        print(f"    Headers saved at {headers_path}")

        # Body.
        body_path = None
        if content_len := self.headers.get("Content-Length"):
            self.out.mkdir(parents=True, exist_ok=True)
            body_path = Path(self.out, f"body_{suffix}")
            with open(body_path, "bw") as f:
                body = self.rfile.read(int(content_len))
                f.write(body)
            print(f"    Body saved at {body_path}")
        else:
            print("    No body")

        # Response.
        self.send_response(200)
        if self.response == Type.HTML:
            if body_path:
                self._html(f"<h3>Request data saved at {body_path.as_posix()}</h1>")
            else:
                self._html("")
        elif self.response == Type.JSON:
            if body_path:
                self._json({"saved_at": body_path.as_posix()})
            else:
                self._json({})
        else:
            raise RuntimeError(f"Unsupportable type '{self.response}'")

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
    parser = ArgumentParser(prog="Dump HTTP Server", description="Dump all requests that came to the server")
    parser.add_argument(
        "--host",
        nargs="?",
        type=str,
        default="0.0.0.0",
        help="Address of server",
    )
    parser.add_argument(
        "--port",
        nargs="?",
        type=int,
        default=8001,
        help="Port that will be listening",
    )
    parser.add_argument(
        "--response",
        nargs="?",
        type=Type,
        default=Type.JSON,
        help="Provide response on every request or not",
    )
    parser.add_argument(
        "--out",
        nargs="?",
        type=Path,
        default="tmp",
        help="Output directory where script save requests",
    )
    args = parser.parse_args()

    print(f"Start Dump HTTP Server at {args.host}:{args.port}")
    print("Press Ctrl+C to stop")

    holder_dir = Path(args.out, datetime.now().strftime("%Y.%m.%d_%H-%M-%S"))
    os.makedirs(holder_dir, exist_ok=True)

    state = State(requests_counter=0)

    custom_handler = partial(DebugRequestHandler, args.response, holder_dir, state)
    server = StoppableHTTPServer((args.host, args.port), custom_handler)
    server.run()
