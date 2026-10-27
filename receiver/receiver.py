import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 5001
OUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test-report.json")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Test report receiver is running.")

    def do_POST(self):
        if self.path != "/report":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return
        with open(OUT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[RECEIVED] status={data.get('overall_status')} commit={data.get('commit_sha')} -> saved {OUT_FILE}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Report saved")


if __name__ == "__main__":
    print(f"Receiver listening on http://127.0.0.1:{PORT}/report  (Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()