#import pytest

from src.basic_data_handling.string_nodes import (
    StringCapitalize,
    StringCasefold,
    StringCenter,
    StringConcat,
    StringCount,
    StringDataListJoin,
    StringDecode,
    StringEncode,
    StringEndswith,
    StringExpandtabs,
    StringFind,
    StringFormatMap,
    StringIn,
    StringIsAlnum,
    StringIsAlpha,
    StringIsAscii,
    StringIsDecimal,
    StringIsDigit,
    StringIsIdentifier,
    StringIsLower,
    StringIsNumeric,
    StringIsPrintable,
    StringIsSpace,
    StringIsTitle,
    StringIsUpper,
    StringLength,
    StringListJoin,
    StringLjust,
    StringLower,
    StringLstrip,
    StringRemoveprefix,
    StringRemovesuffix,
    StringReplace,
    StringRfind,
    StringRjust,
    StringRsplitDataList,
    StringRsplitList,
    StringRstrip,
    StringSplitDataList,
    StringSplitList,
    StringSplitlinesDataList,
    StringSplitlinesList,
    StringStartswith,
    StringStrip,
    StringSwapcase,
    StringTitle,
    StringUpper,
    StringZfill,
)

def test_capitalize():
    node = StringCapitalize()
    assert node.capitalize("example") == ("Example",)
    assert node.capitalize("") == ("",)  # Empty string case
    assert node.capitalize("HELLO") == ("Hello",)  # Already uppercase

def test_casefold():
    node = StringCasefold()
    assert node.casefold("Germany") == ("germany",)
    assert node.casefold("FOO") == ("foo",)
    assert node.casefold("ß") == ("ss",)  # Special case folding

def test_center():
    node = StringCenter()
    # Centering with spaces
    assert node.center("test", 10) == ("   test   ",)
    # Centering with custom characters
    assert node.center("test", 10, "*") == ("***test***",)

    # Edge case: Width smaller than string length
    assert node.center("larger_string", 5) == ("larger_string",)

    # Multiple character fillchar (should use only first character)
    assert node.center("test", 10, "ab") == ("aaatestaaa",)

def test_concat():
    node = StringConcat()
    assert node.concat("hello ", "world") == ("hello world",)
    assert node.concat("", "") == ("",)  # Empty strings
    assert node.concat("123", "456") == ("123456",)  # Numbers as strings

def test_count():
    node = StringCount()
    assert node.count("banana", "a") == (3,)
    assert node.count("banana", "na") == (2,)
    assert node.count("banana", "z") == (0,)  # Non-existent substring
    # With start and end parameters
    assert node.count("banana", "a", 2) == (2,)  # Count from index 2 to end
    assert node.count("banana", "a", 2, 5) == (1,)  # Count from index 2 to 5

def test_decode():
    node = StringDecode()
    assert node.decode("b'test'", "utf-8") == ("test",)
    assert node.decode("b'\\xc3\\xb6\\xc3\\xa4\\xc3\\xbc'", "utf-8") == ("öäü",)
    # Invalid bytes string format
    assert node.decode("test", "utf-8")[0].startswith("Input is not a bytes string")

def test_encode():
    node = StringEncode()
    assert node.encode("test", "utf-8") == ("b'test'",)  # UTF-8 standard
    assert node.encode("öäü", "utf-8") == ("b'\\xc3\\xb6\\xc3\\xa4\\xc3\\xbc'",)  # Special UTF-8 characters

    # Error case: Unsupported encoding
    assert node.encode("äö", "nonexistent-encoding")[0].startswith("Encoding error")

def test_endswith():
    node = StringEndswith()
    assert node.endswith("endswith function", "function") == (True,)
    assert node.endswith("CHECK", "check") == (False,)  # Case sensitivity test
    assert node.endswith("hello world", "hello", 0, 5) == (True,)  # With start and end
    assert node.endswith("", "") == (True,)  # Empty strings

def test_expandtabs():
    node = StringExpandtabs()
    assert node.expandtabs("hello\tworld") == ("hello   world",)  # Default tabsize=8
    assert node.expandtabs("hello\tworld", 4) == ("hello   world",)  # Custom tabsize
    assert node.expandtabs("no tabs here") == ("no tabs here",)  # No tabs

def test_find():
    node = StringFind()
    assert node.find("hello world", "world") == (6,)
    assert node.find("hello world", "earth") == (-1,)  # Substring not found
    assert node.find("hello world", "l", 3, 7) == (3,)  # With start and end
    assert node.find("hello world", "l", 4) == (9,)  # With start

def test_in():
    node = StringIn()
    assert node.contains("hello world", "world") == (True,)
    assert node.contains("hello world", "earth") == (False,)
    assert node.contains("", "") == (True,)  # Empty strings

def test_format_map():
    node = StringFormatMap()
    assert node.format_map("Hello, {name}!", {"name": "World"}) == ("Hello, World!",)
    assert node.format_map("{a} + {b} = {c}", {"a": 1, "b": 2, "c": 3}) == ("1 + 2 = 3",)
    # Missing key
    result = node.format_map("Hello, {missing}!", {})[0]
    assert result.startswith("Key error")

def test_isalnum():
    node = StringIsAlnum()
    assert node.isalnum("abc123") == (True,)
    assert node.isalnum("abc 123") == (False,)  # Space makes it not alphanumeric
    assert node.isalnum("") == (False,)  # Empty string

def test_isalpha():
    node = StringIsAlpha()
    assert node.isalpha("abc") == (True,)
    assert node.isalpha("abc123") == (False,)  # Contains digits
    assert node.isalpha("") == (False,)  # Empty string

def test_isascii():
    node = StringIsAscii()
    assert node.isascii("hello") == (True,)
    assert node.isascii("öäü") == (False,)  # Non-ASCII characters
    assert node.isascii("") == (True,)  # Empty string is ASCII

def test_isdecimal():
    node = StringIsDecimal()
    assert node.isdecimal("123") == (True,)
    assert node.isdecimal("123.45") == (False,)  # Decimal point makes it not decimal
    assert node.isdecimal("") == (False,)  # Empty string

def test_isdigit():
    node = StringIsDigit()
    assert node.isdigit("12345") == (True,)
    assert node.isdigit("123abc") == (False,)
    assert node.isdigit("") == (False,)  # Empty string is not a digit
    assert node.isdigit("²³") == (True,)  # Superscript digits are digits

def test_isidentifier():
    node = StringIsIdentifier()
    assert node.isidentifier("valid_var_name") == (True,)
    assert node.isidentifier("1invalid") == (False,)  # Cannot start with digit
    assert node.isidentifier("") == (False,)  # Empty string

def test_islower():
    node = StringIsLower()
    assert node.islower("lowercase") == (True,)
    assert node.islower("Mixed") == (False,)
    assert node.islower("123") == (False,)  # No cased characters
    assert node.islower("") == (False,)  # Empty string

def test_isnumeric():
    node = StringIsNumeric()
    assert node.isnumeric("123") == (True,)
    assert node.isnumeric("¹²³") == (True,)  # Unicode numeric characters
    assert node.isnumeric("123abc") == (False,)
    assert node.isnumeric("") == (False,)  # Empty string

def test_isprintable():
    node = StringIsPrintable()
    assert node.isprintable("Hello World") == (True,)
    assert node.isprintable("Hello\nWorld") == (False,)  # Contains non-printable character
    assert node.isprintable("") == (True,)  # Empty string is printable

def test_isspace():
    node = StringIsSpace()
    assert node.isspace(" \t\n") == (True,)
    assert node.isspace("   text   ") == (False,)  # Contains non-whitespace
    assert node.isspace("") == (False,)  # Empty string

def test_istitle():
    node = StringIsTitle()
    assert node.istitle("Title Case") == (True,)
    assert node.istitle("Not title Case") == (False,)
    assert node.istitle("") == (False,)  # Empty string

def test_isupper():
    node = StringIsUpper()
    assert node.isupper("UPPERCASE") == (True,)
    assert node.isupper("Mixed") == (False,)
    assert node.isupper("") == (False,)  # Empty string

def test_join():
    node = StringDataListJoin()
    # join expects a data list as input, so we need to simulate this
    assert node.join([", "], ["apple", "banana", "cherry"]) == ("apple, banana, cherry",)
    assert node.join([""], ["a", "b", "c"]) == ("abc",)
    assert node.join(["-"], []) == ("",)  # Empty list

    # Test ListJoin variant
    node_list = StringListJoin()
    assert node_list.join([", "], ["apple", "banana", "cherry"]) == ("apple, banana, cherry",)
    assert node_list.join([""], ["a", "b", "c"]) == ("abc",)
    assert node_list.join(["-"], []) == ("",)  # Empty list

def test_ljust():
    node = StringLjust()
    assert node.ljust("test", 10) == ("test      ",)
    assert node.ljust("test", 10, "*") == ("test******",)
    assert node.ljust("test", 2) == ("test",)  # Width smaller than string length

def test_lower():
    node = StringLower()
    assert node.lower("HELLO") == ("hello",)
    assert node.lower("Hello World") == ("hello world",)
    assert node.lower("") == ("",)  # Empty string

def test_lstrip():
    node = StringLstrip()
    assert node.lstrip("   hello") == ("hello",)
    assert node.lstrip("...hello", ".") == ("hello",)
    assert node.lstrip("hello") == ("hello",)  # No leading chars to strip
    assert node.lstrip("") == ("",)  # Empty string

def test_removeprefix():
    node = StringRemoveprefix()
    assert node.removeprefix("TestPrefix", "Test") == ("Prefix",)
    assert node.removeprefix("Prefix", "Test") == ("Prefix",)  # Prefix not present
    assert node.removeprefix("", "") == ("",)  # Empty strings

def test_removesuffix():
    node = StringRemovesuffix()
    assert node.removesuffix("PrefixTest", "Test") == ("Prefix",)
    assert node.removesuffix("Prefix", "Test") == ("Prefix",)  # Suffix not present
    assert node.removesuffix("", "") == ("",)  # Empty strings

def test_replace():
    node = StringReplace()
    assert node.replace("hello world", "world", "Python") == ("hello Python",)
    assert node.replace("test", "test", "") == ("",)  # Replacement with empty string
    assert node.replace("banana", "a", "o", 2) == ("bonona",)  # Limit replacement to 2 occurrences
    assert node.replace("no matches", "x", "y") == ("no matches",)  # No matches

def test_rfind():
    node = StringRfind()
    assert node.rfind("hello world hello", "hello") == (12,)
    assert node.rfind("hello world", "earth") == (-1,)  # Substring not found
    assert node.rfind("hello world hello", "hello", 1, 11) == (-1,)  # Within range
    assert node.rfind("", "") == (0,)  # Empty strings

def test_rjust():
    node = StringRjust()
    assert node.rjust("test", 10) == ("      test",)
    assert node.rjust("test", 10, "*") == ("******test",)
    assert node.rjust("test", 2) == ("test",)  # Width smaller than string length

def test_rsplit():
    node = StringRsplitDataList()
    assert node.rsplit("apple,banana,cherry", ",") == (["apple", "banana", "cherry"],)
    assert node.rsplit("apple,banana,cherry", ",", 1) == (["apple,banana", "cherry"],)
    assert node.rsplit("   words  with   spaces   ") == (["words", "with", "spaces"],)  # Default splits on whitespace

    # Test List variant
    node_list = StringRsplitList()
    assert node_list.rsplit("apple,banana,cherry", ",") == (["apple", "banana", "cherry"],)
    assert node_list.rsplit("apple,banana,cherry", ",", 1) == (["apple,banana", "cherry"],)
    assert node_list.rsplit("   words  with   spaces   ") == (["words", "with", "spaces"],)  # Default splits on whitespace

def test_rstrip():
    node = StringRstrip()
    assert node.rstrip("hello   ") == ("hello",)
    assert node.rstrip("hello...", ".") == ("hello",)
    assert node.rstrip("hello") == ("hello",)  # No trailing chars to strip
    assert node.rstrip("") == ("",)  # Empty string

def test_split():
    node = StringSplitDataList()
    assert node.split("apple,banana,cherry", ",") == (["apple", "banana", "cherry"],)
    assert node.split("apple,banana,cherry", ",", 1) == (["apple", "banana,cherry"],)
    assert node.split("   words  with   spaces   ") == (["words", "with", "spaces"],)  # Default splits on whitespace

    # Test List variant
    node_list = StringSplitList()
    assert node_list.split("apple,banana,cherry", ",") == (["apple", "banana", "cherry"],)
    assert node_list.split("apple,banana,cherry", ",", 1) == (["apple", "banana,cherry"],)
    assert node_list.split("   words  with   spaces   ") == (["words", "with", "spaces"],)  # Default splits on whitespace

def test_splitlines():
    node = StringSplitlinesDataList()
    assert node.splitlines("line1\nline2\nline3") == (["line1", "line2", "line3"],)
    assert node.splitlines("line1\r\nline2\rline3") == (["line1", "line2", "line3"],)
    assert node.splitlines("line1\nline2\nline3", True) == (["line1\n", "line2\n", "line3"],)  # Keep line endings
    assert node.splitlines("no newlines") == (["no newlines"],)

    # Test List variant
    node_list = StringSplitlinesList()
    assert node_list.splitlines("line1\nline2\nline3") == (["line1", "line2", "line3"],)
    assert node_list.splitlines("line1\r\nline2\rline3") == (["line1", "line2", "line3"],)
    assert node_list.splitlines("line1\nline2\nline3", True) == (["line1\n", "line2\n", "line3"],)  # Keep line endings
    assert node_list.splitlines("no newlines") == (["no newlines"],)

def test_startswith():
    node = StringStartswith()
    assert node.startswith("function startswith", "function") == (True,)
    assert node.startswith("CHECK", "check") == (False,)  # Case sensitivity test
    assert node.startswith("hello world", "world", 6) == (True,)  # With start
    assert node.startswith("", "") == (True,)  # Empty strings

def test_strip():
    node = StringStrip()
    assert node.strip("   hello   ") == ("hello",)
    assert node.strip("...hello...", ".") == ("hello",)
    assert node.strip("hello") == ("hello",)  # No chars to strip
    assert node.strip("") == ("",)  # Empty string

def test_swapcase():
    node = StringSwapcase()
    assert node.swapcase("Hello World") == ("hELLO wORLD",)
    assert node.swapcase("") == ("",)  # Empty string
    assert node.swapcase("123") == ("123",)  # No cased characters

def test_title():
    node = StringTitle()
    assert node.title("hello world") == ("Hello World",)
    assert node.title("HELLO WORLD") == ("Hello World",)
    assert node.title("hello123 world") == ("Hello123 World",)
    assert node.title("") == ("",)  # Empty string

def test_upper():
    node = StringUpper()
    assert node.upper("hello") == ("HELLO",)
    assert node.upper("Hello World") == ("HELLO WORLD",)
    assert node.upper("") == ("",)  # Empty string

def test_zfill():
    node = StringZfill()
    assert node.zfill("123", 5) == ("00123",)
    assert node.zfill("-123", 5) == ("-0123",)  # Preserves sign
    assert node.zfill("123", 2) == ("123",)  # Width smaller than string length
    assert node.zfill("", 3) == ("000",)  # Empty string

def test_length():
    node = StringLength()
    assert node.length("hello") == (5,)
    assert node.length("") == (0,)  # Empty string
    assert node.length("hello world") == (11,)  # String with spaces
