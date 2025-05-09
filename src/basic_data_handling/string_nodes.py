from inspect import cleandoc

class StringCapitalize:
    """Converts the first character of the input string to uppercase and all other characters to lowercase."""
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "capitalize"

    def capitalize(self, string):
        return (string.capitalize(),)


class StringCasefold:
    """
    Converts text to lowercase in a way optimized for case-insensitive comparisons.

    This node is especially useful when comparing text that might contain special characters.
    Unlike standard lowercase, this handles special cases like converting the German 'ß' to "ss".
    Use this node when you need the most accurate case-insensitive text matching.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "casefold"

    def casefold(self, string):
        return (string.casefold(),)


class StringCenter:
    """
    Centers text within a specified width.

    This node takes a string and centers it within a field of the specified width.
    By default, it uses spaces as padding characters, but you can specify any
    single character to use as padding.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "width": ("INT", {"default": 20, "min": 0, "max": 1000}),
            },
            "optional": {
                "fillchar": ("STRING", {"default": " "}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "center"

    def center(self, string, width, fillchar=" "):
        # Use only the first character if fillchar is longer than 1 character
        if len(fillchar) > 1:
            fillchar = fillchar[0]
        elif len(fillchar) == 0:
            fillchar = " "

        return (string.center(width, fillchar),)


class StringConcat:
    """Combines two text strings together, joining them end-to-end."""
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string_a": ("STRING", {"default": "", "defaultInput": True}),
                "string_b": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "concat"

    def concat(self, string_a, string_b):
        return (string_a + string_b,)


class StringCount:
    """
    Counts occurrences of a substring within a string.

    This node returns the number of times the specified substring appears in the input string.
    You can optionally specify start and end positions to limit the search range.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "substring": ("STRING", {"default": ""}),
            },
            "optional": {
                "start": ("INT", {"default": 0, "min": 0}),
                "end": ("INT", {"default": 0, "min": 0}),
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "count"

    def count(self, string, substring, start=0, end=0):
        # If end is 0 or negative, count to the end of the string
        if end <= 0:
            end = len(string)

        return (string.count(substring, start, end),)


class StringDecode:
    """
    Converts a bytes-like string representation back to a text string.

    This node takes a string representation of bytes (like those produced by the StringEncode node)
    and converts it back to a regular text string using the specified encoding.
    Useful for processing encoded data received from files or network sources.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bytes_string": ("STRING", {"default": "b''", "defaultInput": True}),
                "encoding": (["utf-8", "ascii", "latin-1", "utf-16", "utf-32", "cp1252"],),
                "errors": (["strict", "ignore", "replace", "backslashreplace"],),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "decode"

    def decode(self, bytes_string, encoding="utf-8", errors="strict"):
        try:
            # Check if the string is in the form of a bytes literal
            if bytes_string.startswith("b'") or bytes_string.startswith('b"'):
                # Convert the string representation to actual bytes
                # This is a simplified approach and may not handle all cases perfectly
                # Remove b prefix and quotes
                if bytes_string.startswith("b'") and bytes_string.endswith("'"):
                    content = bytes_string[2:-1]
                elif bytes_string.startswith('b"') and bytes_string.endswith('"'):
                    content = bytes_string[2:-1]
                else:
                    return (f"Invalid bytes string format: {bytes_string}",)

                # Handle escape sequences
                content = content.encode('utf-8').decode('unicode_escape').encode('latin-1')

                # Decode using the specified encoding
                result = content.decode(encoding, errors)
                return (result,)
            else:
                return (f"Input is not a bytes string representation: {bytes_string}",)
        except Exception as e:
            return (f"Decoding error: {str(e)}",)


class StringEncode:
    """
    Converts a string to bytes using the specified encoding.

    This node encodes text using different character encodings like UTF-8 (default),
    ASCII, or others. It's useful for preparing text for file saving or
    network transmission in specific formats.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "encoding": (["utf-8", "ascii", "latin-1", "utf-16", "utf-32", "cp1252"],),
                "errors": (["strict", "ignore", "replace", "xmlcharrefreplace", "backslashreplace"],),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "encode"

    def encode(self, string, encoding="utf-8", errors="strict"):
        # Encode the string into bytes and then decode back to a string
        # representation for display/storage in ComfyUI
        try:
            # Encode to bytes
            encoded_bytes = string.encode(encoding, errors)
            # Convert to string representation for display
            result = str(encoded_bytes)
            return (result,)
        except Exception as e:
            return (f"Encoding error: {str(e)}",)


class StringEndswith:
    """
    Checks if a string ends with the specified suffix.

    This node tests whether the input string ends with a particular substring.
    Returns True if the string ends with the specified suffix, otherwise False.
    Optional start and end parameters allow you to check only a specific portion of the string.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "suffix": ("STRING", {"default": ""}),
            },
            "optional": {
                "start": ("INT", {"default": 0, "min": 0}),
                "end": ("INT", {"default": 0, "min": 0}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "endswith"

    def endswith(self, string, suffix, start=0, end=0):
        # If end is 0 or negative, check to the end of the string
        if end <= 0:
            end = len(string)

        return (string.endswith(suffix, start, end),)


class StringExpandtabs:
    """
    Replaces tab characters with spaces.

    This node replaces all tab characters ('\t') in a string with spaces.
    The tab size (number of spaces per tab) can be adjusted,
    with a default value of 8 characters.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            },
            "optional": {
                "tabsize": ("INT", {"default": 8, "min": 1, "max": 100}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "expandtabs"

    def expandtabs(self, string, tabsize=8):
        return (string.expandtabs(tabsize),)


class StringFind:
    """
    Finds the first occurrence of a substring in a string.

    This node searches for the first occurrence of the specified substring within the input string.
    Returns the lowest index where the substring is found. If the substring is not found, it returns -1.
    Optional start and end parameters allow you to limit the search to a specific portion of the string.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "substring": ("STRING", {"default": ""}),
            },
            "optional": {
                "start": ("INT", {"default": 0, "min": 0}),
                "end": ("INT", {"default": 0, "min": 0}),
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "find"

    def find(self, string, substring, start=0, end=0):
        # If end is 0 or negative, search to the end of the string
        if end <= 0:
            end = len(string)

        return (string.find(substring, start, end),)


class StringIn:
    """
    Checks if a string contains a specified substring.

    This node implements the 'in' operator for strings. It checks whether the given substring
    exists within the input string. Returns True if the substring is found,
    otherwise False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "substring": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "contains"

    def contains(self, string, substring):
        return (substring in string,)


class StringFormatMap:
    """
    Formats a string using values from a dictionary.

    This node replaces placeholders in the input string with values from a dictionary.
    It uses the same placeholder syntax as the format() method, but takes the values from a dictionary
    mapping keys to values. For example, the string "Hello, {name}" with a dictionary {"name": "World"}
    would produce "Hello, World".
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template": ("STRING", {"default": "Hello, {key}", "defaultInput": True}),
                "mapping": ("DICT", {"default": {}}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "format_map"

    def format_map(self, template, mapping):
        try:
            result = template.format_map(mapping)
            return (result,)
        except KeyError as e:
            return (f"Key error: {str(e)} not found in mapping",)
        except Exception as e:
            return (f"Formatting error: {str(e)}",)


class StringIsAlnum:
    """
    Checks if all characters in the string are alphanumeric.

    This node returns True if all characters in the string are alphanumeric
    (letters or numbers) and there is at least one character, otherwise False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING/is"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "isalnum"

    def isalnum(self, string):
        return (string.isalnum(),)


class StringIsAlpha:
    """
    Checks if all characters in the string are alphabetic.

    This node returns True if all characters in the string are alphabetic
    (letters) and there is at least one character, otherwise False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING/is"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "isalpha"

    def isalpha(self, string):
        return (string.isalpha(),)


class StringIsAscii:
    """
    Checks if all characters in the string are ASCII characters.

    This node returns True if all characters in the string are in the ASCII character
    set and there is at least one character, otherwise False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING/is"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "isascii"

    def isascii(self, string):
        return (string.isascii(),)


class StringIsDecimal:
    """
    Checks if all characters in the string are decimal characters.

    This node returns True if all characters in the string are decimal
    characters and there is at least one character, otherwise False.
    Decimal characters include digit characters and characters that can be
    used to form decimal numbers in various locales.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING/is"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "isdecimal"

    def isdecimal(self, string):
        return (string.isdecimal(),)


class StringIsDigit:
    """
    Checks if all characters in the string are digits.

    This node returns True if all characters in the string are digits
    and there is at least one character, otherwise False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING/is"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "isdigit"

    def isdigit(self, string):
        return (string.isdigit(),)


class StringIsIdentifier:
    """
    Checks if the string is a valid identifier in Python.

    This node returns True if the string is a valid Python identifier,
    otherwise False. A valid identifier must start with a letter or underscore
    and can only contain letters, digits, or underscores.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING/is"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "isidentifier"

    def isidentifier(self, string):
        return (string.isidentifier(),)


class StringIsLower:
    """
    Checks if all characters in the string are lowercase.

    This node returns True if all cased characters in the string are lowercase
    and there is at least one cased character, otherwise False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING/is"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "islower"

    def islower(self, string):
        return (string.islower(),)


class StringIsNumeric:
    """
    Checks if all characters in the string are numeric.

    This node returns True if all characters in the string are numeric
    and there is at least one character, otherwise False. Numeric characters include
    digit characters and characters that have the Unicode numeric value property.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING/is"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "isnumeric"

    def isnumeric(self, string):
        return (string.isnumeric(),)


class StringIsPrintable:
    """
    Checks if all characters in the string are printable.

    This node returns True if all characters in the string are printable or the string is empty,
    otherwise False. Printable characters are those which are not control characters.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING/is"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "isprintable"

    def isprintable(self, string):
        return (string.isprintable(),)


class StringIsSpace:
    """
    Checks if all characters in the string are whitespace.

    This node returns True if all characters in the string are whitespace
    and there is at least one character, otherwise False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING/is"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "isspace"

    def isspace(self, string):
        return (string.isspace(),)


class StringIsTitle:
    """
    Checks if the string is titlecased.

    This node returns True if the string is titlecased and there is at least one
    character, otherwise False. A titlecased string has all words start with an
    uppercase character and continue with lowercase.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING/is"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "istitle"

    def istitle(self, string):
        return (string.istitle(),)


class StringIsUpper:
    """
    Checks if all characters in the string are uppercase.

    This node returns True if all cased characters in the string are uppercase
    and there is at least one cased character, otherwise False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING/is"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "isupper"

    def isupper(self, string):
        return (string.isupper(),)


class StringLjust:
    """
    Left-aligns the string within a field of a given width.

    This node returns a string left-aligned in a field of the specified width.
    If fillchar is provided, it is used as the padding character instead of a space.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "width": ("INT", {"default": 10, "min": 0}),
            },
            "optional": {
                "fillchar": ("STRING", {"default": " "}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "ljust"

    def ljust(self, string, width, fillchar=" "):
        # Ensure fillchar is only one character
        if len(fillchar) > 0:
            fillchar = fillchar[0]
        return (string.ljust(width, fillchar),)


class StringLstrip:
    """
    Removes leading characters from the string.

    This node returns a copy of the string with leading characters removed.
    If chars is provided, it specifies the set of characters to be removed.
    If chars is not provided, whitespace characters are removed.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            },
            "optional": {
                "chars": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "lstrip"

    def lstrip(self, string, chars=None):
        if chars == "":
            chars = None
        return (string.lstrip(chars),)


class StringRemoveprefix:
    """
    Removes prefix from the string if present.

    This node returns a copy of the string with the specified prefix removed
    if the string starts with that prefix, otherwise returns the original string.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "prefix": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "removeprefix"

    def removeprefix(self, string, prefix):
        return (string.removeprefix(prefix),)


class StringRemovesuffix:
    """
    Removes suffix from the string if present.

    This node returns a copy of the string with the specified suffix removed
    if the string ends with that suffix, otherwise returns the original string.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "suffix": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "removesuffix"

    def removesuffix(self, string, suffix):
        return (string.removesuffix(suffix),)


class StringRsplit:
    """
    Splits the string at the specified separator from the right.

    This node returns a list of strings by splitting the input string at the specified separator,
    starting from the right. If maxsplit is provided, at most maxsplit splits are done.
    If the separator is not specified or is None, any whitespace string is a separator.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            },
            "optional": {
                "sep": ("STRING", {"default": ""}),
                "maxsplit": ("INT", {"default": -1, "min": -1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "rsplit"
    OUTPUT_IS_LIST = (True,)

    def rsplit(self, string, sep=None, maxsplit=-1):
        if sep == "":
            sep = None
        return (string.rsplit(sep, maxsplit),)


class StringLower:
    """
    Converts the string to lowercase.

    This node returns a copy of the string with all uppercase characters converted to lowercase.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "lower"

    def lower(self, string):
        return (string.lower(),)


class StringReplace:
    """
    Replaces occurrences of a substring with another substring.

    This node returns a copy of the string with all occurrences of substring
    old replaced by new. If the optional argument count is given, only the
    first count occurrences are replaced.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "old": ("STRING", {"default": ""}),
                "new": ("STRING", {"default": ""}),
            },
            "optional": {
                "count": ("INT", {"default": -1, "min": -1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "replace"

    def replace(self, string, old, new, count=-1):
        return (string.replace(old, new, count),)


class StringRjust:
    """
    Right-aligns the string within a field of a given width.

    This node returns a string right-aligned in a field of the specified width.
    If fillchar is provided, it is used as the padding character instead of a space.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "width": ("INT", {"default": 10, "min": 0}),
            },
            "optional": {
                "fillchar": ("STRING", {"default": " "}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "rjust"

    def rjust(self, string, width, fillchar=" "):
        # Ensure fillchar is only one character
        if len(fillchar) > 0:
            fillchar = fillchar[0]
        return (string.rjust(width, fillchar),)


class StringJoin:
    """
    Joins strings from a data list with a specified separator.

    This node takes a data list of strings and concatenates them, with the specified
    separator string between each element. The separator is inserted between the strings,
    not at the beginning or end of the result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sep": ("STRING", {"default": " ", "defaultInput": True}),
                "strings": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "join"
    INPUT_IS_LIST = True  # The "strings" input accepts a data list

    def join(self, sep, strings):
        separator = sep[0]    # everything comes as a list, so sep is list[str]
        return (separator.join(strings),)


class StringRfind:
    """
    Finds the highest index of the substring in the string.

    This node searches for the last occurrence of the specified substring within the input string.
    Returns the highest index where the substring is found. If the substring is not found, it returns -1.
    Optional start and end parameters allow you to limit the search to a specific portion of the string.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "substring": ("STRING", {"default": ""}),
            },
            "optional": {
                "start": ("INT", {"default": 0, "min": 0}),
                "end": ("INT", {"default": 0, "min": 0}),
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "rfind"

    def rfind(self, string, substring, start=0, end=0):
        # If end is 0 or negative, search to the end of the string
        if end <= 0:
            end = len(string)

        return (string.rfind(substring, start, end),)


class StringRstrip:
    """
    Removes trailing characters from the string.

    This node returns a copy of the string with trailing characters removed.
    If chars is provided, it specifies the set of characters to be removed.
    If chars is not provided, whitespace characters are removed.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            },
            "optional": {
                "chars": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "rstrip"

    def rstrip(self, string, chars=None):
        if chars == "":
            chars = None
        return (string.rstrip(chars),)


class StringSplit:
    """
    Splits the string at the specified separator.

    This node splits the input string at the specified separator and returns a
    data list containing all parts. If maxsplit is provided, at most maxsplit
    splits are done.

    If the separator is not specified or is None, any whitespace string is a separator.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            },
            "optional": {
                "sep": ("STRING", {"default": ""}),
                "maxsplit": ("INT", {"default": -1, "min": -1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "split"
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    OUTPUT_IS_LIST = (True,)  # This indicates that the output is a data list

    def split(self, string, sep=None, maxsplit=-1):
        if sep == "":
            sep = None

        parts = string.split(sep, maxsplit)
        # Return a data list where each item is a separate string
        return (parts,)


class StringSplitlines:
    """
    Splits the string at line boundaries.

    This node returns a list of the lines in the string, breaking at line boundaries.
    If keepends is True, line breaks are included in the resulting list.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            },
            "optional": {
                "keepends": (["False", "True"], {"default": "False"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "splitlines"
    OUTPUT_IS_LIST = (True,)

    def splitlines(self, string, keepends="False"):
        keepends_bool = (keepends == "True")
        lines = string.splitlines(keepends_bool)
        return (lines,)


class StringStartswith:
    """
    Checks if a string starts with the specified prefix.

    This node tests whether the input string starts with a particular substring.
    Returns True if the string starts with the specified prefix, otherwise False.
    Optional start and end parameters allow you to check only a specific portion of the string.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "prefix": ("STRING", {"default": ""}),
            },
            "optional": {
                "start": ("INT", {"default": 0, "min": 0}),
                "end": ("INT", {"default": 0, "min": 0}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "startswith"

    def startswith(self, string, prefix, start=0, end=0):
        # If end is 0 or negative, check to the end of the string
        if end <= 0:
            end = len(string)

        return (string.startswith(prefix, start, end),)


class StringStrip:
    """
    Removes leading and trailing characters from the string.

    This node returns a copy of the string with both leading and trailing characters removed.
    If chars is provided, it specifies the set of characters to be removed.
    If chars is not provided, whitespace characters are removed.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            },
            "optional": {
                "chars": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "strip"

    def strip(self, string, chars=None):
        if chars == "":
            chars = None
        return (string.strip(chars),)


class StringSwapcase:
    """
    Swaps case of all characters in the string.

    This node returns a copy of the string with uppercase characters converted to lowercase
    and lowercase characters converted to uppercase.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "swapcase"

    def swapcase(self, string):
        return (string.swapcase(),)


class StringTitle:
    """
    Converts the string to titlecase.

    This node returns a titlecased version of the string where words start with an uppercase
    character and the remaining characters are lowercase.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "title"

    def title(self, string):
        return (string.title(),)


class StringUpper:
    """
    Converts the string to uppercase.

    This node returns a copy of the string with all lowercase characters converted to uppercase.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "upper"

    def upper(self, string):
        return (string.upper(),)


class StringZfill:
    """
    Pads the string with zeros on the left.

    This node returns a copy of the string left filled with ASCII '0' digits to make a string
    of length width. A leading sign prefix ('+'/'-') is handled by inserting the padding
    after the sign character rather than before.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "defaultInput": True}),
                "width": ("INT", {"default": 10, "min": 0}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/STRING"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "zfill"

    def zfill(self, string, width):
        return (string.zfill(width),)



NODE_CLASS_MAPPINGS = {
    "Basic data handling: StringCapitalize": StringCapitalize,
    "Basic data handling: StringCasefold": StringCasefold,
    "Basic data handling: StringCenter": StringCenter,
    "Basic data handling: StringConcat": StringConcat,
    "Basic data handling: StringCount": StringCount,
    "Basic data handling: StringDecode": StringDecode,
    "Basic data handling: StringEncode": StringEncode,
    "Basic data handling: StringExpandtabs": StringExpandtabs,
    "Basic data handling: StringEndswith": StringEndswith,
    "Basic data handling: StringFind": StringFind,
    "Basic data handling: StringFormatMap": StringFormatMap,
    "Basic data handling: StringIsAlnum": StringIsAlnum,
    "Basic data handling: StringIsAlpha": StringIsAlpha,
    "Basic data handling: StringIsAscii": StringIsAscii,
    "Basic data handling: StringIsDecimal": StringIsDecimal,
    "Basic data handling: StringIsDigit": StringIsDigit,
    "Basic data handling: StringIsIdentifier": StringIsIdentifier,
    "Basic data handling: StringIsLower": StringIsLower,
    "Basic data handling: StringIsNumeric": StringIsNumeric,
    "Basic data handling: StringIsPrintable": StringIsPrintable,
    "Basic data handling: StringIsSpace": StringIsSpace,
    "Basic data handling: StringIsTitle": StringIsTitle,
    "Basic data handling: StringIsUpper": StringIsUpper,
    "Basic data handling: StringJoin": StringJoin,
    "Basic data handling: StringLjust": StringLjust,
    "Basic data handling: StringLower": StringLower,
    "Basic data handling: StringLstrip": StringLstrip,
    "Basic data handling: StringRemoveprefix": StringRemoveprefix,
    "Basic data handling: StringRemovesuffix": StringRemovesuffix,
    "Basic data handling: StringReplace": StringReplace,
    "Basic data handling: StringRfind": StringRfind,
    "Basic data handling: StringRjust": StringRjust,
    "Basic data handling: StringRsplit": StringRsplit,
    "Basic data handling: StringRstrip": StringRstrip,
    "Basic data handling: StringSplit": StringSplit,
    "Basic data handling: StringSplitlines": StringSplitlines,
    "Basic data handling: StringStartswith": StringStartswith,
    "Basic data handling: StringStrip": StringStrip,
    "Basic data handling: StringSwapcase": StringSwapcase,
    "Basic data handling: StringTitle": StringTitle,
    "Basic data handling: StringUpper": StringUpper,
    "Basic data handling: StringZfill": StringZfill,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: StringCapitalize": "capitalize",
    "Basic data handling: StringCasefold": "casefold",
    "Basic data handling: StringCenter": "center",
    "Basic data handling: StringConcat": "concat",
    "Basic data handling: StringCount": "count",
    "Basic data handling: StringDecode": "decode",
    "Basic data handling: StringEncode": "encode",
    "Basic data handling: StringExpandtabs": "expandtabs",
    "Basic data handling: StringEndswith": "endswith",
    "Basic data handling: StringFind": "find",
    "Basic data handling: StringFormatMap": "format_map",
    "Basic data handling: StringIn": "in (contains)",
    "Basic data handling: StringIsAlnum": "isalnum",
    "Basic data handling: StringIsAlpha": "isalpha",
    "Basic data handling: StringIsAscii": "isascii",
    "Basic data handling: StringIsDecimal": "isdecimal",
    "Basic data handling: StringIsDigit": "isdigit",
    "Basic data handling: StringIsIdentifier": "isidentifier",
    "Basic data handling: StringIsLower": "islower",
    "Basic data handling: StringIsNumeric": "isnumeric",
    "Basic data handling: StringIsPrintable": "isprintable",
    "Basic data handling: StringIsSpace": "isspace",
    "Basic data handling: StringIsTitle": "istitle",
    "Basic data handling: StringIsUpper": "isupper",
    "Basic data handling: StringJoin": "join",
    "Basic data handling: StringLjust": "ljust",
    "Basic data handling: StringLower": "lower",
    "Basic data handling: StringLstrip": "lstrip",
    "Basic data handling: StringRemoveprefix": "removeprefix",
    "Basic data handling: StringRemovesuffix": "removesuffix",
    "Basic data handling: StringReplace": "replace",
    "Basic data handling: StringRfind": "rfind",
    "Basic data handling: StringRjust": "rjust",
    "Basic data handling: StringRsplit": "rsplit",
    "Basic data handling: StringRstrip": "rstrip",
    "Basic data handling: StringSplit": "split",
    "Basic data handling: StringSplitlines": "splitlines",
    "Basic data handling: StringStartswith": "startswith",
    "Basic data handling: StringStrip": "strip",
    "Basic data handling: StringSwapcase": "swapcase",
    "Basic data handling: StringTitle": "title",
    "Basic data handling: StringUpper": "upper",
    "Basic data handling: StringZfill": "zfill",
}
