import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from openai import OpenAI

API_KEY = os.environ.get("OPENAI_API_KEY")

if not API_KEY:
    print("ERROR: OPENAI_API_KEY is not set.")
    raise SystemExit

client = OpenAI(api_key=API_KEY)


class Server(BaseHTTPRequestHandler):

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(
            json.dumps(data, ensure_ascii=False).encode("utf-8")
        )

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.end_headers()

    def do_POST(self):
        if self.path != "/ask":
            self._send_json({"error": "Unknown path"}, 404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)

            question = data.get("question", "").strip()

            if not question:
                self._send_json({"error": "لم يتم إرسال سؤال"}, 400)
                return

            response = client.responses.create(
                model="gpt-5-mini",
                input=question
            )

            answer = response.output_text

            self._send_json({"answer": answer})

        except Exception as e:
            print("ERROR:", e)
            self._send_json({
                "error": "حدث خطأ في الخادم",
                "details": str(e)
            }, 500)


server = HTTPServer(("127.0.0.1", 8000), Server)

print("Server is running...")
print("http://127.0.0.1:8000")

server.serve_forever()
