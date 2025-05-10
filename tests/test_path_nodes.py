import os
import pytest

from src.basic_data_handling.path_nodes import (
    PathJoin, PathAbspath, PathExists, PathIsFile, PathIsDir, PathGetSize,
    PathSplit, PathSplitExt, PathBasename, PathDirname, PathGetExtension,
    PathNormalize, PathRelative, PathGlob, PathExpandVars, PathGetCwd,
    PathListDir, PathIsAbsolute, PathCommonPrefix,
)


def test_path_join():
    node = PathJoin()
    assert node.join_paths("folder", "file.txt") == (os.path.join("folder", "file.txt"),)
    assert node.join_paths("folder", "") == (os.path.join("folder"),)
    assert node.join_paths(".", "") == (".",)


def test_path_abspath():
    node = PathAbspath()
    assert node.get_abspath(".") == (os.path.abspath("."),)
    assert node.get_abspath("folder/file.txt") == (os.path.abspath("folder/file.txt"),)


def test_path_exists(tmp_path):
    node = PathExists()
    existing_file = tmp_path / "file.txt"
    existing_file.write_text("content")

    assert node.check_exists(str(existing_file)) == (True,)
    assert node.check_exists("nonexistent.file") == (False,)


def test_path_is_file(tmp_path):
    node = PathIsFile()
    file = tmp_path / "file.txt"
    file.write_text("content")
    directory = tmp_path / "directory"
    directory.mkdir()

    assert node.check_is_file(str(file)) == (True,)
    assert node.check_is_file(str(directory)) == (False,)
    assert node.check_is_file("nonexistent.file") == (False,)


def test_path_is_dir(tmp_path):
    node = PathIsDir()
    directory = tmp_path / "directory"
    directory.mkdir()
    file = tmp_path / "file.txt"
    file.write_text("content")

    assert node.check_is_dir(str(directory)) == (True,)
    assert node.check_is_dir(str(file)) == (False,)
    assert node.check_is_dir("nonexistent.dir") == (False,)


def test_path_get_size(tmp_path):
    node = PathGetSize()
    file = tmp_path / "file.txt"
    file.write_text("content")

    assert node.get_size(str(file)) == (len("content"),)

    with pytest.raises(FileNotFoundError):
        node.get_size("nonexistent.file")

    directory = tmp_path / "directory"
    directory.mkdir()

    with pytest.raises(ValueError):
        node.get_size(str(directory))


def test_path_split():
    node = PathSplit()
    path = os.path.join("folder", "file.txt")

    assert node.split_path(path) == (os.path.dirname(path), os.path.basename(path))
    assert node.split_path("file.txt") == ("", "file.txt")


def test_path_splitext():
    node = PathSplitExt()
    assert node.split_ext("file.txt") == ("file", ".txt")
    assert node.split_ext("file") == ("file", "")


def test_path_basename():
    node = PathBasename()
    assert node.get_basename("folder/file.txt") == ("file.txt",)
    assert node.get_basename("file.txt") == ("file.txt",)


def test_path_dirname():
    node = PathDirname()
    assert node.get_dirname("folder/file.txt") == ("folder",)
    assert node.get_dirname("file.txt") == ("",)


def test_path_get_extension():
    node = PathGetExtension()
    assert node.get_extension("file.txt") == (".txt",)
    assert node.get_extension("file") == ("",)


def test_path_normalize():
    node = PathNormalize()
    assert node.normalize_path("folder/../file.txt") == (os.path.normpath("folder/../file.txt"),)
    assert node.normalize_path("folder//file.txt") == (os.path.normpath("folder//file.txt"),)


def test_path_relative(tmp_path):
    node = PathRelative()
    start = tmp_path / "start"
    start.mkdir()
    target = tmp_path / "start/target"
    target.mkdir()

    assert node.get_relative_path(str(target), str(start)) == (os.path.relpath(str(target), str(start)),)
    assert node.get_relative_path(str(target)) == (os.path.relpath(str(target), os.getcwd()),)


def test_path_glob(tmp_path):
    node = PathGlob()
    (tmp_path / "file1.txt").write_text("content")
    (tmp_path / "file2.txt").write_text("content")
    (tmp_path / "file3.txt").write_text("content")

    result = node.glob_paths(str(tmp_path / "*.txt"))
    expected = sorted([str(tmp_path / f"file{i}.txt") for i in range(1, 4)])

    assert sorted(result[0]) == expected

    recursive_node = PathGlob()
    assert recursive_node.glob_paths(str(tmp_path), recursive="True")[0]


def test_path_expand_vars(monkeypatch):
    node = PathExpandVars()
    monkeypatch.setenv("TEST_VAR", "test_value")

    assert node.expand_vars("$TEST_VAR/path") == ("test_value/path",)
    assert node.expand_vars("${TEST_VAR}/path") == ("test_value/path",)


def test_path_get_cwd():
    node = PathGetCwd()
    assert node.get_cwd() == (os.getcwd(),)


def test_path_list_dir(tmp_path):
    node = PathListDir()
    (tmp_path / "file1.txt").write_text("content")
    (tmp_path / "dir1").mkdir()

    all_entries = node.list_directory(str(tmp_path))
    assert "file1.txt" in all_entries[0]
    assert "dir1" in all_entries[0]

    only_files = node.list_directory(str(tmp_path), files_only="True")
    assert "file1.txt" in only_files[0]
    assert "dir1" not in only_files[0]

    only_dirs = node.list_directory(str(tmp_path), dirs_only="True")
    assert "file1.txt" not in only_dirs[0]
    assert "dir1" in only_dirs[0]


def test_path_is_absolute():
    node = PathIsAbsolute()
    assert node.check_is_absolute("/") == (True,)
    assert node.check_is_absolute("relative/path") == (False,)


def test_path_common_prefix():
    node = PathCommonPrefix()
    path1 = "/path/to/file1.txt"
    path2 = "/path/to/file2.txt"

    assert node.get_common_prefix(path1, path2) == (os.path.commonprefix([path1, path2]),)
