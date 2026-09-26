import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

port = int(os.environ.get("PORT", 10000))

class Handler(SimpleHTTPRequestHandler):
    pass

server = HTTPServer(("0.0.0.0", port), Handler)

print("SERVER IS RUNNING ON PORT", port)

server.serve_forever()
