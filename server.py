from BaseHTTPServer import BaseHTTPRequestHandler
from SocketServer import TCPServer

PORT = 8080


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        method_name = "GET_" + self.path.strip('/')
        try:
            method = getattr(self, method_name)
        except AttributeError:
            self.send_error(404)
            return
        method()

    def GET_too_many_redirects(self):
        """
        http://127.0.0.1:8080/too_many_redirects
        """
        self.send_response(302)
        self.send_header("Content-Length", 0)
        self.send_header("Location", self.path)
        self.end_headers()
        return None

    def GET_headers_multiple_location(self):
        """
        http://127.0.0.1:8080/headers_multiple_location
        """
        self.send_response(302)
        self.send_header("Content-Length", 0)
        self.send_header("Location", self.path)
        self.send_header("Location", self.path + '/wrong')
        self.end_headers()
        return None

    def GET_headers_multiple_content_length(self):
        """
        http://127.0.0.1:8080/headers_multiple_content_length
        """
        self.send_response(200)
        self.send_header("Content-Length", 0)
        self.send_header("Content-Length", 1)
        self.end_headers()
        return None

    def GET_headers_multiple_content_disposition(self):
        """
        http://127.0.0.1:8080/headers_multiple_content_disposition
        """
        self.send_response(200)
        self.send_header("Content-Length", 0)
        self.send_header("Content-Disposition", "inline")
        self.send_header("Content-Disposition", "attachment")
        self.end_headers()
        return None

    def GET_content_length_mismatch(self):
        """
        http://127.0.0.1:8080/content_length_mismatch
        """
        self.send_response(200)
        self.send_header("Content-Length", 234234234)
        self.end_headers()
        return None

    def GET_invalid_http_response(self):
        """
        http://127.0.0.1:8080/invalid_http_response
        """
        self.wfile.write("blah")
        self.end_headers()
        return None


server = TCPServer(("", PORT), MyHandler)

server.serve_forever()
