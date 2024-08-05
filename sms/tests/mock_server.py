import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set HTTP 200
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Data example
        response_content = [
            {"number": "6664565590", "name": "User3"},
            {"number": "6667656621", "name": "User4"}
        ]

        # Send JSON data
        self.wfile.write(bytes(json.dumps(response_content), "utf8"))

    def do_POST(self):
        self.send_response(501)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"POST method not supported by this server.")


def run(server_class=HTTPServer, handler_class=MockServerRequestHandler, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting mock server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
