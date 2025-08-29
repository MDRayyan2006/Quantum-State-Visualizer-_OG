import http.server
import socketserver
import os

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Get the absolute path to the requested file
        path = super().translate_path(path)
        
        # If the request is for documentation assets, serve from current directory
        doc_path = os.path.abspath('.')
        relative_path = os.path.relpath(path, os.getcwd())
        return os.path.join(doc_path, relative_path)

    def end_headers(self):
        # Add security headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('X-Content-Type-Options', 'nosniff')
        
        # Set cache-control for better performance
        if self.path.endswith('.css') or self.path.endswith('.js') or self.path.endswith('.png'):
            self.send_header('Cache-Control', 'max-age=604800')  # 1 week
        else:
            self.send_header('Cache-Control', 'no-cache')
            
        super().end_headers()

    def guess_type(self, path):
        # Improve MIME type detection
        if path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.tsx'):
            return 'application/typescript'
        elif path.endswith('.ts'):
            return 'application/typescript'
        return super().guess_type(path)

# No need to change directory, serve from current directory

with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
    print(f"Serving documentation on port {PORT}...")
    print("Open your browser and go to http://localhost:8000")
    print("Serving files from: ", os.getcwd())
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()