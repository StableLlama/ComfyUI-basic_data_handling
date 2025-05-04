from inspect import cleandoc

class DictGet:
    """
    Retrieves a value from a dictionary using the specified key.

    If the key is not found, the node will return None.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT",),
                "key": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("ANY",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get"

    def get(self, input_dict, key):
        return (input_dict.get(key, None),)

class DictSet:
    """
    Adds or updates a key-value pair in a dictionary.

    This node takes a dictionary, key, and value as inputs, then returns
    a modified dictionary with the new key-value pair.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT",),
                "key": ("STRING", {"default": ""}),
                "value": ("ANY",),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "set"

    def set(self, input_dict, key, value):
        input_dict[key] = value
        return (input_dict,)

NODE_CLASS_MAPPINGS = {
    "DictGet": DictGet,
    "DictSet": DictSet,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DictGet": "get",
    "DictSet": "set",
}
