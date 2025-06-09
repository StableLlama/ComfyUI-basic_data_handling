"""Top-level package for basic_data_handling."""
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

from src.basic_data_handling import NODE_CLASS_MAPPINGS
from src.basic_data_handling import NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./web"
