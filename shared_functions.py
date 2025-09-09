"""
Funciones compartidas de cálculo
Estas funciones pueden ser usadas tanto por el servidor MCP como por el servidor web
"""

import logging

# Configure logging
logger = logging.getLogger(__name__)

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
