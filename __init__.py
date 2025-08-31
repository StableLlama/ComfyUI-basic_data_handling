"""Top-level package for basic_data_handling."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

try:
    # For ComfyUI
    from .src.basic_data_handling import NODE_CLASS_MAPPINGS
    from .src.basic_data_handling import NODE_DISPLAY_NAME_MAPPINGS
except ImportError:
    # For running tests
    from src.basic_data_handling import NODE_CLASS_MAPPINGS
    from src.basic_data_handling import NODE_DISPLAY_NAME_MAPPINGS


WEB_DIRECTORY = "./web"
