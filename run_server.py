"""
Script simple para ejecutar el servidor web proxy
"""

import os
import sys
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
HOST_UI = os.getenv('HOST_UI', '127.0.0.1')
PORT_UI = int(os.getenv('PORT_UI', '8001'))
STATIC_DIR = os.getenv('STATIC_DIR', 'static')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

class SimpleWebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.serve_file('index.html', 'text/html')
        elif self.path.startswith('/static/'):
            filename = self.path[8:]
            self.serve_file(filename, self.get_content_type(filename))
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/call_tool':
            self.handle_tool_call()
        else:
            self.send_error(404)

    def serve_file(self, filename, content_type):
        try:
            filepath = os.path.join(STATIC_DIR, filename)
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404)
        except Exception as e:
            logger.error(f"Error serving file {filename}: {e}")
            self.send_error(500)

    def get_content_type(self, filename):
        if filename.endswith('.css'):
            return 'text/css'
        elif filename.endswith('.js'):
            return 'application/javascript'
        elif filename.endswith('.html'):
            return 'text/html'
        else:
            return 'text/plain'

    def handle_tool_call(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            tool_name = request_data.get("name")
            arguments = request_data.get("arguments", {})
            
            # Simple calculation functions
            x = arguments.get("x", 0)
            y = arguments.get("y", 0)
            
            if tool_name == "add":
                result = x + y
            elif tool_name == "subtract":
                result = x - y
            elif tool_name == "multiply":
                result = x * y
            elif tool_name == "divide":
                if y == 0:
                    response = {"error": "Cannot divide by zero"}
                    self.send_json_response(400, response)
                    return
                result = x / y
            else:
                response = {"error": f"Herramienta '{tool_name}' no encontrada"}
                self.send_json_response(400, response)
                return
            
            response = {"content": [{"text": str(result)}]}
            self.send_json_response(200, response)
            
        except Exception as e:
            logger.error(f"Error en call_tool: {str(e)}")
            response = {"error": str(e)}
            self.send_json_response(500, response)

    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def main():
    # Create static directory if it doesn't exist
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)
    
    server = HTTPServer((HOST_UI, PORT_UI), SimpleWebHandler)
    logger.info(f"Servidor web iniciado en http://{HOST_UI}:{PORT_UI}")
    logger.info("Presiona Ctrl+C para detener el servidor")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Servidor detenido")
        server.shutdown()

if __name__ == "__main__":
    main()
