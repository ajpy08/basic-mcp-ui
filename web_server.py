"""
Servidor Web - Interfaz web para la calculadora MCP
Maneja las peticiones HTTP y sirve la interfaz web
"""

import os
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
from shared_functions import add_numbers, subtract_numbers, multiply_numbers, divide_numbers

# Load environment variables
load_dotenv()

# Get configuration from environment variables
HOST_UI = os.getenv('HOST_UI', '127.0.0.1')
PORT_UI = int(os.getenv('PORT_UI', '8001'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(levelname)s | %(name)s | %(message)s')
STATIC_DIR = os.getenv('STATIC_DIR', 'static')
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
CORS_METHODS = os.getenv('CORS_METHODS', 'GET,POST,OPTIONS')
CORS_HEADERS = os.getenv('CORS_HEADERS', 'Content-Type')

# Configure logging
logging.basicConfig(
    format=LOG_FORMAT, 
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

class WebHandler(BaseHTTPRequestHandler):
    """Manejador HTTP para la interfaz web"""
    
    def do_GET(self):
        """Maneja peticiones GET"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_file('index.html', 'text/html')
        elif self.path == '/config':
            self.serve_config()
        elif self.path.startswith('/static/'):
            filename = self.path[8:]  # Remove '/static/'
            self.serve_file(filename, self.get_content_type(filename))
        else:
            self.send_error(404)

    def do_POST(self):
        """Maneja peticiones POST"""
        if self.path == '/call_tool':
            self.handle_tool_call()
        else:
            self.send_error(404)

    def serve_file(self, filename, content_type):
        """Sirve archivos estáticos"""
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
        """Determina el tipo de contenido basado en la extensión del archivo"""
        if filename.endswith('.css'):
            return 'text/css'
        elif filename.endswith('.js'):
            return 'application/javascript'
        elif filename.endswith('.html'):
            return 'text/html'
        else:
            return 'text/plain'

    def serve_config(self):
        """Sirve la configuración para el frontend"""
        from dotenv import load_dotenv
        load_dotenv()
        
        config = {
            "mcp_host": os.getenv('HOST_MCP', '127.0.0.1'),
            "mcp_port": int(os.getenv('PORT_MCP', '8000')),
            "ui_host": HOST_UI,
            "ui_port": PORT_UI
        }
        self.send_json_response(200, config)

    def handle_tool_call(self):
        """Maneja las llamadas a herramientas de cálculo"""
        try:
            # Leer datos de la petición
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            tool_name = request_data.get("name")
            arguments = request_data.get("arguments", {})
            
            # Llamar a la función correspondiente
            if tool_name == "add":
                result = add_numbers(arguments.get("x", 0), arguments.get("y", 0))
            elif tool_name == "subtract":
                result = subtract_numbers(arguments.get("x", 0), arguments.get("y", 0))
            elif tool_name == "multiply":
                result = multiply_numbers(arguments.get("x", 0), arguments.get("y", 0))
            elif tool_name == "divide":
                result = divide_numbers(arguments.get("x", 0), arguments.get("y", 0))
            else:
                response = {"error": f"Herramienta '{tool_name}' no encontrada"}
                self.send_json_response(400, response)
                return
            
            # Enviar respuesta exitosa
            response = {"content": [{"text": str(result)}]}
            self.send_json_response(200, response)
            
        except Exception as e:
            logger.error(f"Error en call_tool: {str(e)}")
            response = {"error": str(e)}
            self.send_json_response(500, response)

    def send_json_response(self, status_code, data):
        """Envía una respuesta JSON"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', CORS_ORIGINS)
        self.send_header('Access-Control-Allow-Methods', CORS_METHODS)
        self.send_header('Access-Control-Allow-Headers', CORS_HEADERS)
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        """Maneja peticiones OPTIONS para CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', CORS_ORIGINS)
        self.send_header('Access-Control-Allow-Methods', CORS_METHODS)
        self.send_header('Access-Control-Allow-Headers', CORS_HEADERS)
        self.end_headers()

def main():
    """Función principal para ejecutar solo el servidor web"""
    # Crear directorio estático si no existe
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)
        logger.info(f"Directorio {STATIC_DIR} creado")
    
    server = HTTPServer((HOST_UI, PORT_UI), WebHandler)
    logger.info(f"Servidor web iniciado en http://{HOST_UI}:{PORT_UI}")
    logger.info("Presiona Ctrl+C para detener")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Servidor web detenido")

if __name__ == "__main__":
    main()
