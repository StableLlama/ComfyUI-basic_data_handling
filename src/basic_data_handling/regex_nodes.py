from inspect import cleandoc
import re

class RegexSearchGroups:
    """
    Searches the string for a match to the pattern and returns a LIST of match groups.
    If no match is found, it returns an empty LIST.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pattern": ("STRING", {}),
                "string": ("STRING", {}),
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


class RegexGroupDict:
    """
    Searches the string with the given pattern and returns a DICT of named groups.
    If no match is found, it returns an empty DICT.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pattern": ("STRING", {}),
                "string": ("STRING", {}),
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


class RegexFindall:
    """
    Returns all non-overlapping matches of a pattern in the string as a list of strings.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pattern": ("STRING", {}),
                "string": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/STRING/regex"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "findall"

    def findall(self, pattern: str, string: str) -> tuple[list[str]]:
        return (re.findall(pattern, string),)


class RegexSplit:
    """
    Splits the string at each match of the pattern and returns a list of substrings.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pattern": ("STRING", {}),
                "string": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/STRING/regex"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "split"

    def split(self, pattern: str, string: str) -> tuple[list[str]]:
        return (re.split(pattern, string),)


class RegexSub:
    """
    Substitutes matches of the pattern in the string with a replacement string.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pattern": ("STRING", {}),
                "repl": ("STRING", {}),
                "string": ("STRING", {}),
                "count": ("INT", {"default": 0}),  # 0 means replace all occurrences
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING/regex"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "sub"

    def sub(self, pattern: str, repl: str, string: str, count: int = 0) -> tuple[str]:
        return (re.sub(pattern, repl, string, count),)


class RegexTest:
    """
    Tests whether a given regex pattern matches any part of the input string.
    Returns True if a match is found, otherwise False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pattern": ("STRING", {}),
                "string": ("STRING", {}),
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
    "Basic data handling: RegexSearchGroups": RegexSearchGroups,
    "Basic data handling: RegexGroupDict": RegexGroupDict,
    "Basic data handling: RegexFindall": RegexFindall,
    "Basic data handling: RegexSplit": RegexSplit,
    "Basic data handling: RegexSub": RegexSub,
    "Basic data handling: RegexTest": RegexTest,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: RegexSearchGroups": "search groups",
    "Basic data handling: RegexGroupDict": "search named groups",
    "Basic data handling: RegexFindall": "find all",
    "Basic data handling: RegexSplit": "split",
    "Basic data handling: RegexSub": "substitute",
    "Basic data handling: RegexTest": "test",
}
