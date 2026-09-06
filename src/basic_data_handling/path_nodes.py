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

    if 'A' in img.getbands():
        alpha = np.array(img.getchannel('A')).astype(np.float32) / 255.0
        mask_tensor = 1.0 - torch.from_numpy(alpha)
    elif img.mode == 'P' and 'transparency' in img.info:
        alpha = np.array(img.convert('RGBA').getchannel('A')).astype(np.float32) / 255.0
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

    if img.mode == 'L':
        # Image is already greyscale
        gray = np.array(img).astype(np.float32) / 255.0
    elif img.mode == 'RGB' or img.mode == 'RGBA':
        # Use the red channel of RGB or RGBA
        gray = np.array(img.getchannel('R')).astype(np.float32) / 255.0
    else:
        # Convert to greyscale if it's another format
        gray_img = img.convert('L')
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
            }
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
            }
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
            }
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
            }
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
        if not extension.startswith('.') and extension:
            extension = '.' + extension

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
            }
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
    OUTPUT_TOOLTIPS = ("The RGB image as a tensor.", "The alpha channel as a mask (blank when the image has none).", "True when the image was loaded.")
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
            }
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
        '<dc:description><rdf:Alt><rdf:li xml:lang="x-default">' + body + '</rdf:li></rdf:Alt></dc:description>\n'
        '</rdf:Description>\n'
        '</rdf:RDF>\n'
        '</x:xmpmeta>\n'
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


class PathSaveImageRGB(ComfyNodeABC):
    """
    Saves an image to a file.

    This node takes an image tensor and saves it to the specified path.
    Supports various image formats like PNG, JPG, WEBP, JXL (if pillow-jxl is installed), etc.

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
                "path": (IO.STRING, {"default": "", "tooltip": "Destination file path (an extension is added from the format when missing)."}),
            },
            "optional": {
                "format": (IO.STRING, {"default": "png", "tooltip": "Image format: png, jpg, webp or jxl (jxl needs pillow-jxl installed)."}),
                "quality": (IO.INT, {"default": 95, "min": 1, "max": 100, "tooltip": "Quality for lossy formats (jpg/webp/jxl)."}),
                "create_dirs": (IO.BOOLEAN, {"default": True, "tooltip": "Create missing parent directories."}),
                "prompt": (IO.STRING, {"default": "", "tooltip": "Optional positive prompt embedded as parameters metadata."}),
                "negative_prompt": (IO.STRING, {"default": "", "tooltip": "Optional negative prompt embedded as parameters metadata."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("success",)
    OUTPUT_TOOLTIPS = ("True when the image was saved successfully.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "save_image"
    OUTPUT_NODE = True

    def save_image(self, images, path: str, format: str = "png", quality: int = 95,
                   create_dirs: bool = True, prompt: str = "", negative_prompt: str = ""):
        if not path:
            print("Basic data handling: Save failed - no path specified")
            return (False,)

        # If the path doesn't have an extension or it doesn't match the format, add it
        if not path.lower().endswith(f".{format.lower()}"):
            path = f"{path}.{format.lower()}"

        try:
            import numpy as np
            from PIL import Image

            # Check if pillow_jxl is available for JXL support
            has_jxl_support = False
            try:
                import pillow_jxl # noqa: F401 - imported but unused, kept for JPEG XL support
                has_jxl_support = True
            except ModuleNotFoundError:
                # pillow_jxl is not installed
                if format.lower() == "jxl":
                    print("Basic data handling: JPEG XL format requested but pillow_jxl module is not installed. "
                          "Please install it with 'pip install pillow-jxl-plugin'.")
                    return (False,)

            # Create directories if needed
            directory = os.path.dirname(path)
            if directory and create_dirs and not os.path.exists(directory):
                os.makedirs(directory)

            # Convert from tensor format back to PIL Image
            # Extract the first image from the batch
            i = 0
            img_tensor = images[i].cpu().numpy()

            # Convert to uint8 format for PIL
            img_np = (img_tensor * 255).astype(np.uint8)

            # Create PIL image
            pil_img = Image.fromarray(img_np)

            # Compose the prompt metadata to embed into the saved file
            metadata_text = compose_prompt_text(prompt, negative_prompt)
            fmt = format.lower()

            # Save the image, embedding prompt metadata where the format supports it
            if fmt == "jpg" or fmt == "jpeg":
                pil_img.save(path, format="JPEG", quality=quality, **metadata_save_kwargs(metadata_text, fmt))
            elif fmt == "webp":
                pil_img.save(path, format="WEBP", quality=quality, **metadata_save_kwargs(metadata_text, fmt))
            elif fmt == "jxl" and has_jxl_support:
                # JPEG XL specific options
                pil_img.save(path, format="JXL", quality=quality, **metadata_save_kwargs(metadata_text, fmt))
            elif fmt == "png":
                pil_img.save(path, format="PNG", **metadata_save_kwargs(metadata_text, fmt))
            else:
                if metadata_text:
                    print("Basic data handling: Prompt metadata is not supported for this format; skipping it.")
                pil_img.save(path, format=format.upper())

            print(f"Basic data handling: Successfully saved image to {path}")
            return (True,)
        except Exception as e:
            print(f"Basic data handling: Error saving image: {e}")
            return (False,)


class PathSaveImageRGBA(ComfyNodeABC):
    """
    Saves an image with a mask to a file with transparency.

    This node takes an image tensor and a mask tensor and saves them to the
    specified path as an image with transparency, where the mask defines the
    alpha channel.

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
                "path": (IO.STRING, {"default": "", "tooltip": "Destination file path (an extension is added from the format when missing)."}),
            },
            "optional": {
                "format": (IO.STRING, {"default": "png", "tooltip": "Image format supporting alpha: png, webp or jxl; jpg is coerced to png."}),
                "quality": (IO.INT, {"default": 95, "min": 1, "max": 100, "tooltip": "Quality for lossy formats (webp/jxl)."}),
                "invert_mask": (IO.BOOLEAN, {"default": False, "tooltip": "Invert the mask before using it as the alpha channel."}),
                "create_dirs": (IO.BOOLEAN, {"default": True, "tooltip": "Create missing parent directories."}),
                "prompt": (IO.STRING, {"default": "", "tooltip": "Optional positive prompt embedded as parameters metadata."}),
                "negative_prompt": (IO.STRING, {"default": "", "tooltip": "Optional negative prompt embedded as parameters metadata."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("success",)
    OUTPUT_TOOLTIPS = ("True when the image with alpha was saved successfully.",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "save_image_with_mask"
    OUTPUT_NODE = True

    def save_image_with_mask(self, images, mask, path: str, format: str = "png",
                             quality: int = 95, invert_mask: bool = False,
                             create_dirs: bool = True, prompt: str = "",
                             negative_prompt: str = ""):
        if not path:
            print("Basic data handling: Save failed - no path specified")
            return (False,)

        # Check format compatibility - needs to support alpha channel
        if format.lower() in ["jpg", "jpeg"]:
            print("Basic data handling: JPEG format doesn't support transparency. Using PNG instead.")
            format = "png"

        # If the path doesn't have an extension or it doesn't match the format, add it
        if not path.lower().endswith(f".{format.lower()}"):
            path = f"{path}.{format.lower()}"

        try:
            import numpy as np
            from PIL import Image

            # Check if pillow_jxl is available for JXL support
            has_jxl_support = False
            try:
                import pillow_jxl # noqa: F401 - imported but unused, kept for JPEG XL support
                has_jxl_support = True
            except ModuleNotFoundError:
                # pillow_jxl is not installed
                if format.lower() == "jxl":
                    print("Basic data handling: JPEG XL format requested but pillow_jxl module is not installed. "
                          "Please install it with 'pip install pillow-jxl-plugin'.")
                    return (False,)

            # Create directories if needed
            directory = os.path.dirname(path)
            if directory and create_dirs and not os.path.exists(directory):
                os.makedirs(directory)

            # Convert from tensor format back to PIL Image
            # Extract the first image from the batch
            i = 0
            img_tensor = images[i].cpu().numpy()
            mask_tensor = mask[i].cpu()

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

            # Compose the prompt metadata to embed into the saved file
            metadata_text = compose_prompt_text(prompt, negative_prompt)
            fmt = format.lower()

            # Save the image, embedding prompt metadata where the format supports it
            if fmt == "webp":
                pil_img_rgba.save(path, format="WEBP", quality=quality, **metadata_save_kwargs(metadata_text, fmt))
            elif fmt == "jxl" and has_jxl_support:
                # JPEG XL supports alpha channel
                pil_img_rgba.save(path, format="JXL", quality=quality, **metadata_save_kwargs(metadata_text, fmt))
            elif fmt == "png":
                pil_img_rgba.save(path, format="PNG", **metadata_save_kwargs(metadata_text, fmt))
            else:
                if metadata_text:
                    print("Basic data handling: Prompt metadata is not supported for this format; skipping it.")
                pil_img_rgba.save(path, format=format.upper())

            print(f"Basic data handling: Successfully saved image with mask to {path}")
            return (True,)
        except Exception as e:
            print(f"Basic data handling: Error saving image with mask: {e}")
            return (False,)


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
