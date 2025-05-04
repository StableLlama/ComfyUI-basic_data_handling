from inspect import cleandoc

class ListAppend:
    """
    Adds an item to the end of a list.

    This node takes a list and any item as inputs, then returns the modified
    list with the new item appended.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_list": ("LIST",),
                "item": ("ANY",),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "append"

    def append(self, input_list, item):
        input_list.append(item)
        return (input_list,)

class ListLength:
    """
    Counts the number of items in a list.

    This node takes a list as input and returns its length as an integer.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_list": ("LIST",),
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "length"

    def length(self, input_list):
        return (len(input_list),)

NODE_CLASS_MAPPINGS = {
    "ListAppend": ListAppend,
    "ListLength": ListLength,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ListAppend": "append",
    "ListLength": "length",
}
