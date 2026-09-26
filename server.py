import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class Handler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.end_headers()

        self.wfile.write(
            json.dumps(data, ensure_ascii=False).encode("utf-8")
        )

    def do_OPTIONS(self):
        self.send_json({})

    def do_POST(self):

        if self.path != "/ask":
            self.send_json({"error": "Wrong path"}, 404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

            data = json.loads(body)
            question = data.get("question", "").strip()

            if not question:
                self.send_json({"error": "السؤال فارغ"}, 400)
                return

            print("Question:", question)

            response = client.responses.create(
                model="gpt-5-mini",
                input=question
            )

            answer = response.output_text

            print("Answer:", answer)

            self.send_json({
                "answer": answer
            })

        except Exception as e:

            print("ERROR:", str(e))

            self.send_json({
                "error": str(e)
            }, 500)


server = HTTPServer(("127.0.0.1", 8000), Handler)

print("SERVER STARTED")
print("http://127.0.0.1:8000")

server.serve_forever()
