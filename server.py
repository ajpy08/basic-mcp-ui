"""
Servidor MCP - Solo herramientas de cálculo
Este archivo contiene únicamente las herramientas MCP y su ejecución
"""

from fastmcp import FastMCP
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables
HOST_MCP = os.getenv('HOST_MCP', '127.0.0.1')
PORT_MCP = int(os.getenv('PORT_MCP', '8000'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(levelname)s | %(name)s | %(message)s')
APP_NAME = os.getenv('APP_NAME', 'Calculator Server')

# Configure logging
logging.basicConfig(
    format=LOG_FORMAT, 
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

# Initialize MCP server
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

# Start MCP server
if __name__ == "__main__":
    logger.info(f"Servidor MCP iniciado en http://{HOST_MCP}:{PORT_MCP}")
    mcp.run(transport="http", host=HOST_MCP, port=PORT_MCP)
