"""Top-level package for basic_data_handling."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """Basic data handling"""
__email__ = "stablellama@tutanota.com"
__version__ = "0.0.1"

from .src.basic_data_handling.nodes import NODE_CLASS_MAPPINGS
from .src.basic_data_handling.nodes import NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./web"
