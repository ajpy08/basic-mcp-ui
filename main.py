"""
Archivo principal para ejecutar tanto el servidor MCP como el servidor web
"""

import threading
import logging
import os
import time
from dotenv import load_dotenv

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
    try:
        from mcp_server import main as mcp_main
        mcp_main()
    except Exception as e:
        logger.error(f"Error iniciando servidor MCP: {e}")

def start_web_server():
    """Inicia el servidor web"""
    try:
        from web_server import main as web_main
        web_main()
    except Exception as e:
        logger.error(f"Error iniciando servidor web: {e}")

def main():
    """Función principal que ejecuta ambos servidores"""
    logger.info("🚀 Iniciando servidores...")
    
    # Iniciar servidor MCP en un hilo separado
    mcp_thread = threading.Thread(target=start_mcp_server, daemon=True)
    mcp_thread.start()
    
    # Esperar un momento para que el servidor MCP se inicie
    import time
    time.sleep(1)
    
    # Iniciar servidor web en el hilo principal
    logger.info("✅ Servidor MCP iniciado en segundo plano")
    logger.info("🌐 Iniciando servidor web...")
    start_web_server()

if __name__ == "__main__":
    main()
