from inspect import cleandoc
import os
import glob


class PathJoin:
    """
    Joins multiple path components into a single path.

    This node takes multiple path components and joins them intelligently
    to form a single path. It handles directory separators correctly
    for the operating system.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path1": ("STRING", {"default": ""}),
            },
            "optional": {
                "path2": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("path",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "join_paths"

    def join_paths(self, path1: str, path2: str = "") -> tuple[str]:
        paths = [p for p in [path1, path2] if p]
        return (str(os.path.join(*paths)),)


class PathAbspath:
    """
    Returns the absolute path of a file or directory.

    This node takes a path and returns its absolute (full) path
    by resolving any relative path components and symbolic links.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("absolute_path",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_abspath"

    def get_abspath(self, path: str) -> tuple[str]:
        return (os.path.abspath(path),)


class PathExists:
    """
    Checks if a path exists in the filesystem.

    This node returns True if the path exists (either as a file or a directory),
    and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("exists",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_exists"

    def check_exists(self, path: str) -> tuple[bool]:
        return (os.path.exists(path),)


class PathIsFile:
    """
    Checks if a path points to a file.

    This node returns True if the path exists and is a regular file,
    and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_file",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_is_file"

    def check_is_file(self, path: str) -> tuple[bool]:
        return (os.path.isfile(path),)


class PathIsDir:
    """
    Checks if a path points to a directory.

    This node returns True if the path exists and is a directory,
    and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_dir",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_is_dir"

    def check_is_dir(self, path: str) -> tuple[bool]:
        return (os.path.isdir(path),)


class PathGetSize:
    """
    Returns the size of a file in bytes.

    This node returns the size in bytes of the file at the given path.
    Raises an error if the path doesn't exist or isn't a file.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("size_bytes",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_size"

    def get_size(self, path: str) -> tuple[int]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Basic data handling: Path does not exist: {path}")
        if not os.path.isfile(path):
            raise ValueError(f"Basic data handling: Path is not a file: {path}")
        return (os.path.getsize(path),)


class PathSplit:
    """
    Splits a path into directory and filename components.

    This node takes a path and returns a tuple containing the directory path
    and the filename.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("directory", "filename")
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "split_path"

    def split_path(self, path: str) -> tuple[str, str]:
        return os.path.split(path)


class PathSplitExt:
    """
    Splits a path into name and extension components.

    This node takes a path and returns a tuple containing the path without
    the extension and the extension (including the dot).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("path_without_ext", "extension")
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "split_ext"

    def split_ext(self, path: str) -> tuple[str, str]:
        return os.path.splitext(path)


class PathBasename:
    """
    Returns the base name of a path.

    This node extracts the filename component from a path,
    removing any directory information.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("basename",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_basename"

    def get_basename(self, path: str) -> tuple[str]:
        return (os.path.basename(path),)


class PathDirname:
    """
    Returns the directory name of a path.

    This node extracts the directory component from a path,
    removing the filename.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("dirname",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_dirname"

    def get_dirname(self, path: str) -> tuple[str]:
        return (os.path.dirname(path),)


class PathGetExtension:
    """
    Returns the extension of a file.

    This node extracts the file extension from a path,
    including the dot (e.g., '.txt').
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("extension",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_extension"

    def get_extension(self, path: str) -> tuple[str]:
        return (os.path.splitext(path)[1],)


class PathNormalize:
    """
    Normalizes a path.

    This node normalizes a path by collapsing redundant separators,
    resolving up-level references, and converting to the correct
    separator for the operating system.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("normalized_path",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "normalize_path"

    def normalize_path(self, path: str) -> tuple[str]:
        return (os.path.normpath(path),)


class PathRelative:
    """
    Returns a relative path.

    This node computes a relative path from the 'start' path to the 'path'.
    If 'start' is not provided, the current working directory is used.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            },
            "optional": {
                "start": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("relative_path",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_relative_path"

    def get_relative_path(self, path: str, start: str = "") -> tuple[str]:
        if not start:
            start = os.getcwd()
        return (os.path.relpath(path, start),)


class PathGlob:
    """
    Finds paths matching a pattern.

    This node returns a list of paths matching the given pattern.
    The pattern follows shell-style wildcard rules:
    * - matches any number of characters
    ? - matches a single character
    [seq] - matches any character in seq
    [!seq] - matches any character not in seq
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pattern": ("STRING", {"default": "*.txt"}),
            },
            "optional": {
                "recursive": (["False", "True"], {"default": "False"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("matching_paths",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "glob_paths"
    OUTPUT_IS_LIST = (True,)

    def glob_paths(self, pattern: str, recursive: str = "False") -> tuple[list[str]]:
        is_recursive = (recursive == "True")
        if is_recursive:
            # If recursive, use ** pattern with glob.glob's recursive option
            return (glob.glob(pattern, recursive=True),)
        else:
            return (glob.glob(pattern),)


class PathExpandVars:
    """
    Expands environment variables in a path.

    This node replaces environment variables in a path with their values.
    For example, $HOME or ${HOME} on Unix, or %USERPROFILE% on Windows.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("expanded_path",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "expand_vars"

    def expand_vars(self, path: str) -> tuple[str]:
        return (os.path.expandvars(path),)


class PathGetCwd:
    """
    Returns the current working directory.

    This node returns the current working directory as an absolute path.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("current_directory",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_cwd"

    def get_cwd(self) -> tuple[str]:
        return (os.getcwd(),)


class PathListDir:
    """
    Lists the contents of a directory.

    This node returns a list of files and directories in the specified path.
    If 'files_only' is True, it only returns files.
    If 'dirs_only' is True, it only returns directories.
    If both are False, it returns all contents.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            },
            "optional": {
                "files_only": (["False", "True"], {"default": "False"}),
                "dirs_only": (["False", "True"], {"default": "False"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("entries",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "list_directory"
    OUTPUT_IS_LIST = (True,)

    def list_directory(self, path: str, files_only: str = "False", dirs_only: str = "False") -> tuple[list[str]]:
        if not path:
            path = os.getcwd()

        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory does not exist: {path}")
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Basic data handling: Path is not a directory: {path}")

        entries = os.listdir(path)

        if files_only == "True":
            entries = [e for e in entries if os.path.isfile(os.path.join(path, e))]
        elif dirs_only == "True":
            entries = [e for e in entries if os.path.isdir(os.path.join(path, e))]

        return (entries,)


class PathIsAbsolute:
    """
    Checks if a path is absolute.

    This node returns True if the path is absolute (begins at the root directory),
    and False if it's relative.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_absolute",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_is_absolute"

    def check_is_absolute(self, path: str) -> tuple[bool]:
        return (os.path.isabs(path),)


class PathCommonPrefix:
    """
    Finds the common prefix of multiple paths.

    This node returns the longest common leading component of the given paths.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path1": ("STRING", {"default": ""}),
            },
            "optional": {
                "path2": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("common_prefix",)
    CATEGORY = "Basic/path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_common_prefix"

    def get_common_prefix(self, path1: str, path2: str = "") -> tuple[str]:
        paths = [p for p in [path1, path2] if p]
        return (os.path.commonprefix(paths),)


NODE_CLASS_MAPPINGS = {
    "Basic data handling: PathJoin": PathJoin,
    "Basic data handling: PathAbspath": PathAbspath,
    "Basic data handling: PathExists": PathExists,
    "Basic data handling: PathIsFile": PathIsFile,
    "Basic data handling: PathIsDir": PathIsDir,
    "Basic data handling: PathGetSize": PathGetSize,
    "Basic data handling: PathSplit": PathSplit,
    "Basic data handling: PathSplitExt": PathSplitExt,
    "Basic data handling: PathBasename": PathBasename,
    "Basic data handling: PathDirname": PathDirname,
    "Basic data handling: PathGetExtension": PathGetExtension,
    "Basic data handling: PathNormalize": PathNormalize,
    "Basic data handling: PathRelative": PathRelative,
    "Basic data handling: PathGlob": PathGlob,
    "Basic data handling: PathExpandVars": PathExpandVars,
    "Basic data handling: PathGetCwd": PathGetCwd,
    "Basic data handling: PathListDir": PathListDir,
    "Basic data handling: PathIsAbsolute": PathIsAbsolute,
    "Basic data handling: PathCommonPrefix": PathCommonPrefix,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: PathJoin": "join",
    "Basic data handling: PathAbspath": "abspath",
    "Basic data handling: PathExists": "exists",
    "Basic data handling: PathIsFile": "is_file",
    "Basic data handling: PathIsDir": "is_dir",
    "Basic data handling: PathGetSize": "get_size",
    "Basic data handling: PathSplit": "split",
    "Basic data handling: PathSplitExt": "splitext",
    "Basic data handling: PathBasename": "basename",
    "Basic data handling: PathDirname": "dirname",
    "Basic data handling: PathGetExtension": "get_extension",
    "Basic data handling: PathNormalize": "normalize",
    "Basic data handling: PathRelative": "relative",
    "Basic data handling: PathGlob": "glob",
    "Basic data handling: PathExpandVars": "expand_vars",
    "Basic data handling: PathGetCwd": "get_cwd",
    "Basic data handling: PathListDir": "list_dir",
    "Basic data handling: PathIsAbsolute": "is_absolute",
    "Basic data handling: PathCommonPrefix": "common_prefix",
}
