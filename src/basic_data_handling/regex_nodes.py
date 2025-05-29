from inspect import cleandoc
import re

try:
    from comfy.comfy_types.node_typing import IO, ComfyNodeABC
except:
    class IO:
        BOOLEAN = "BOOLEAN"
        INT = "INT"
        FLOAT = "FLOAT"
        STRING = "STRING"
        NUMBER = "FLOAT,INT"
        ANY = "*"
    ComfyNodeABC = object

class RegexFindallDataList(ComfyNodeABC):
    """
    Returns all non-overlapping matches of a pattern in the string as a list of strings.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": (IO.STRING, {}),
                "pattern": (IO.STRING, {}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    CATEGORY = "Basic/STRING/regex"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "findall"
    OUTPUT_IS_LIST = (True,)

    def findall(self, pattern: str, string: str) -> tuple[list[str]]:
        return (re.findall(pattern, string),)


class RegexFindallList(ComfyNodeABC):
    """
    Returns all non-overlapping matches of a pattern in the string as a list of strings.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": (IO.STRING, {}),
                "pattern": (IO.STRING, {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/STRING/regex"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "findall"

    def findall(self, pattern: str, string: str) -> tuple[list[str]]:
        return (re.findall(pattern, string),)


class RegexGroupDict(ComfyNodeABC):
    """
    Searches the string with the given pattern and returns a DICT of named groups.
    If no match is found, it returns an empty DICT.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": (IO.STRING, {}),
                "pattern": (IO.STRING, {}),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/STRING/regex"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "groupdict"

    def groupdict(self, pattern: str, string: str) -> tuple[dict]:
        match = re.search(pattern, string)
        if match:
            return (match.groupdict(),)
        return ({},)


class RegexSearchGroupsDataList(ComfyNodeABC):
    """
    Searches the string for a match to the pattern and returns a LIST of match groups.
    If no match is found, it returns an empty LIST.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": (IO.STRING, {}),
                "pattern": (IO.STRING, {}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    CATEGORY = "Basic/STRING/regex"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "search_groups"
    OUTPUT_IS_LIST = (True,)

    def search_groups(self, pattern: str, string: str) -> tuple[list[str]]:
        match = re.search(pattern, string)
        if match:
            return (list(match.groups()),)
        return ([],)


class RegexSearchGroupsList(ComfyNodeABC):
    """
    Searches the string for a match to the pattern and returns a data list of match groups.
    If no match is found, it returns an empty data list.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": (IO.STRING, {}),
                "pattern": (IO.STRING, {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/STRING/regex"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "search_groups"

    def search_groups(self, pattern: str, string: str) -> tuple[list[str]]:
        match = re.search(pattern, string)
        if match:
            return (list(match.groups()),)
        return ([],)


class RegexSplitDataList(ComfyNodeABC):
    """
    Splits the string at each match of the pattern and returns a list of substrings.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": (IO.STRING, {}),
                "pattern": (IO.STRING, {}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    CATEGORY = "Basic/STRING/regex"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "split"
    OUTPUT_IS_LIST = (True,)

    def split(self, pattern: str, string: str) -> tuple[list[str]]:
        return (re.split(pattern, string),)


class RegexSplitList(ComfyNodeABC):
    """
    Splits the string at each match of the pattern and returns a list of substrings.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": (IO.STRING, {}),
                "pattern": (IO.STRING, {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/STRING/regex"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "split"

    def split(self, pattern: str, string: str) -> tuple[list[str]]:
        return (re.split(pattern, string),)


class RegexSub(ComfyNodeABC):
    """
    Substitutes matches of the pattern in the string with a replacement string.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": (IO.STRING, {}),
                "pattern": (IO.STRING, {}),
                "repl": (IO.STRING, {}),
                "count": ("INT", {"default": 0}),  # 0 means replace all occurrences
            }
        }

    RETURN_TYPES = (IO.STRING,)
    CATEGORY = "Basic/STRING/regex"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "sub"

    def sub(self, pattern: str, repl: str, string: str, count: int = 0) -> tuple[str]:
        return (re.sub(pattern, repl, string, count),)


class RegexTest(ComfyNodeABC):
    """
    Tests whether a given regex pattern matches any part of the input string.
    Returns True if a match is found, otherwise False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": (IO.STRING, {}),
                "pattern": (IO.STRING, {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING/regex"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "test"

    def test(self, pattern: str, string: str) -> tuple[bool]:
        match = re.search(pattern, string)
        return (match is not None,)


NODE_CLASS_MAPPINGS = {
    "Basic data handling: RegexFindallDataList": RegexFindallDataList,
    "Basic data handling: RegexFindallList": RegexFindallList,
    "Basic data handling: RegexGroupDict": RegexGroupDict,
    "Basic data handling: RegexSearchGroupsDataList": RegexSearchGroupsDataList,
    "Basic data handling: RegexSearchGroupsList": RegexSearchGroupsList,
    "Basic data handling: RegexSplitDataList": RegexSplitDataList,
    "Basic data handling: RegexSplitList": RegexSplitList,
    "Basic data handling: RegexSub": RegexSub,
    "Basic data handling: RegexTest": RegexTest,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: RegexFindallDataList": "find all (data list)",
    "Basic data handling: RegexFindallList": "find all (LIST)",
    "Basic data handling: RegexGroupDict": "search named groups",
    "Basic data handling: RegexSearchGroupsDataList": "search groups (data list)",
    "Basic data handling: RegexSearchGroupsList": "search groups (LIST)",
    "Basic data handling: RegexSplitDataList": "split (data list)",
    "Basic data handling: RegexSplitList": "split (LIST)",
    "Basic data handling: RegexSub": "substitute",
    "Basic data handling: RegexTest": "test",
}
