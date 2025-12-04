"""
Simple standalone Tesouraria Application (No Dependencies)
This is a minimal HTTP server that demonstrates the deployment setup without external dependencies.
Replace this with your actual application code.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime

class TesourariaHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler for Tesouraria."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'message': 'Welcome to Tesouraria - Personal Finance Management',
                'status': 'running',
                'version': '1.0.0'
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat(),
                'service': 'tesouraria'
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'application': 'Tesouraria',
                'environment': os.getenv('NODE_ENV', 'development'),
                'port': os.getenv('PORT', '8080')
            }
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Not Found'}
            self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        """Log requests to stdout."""
        print(f"{self.address_string()} - [{self.log_date_time_string()}] {format % args}")

def run_server():
    """Start the HTTP server."""
    port = int(os.getenv('PORT', 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, TesourariaHandler)
    
    print(f"Starting Tesouraria on port {port}")
    print(f"Environment: {os.getenv('NODE_ENV', 'development')}")
    print(f"Access the application at: http://localhost:{port}")
    print(f"Health check endpoint: http://localhost:{port}/health")
    print(f"\nPress Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
