# Python miscellaneous code

This code can be used as a template for other Python projects.

Uses Python 3.

## Scripts overview

### [`utils.py`](scripts/utils.py)

Contain utility methods:

-   `sizeof_fmt` return integer value in bytes in human-readable format;
-   `permissions_str` return string representation of octal of Unix permissions;
-   `permissions_oct` return octal representation of string value of Unix permissions;
-   `repeat_if` repeat method call if exception happens;
-   `check_if_url_available` open given URL and check if response is 200.

### [`dump_http_server.py`](scripts/dump_http_server.py)

Server that dump all requests in console and save request headers (as `header.json`) and request bodies (as `body` file)
at disk.

Examples cURL queries:

```sh
    $ curl -X POST -H "Content-Type: application/json" -d '{"k": "v"}' http://localhost:8001/a/b?c=d
    $ curl -X POST -F "data=@README.md" http://localhost:8001/file
```

### [`proxy_get_http_server.py`](scripts/proxy_get_http_server.py)

Proxy server for HTTP GET requests. You are provide `hostname:port/path` as a request parameters:

```sh
    $ curl http://localhost:8002/google.com:80/
```

## License

Distributed under MIT license.
