import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

PORT = int(os.environ.get("PORT", 10000))


class Handler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):

        if self.path != "/ask":
            self.send_json({"error": "Not found"}, 404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

            data = json.loads(body.decode("utf-8"))
            question = data.get("question", "").strip()

            if not question:
                self.send_json({"error": "No question"}, 400)
                return

            response = client.responses.create(
                model="gpt-5.6-luna",
                instructions="Answer the user's question clearly and helpfully.",
                input=question
            )

            self.send_json({
                "answer": response.output_text
            })

        except Exception as e:
            print("ERROR:", e, flush=True)
            self.send_json({
                "error": "Server error"
            }, 500)


server = HTTPServer(("0.0.0.0", PORT))

print("SERVER IS RUNNING ON PORT", PORT, flush=True)

server.serve_forever()
