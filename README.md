# Python miscellaneous code

This code can be used as a template for other Python projects.

## Scripts overview

### [`dump_http_server.py`](scripts/dump_http_server.py)

Server that dump all requests in console and save request headers (as `header.json`) and request bodies (as `body` file)
at disk.

Examples cURL queries:

```sh
    $ curl -X POST -H "Content-Type: application/json" -d '{"k": "v"}' http://localhost:8001/a/b?c=d
    $ curl -X POST -F "data=@README.md" http://localhost:8001/file
```

## License

Distributed under MIT license.
