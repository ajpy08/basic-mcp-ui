from fastmcp import FastMCP
import logging
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables
HOST_MCP = os.getenv('HOST_MCP', '127.0.0.1')
PORT_MCP = int(os.getenv('PORT_MCP', '8000'))
HOST_UI = os.getenv('HOST_UI', '127.0.0.1')
PORT_UI = int(os.getenv('PORT_UI', '8001'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(levelname)s | %(name)s | %(message)s')
APP_NAME = os.getenv('APP_NAME', 'Calculator Server')
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

mcp = FastMCP(APP_NAME)

# Core calculation functions
def add_numbers(x: float, y: float) -> float:
    """Add two numbers and return the result."""
    logger.info(f"Add operation: {x} + {y}")
    result = x + y
    logger.info(f"Add result: {result}")
    return result

def subtract_numbers(x: float, y: float) -> float:
    """Subtract two numbers and return the result."""
    logger.info(f"Subtract operation: {x} - {y}")
    result = x - y
    logger.info(f"Subtract result: {result}")
    return result

def multiply_numbers(x: float, y: float) -> float:
    """Multiply two numbers and return the result."""
    logger.info(f"Multiply operation: {x} * {y}")
    result = x * y
    logger.info(f"Multiply result: {result}")
    return result

def divide_numbers(x: float, y: float) -> float:
    """Divide two numbers and return the result."""
    logger.info(f"Divide operation: {x} / {y}")
    if y == 0:
        logger.error("Division by zero attempted")
        raise ValueError("Cannot divide by zero")
    result = x / y
    logger.info(f"Divide result: {result}")
    return result

# MCP tool wrappers
@mcp.tool(description="Add two numbers together")
def add(x: float, y: float) -> float:
    """Add two numbers and return the result."""
    return add_numbers(x, y)

@mcp.tool(description="Subtract two numbers")
def subtract(x: float, y: float) -> float:
    """Subtract two numbers and return the result."""
    return subtract_numbers(x, y)

@mcp.tool(description="Multiply two numbers")
def multiply(x: float, y: float) -> float:
    """Multiply two numbers and return the result."""
    return multiply_numbers(x, y)

@mcp.tool(description="Divide two numbers")
def divide(x: float, y: float) -> float:
    """Divide two numbers and return the result."""
    return divide_numbers(x, y)

# Create static directory if it doesn't exist
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
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

    def serve_config(self):
        """Serve configuration for the frontend"""
        config = {
            "mcp_host": HOST_MCP,
            "mcp_port": PORT_MCP,
            "ui_host": HOST_UI,
            "ui_port": PORT_UI
        }
        self.send_json_response(200, config)

    def handle_tool_call(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            tool_name = request_data.get("name")
            arguments = request_data.get("arguments", {})
            
            # Call the core calculation functions directly
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
            
            response = {"content": [{"text": str(result)}]}
            self.send_json_response(200, response)
            
        except Exception as e:
            logger.error(f"Error en call_tool: {str(e)}")
            response = {"error": str(e)}
            self.send_json_response(500, response)

    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', CORS_ORIGINS)
        self.send_header('Access-Control-Allow-Methods', CORS_METHODS)
        self.send_header('Access-Control-Allow-Headers', CORS_HEADERS)
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', CORS_ORIGINS)
        self.send_header('Access-Control-Allow-Methods', CORS_METHODS)
        self.send_header('Access-Control-Allow-Headers', CORS_HEADERS)
        self.end_headers()

def start_web_server():
    server = HTTPServer((HOST_UI, PORT_UI), WebHandler)
    logger.info(f"Servidor web iniciado en http://{HOST_UI}:{PORT_UI}")
    server.serve_forever()

# Start web server in a separate thread
web_thread = threading.Thread(target=start_web_server, daemon=True)
web_thread.start()

# Start MCP server
logger.info(f"Servidor MCP iniciado en http://{HOST_MCP}:{PORT_MCP}")
mcp.run(transport="http", host=HOST_MCP, port=PORT_MCP)
