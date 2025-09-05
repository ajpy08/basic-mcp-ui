#!/usr/bin/env python3
"""
Servidor web simple para la calculadora MCP
"""

import http.server
import socketserver
import os
import json
from urllib.parse import urlparse, parse_qs

# Configuración
PORT = 8001
STATIC_DIR = "static"

class CalculatorHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/call_tool':
            self.handle_tool_call()
        else:
            self.send_error(404)
    
    def handle_tool_call(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            tool_name = request_data.get("name")
            arguments = request_data.get("arguments", {})
            
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
                    self.send_json_response(400, {"error": "Cannot divide by zero"})
                    return
                result = x / y
            else:
                self.send_json_response(400, {"error": f"Herramienta '{tool_name}' no encontrada"})
                return
            
            self.send_json_response(200, {"content": [{"text": str(result)}]})
            
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})
    
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
    # Crear directorio estático si no existe
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)
    
    try:
        with socketserver.TCPServer(("", PORT), CalculatorHandler) as httpd:
            print(f"Servidor iniciado en http://localhost:{PORT}")
            print("Presiona Ctrl+C para detener")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
