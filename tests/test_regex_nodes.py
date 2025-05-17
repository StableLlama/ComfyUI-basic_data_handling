#import pytest
from src.basic_data_handling.regex_nodes import (
    RegexSearchGroupsDataList,
    RegexGroupDict,
    RegexFindallDataList,
    RegexSplitDataList,
    RegexSub,
    RegexTest,
    RegexFindallList,
    RegexSearchGroupsList,
    RegexSplitList
)

def test_regex_search_groups():
    node = RegexSearchGroupsDataList()
    assert node.search_groups(r"(foo)(bar)", "foobar") == (["foo", "bar"],)
    assert node.search_groups(r"(test)(\d+)", "test123") == (["test", "123"],)
    assert node.search_groups(r"(nothing)", "no match here") == ([],)  # No match
    assert node.search_groups(r"(\w+)", "word") == (["word"],)  # Single group


def test_regex_search_groups_list():
    node = RegexSearchGroupsList()
    assert node.search_groups(r"(foo)(bar)", "foobar") == (["foo", "bar"],)
    assert node.search_groups(r"(test)(\d+)", "test123") == (["test", "123"],)
    assert node.search_groups(r"(nothing)", "no match here") == ([],)  # No match
    assert node.search_groups(r"(\w+)", "word") == (["word"],)  # Single group


def test_regex_search_groups_list():
    node = RegexSearchGroupsList()
    assert node.search_groups(r"(foo)(bar)", "foobar") == (["foo", "bar"],)
    assert node.search_groups(r"(test)(\d+)", "test123") == (["test", "123"],)
    assert node.search_groups(r"(nothing)", "no match here") == ([],)  # No match
    assert node.search_groups(r"(\w+)", "word") == (["word"],)  # Single group


def test_regex_search_groups_list():
    node = RegexSearchGroupsList()
    assert node.search_groups(r"(foo)(bar)", "foobar") == (["foo", "bar"],)
    assert node.search_groups(r"(test)(\d+)", "test123") == (["test", "123"],)
    assert node.search_groups(r"(nothing)", "no match here") == ([],)  # No match
    assert node.search_groups(r"(\w+)", "word") == (["word"],)  # Single group


def test_regex_search_groups_list():
    node = RegexSearchGroupsList()
    assert node.search_groups(r"(foo)(bar)", "foobar") == (["foo", "bar"],)
    assert node.search_groups(r"(test)(\d+)", "test123") == (["test", "123"],)
    assert node.search_groups(r"(nothing)", "no match here") == ([],)  # No match
    assert node.search_groups(r"(\w+)", "word") == (["word"],)  # Single group


def test_regex_search_groups_list():
    node = RegexSearchGroupsList()
    assert node.search_groups(r"(foo)(bar)", "foobar") == (["foo", "bar"],)
    assert node.search_groups(r"(test)(\d+)", "test123") == (["test", "123"],)
    assert node.search_groups(r"(nothing)", "no match here") == ([],)  # No match
    assert node.search_groups(r"(\w+)", "word") == (["word"],)  # Single group


def test_regex_group_dict():
    node = RegexGroupDict()
    pattern = r"(?P<word>\w+)-(?P<number>\d+)"
    string = "test-123"
    assert node.groupdict(pattern, string) == ({"word": "test", "number": "123"},)
    assert node.groupdict(pattern, "no-match") == ({},)  # No match
    assert node.groupdict(r"(?P<name>\w+)", "Example") == ({"name": "Example"},)


def test_regex_findall():
    node = RegexFindallDataList()
    assert node.findall(r"\d+", "abc 123 def 456") == (["123", "456"],)
    assert node.findall(r"\b[a-zA-Z]+\b", "Multiple words here") == (["Multiple", "words", "here"],)
    assert node.findall(r"nonexistent", "no match") == ([],)  # No match
    assert node.findall(r"(a)(b)", "ab ab") == ([("a", "b"), ("a", "b")],)  # Multiple groups


def test_regex_findall_list():
    node = RegexFindallList()
    assert node.findall(r"\d+", "abc 123 def 456") == (["123", "456"],)
    assert node.findall(r"\b[a-zA-Z]+\b", "Multiple words here") == (["Multiple", "words", "here"],)
    assert node.findall(r"nonexistent", "no match") == ([],)  # No match
    assert node.findall(r"(a)(b)", "ab ab") == ([("a", "b"), ("a", "b")],)  # Multiple groups


def test_regex_split():
    node = RegexSplitDataList()
    pattern = r",\s*"
    string = "one, two, three"
    assert node.split(pattern, string) == (["one", "two", "three"],)
    assert node.split(r"\s+", "split several words") == (["split", "several", "words"],)  # Whitespace split
    assert node.split(r"z", "nozsplit") == (["no", "split"],)  # Split by 'z'


def test_regex_split_list():
    node = RegexSplitList()
    pattern = r",\s*"
    string = "one, two, three"
    assert node.split(pattern, string) == (["one", "two", "three"],)
    assert node.split(r"\s+", "split several words") == (["split", "several", "words"],)  # Whitespace split
    assert node.split(r"z", "nozsplit") == (["no", "split"],)  # Split by 'z'


def test_regex_sub():
    node = RegexSub()
    assert node.sub(r"cat", "dog", "cat is here") == ("dog is here",)
    assert node.sub(r"\d+", "NUMBER", "abc 123 def 456") == ("abc NUMBER def NUMBER",)
    assert node.sub(r"\d+", "NUMBER", "abc 123 def 456", count=1) == ("abc NUMBER def 456",)  # Limit replacements
    assert node.sub(r"[aeiou]", "*", "hello") == ("h*ll*",)


def test_regex_test():
    node = RegexTest()
    assert node.test(r"abc", "a quick abc") == (True,)
    assert node.test(r"def", "a quick abc") == (False,)
    assert node.test(r"\d+", "contains 456") == (True,)
    assert node.test(r"^\s*$", "") == (True,)  # Empty string matches whitespace pattern
