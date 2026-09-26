import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class WebsiteHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/ask":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body.decode("utf-8"))
            question = data.get("question", "").strip()

            if not question:
                self.send_json({"answer": "Please write a question."})
                return

            response = client.responses.create(
                model="gpt-5.6-mini",
                input=question
            )

            self.send_json({
                "answer": response.output_text
            })

        except Exception as error:
            print("ERROR:", error)
            self.send_json({
                "answer": "Sorry, an error occurred."
            })

    def send_json(self, data):
        result = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header(
            "Content-Length",
            str(len(result))
        )
        self.end_headers()
        self.wfile.write(result)


port = int(os.environ.get("PORT", 8000))

server = HTTPServer(
    ("0.0.0.0", port),
    WebsiteHandler
)

print("Server running on port", port)

server.serve_forever()
