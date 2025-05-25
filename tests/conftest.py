#import os
#import sys
# from unittest.mock import MagicMock
#
# # Add the project root directory to Python path
# # This allows the tests to import the project
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
# print("=======================================================================")
# print("Mocking 'comfy.comfy_types.node_typing' via conftest.py")
# print("=======================================================================")
#
# # Create a dummy 'comfy.comfy_types.node_typing' module
# mock_comfy = MagicMock()
# mock_comfy.IO = MagicMock(
#     BOOLEAN="BOOLEAN",
#     INT="INT",
#     FLOAT="FLOAT",
#     STRING="STRING",
#     NUMBER = "FLOAT,INT",
#     ANY="*",
# )
# mock_comfy.ComfyNodeABC = object
#
# # Inject the mocked module into sys.modules
# sys.modules["comfy"] = mock_comfy
# sys.modules["comfy.comfy_types"] = mock_comfy
# sys.modules["comfy.comfy_types.node_typing"] = mock_comfy
#
# def mock_execution_blocker(_):
#     return None
#
# mock_comfy_execution = MagicMock()
# mock_comfy_execution.ExecutionBlocker = mock_execution_blocker
# sys.modules["comfy_execution"] = mock_comfy_execution
# sys.modules["comfy_execution.graph"] = mock_comfy_execution
