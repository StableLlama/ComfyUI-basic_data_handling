import os
import pytest
import platform

from src.basic_data_handling.path_nodes import (
    PathJoin, PathAbspath, PathExists, PathIsFile, PathIsDir, PathGetSize,
    PathSplit, PathSplitExt, PathBasename, PathDirname, PathGetExtension,
    PathSetExtension, PathNormalize, PathRelative, PathGlob, PathExpandVars, PathGetCwd,
    PathListDir, PathIsAbsolute, PathCommonPrefix,
)


def test_path_join():
    node = PathJoin()
    assert node.join_paths("folder", "file.txt") == (os.path.join("folder", "file.txt"),)
    assert node.join_paths("folder", "") == (os.path.join("folder"),)
    assert node.join_paths(".", "") == (".",)
    # Test join with empty first path
    assert node.join_paths("", "file.txt") == ("file.txt",)
    # Test with multiple path components
    nested_path = os.path.join("folder", "subfolder", "file.txt")
    assert node.join_paths("folder", os.path.join("subfolder", "file.txt")) == (nested_path,)


def test_path_abspath():
    node = PathAbspath()
    assert node.get_abspath(".") == (os.path.abspath("."),)
    assert node.get_abspath("folder/file.txt") == (os.path.abspath("folder/file.txt"),)
    # Test with empty string (should return current directory)
    assert node.get_abspath("") == (os.path.abspath(os.getcwd()),)
    # Test with relative path with special characters
    assert node.get_abspath("./file.txt") == (os.path.abspath("./file.txt"),)
    assert node.get_abspath("../file.txt") == (os.path.abspath("../file.txt"),)


def test_path_exists(tmp_path):
    node = PathExists()
    existing_file = tmp_path / "file.txt"
    existing_file.write_text("content")
    existing_dir = tmp_path / "directory"
    existing_dir.mkdir()

    assert node.check_exists(str(existing_file)) == (True,)
    assert node.check_exists(str(existing_dir)) == (True,)
    assert node.check_exists("nonexistent.file") == (False,)
    # Test with special paths
    assert node.check_exists(".") == (True,)
    # Test with path containing non-existent parent directory
    assert node.check_exists(str(tmp_path / "nonexistent" / "file.txt")) == (False,)


def test_path_is_file(tmp_path):
    node = PathIsFile()
    file = tmp_path / "file.txt"
    file.write_text("content")
    directory = tmp_path / "directory"
    directory.mkdir()

    assert node.check_is_file(str(file)) == (True,)
    assert node.check_is_file(str(directory)) == (False,)
    assert node.check_is_file("nonexistent.file") == (False,)
    # Test with empty path
    assert node.check_is_file("") == (False,)
    # Test with special paths
    assert node.check_is_file(".") == (False,)
    # Test with symlink to file if platform supports
    if hasattr(os, 'symlink'):
        try:
            symlink = tmp_path / "symlink.txt"
            os.symlink(str(file), str(symlink))
            assert node.check_is_file(str(symlink)) == (True,)
        except (OSError, NotImplementedError):
            # Symlinks might not be supported on all platforms
            pass


def test_path_is_dir(tmp_path):
    node = PathIsDir()
    directory = tmp_path / "directory"
    directory.mkdir()
    file = tmp_path / "file.txt"
    file.write_text("content")

    assert node.check_is_dir(str(directory)) == (True,)
    assert node.check_is_dir(str(file)) == (False,)
    assert node.check_is_dir("nonexistent.dir") == (False,)
    # Test with special paths
    assert node.check_is_dir(".") == (True,)
    assert node.check_is_dir("") == (False,)
    # Test with nested directory
    nested_dir = directory / "nested"
    nested_dir.mkdir()
    assert node.check_is_dir(str(nested_dir)) == (True,)
    # Test with symlink to directory if platform supports
    if hasattr(os, 'symlink'):
        try:
            symlink = tmp_path / "symlink_dir"
            os.symlink(str(directory), str(symlink), target_is_directory=True)
            assert node.check_is_dir(str(symlink)) == (True,)
        except (OSError, NotImplementedError, TypeError):
            # Symlinks might not be supported on all platforms
            pass


def test_path_get_size(tmp_path):
    node = PathGetSize()
    file = tmp_path / "file.txt"
    file.write_text("content")
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")
    large_file = tmp_path / "large.txt"
    large_file.write_text("a" * 1024)  # 1KB file

    assert node.get_size(str(file)) == (len("content"),)
    assert node.get_size(str(empty_file)) == (0,)
    assert node.get_size(str(large_file)) == (1024,)

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
    # Test with empty path
    assert node.split_path("") == ("", "")
    # Test with just directory separator
    assert node.split_path("/") == ("/", "")
    # Test with nested paths
    nested_path = os.path.join("folder", "subfolder", "file.txt")
    assert node.split_path(nested_path) == (os.path.dirname(nested_path), "file.txt")
    # Test with trailing separator
    dir_with_sep = "folder" + os.sep
    assert node.split_path(dir_with_sep) == ("folder", "")


def test_path_splitext():
    node = PathSplitExt()
    assert node.split_ext("file.txt") == ("file", ".txt")
    assert node.split_ext("file") == ("file", "")
    # Test with multiple extensions
    assert node.split_ext("file.tar.gz") == ("file.tar", ".gz")
    # Test with path containing directory
    path = os.path.join("folder", "file.txt")
    assert node.split_ext(path) == (os.path.join("folder", "file"), ".txt")
    # Test with hidden file
    assert node.split_ext(".gitignore") == (".gitignore", "")
    # Test with empty string
    assert node.split_ext("") == ("", "")


def test_path_basename():
    node = PathBasename()
    assert node.get_basename("folder/file.txt") == ("file.txt",)
    assert node.get_basename("file.txt") == ("file.txt",)
    # Test with trailing slash
    assert node.get_basename("folder/") == ("",)
    # Test with empty path
    assert node.get_basename("") == ("",)
    # Test with root directory
    assert node.get_basename("/") == ("",)
    # Test with multiple nested directories
    assert node.get_basename("folder/subfolder/file.txt") == ("file.txt",)


def test_path_dirname():
    node = PathDirname()
    assert node.get_dirname("folder/file.txt") == ("folder",)
    assert node.get_dirname("file.txt") == ("",)
    # Test with trailing slash
    assert node.get_dirname("folder/") == ("folder",)
    # Test with empty path
    assert node.get_dirname("") == ("",)
    # Test with root directory
    assert node.get_dirname("/") == ("/",)
    # Test with nested directories
    assert node.get_dirname("folder/subfolder/file.txt") == (os.path.join("folder", "subfolder"),)


def test_path_get_extension():
    node = PathGetExtension()
    assert node.get_extension("file.txt") == (".txt",)
    assert node.get_extension("file") == ("",)
    # Test with multiple dots
    assert node.get_extension("file.tar.gz") == (".gz",)
    # Test with hidden file
    assert node.get_extension(".gitignore") == ("",)
    # Test with path containing directory
    assert node.get_extension("folder/file.txt") == (".txt",)
    # Test with empty string
    assert node.get_extension("") == ("",)

def test_path_set_extension():
    node = PathSetExtension()
    # Test basic extension replacement
    assert node.set_extension("file.txt", ".jpg") == ("file.jpg",)
    # Test adding extension to file without extension
    assert node.set_extension("file", ".png") == ("file.png",)
    # Test with extension without dot prefix
    assert node.set_extension("document.docx", "pdf") == ("document.pdf",)
    # Test with path containing directory
    assert node.set_extension("folder/image.jpg", ".png") == ("folder/image.png",)
    # Test with multiple dots in filename
    assert node.set_extension("archive.tar.gz", ".zip") == ("archive.tar.zip",)
    # Test with empty extension (removes extension)
    assert node.set_extension("config.ini", "") == ("config",)
    # Test with empty string as path
    assert node.set_extension("", ".txt") == (".txt",)



def test_path_normalize():
    node = PathNormalize()
    assert node.normalize_path("folder/../file.txt") == (os.path.normpath("folder/../file.txt"),)
    assert node.normalize_path("folder//file.txt") == (os.path.normpath("folder//file.txt"),)
    # Test with empty path
    assert node.normalize_path("") == (".",)
    # Test with current directory references
    assert node.normalize_path("./folder/./file.txt") == (os.path.normpath("./folder/./file.txt"),)
    # Test with parent directory references that cancel out
    assert node.normalize_path("folder/../folder/file.txt") == (os.path.normpath("folder/../folder/file.txt"),)
    # Test with mixed separators
    mixed_sep_path = "folder" + os.sep + "subfolder" + ("/" if os.sep == "\\" else "\\") + "file.txt"
    assert node.normalize_path(mixed_sep_path) == (os.path.normpath(mixed_sep_path),)


def test_path_relative(tmp_path):
    node = PathRelative()
    start = tmp_path / "start"
    start.mkdir()
    target = tmp_path / "start/target"
    target.mkdir()

    assert node.get_relative_path(str(target), str(start)) == (os.path.relpath(str(target), str(start)),)
    assert node.get_relative_path(str(target)) == (os.path.relpath(str(target), os.getcwd()),)
    # Test with same path
    assert node.get_relative_path(str(start), str(start)) == (".",)
    # Test with sibling paths
    sibling = tmp_path / "sibling"
    sibling.mkdir()
    expected = os.path.relpath(str(sibling), str(start))
    assert node.get_relative_path(str(sibling), str(start)) == (expected,)
    # Test with parent directory
    parent_rel = os.path.relpath(str(tmp_path), str(target))
    assert node.get_relative_path(str(tmp_path), str(target)) == (parent_rel,)


def test_path_glob(tmp_path):
    node = PathGlob()
    (tmp_path / "file1.txt").write_text("content")
    (tmp_path / "file2.txt").write_text("content")
    (tmp_path / "file3.txt").write_text("content")
    (tmp_path / "image1.jpg").write_text("image")
    (tmp_path / "image2.png").write_text("image")
    # Create subdirectory with files
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "subfile1.txt").write_text("sub content")
    (subdir / "subfile2.txt").write_text("sub content")

    # Test simple glob pattern
    result = node.glob_paths(str(tmp_path / "*.txt"))
    expected = sorted([str(tmp_path / f"file{i}.txt") for i in range(1, 4)])
    assert sorted(result[0]) == expected

    # Test with image files
    img_result = node.glob_paths(str(tmp_path / "image*"))
    img_expected = sorted([str(tmp_path / "image1.jpg"), str(tmp_path / "image2.png")])
    assert sorted(img_result[0]) == img_expected

    # Test with character class
    char_result = node.glob_paths(str(tmp_path / "file[1-2].txt"))
    char_expected = sorted([str(tmp_path / f"file{i}.txt") for i in range(1, 3)])
    assert sorted(char_result[0]) == char_expected

    # Test recursive globbing
    recursive_result = node.glob_paths(str(tmp_path / "**/*.txt"), recursive=True)
    recursive_expected = sorted([
        str(tmp_path / f"file{i}.txt") for i in range(1, 4)
    ] + [
        str(subdir / f"subfile{i}.txt") for i in range(1, 3)
    ])
    assert sorted(recursive_result[0]) == recursive_expected

    # Test with no matches
    no_match_result = node.glob_paths(str(tmp_path / "nomatch*.txt"))
    assert len(no_match_result[0]) == 0


def test_path_expand_vars(monkeypatch):
    node = PathExpandVars()
    monkeypatch.setenv("TEST_VAR", "test_value")
    monkeypatch.setenv("PATH_VAR", "path/to/somewhere")
    monkeypatch.setenv("EMPTY_VAR", "")

    assert node.expand_vars("$TEST_VAR/path") == ("test_value/path",)
    assert node.expand_vars("${TEST_VAR}/path") == ("test_value/path",)
    # Test with multiple variables
    assert node.expand_vars("$TEST_VAR/$PATH_VAR") == ("test_value/path/to/somewhere",)
    # Test with empty variable
    assert node.expand_vars("$EMPTY_VAR/path") == ("/path",)
    # Test with no variables
    assert node.expand_vars("regular/path") == ("regular/path",)
    # Test with empty string
    assert node.expand_vars("") == ("",)


def test_path_get_cwd():
    node = PathGetCwd()
    assert node.get_cwd() == (os.getcwd(),)
    # Verify that the result is an absolute path
    assert os.path.isabs(node.get_cwd()[0])
    # Verify that the directory exists
    assert os.path.exists(node.get_cwd()[0])
    assert os.path.isdir(node.get_cwd()[0])


def test_path_list_dir(tmp_path):
    node = PathListDir()
    # Set up a directory structure for testing
    (tmp_path / "file1.txt").write_text("content")
    (tmp_path / "file2.txt").write_text("content")
    (tmp_path / "image.jpg").write_text("image")
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()
    (tmp_path / ".hidden_file").write_text("hidden")
    (tmp_path / ".hidden_dir").mkdir()

    # Test listing all entries
    all_entries = node.list_directory(str(tmp_path))
    assert "file1.txt" in all_entries[0]
    assert "file2.txt" in all_entries[0]
    assert "image.jpg" in all_entries[0]
    assert "dir1" in all_entries[0]
    assert "dir2" in all_entries[0]
    assert ".hidden_file" in all_entries[0]
    assert ".hidden_dir" in all_entries[0]

    # Test listing only files
    only_files = node.list_directory(str(tmp_path), files_only=True)
    assert "file1.txt" in only_files[0]
    assert "file2.txt" in only_files[0]
    assert "image.jpg" in only_files[0]
    assert ".hidden_file" in only_files[0]
    assert "dir1" not in only_files[0]
    assert "dir2" not in only_files[0]
    assert ".hidden_dir" not in only_files[0]

    # Test listing only directories
    only_dirs = node.list_directory(str(tmp_path), dirs_only=True)
    assert "file1.txt" not in only_dirs[0]
    assert "file2.txt" not in only_dirs[0]
    assert "image.jpg" not in only_dirs[0]
    assert ".hidden_file" not in only_dirs[0]
    assert "dir1" in only_dirs[0]
    assert "dir2" in only_dirs[0]
    assert ".hidden_dir" in only_dirs[0]

    # Test with non-existent directory
    with pytest.raises(FileNotFoundError):
        node.list_directory(str(tmp_path / "nonexistent"))

    # Test with file instead of directory
    with pytest.raises(NotADirectoryError):
        node.list_directory(str(tmp_path / "file1.txt"))

    # Test with empty path (should use current directory)
    assert len(node.list_directory("")[0]) > 0


def test_path_is_absolute():
    node = PathIsAbsolute()
    # Test with absolute paths
    assert node.check_is_absolute("/") == (True,)
    assert node.check_is_absolute(os.path.abspath(".")) == (True,)
    # Test with relative paths
    assert node.check_is_absolute("relative/path") == (False,)
    assert node.check_is_absolute("./path") == (False,)
    assert node.check_is_absolute("../path") == (False,)
    # Test with empty path
    assert node.check_is_absolute("") == (False,)
    # Test Windows-specific paths if applicable
    if platform.system() == "Windows":
        assert node.check_is_absolute("C:\\Windows") == (True,)
        assert node.check_is_absolute("C:/Windows") == (True,)
        assert node.check_is_absolute("\\\\server\\share") == (True,)
        assert node.check_is_absolute("C:relative\\path") == (False,)


def test_path_common_prefix():
    node = PathCommonPrefix()
    # Test with paths having common prefix
    path1 = "/path/to/file1.txt"
    path2 = "/path/to/file2.txt"
    assert node.get_common_prefix(path1, path2) == ("/path/to/file",)

    # Test with paths without common prefix
    path3 = "/path/to/file.txt"
    path4 = "/different/path/file.txt"
    assert node.get_common_prefix(path3, path4) == ("/",)

    # Test with exact same paths
    assert node.get_common_prefix(path1, path1) == (path1,)

    # Test with one path being a prefix of the other
    path5 = "/path/to"
    path6 = "/path/to/subdir/file.txt"
    assert node.get_common_prefix(path5, path6) == ("/path/to",)

    # Test with both empty paths
    assert node.get_common_prefix("", "") == ("",)
