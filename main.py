"""
Archivo principal para ejecutar tanto el servidor MCP como el proxy web
"""

import threading
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(levelname)s | %(name)s | %(message)s')

logging.basicConfig(
    format=LOG_FORMAT, 
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

def start_mcp_server():
    """Inicia el servidor MCP"""
    from server import mcp, HOST_MCP, PORT_MCP
    logger.info(f"Servidor MCP iniciado en http://{HOST_MCP}:{PORT_MCP}")
    mcp.run(transport="http", host=HOST_MCP, port=PORT_MCP)

def start_proxy_server():
    """Inicia el servidor proxy web"""
    from proxy import start_web_server
    start_web_server()

def main():
    """Función principal que ejecuta ambos servidores"""
    logger.info("Iniciando servidores...")
    
    # Iniciar servidor MCP en un hilo separado
    mcp_thread = threading.Thread(target=start_mcp_server, daemon=True)
    mcp_thread.start()
    
    # Iniciar servidor proxy web en el hilo principal
    start_proxy_server()

if __name__ == "__main__":
    main()
