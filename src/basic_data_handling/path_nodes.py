from inspect import cleandoc
import os
import glob

try:
    from comfy.comfy_types.node_typing import IO, ComfyNodeABC
except:

    class IO:
        BOOLEAN = "BOOLEAN"
        INT = "INT"
        FLOAT = "FLOAT"
        STRING = "STRING"
        NUMBER = "FLOAT,INT"
        IMAGE = "IMAGE"
        MASK = "MASK"
        ANY = "*"

    ComfyNodeABC = object

try:
    from folder_paths import get_input_directory, get_output_directory
except:

    def get_input_directory():
        return "./"

    get_output_directory = get_input_directory

# ComfyUI's official prefix->path resolver is reused when running under ComfyUI
# so the nodes follow upstream naming exactly (folder layout, %width%/%height%/
# date token expansion, auto-incrementing counters and containment checks).
# Outside ComfyUI (e.g. the standalone test-suite) `folder_paths` is not
# importable, so a minimal local equivalent is used as a fallback only.
try:
    from folder_paths import get_save_image_path as _official_get_save_image_path
except Exception:
    _official_get_save_image_path = None


def _require_numpy():
    try:
        import numpy as np

        return np
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            "basic_data_handling: Missing dependency 'numpy'. It seems your ComfyUI installation is faulty."
            "Only for development purposes: Install it with `pip install .[dev] numpy torch pillow` or `pip install numpy`."
        ) from e


def _require_torch():
    try:
        import torch

        return torch
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            "basic_data_handling: Missing dependency 'torch'. It seems your ComfyUI installation is faulty."
            "Only for development purposes: Install it with `pip install .[dev] numpy torch pillow` or `pip install torch`."
        ) from e


def _require_pillow():
    try:
        from PIL import Image, ImageOps

        return Image, ImageOps
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            "basic_data_handling: Missing dependency 'pillow'. It seems your ComfyUI installation is faulty."
            "Only for development purposes: Install it with `pip install .[dev] numpy torch pillow` or `pip install pillow`."
        ) from e


# helper functions:


def load_image_helper(path: str):
    """Helper function to load an image from a path"""
    Image, ImageOps = _require_pillow()
    try:
        import pillow_jxl  # noqa: F401 - imported but unused, kept for JPEG XL support
    except ModuleNotFoundError:
        pass

    if not os.path.exists(path):
        return None

    # Open and process the image
    try:
        img = Image.open(path)
        img = ImageOps.exif_transpose(img)
        return img
    except Exception:
        return None


def extract_mask_from_alpha(img):
    """Extract a mask from the alpha channel of an image"""
    np = _require_numpy()
    torch = _require_torch()

    if "A" in img.getbands():
        alpha = np.array(img.getchannel("A")).astype(np.float32) / 255.0
        mask_tensor = 1.0 - torch.from_numpy(alpha)
    elif img.mode == "P" and "transparency" in img.info:
        alpha = np.array(img.convert("RGBA").getchannel("A")).astype(np.float32) / 255.0
        mask_tensor = 1.0 - torch.from_numpy(alpha)
    else:
        # Create a blank mask if no alpha channel
        mask_tensor = torch.zeros((img.height, img.width), dtype=torch.float32)

    # Add batch dimension to mask
    mask_tensor = mask_tensor.unsqueeze(0)

    return mask_tensor


def extract_mask_from_greyscale(img):
    """Extract a mask from a greyscale image or the red channel of an RGB image"""
    np = _require_numpy()
    torch = _require_torch()

    if img.mode == "L":
        # Image is already greyscale
        gray = np.array(img).astype(np.float32) / 255.0
    elif img.mode == "RGB" or img.mode == "RGBA":
        # Use the red channel of RGB or RGBA
        gray = np.array(img.getchannel("R")).astype(np.float32) / 255.0
    else:
        # Convert to greyscale if it's another format
        gray_img = img.convert("L")
        gray = np.array(gray_img).astype(np.float32) / 255.0

    # Convert to tensor and invert (white pixels in image = transparent in mask)
    mask_tensor = 1.0 - torch.from_numpy(gray)

    # Add batch dimension
    mask_tensor = mask_tensor.unsqueeze(0)

    return mask_tensor


# the nodes:


class PathAbspath(ComfyNodeABC):
    """
    Returns the absolute path of a file or directory.

    This node takes a path and returns its absolute (full) path
    by resolving any relative path components and symbolic links.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path to resolve to an absolute path."}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("absolute path",)
    OUTPUT_TOOLTIPS = ("The absolute path with relative components and symlinks resolved.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_abspath"

    def get_abspath(self, path: str) -> tuple[str]:
        return (os.path.abspath(path),)


class PathBasename(ComfyNodeABC):
    """
    Returns the base name of a path.

    This node extracts the filename component from a path,
    removing any directory information.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path whose final filename component is returned."}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("basename",)
    OUTPUT_TOOLTIPS = ("The final filename component of the path.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_basename"

    def get_basename(self, path: str) -> tuple[str]:
        return (os.path.basename(path),)


class PathCommonPrefix(ComfyNodeABC):
    """
    Finds the common prefix of multiple paths.

    This node returns the longest common leading component of the given paths.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path1": (IO.STRING, {"default": "", "tooltip": "First path."}),
            },
            "optional": {
                "path2": (IO.STRING, {"default": "", "tooltip": "Second path."}),
            },
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("common prefix",)
    OUTPUT_TOOLTIPS = ("The longest common leading component of the given paths.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_common_prefix"

    def get_common_prefix(self, path1: str, path2: str = "") -> tuple[str]:
        paths = [p for p in [path1, path2] if p]
        return (os.path.commonprefix(paths),)


class PathDirname(ComfyNodeABC):
    """
    Returns the directory name of a path.

    This node extracts the directory component from a path,
    removing the filename.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path whose directory component is returned."}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("dirname",)
    OUTPUT_TOOLTIPS = ("The directory (parent) component of the path.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_dirname"

    def get_dirname(self, path: str) -> tuple[str]:
        return (os.path.dirname(path),)


class PathExists(ComfyNodeABC):
    """
    Checks if a path exists in the filesystem.

    This node returns True if the path exists (either as a file or a directory),
    and False otherwise.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path to check for existence."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("exists",)
    OUTPUT_TOOLTIPS = ("True when the path exists as a file or directory.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_exists"

    def check_exists(self, path: str) -> tuple[bool]:
        return (os.path.exists(path),)


class PathExpandVars(ComfyNodeABC):
    """
    Expands environment variables in a path.

    This node replaces environment variables in a path with their values.
    For example, $HOME or ${HOME} on Unix, or %USERPROFILE% on Windows.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path that may contain environment variables (e.g. $HOME, %USERPROFILE%)."}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("expanded path",)
    OUTPUT_TOOLTIPS = ("The path with environment variables expanded.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "expand_vars"

    def expand_vars(self, path: str) -> tuple[str]:
        return (os.path.expandvars(path),)


class PathGetCwd(ComfyNodeABC):
    """
    Returns the current working directory.

    This node returns the current working directory as an absolute path.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("current directory",)
    OUTPUT_TOOLTIPS = ("The current working directory as an absolute path.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_cwd"

    def get_cwd(self) -> tuple[str]:
        return (os.getcwd(),)


class PathGetExtension(ComfyNodeABC):
    """
    Returns the extension of a file.

    This node extracts the file extension from a path,
    including the dot (e.g., '.txt').
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path whose file extension is extracted."}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("extension",)
    OUTPUT_TOOLTIPS = ("The extension including the dot (e.g. '.txt'); empty when there is none.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_extension"

    def get_extension(self, path: str) -> tuple[str]:
        return (os.path.splitext(path)[1],)


class PathGetSize(ComfyNodeABC):
    """
    Returns the size of a file in bytes.

    This node returns the size in bytes of the file at the given path.
    Raises an error if the path doesn't exist or isn't a file.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "File whose size in bytes is returned."}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    RETURN_NAMES = ("size (bytes)",)
    OUTPUT_TOOLTIPS = ("The file size in bytes.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_size"

    def get_size(self, path: str) -> tuple[int]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Basic data handling: Path does not exist: {path}")
        if not os.path.isfile(path):
            raise ValueError(f"Basic data handling: Path is not a file: {path}")
        return (os.path.getsize(path),)


class PathGlob(ComfyNodeABC):
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
                "pattern": (IO.STRING, {"default": "*.txt", "tooltip": "Shell-style pattern to match, e.g. '*.txt'."}),
            },
            "optional": {
                "recursive": (IO.BOOLEAN, {"default": False, "tooltip": "When True, '**' also matches inside subdirectories."}),
            },
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("matching paths",)
    OUTPUT_TOOLTIPS = ("All paths matching the pattern, as a data list.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "glob_paths"
    OUTPUT_IS_LIST = (True,)

    # Class variable to store the last matched paths
    _last_matched_paths = {}

    @classmethod
    def IS_CHANGED(s, pattern: str, recursive: bool = False):
        # Get current paths
        current_paths = glob.glob(pattern, recursive=recursive)

        # Create a key for this specific pattern and recursive setting
        key = f"{pattern}_{recursive}"

        # If we haven't seen this pattern before, store it and trigger recalculation
        if key not in s._last_matched_paths:
            s._last_matched_paths[key] = current_paths
            return float("NaN")

        # Compare with previous paths
        previous_paths = s._last_matched_paths[key]
        if previous_paths != current_paths:
            # Update stored paths and trigger recalculation
            s._last_matched_paths[key] = current_paths
            return float("NaN")

        # No changes, return a consistent value
        import hashlib

        m = hashlib.md5()
        m.update(str(current_paths).encode())
        return m.hexdigest()

    def glob_paths(self, pattern: str, recursive: bool = False) -> tuple[list[str]]:
        return (glob.glob(pattern, recursive=recursive),)


class PathIsAbsolute(ComfyNodeABC):
    """
    Checks if a path is absolute.

    This node returns True if the path is absolute (begins at the root directory),
    and False if it's relative.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path to test."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is absolute",)
    OUTPUT_TOOLTIPS = ("True when the path is absolute (starts at the root).",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_is_absolute"

    def check_is_absolute(self, path: str) -> tuple[bool]:
        return (os.path.isabs(path),)


class PathIsDir(ComfyNodeABC):
    """
    Checks if a path points to a directory.

    This node returns True if the path exists and is a directory,
    and False otherwise.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path to test."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is dir",)
    OUTPUT_TOOLTIPS = ("True when the path exists and is a directory.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_is_dir"

    def check_is_dir(self, path: str) -> tuple[bool]:
        return (os.path.isdir(path),)


class PathIsFile(ComfyNodeABC):
    """
    Checks if a path points to a file.

    This node returns True if the path exists and is a regular file,
    and False otherwise.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path to test."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is file",)
    OUTPUT_TOOLTIPS = ("True when the path exists and is a regular file.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_is_file"

    def check_is_file(self, path: str) -> tuple[bool]:
        return (os.path.isfile(path),)


class PathJoin(ComfyNodeABC):
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
                "path1": (IO.STRING, {"default": "", "tooltip": "First path component."}),
            },
            "optional": {
                "path2": (IO.STRING, {"default": "", "tooltip": "Second path component."}),
            },
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("path",)
    OUTPUT_TOOLTIPS = ("The components joined into a single path.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "join_paths"

    def join_paths(self, path1: str, path2: str = "") -> tuple[str]:
        paths = [p for p in [path1, path2] if p]
        return (str(os.path.join(*paths)),)


class PathListDir(ComfyNodeABC):
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
                "path": (IO.STRING, {"default": "", "tooltip": "Directory to list."}),
            },
            "optional": {
                "files_only": (IO.BOOLEAN, {"default": False, "tooltip": "When True, only files are returned."}),
                "dirs_only": (IO.BOOLEAN, {"default": False, "tooltip": "When True, only directories are returned."}),
            },
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("entries",)
    OUTPUT_TOOLTIPS = ("The names of the directory entries, as a data list.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "list_directory"
    OUTPUT_IS_LIST = (True,)

    def list_directory(self, path: str, files_only: str = False, dirs_only: str = False) -> tuple[list[str]]:
        if not path:
            path = os.getcwd()

        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory does not exist: {path}")
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Basic data handling: Path is not a directory: {path}")

        entries = os.listdir(path)

        if files_only:
            entries = [e for e in entries if os.path.isfile(os.path.join(path, e))]
        elif dirs_only:
            entries = [e for e in entries if os.path.isdir(os.path.join(path, e))]

        return (entries,)


class PathNormalize(ComfyNodeABC):
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
                "path": (IO.STRING, {"default": "", "tooltip": "Path to normalize."}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("normalized path",)
    OUTPUT_TOOLTIPS = ("The path with redundant separators and up-level references collapsed.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "normalize_path"

    def normalize_path(self, path: str) -> tuple[str]:
        return (os.path.normpath(path),)


class PathSetExtension(ComfyNodeABC):
    """
    Sets the file extension for a path.

    This node replaces the current extension in a path with a new one.
    The extension should include the dot (e.g., '.jpg').
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path whose extension is replaced."}),
                "extension": (IO.STRING, {"default": ".txt", "tooltip": "The new extension; a leading dot is added if missing."}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("path",)
    OUTPUT_TOOLTIPS = ("The path with its extension replaced.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "set_extension"

    def set_extension(self, path: str, extension: str) -> tuple[str]:
        # Make sure extension starts with a dot
        if not extension.startswith(".") and extension:
            extension = "." + extension

        root, _ = os.path.splitext(path)
        return (root + extension,)


class PathRelative(ComfyNodeABC):
    """
    Returns a relative path.

    This node computes a relative path from the 'start' path to the 'path'.
    If 'start' is not provided, the current working directory is used.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path to express relative to start."}),
            },
            "optional": {
                "start": (IO.STRING, {"default": "", "tooltip": "Base path; the current working directory is used when empty."}),
            },
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("relative path",)
    OUTPUT_TOOLTIPS = ("The path expressed relative to start.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_relative_path"

    def get_relative_path(self, path: str, start: str = "") -> tuple[str]:
        if not start:
            start = os.getcwd()
        return (os.path.relpath(path, start),)


class PathSplit(ComfyNodeABC):
    """
    Splits a path into directory and filename components.

    This node takes a path and returns a tuple containing the directory path
    and the filename.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path to split into directory and filename."}),
            }
        }

    RETURN_TYPES = (IO.STRING, IO.STRING)
    RETURN_NAMES = ("directory", "filename")
    OUTPUT_TOOLTIPS = ("The directory (head) component.", "The filename (tail) component.")
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "split_path"

    def split_path(self, path: str) -> tuple[str, str]:
        return os.path.split(path)


class PathSplitExt(ComfyNodeABC):
    """
    Splits a path into name and extension components.

    This node takes a path and returns a tuple containing the path without
    the extension and the extension (including the dot).
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path to split into name and extension."}),
            }
        }

    RETURN_TYPES = (IO.STRING, IO.STRING)
    RETURN_NAMES = ("path without ext", "extension")
    OUTPUT_TOOLTIPS = ("The path without its extension.", "The extension including the dot (empty when none).")
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "split_ext"

    def split_ext(self, path: str) -> tuple[str, str]:
        return os.path.splitext(path)


class PathLoadStringFile(ComfyNodeABC):
    """
    Loads a text file in UTF-8 encoding and returns its content as a STRING
    without any further processing.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path of the UTF-8 text file to read."}),
            },
        }

    RETURN_TYPES = (IO.STRING, IO.BOOLEAN)
    RETURN_NAMES = ("text", "exists")
    OUTPUT_TOOLTIPS = ("The file content (empty when the file is missing or unreadable).", "True when the file exists and was read.")
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "load_text"

    @classmethod
    def IS_CHANGED(cls, path):
        try:
            if os.path.exists(path):
                return os.path.getmtime(path)
        except Exception:
            pass
        return float("NaN")  # Return NaN if file doesn't exist or can't access modification time

    def load_text(self, path: str):
        exists = os.path.exists(path)

        if not exists:
            return ("", False)

        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            return (text, True)
        except Exception:
            return ("", False)


class PathLoadImageRGB(ComfyNodeABC):
    """
    Loads an image from a file path and returns only the RGB channels.

    This node loads an image from the specified path and processes it to
    return only the RGB channels as a tensor, ignoring any alpha channel.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path of the image file to load."}),
            },
        }

    RETURN_TYPES = (IO.IMAGE, IO.BOOLEAN)
    RETURN_NAMES = ("image", "exists")
    OUTPUT_TOOLTIPS = ("The RGB image as a tensor (a blank 1x1 image when the file is missing).", "True when the image was loaded.")
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "load_image_rgb"

    @classmethod
    def IS_CHANGED(cls, path):
        try:
            if os.path.exists(path):
                return os.path.getmtime(path)
        except Exception:
            pass
        return float("NaN")  # Return NaN if file doesn't exist or can't access modification time

    def load_image_rgb(self, path: str):
        import numpy as np
        import torch

        img = load_image_helper(path)

        if img is None:
            # Create an empty 1x1 image
            empty_tensor = torch.zeros((1, 1, 1, 3), dtype=torch.float32)
            return (empty_tensor, False)

        # Convert to RGB (removing alpha if present)
        img_rgb = img.convert("RGB")

        # Convert to tensor format expected by ComfyUI
        image_tensor = np.array(img_rgb).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_tensor)[None,]

        return (image_tensor, True)


class PathLoadImageRGBA(ComfyNodeABC):
    """
    Loads an image from a file path and returns RGB channels and Alpha as a mask.

    This node loads an image from the specified path and processes it to
    return the RGB channels as a tensor and the Alpha channel as a mask tensor.
    If the image has no alpha channel, a blank mask is returned.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path of the image file to load."}),
            },
        }

    RETURN_TYPES = (IO.IMAGE, IO.MASK, IO.BOOLEAN)
    RETURN_NAMES = ("image", "mask", "exists")
    OUTPUT_TOOLTIPS = (
        "The RGB image as a tensor.",
        "The alpha channel as a mask (blank when the image has none).",
        "True when the image was loaded.",
    )
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "load_image_rgba"

    @classmethod
    def IS_CHANGED(cls, path):
        try:
            if os.path.exists(path):
                return os.path.getmtime(path)
        except Exception:
            pass
        return float("NaN")  # Return NaN if file doesn't exist or can't access modification time

    def load_image_rgba(self, path: str):
        import numpy as np
        import torch

        img = load_image_helper(path)

        if img is None:
            # Create empty 1x1 image and mask
            empty_image = torch.zeros((1, 1, 1, 3), dtype=torch.float32)
            empty_mask = torch.zeros((1, 1, 1), dtype=torch.float32)
            return (empty_image, empty_mask, False)

        # Convert to RGB for the image
        img_rgb = img.convert("RGB")

        # Convert to tensor format expected by ComfyUI
        image_tensor = np.array(img_rgb).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_tensor)[None,]

        # Extract alpha channel as mask
        mask_tensor = extract_mask_from_alpha(img)

        return (image_tensor, mask_tensor, True)


class PathLoadMaskFromAlpha(ComfyNodeABC):
    """
    Loads a mask from the alpha channel of an image.

    This node loads an image from the specified path and extracts the alpha
    channel to use as a mask. If the image has no alpha channel, a blank mask
    is returned.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path of the image whose alpha channel is used."}),
            },
        }

    RETURN_TYPES = (IO.MASK, IO.BOOLEAN)
    RETURN_NAMES = ("mask", "exists")
    OUTPUT_TOOLTIPS = ("The alpha channel as a mask (blank when the image has none or is missing).", "True when the image was loaded.")
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "load_mask_from_alpha"

    @classmethod
    def IS_CHANGED(cls, path):
        try:
            if os.path.exists(path):
                return os.path.getmtime(path)
        except Exception:
            pass
        return float("NaN")  # Return NaN if file doesn't exist or can't access modification time

    def load_mask_from_alpha(self, path: str):
        import torch

        img = load_image_helper(path)

        if img is None:
            # Return empty 1x1 mask
            empty_mask = torch.zeros((1, 1, 1), dtype=torch.float32)
            return (empty_mask, False)

        mask_tensor = extract_mask_from_alpha(img)
        return (mask_tensor, True)


class PathLoadMaskFromGreyscale(ComfyNodeABC):
    """
    Loads a mask from a greyscale image or the red channel of an RGB image.

    This node loads an image from the specified path and creates a mask from it.
    If the image is greyscale, the intensity is used directly.
    If the image is RGB, the red channel is used.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": (IO.STRING, {"default": "", "tooltip": "Path of the image to build the mask from."}),
            },
            "optional": {
                "invert": (IO.BOOLEAN, {"default": False, "tooltip": "Invert the mask (1.0 - mask) after extraction."}),
            },
        }

    RETURN_TYPES = (IO.MASK, IO.BOOLEAN)
    RETURN_NAMES = ("mask", "exists")
    OUTPUT_TOOLTIPS = ("The mask derived from the greyscale/red channel.", "True when the image was loaded.")
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "load_mask_from_greyscale"

    @classmethod
    def IS_CHANGED(cls, path):
        try:
            if os.path.exists(path):
                return os.path.getmtime(path)
        except Exception:
            pass
        return float("NaN")  # Return NaN if file doesn't exist or can't access modification time

    def load_mask_from_greyscale(self, path: str, invert: bool = False):
        import torch

        img = load_image_helper(path)

        if img is None:
            # Return empty 1x1 mask
            empty_mask = torch.zeros((1, 1, 1), dtype=torch.float32)
            return (empty_mask, False)

        mask_tensor = extract_mask_from_greyscale(img)

        # Optionally invert the mask (1.0 - mask)
        if invert:
            mask_tensor = 1.0 - mask_tensor

        return (mask_tensor, True)


class PathSaveStringFile(ComfyNodeABC):
    """
    Saves a string to a text file.

    This node takes a string and saves it to the specified path as a text file.
    Optionally, you can choose to create the directory if it doesn't exist.
    If 'append' is True, the text is appended to an existing file instead of
    overwriting it.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": (IO.STRING, {"default": "", "tooltip": "The text to write."}),
                "path": (IO.STRING, {"default": "", "tooltip": "Destination file path."}),
            },
            "optional": {
                "create_dirs": (IO.BOOLEAN, {"default": True, "tooltip": "Create missing parent directories."}),
                "append": (IO.BOOLEAN, {"default": False, "tooltip": "Append to an existing file instead of overwriting it."}),
                "encoding": (IO.STRING, {"default": "utf-8", "tooltip": "Text encoding to use when writing."}),
            },
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("success",)
    OUTPUT_TOOLTIPS = ("True when the file was written successfully.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "save_text"
    OUTPUT_NODE = True

    def save_text(self, text: str, path: str, create_dirs: bool = True, append: bool = False, encoding: str = "utf-8"):
        if not path:
            print("Basic data handling: Save failed - no path specified")
            return (False,)

        try:
            # Create directories if needed
            directory = os.path.dirname(path)
            if directory and create_dirs and not os.path.exists(directory):
                os.makedirs(directory)

            mode = "a" if append else "w"
            with open(path, mode, encoding=encoding) as f:
                f.write(text)

            action = "appended" if append else "saved"
            print(f"Basic data handling: Successfully {action} text to {path}")
            return (True,)
        except Exception as e:
            print(f"Basic data handling: Error saving text file: {e}")
            return (False,)


def compose_prompt_text(prompt: str, negative_prompt: str) -> str:
    """
    Build the generation-parameter text embedded into saved images.

    Follows the Stable Diffusion WebUI convention: the (optional) positive
    prompt is written first, followed by an optional ``Negative prompt:``
    line::

        <positive prompt>
        Negative prompt: <negative prompt>

    Returns an empty string when neither value is provided, in which case no
    metadata is embedded into the file.
    """
    lines = []
    if prompt.strip():
        lines.append(prompt.strip())
    if negative_prompt.strip():
        lines.append(f"Negative prompt: {negative_prompt.strip()}")
    return "\n".join(lines)


def build_png_info(metadata_text: str):
    """
    Wrap ``metadata_text`` in a Pillow ``PngInfo`` container under the standard
    ``parameters`` text-chunk key so it can be embedded in a PNG file.

    Returns ``None`` when there is no text to embed (or Pillow's PNG metadata
    support is unavailable), in which case the image should be saved without
    extra metadata.
    """
    if not metadata_text:
        return None
    try:
        from PIL import PngImagePlugin
    except ModuleNotFoundError:
        return None
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", metadata_text)
    return pnginfo


def build_image_exif(metadata_text: str, include_description: bool = True):
    """
    Build an EXIF block that stores ``metadata_text`` for formats without a
    native text chunk (JPEG, WEBP, JXL).

    The payload is written into the EXIF ``UserComment`` field (tag 0x9286) of
    the Exif IFD as ``UNICODE\0`` + UTF-16-BE, which matches what Stable
    Diffusion WebUI / piexif based readers expect. When ``include_description``
    is true, the payload is also written as UTF-8 into the EXIF
    ``ImageDescription`` field (tag 0x010E) of IFD0.

    Returns the EXIF bytes (starting with the ``Exif\0\0`` marker), or ``None``
    when there is no text to embed.
    """
    if not metadata_text:
        return None
    try:
        from PIL import ExifTags
    except ModuleNotFoundError:
        return None
    Image, _ = _require_pillow()
    exif = Image.Exif()
    if include_description:
        exif[0x010E] = metadata_text.encode("utf-8")
    exif.get_ifd(ExifTags.IFD.Exif)[0x9286] = b"UNICODE\x00" + metadata_text.encode("utf-16-be")
    return exif.tobytes()


def build_xmp_packet(metadata_text: str) -> bytes:
    """
    Build an XMP packet storing ``metadata_text`` in the Dublin Core
    ``dc:description`` tag, as expected for JPEG XL ``xml `` boxes.
    """
    from xml.sax.saxutils import escape

    body = escape(metadata_text)
    packet = (
        '<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>\n'
        '<x:xmpmeta xmlns:x="adobe:ns:meta/">\n'
        '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
        '<rdf:Description xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        '<dc:description><rdf:Alt><rdf:li xml:lang="x-default">' + body + "</rdf:li></rdf:Alt></dc:description>\n"
        "</rdf:Description>\n"
        "</rdf:RDF>\n"
        "</x:xmpmeta>\n"
        '<?xpacket end="w"?>'
    )
    return packet.encode("utf-8")


def metadata_save_kwargs(metadata_text: str, fmt: str) -> dict:
    """
    Return the extra keyword arguments that embed ``metadata_text`` when saving
    an image in the (lower-case) format ``fmt``.

    Returns an empty dict when there is no text to embed or when the format
    cannot carry text metadata.
    """
    if not metadata_text:
        return {}
    if fmt == "png":
        return {"pnginfo": build_png_info(metadata_text)}
    if fmt in ("jpg", "jpeg"):
        exif = build_image_exif(metadata_text, include_description=True)
        return {"exif": exif} if exif is not None else {}
    if fmt in ("webp", "jxl"):
        exif = build_image_exif(metadata_text, include_description=False)
        kwargs = {"exif": exif} if exif is not None else {}
        if fmt == "jxl":
            # EXIF and XMP boxes are only available in the JXL container format
            kwargs["use_container"] = True
            kwargs["xmp"] = build_xmp_packet(metadata_text)
        return kwargs
    return {}


# --- shared helpers for the image-save nodes --------------------------------
#
# The save-format dropdown is not hard-coded: it is derived from the installed
# Pillow (+ any image plugins such as pillow-jxl it can save with), so it always
# matches what the running library supports and automatically picks up new
# formats/plugins. Only "formats" that are not meaningful photographic raster
# output (icons / GPU textures / vector / multi-image containers, e.g. DDS,
# ICNS, EPS, MPO) are never offered even when Pillow can technically write them.
#
# A save *token* is the short, user-facing format name and equals the file
# extension we write (jpg/tif/jp2/...). Each token maps to the Pillow format-id
# used with ``Image.save(format=...)``.
_PIL_FORMAT_BY_TOKEN: dict[str, str] = {
    "png": "PNG",
    "jpg": "JPEG",
    "jpeg": "JPEG",  # alias; normalised to "jpg"
    "webp": "WEBP",
    "jxl": "JXL",
    "bmp": "BMP",
    "tif": "TIFF",
    "tiff": "TIFF",  # alias; normalised to "tif"
    "gif": "GIF",
    "jp2": "JPEG2000",
    "jpeg2000": "JPEG2000",  # alias; normalised to "jp2"
    "ppm": "PPM",
    "pcx": "PCX",
    "tga": "TGA",
    "qoi": "QOI",
    "avif": "AVIF",
}

# friendly ordering for the dropdown: the well-known set first, then whatever
# else is discovered in the installed library/plugins.
_IMAGE_SAVE_ORDER = ["png", "jpg", "webp", "jxl", "bmp", "tif", "gif", "jp2", "ppm", "pcx", "tga", "qoi", "avif"]

# Pillow format-ids that are not meaningful photographic raster *stills* for this
# save node (icons/cursors, GPU textures, vector/postscript, single-multi-image
# containers, scientific dumps). Never offered even if Pillow can write them.
_NON_PHOTOGRAPHIC_RASTER_IDS = {
    "ICO",
    "CUR",
    "ICNS",
    "DDS",
    "DIB",
    "EPS",
    "IM",
    "MPO",
    "SGI",
    "PDF",
    "WMF",
    "EMF",
    "BUFR",
    "GRIB",
    "HDF5",
    "FITS",
}

# canonical token for a couple of common user-spelled aliases
_FORMAT_ALIASES = {"jpeg": "jpg", "tiff": "tif", "jpeg2000": "jp2"}


def _load_image_plugins() -> None:
    """Import optional Pillow plugins (e.g. pillow-jxl) so Pillow knows about
    every format the library can actually save."""
    try:
        import pillow_jxl  # noqa: F401 - imported but unused, registers the JXL plugin
    except ModuleNotFoundError:
        pass


def _writable_pillow_formats(mode: str) -> set[str]:
    """
    The set of Pillow format-ids that can successfully encode a small image in
    ``mode`` (probed at runtime against the actually installed library/plugins).
    """
    import io as _io
    from PIL import Image as _PIL

    _load_image_plugins()
    ids = set(_PIL.SAVE.keys())
    ids.update(str(v).upper() for v in _PIL.registered_extensions().values())
    writable: set[str] = set()
    for fid in sorted(ids):
        try:
            buf = _io.BytesIO()
            _PIL.new(mode, (4, 4)).save(buf, format=fid)
            buf.seek(0)
            _PIL.open(buf).load()
            writable.add(str(fid).upper())
        except Exception:
            continue
    return writable


def _discover_save_formats() -> tuple[list[str], list[str]]:
    """
    Derive ``(all_formats, alpha_formats)`` dropdown lists from Pillow/plugins.
    ``alpha_formats`` (surfaced on the IMAGE+MASK node) is the subset that can
    also hold an alpha channel.
    """
    writable_rgb = _writable_pillow_formats("RGB")
    writable_rgba = _writable_pillow_formats("RGBA")

    # 1) tokens we already know about and that are actually writable
    offered = [t for t in _IMAGE_SAVE_ORDER if _PIL_FORMAT_BY_TOKEN[t] in writable_rgb]
    known_ids = {_PIL_FORMAT_BY_TOKEN[t] for t in offered}

    # 2) any additional writable photographic format in the library/plugins
    extras = []
    for pid in sorted(writable_rgb):
        if pid in known_ids or pid in _NON_PHOTOGRAPHIC_RASTER_IDS:
            continue
        token = pid.lower()
        # register it so it can be written through the same machinery
        _PIL_FORMAT_BY_TOKEN[token] = pid
        if token not in _IMAGE_SAVE_ORDER:
            _IMAGE_SAVE_ORDER.append(token)
        extras.append(token)

    all_formats = offered + extras
    alpha_formats = [t for t in all_formats if _PIL_FORMAT_BY_TOKEN[t] in writable_rgba]
    return all_formats, alpha_formats


# Discovering the formats probes the installed Pillow/plugins, so it must not be
# required for importing this module: environments that only inspect the node
# metadata (e.g. the comfy-org/node-diff CI) have no Pillow installed. Fall back
# to the classic formats there instead of failing to load the whole node pack.
try:
    (_IMAGE_SAVE_FORMATS, _IMAGE_SAVE_ALPHA_FORMATS) = _discover_save_formats()
except ModuleNotFoundError:
    _IMAGE_SAVE_FORMATS = ["png", "jpg", "webp", "jxl", "bmp", "tif", "gif"]
    _IMAGE_SAVE_ALPHA_FORMATS = ["png", "webp", "jxl"]
else:
    # Always make sure the most common formats are present when the backend
    # supports them (guards against an odd Pillow not probing its core formats).
    for _token in ("png", "jpg", "webp"):
        if _token in _PIL_FORMAT_BY_TOKEN and _PIL_FORMAT_BY_TOKEN[_token] and _token not in _IMAGE_SAVE_FORMATS:
            _IMAGE_SAVE_FORMATS.insert(0, _token)

    # Log the supported save formats once at node-load time, so users can see
    # what the running Pillow/image plugins can write.
    print("Basic data handling: supported image formats: " + ", ".join(_IMAGE_SAVE_FORMATS))
    print("Basic data handling: supported IMAGE+MASK (alpha) formats: " + ", ".join(_IMAGE_SAVE_ALPHA_FORMATS))


def _normalize_image_format(format: str) -> str:
    """
    Normalise a user-supplied format to its canonical save token (lower-cased),
    mapping common aliases (jpeg->jpg, tiff->tif, jpeg2000->jp2) so both the
    dropdown spellings and values wired in from elsewhere are accepted. Unknown
    tokens are passed through unchanged (they may name a format the writer will
    then attempt, or reject gracefully).
    """
    token = str(format or "png").strip().lower()
    return _FORMAT_ALIASES.get(token, token)


def _comfy_format_date(fmt_text: str, when) -> str:
    """
    Format ``when`` using ComfyUI's own ``formatDate`` semantics (used by
    ``%date:<format>%``). Supported tokens: ``yyyy``/``yy`` for the year, and
    ``M``/``MM``, ``d``/``dd``, ``h``/``hh``, ``m``/``mm``, ``s``/``ss``
    (lower-case ``h`` for hours, exactly like ComfyUI). Single letters are
    unpadded, doubled letters are zero-padded.
    """
    import re

    parts = {
        "d": when.day,
        "M": when.month,
        "h": when.hour,
        "m": when.minute,
        "s": when.second,
    }
    # Mirrors ComfyUI's regex: dd?|MM?|hh?|mm?|ss?|yyy?y? (yyy?y? last so a
    # four-digit year is matched as a single token, not two "yy" groups).
    pattern = re.compile(r"dd?|MM?|hh?|mm?|ss?|yyy?y?")

    def replace(token: str) -> str:
        if token == "yy":
            return str(when.year)[-2:]
        if token == "yyyy":
            return str(when.year)
        if token and token[0] in parts:
            # padStart(token.length, "0")
            return str(parts[token[0]]).zfill(len(token))
        return token

    return pattern.sub(lambda m: replace(m.group(0)), fmt_text)


def _expand_filename_tokens(text: str, width: int = 0, height: int = 0) -> str:
    """
    Expand ComfyUI-style filename templates in ``text`` for both the plain path
    and the ``filename_prefix`` modes.

    Handles ``%date:<format>%`` (using ComfyUI's own date formatting) as well as
    the standard built-in tokens ``%width%``, ``%height%``, ``%year%``,
    ``%month%``, ``%day%``, ``%hour%``, ``%minute%`` and ``%second%``. Node
    reference tokens (``%Node.widget%``) can only be resolved by the ComfyUI
    frontend, so they are left untouched here.
    """
    import re
    from datetime import datetime

    if not text:
        return text

    now = datetime.now()
    text = re.sub(r"%date:(.*?)%", lambda m: _comfy_format_date(m.group(1), now), text)
    text = text.replace("%width%", str(width))
    text = text.replace("%height%", str(height))
    text = text.replace("%year%", str(now.year))
    text = text.replace("%month%", str(now.month).zfill(2))
    text = text.replace("%day%", str(now.day).zfill(2))
    text = text.replace("%hour%", str(now.hour).zfill(2))
    text = text.replace("%minute%", str(now.minute).zfill(2))
    text = text.replace("%second%", str(now.second).zfill(2))
    return text


def _official_save_image_path(filename_prefix, output_dir, image_width=0, image_height=0):
    """
    Resolve ``filename_prefix`` to concrete output folder/filename/counter using
    ComfyUI's own ``folder_paths.get_save_image_path`` wherever possible.

    Returns ``(full_output_folder, filename, counter, subfolder, resolved_prefix)``
    exactly like the official function. When ``folder_paths`` is unavailable
    (standalone test-suite / non-ComfyUI host), a minimal local equivalent that
    mirrors the same subfolder + ``_<counter>_`` scheme is used instead.
    """
    if _official_get_save_image_path is not None:
        return _official_get_save_image_path(filename_prefix, output_dir, image_width, image_height)

    # --- fallback (only reached outside ComfyUI) -------------------------
    def expand(text, w, h):
        import time

        now = time.localtime()
        text = text.replace("%width%", str(w)).replace("%height%", str(h))
        text = text.replace("%year%", str(now.tm_year))
        text = text.replace("%month%", str(now.tm_mon).zfill(2))
        text = text.replace("%day%", str(now.tm_mday).zfill(2))
        text = text.replace("%hour%", str(now.tm_hour).zfill(2))
        text = text.replace("%minute%", str(now.tm_min).zfill(2))
        text = text.replace("%second%", str(now.tm_sec).zfill(2))
        return text

    if "%" in filename_prefix:
        filename_prefix = expand(filename_prefix, image_width, image_height)
    subfolder = os.path.dirname(os.path.normpath(filename_prefix))
    filename = os.path.basename(os.path.normpath(filename_prefix))
    full_output_folder = os.path.join(output_dir, subfolder)

    highest = 0
    try:
        for entry in os.listdir(full_output_folder):
            stem, _, _ = entry.rpartition(".")
            if stem.startswith(filename + "_") and stem[len(filename) + 1 :].rstrip("_").isdigit():
                digits = stem[len(filename) + 1 :].rstrip("_")
                if digits.isdigit():
                    highest = max(highest, int(digits))
    except FileNotFoundError:
        os.makedirs(full_output_folder, exist_ok=True)
    return full_output_folder, filename, highest + 1, subfolder, filename_prefix


def _plan_save_paths(path: str, format: str, use_prefix_mode: bool, frame_count: int, width: int, height: int) -> tuple[list[str], bool]:
    """
    Compute the absolute destination path(s) for ``frame_count`` images.

    Returns ``(paths, create_dirs)``:
    - ``use_prefix_mode`` False: ``path`` is a concrete file location. A single
      frame writes exactly to ``path`` (+ extension); several frames get an
      incrementing ``_00000``-style suffix so they do not overwrite each other.
    - ``use_prefix_mode`` True: ``path`` is a ComfyUI ``filename_prefix`` under
      the output folder, resolved through ComfyUI's own filename helpers and
      auto-numbered like the built-in "Save Image" node.
    """
    fmt = _normalize_image_format(format)
    # Expand ComfyUI-style templates (%date:...%, %width%, %height%, ...) up
    # front so they apply in both the plain-path and the prefix modes.
    path = _expand_filename_tokens(path, width, height)

    if use_prefix_mode:
        full_output_folder, filename, counter, _, _ = _official_save_image_path(path, get_output_directory(), width, height)
        paths = []
        for _ in range(frame_count):
            name = f"{filename}_{counter:05}_.{fmt}"
            paths.append(os.path.join(full_output_folder, name))
            counter += 1
        return paths, False

    if not path.endswith(f".{fmt}"):
        base = f"{path}.{fmt}"
    else:
        base = path

    if frame_count <= 1:
        return [base], True

    root, ext = os.path.splitext(base)
    paths = [f"{root}_{i:05}{ext}" for i in range(frame_count)]
    return paths, True


def _ensure_parent_directories(path: str, create_dirs: bool) -> None:
    """Create the parent directory(ies) of ``path`` when requested."""
    directory = os.path.dirname(path)
    if directory and create_dirs and not os.path.exists(directory):
        os.makedirs(directory)


def _has_jxl_support() -> bool:
    """Return True when the pillow-jxl plugin is importable."""
    try:
        import pillow_jxl  # noqa: F401 - imported but unused, kept for JPEG XL support

        return True
    except ModuleNotFoundError:
        return False


def _write_pil_image(pil_img, path: str, fmt: str, quality: int, metadata_text: str) -> bool:
    """
    Write ``pil_img`` to ``path``. ``fmt`` is a canonical save token (see
    ``_PIL_FORMAT_BY_TOKEN``). For the lossy/metadata-capable set (png/jpg/webp/
    jxl) the prompt text is embedded as ``parameters`` metadata and ``quality``
    is honoured; all other discovered formats are written plainly. Returns True
    on success.
    """
    try:
        if fmt == "png":
            pil_img.save(path, format="PNG", **metadata_save_kwargs(metadata_text, fmt))
        elif fmt == "jpg":
            # JPEG cannot carry alpha; drop it so an RGBA input still saves.
            pil_img.convert("RGB").save(path, format="JPEG", quality=quality, **metadata_save_kwargs(metadata_text, fmt))
        elif fmt == "webp":
            pil_img.save(path, format="WEBP", quality=quality, **metadata_save_kwargs(metadata_text, fmt))
        elif fmt == "jxl":
            pil_img.save(path, format="JXL", quality=quality, **metadata_save_kwargs(metadata_text, fmt))
        else:
            if metadata_text:
                print("Basic data handling: Prompt metadata is not supported for this format; skipping it.")
            pil_img.save(path, format=_PIL_FORMAT_BY_TOKEN.get(fmt, fmt.upper()))
        return True
    except Exception as e:
        print(f"Basic data handling: Error saving image: {e}")
        return False


class PathSaveImageRGB(ComfyNodeABC):
    """
    Saves an image to a file.

    This node takes an image tensor and saves it to the specified path.
    Supports various image formats like PNG, JPG, WEBP, JXL (if pillow-jxl is installed), etc.

    By default ``path`` is a concrete absolute/relative file location and every
    image frame of the batch is written (several frames get an incrementing
    suffix). When ``use_prefix_mode`` is enabled ``path`` is instead treated as
    a ComfyUI ``filename_prefix`` under the output folder, named and
    auto-numbered exactly like the built-in "Save Image" node.

    When ``prompt`` and/or ``negative_prompt`` are provided, they are embedded
    into the saved image as ``parameters`` metadata: in the PNG text chunk, in
    the EXIF ``UserComment`` (and ``ImageDescription`` for JPEG) fields, and in
    the EXIF + XMP boxes for JPEG XL. Formats that cannot carry text metadata
    ignore the prompts.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": (IO.IMAGE,),
                "path": (
                    IO.STRING,
                    {
                        "default": "",
                        "tooltip": 'Destination file path (an extension is added from the format when missing), or a ComfyUI filename_prefix under the output folder when "use prefix mode" is enabled.',
                    },
                ),
            },
            "optional": {
                "format": (
                    _IMAGE_SAVE_FORMATS,
                    {
                        "default": "png",
                        "tooltip": "Image save format (png, jpg, webp, bmp, ...). The list is derived from what the installed Pillow/plugins can write. Drag a STRING onto this to override it.",
                    },
                ),
                "quality": (IO.INT, {"default": 95, "min": 1, "max": 100, "tooltip": "Quality for lossy formats (jpg/webp/jxl)."}),
                "create_dirs": (IO.BOOLEAN, {"default": True, "tooltip": "Create missing parent directories (plain path mode only)."}),
                "prompt": (IO.STRING, {"default": "", "tooltip": "Optional positive prompt embedded as parameters metadata."}),
                "negative_prompt": (IO.STRING, {"default": "", "tooltip": "Optional negative prompt embedded as parameters metadata."}),
                # Appended last on purpose: the node stores widget values
                # positionally, so adding before the existing widgets would shift
                # old workflows and mis-assign their saved values.
                "use_prefix_mode": (
                    IO.BOOLEAN,
                    {
                        "default": False,
                        "tooltip": "When True, 'path' is treated as a ComfyUI filename_prefix under the output folder and files are named/auto-numbered exactly like ComfyUI's \"Save Image\" node.",
                    },
                ),
            },
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("success",)
    OUTPUT_TOOLTIPS = ("True when the image was saved successfully.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "save_image"
    OUTPUT_NODE = True

    def save_image(
        self,
        images,
        path: str = "",
        use_prefix_mode: bool = False,
        format: str = "png",
        quality: int = 95,
        create_dirs: bool = True,
        prompt: str = "",
        negative_prompt: str = "",
    ):
        if not path:
            print("Basic data handling: Save failed - no path specified")
            return (False,)

        import numpy as np
        from PIL import Image

        fmt = _normalize_image_format(format)
        if fmt == "jxl" and not _has_jxl_support():
            print(
                "Basic data handling: JPEG XL format requested but pillow_jxl module is not installed. "
                "Please install it with 'pip install pillow-jxl-plugin'."
            )
            return (False,)

        batch = len(images)
        height, width = images.shape[1], images.shape[2]
        paths, create_dirs = _plan_save_paths(path, fmt, use_prefix_mode, batch, width, height)

        # Compose the prompt metadata to embed into the saved file once.
        metadata_text = compose_prompt_text(prompt, negative_prompt)

        for index, target_path in enumerate(paths):
            _ensure_parent_directories(target_path, create_dirs)

            # Convert from tensor format back to PIL Image
            img_tensor = images[index].cpu().numpy()
            img_np = (img_tensor * 255).astype(np.uint8)
            pil_img = Image.fromarray(img_np)

            if not _write_pil_image(pil_img, target_path, fmt, quality, metadata_text):
                return (False,)
            print(f"Basic data handling: Successfully saved image to {target_path}")

        return (True,)


class PathSaveImageRGBA(ComfyNodeABC):
    """
    Saves an image with a mask to a file with transparency.

    This node takes an image tensor and a mask tensor and saves them to the
    specified path as an image with transparency, where the mask defines the
    alpha channel.

    By default ``path`` is a concrete absolute/relative file location and every
    image frame of the batch is written (several frames get an incrementing
    suffix). When ``use_prefix_mode`` is enabled ``path`` is instead treated as
    a ComfyUI ``filename_prefix`` under the output folder, named and
    auto-numbered exactly like the built-in "Save Image" node.

    When ``prompt`` and/or ``negative_prompt`` are provided, they are embedded
    into the saved image as ``parameters`` metadata: in the PNG text chunk, in
    the EXIF ``UserComment`` (and ``ImageDescription`` for JPEG) fields, and in
    the EXIF + XMP boxes for JPEG XL. Formats that cannot carry text metadata
    ignore the prompts.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": (IO.IMAGE,),
                "mask": (IO.MASK,),
                "path": (
                    IO.STRING,
                    {
                        "default": "",
                        "tooltip": 'Destination file path (an extension is added from the format when missing), or a ComfyUI filename_prefix under the output folder when "use prefix mode" is enabled.',
                    },
                ),
            },
            "optional": {
                "format": (
                    _IMAGE_SAVE_ALPHA_FORMATS,
                    {
                        "default": "png",
                        "tooltip": "Image save format that can hold an alpha channel (png, webp, ...; jpg is coerced to png). Derived from what the installed Pillow/plugins can write. Drag a STRING onto this to override it.",
                    },
                ),
                "quality": (IO.INT, {"default": 95, "min": 1, "max": 100, "tooltip": "Quality for lossy formats (webp/jxl)."}),
                "invert_mask": (IO.BOOLEAN, {"default": False, "tooltip": "Invert the mask before using it as the alpha channel."}),
                "create_dirs": (IO.BOOLEAN, {"default": True, "tooltip": "Create missing parent directories (plain path mode only)."}),
                "prompt": (IO.STRING, {"default": "", "tooltip": "Optional positive prompt embedded as parameters metadata."}),
                "negative_prompt": (IO.STRING, {"default": "", "tooltip": "Optional negative prompt embedded as parameters metadata."}),
                # Appended last on purpose: the node stores widget values
                # positionally, so adding before the existing widgets would shift
                # old workflows and mis-assign their saved values.
                "use_prefix_mode": (
                    IO.BOOLEAN,
                    {
                        "default": False,
                        "tooltip": "When True, 'path' is treated as a ComfyUI filename_prefix under the output folder and files are named/auto-numbered exactly like ComfyUI's \"Save Image\" node.",
                    },
                ),
            },
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("success",)
    OUTPUT_TOOLTIPS = ("True when the image with alpha was saved successfully.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "save_image_with_mask"
    OUTPUT_NODE = True

    def save_image_with_mask(
        self,
        images,
        mask,
        path: str = "",
        use_prefix_mode: bool = False,
        format: str = "png",
        quality: int = 95,
        invert_mask: bool = False,
        create_dirs: bool = True,
        prompt: str = "",
        negative_prompt: str = "",
    ):
        if not path:
            print("Basic data handling: Save failed - no path specified")
            return (False,)

        import numpy as np
        from PIL import Image

        # JPEG doesn't support transparency -> coerce to PNG, as before.
        fmt = _normalize_image_format(format)
        if fmt in ("jpg", "jpeg"):
            print("Basic data handling: JPEG format doesn't support transparency. Using PNG instead.")
            fmt = "png"
        if fmt == "jxl" and not _has_jxl_support():
            print(
                "Basic data handling: JPEG XL format requested but pillow_jxl module is not installed. "
                "Please install it with 'pip install pillow-jxl-plugin'."
            )
            return (False,)

        batch = len(images)
        height, width = images.shape[1], images.shape[2]
        paths, create_dirs = _plan_save_paths(path, fmt, use_prefix_mode, batch, width, height)

        mask_batch = len(mask)
        # Mask tensor may be padded to the image batches; round-robin when the
        # mask has fewer frames (e.g. a single mask applied to every frame).
        mask_frames = mask.cpu()

        metadata_text = compose_prompt_text(prompt, negative_prompt)

        for index, target_path in enumerate(paths):
            _ensure_parent_directories(target_path, create_dirs)

            img_tensor = images[index].cpu().numpy()
            mask_tensor = mask_frames[index % mask_batch]

            # Invert the mask if needed (1.0 becomes transparent, 0.0 becomes opaque)
            if invert_mask:
                mask_tensor = 1.0 - mask_tensor

            # Convert to alpha channel (0-255)
            alpha_np = (255.0 * (1.0 - mask_tensor.numpy())).astype(np.uint8)

            # Convert to uint8 format for PIL
            img_np = (img_tensor * 255).astype(np.uint8)

            # Create PIL image (RGB)
            pil_img = Image.fromarray(img_np)

            # Create alpha channel image (avoid deprecated 'mode' kwarg in Pillow 13+)
            alpha_img = Image.fromarray(alpha_np).convert("L")

            # Convert to RGBA and add alpha channel
            pil_img_rgba = pil_img.convert("RGBA")
            pil_img_rgba.putalpha(alpha_img)

            if not _write_pil_image(pil_img_rgba, target_path, fmt, quality, metadata_text):
                return (False,)
            print(f"Basic data handling: Successfully saved image with mask to {target_path}")

        return (True,)


class PathInputDir(ComfyNodeABC):
    """
    Returns the ComfyUI input path.

    This is where input images are usually stored when using ComfyUI
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {}

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("input_path",)
    OUTPUT_TOOLTIPS = ("Absolute path of ComfyUI's input directory.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "execute"
    DISPLAY_NAME = "Get ComfyUI Input Path"

    def execute(self) -> tuple[str]:
        return (get_input_directory(),)


class PathOutputDir(ComfyNodeABC):
    """
    Returns the ComfyUI output path.

    This is where output images are usually stored when using ComfyUI
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {}

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("output_path",)
    OUTPUT_TOOLTIPS = ("Absolute path of ComfyUI's output directory.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "execute"
    DISPLAY_NAME = "Get ComfyUI Output Path"

    def execute(self) -> tuple[str]:
        return (get_output_directory(),)


NODE_CLASS_MAPPINGS = {
    "Basic data handling: PathAbspath": PathAbspath,
    "Basic data handling: PathBasename": PathBasename,
    "Basic data handling: PathCommonPrefix": PathCommonPrefix,
    "Basic data handling: PathDirname": PathDirname,
    "Basic data handling: PathExists": PathExists,
    "Basic data handling: PathExpandVars": PathExpandVars,
    "Basic data handling: PathGetCwd": PathGetCwd,
    "Basic data handling: PathGetExtension": PathGetExtension,
    "Basic data handling: PathSetExtension": PathSetExtension,
    "Basic data handling: PathGetSize": PathGetSize,
    "Basic data handling: PathGlob": PathGlob,
    "Basic data handling: PathInputDir": PathInputDir,
    "Basic data handling: PathIsAbsolute": PathIsAbsolute,
    "Basic data handling: PathIsDir": PathIsDir,
    "Basic data handling: PathIsFile": PathIsFile,
    "Basic data handling: PathJoin": PathJoin,
    "Basic data handling: PathListDir": PathListDir,
    "Basic data handling: PathNormalize": PathNormalize,
    "Basic data handling: PathOutputDir": PathOutputDir,
    "Basic data handling: PathRelative": PathRelative,
    "Basic data handling: PathSplit": PathSplit,
    "Basic data handling: PathSplitExt": PathSplitExt,
    "Basic data handling: PathLoadStringFile": PathLoadStringFile,
    "Basic data handling: PathLoadImageRGB": PathLoadImageRGB,
    "Basic data handling: PathLoadImageRGBA": PathLoadImageRGBA,
    "Basic data handling: PathLoadMaskFromAlpha": PathLoadMaskFromAlpha,
    "Basic data handling: PathLoadMaskFromGreyscale": PathLoadMaskFromGreyscale,
    "Basic data handling: PathSaveStringFile": PathSaveStringFile,
    "Basic data handling: PathSaveImageRGB": PathSaveImageRGB,
    "Basic data handling: PathSaveImageRGBA": PathSaveImageRGBA,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: PathAbspath": "abspath",
    "Basic data handling: PathBasename": "basename",
    "Basic data handling: PathCommonPrefix": "common prefix",
    "Basic data handling: PathDirname": "dirname",
    "Basic data handling: PathExists": "exists",
    "Basic data handling: PathExpandVars": "expand vars",
    "Basic data handling: PathGetCwd": "get current working directory",
    "Basic data handling: PathGetExtension": "get extension",
    "Basic data handling: PathSetExtension": "set extension",
    "Basic data handling: PathGetSize": "get size",
    "Basic data handling: PathGlob": "glob",
    "Basic data handling: PathInputDir": "input dir",
    "Basic data handling: PathIsAbsolute": "is absolute",
    "Basic data handling: PathIsDir": "is dir",
    "Basic data handling: PathIsFile": "is file",
    "Basic data handling: PathJoin": "join",
    "Basic data handling: PathListDir": "list dir",
    "Basic data handling: PathNormalize": "normalize",
    "Basic data handling: PathOutputDir": "output dir",
    "Basic data handling: PathRelative": "relative",
    "Basic data handling: PathSplit": "split",
    "Basic data handling: PathSplitExt": "splitext",
    "Basic data handling: PathLoadStringFile": "load STRING from file",
    "Basic data handling: PathLoadImageRGB": "load IMAGE from file (RGB)",
    "Basic data handling: PathLoadImageRGBA": "load IMAGE+MASK from file (RGBA)",
    "Basic data handling: PathLoadMaskFromAlpha": "load MASK from alpha channel",
    "Basic data handling: PathLoadMaskFromGreyscale": "load MASK from greyscale/red",
    "Basic data handling: PathSaveStringFile": "save STRING to file",
    "Basic data handling: PathSaveImageRGB": "save IMAGE to file",
    "Basic data handling: PathSaveImageRGBA": "save IMAGE+MASK to file",
}
