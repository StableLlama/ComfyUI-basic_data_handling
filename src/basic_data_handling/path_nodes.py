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


# helper functions:

def load_image_helper(path: str):
    """Helper function to load an image from a path"""
    from PIL import Image, ImageOps
    try:
        import pillow_jxl
    except ModuleNotFoundError:
        pass

    if not os.path.exists(path):
        raise FileNotFoundError(f"Basic data handling: Image file not found: {path}")

    # Open and process the image
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)

    return img


def extract_mask_from_alpha(img):
    """Extract a mask from the alpha channel of an image"""
    import numpy as np
    import torch

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
    import numpy as np
    import torch

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
                "path": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("absolute path",)
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
                "path": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("basename",)
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
                "path1": (IO.STRING, {"default": ""}),
            },
            "optional": {
                "path2": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("common prefix",)
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
                "path": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("dirname",)
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
                "path": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("exists",)
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
                "path": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("expanded path",)
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
                "path": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("extension",)
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
                "path": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    RETURN_NAMES = ("size (bytes)",)
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
                "pattern": (IO.STRING, {"default": "*.txt"}),
            },
            "optional": {
                "recursive": (IO.BOOLEAN, {"default": False}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("matching paths",)
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
                "path": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is absolute",)
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
                "path": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is dir",)
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
                "path": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is file",)
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
                "path1": (IO.STRING, {"default": ""}),
            },
            "optional": {
                "path2": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("path",)
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
                "path": (IO.STRING, {"default": ""}),
            },
            "optional": {
                "files_only": (IO.BOOLEAN, {"default": False}),
                "dirs_only": (IO.BOOLEAN, {"default": False}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("entries",)
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
                "path": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("normalized path",)
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
                "path": (IO.STRING, {}),
                "extension": (IO.STRING, {"default": ".txt"}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("path",)
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
                "path": (IO.STRING, {"default": ""}),
            },
            "optional": {
                "start": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("relative path",)
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
                "path": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.STRING, IO.STRING)
    RETURN_NAMES = ("directory", "filename")
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
                "path": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.STRING, IO.STRING)
    RETURN_NAMES = ("path without ext", "extension")
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
                "path": (IO.STRING, {"default": ""}),
            },
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("text",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "load_text"

    def load_text(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Basic data handling: String file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        return (text,)


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
                "path": (IO.STRING, {"default": ""}),
            },
        }

    RETURN_TYPES = (IO.IMAGE,)
    RETURN_NAMES = ("image",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "load_image_rgb"

    def load_image_rgb(self, path: str):
        import numpy as np
        import torch

        img = load_image_helper(path)

        # Convert to RGB (removing alpha if present)
        img_rgb = img.convert("RGB")

        # Convert to tensor format expected by ComfyUI
        image_tensor = np.array(img_rgb).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_tensor)[None,]

        return (image_tensor,)


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
                "path": (IO.STRING, {"default": ""}),
            },
        }

    RETURN_TYPES = (IO.IMAGE, IO.MASK)
    RETURN_NAMES = ("image", "mask")
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "load_image_rgba"

    def load_image_rgba(self, path: str):
        import numpy as np
        import torch

        img = load_image_helper(path)

        # Convert to RGB for the image
        img_rgb = img.convert("RGB")

        # Convert to tensor format expected by ComfyUI
        image_tensor = np.array(img_rgb).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_tensor)[None,]

        # Extract alpha channel as mask
        mask_tensor = extract_mask_from_alpha(img)

        return (image_tensor, mask_tensor)


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
                "path": (IO.STRING, {"default": ""}),
            },
        }

    RETURN_TYPES = (IO.MASK,)
    RETURN_NAMES = ("mask",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "load_mask_from_alpha"

    def load_mask_from_alpha(self, path: str):
        img = load_image_helper(path)
        mask_tensor = extract_mask_from_alpha(img)
        return (mask_tensor,)


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
                "path": (IO.STRING, {"default": ""}),
            },
            "optional": {
                "invert": (IO.BOOLEAN, {"default": False}),
            },
        }

    RETURN_TYPES = (IO.MASK,)
    RETURN_NAMES = ("mask",)
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "load_mask_from_greyscale"

    def load_mask_from_greyscale(self, path: str, invert: bool = False):
        img = load_image_helper(path)
        mask_tensor = extract_mask_from_greyscale(img)

        # Optionally invert the mask (1.0 - mask)
        if invert:
            mask_tensor = 1.0 - mask_tensor

        return (mask_tensor,)


class PathSaveStringFile(ComfyNodeABC):
    """
    Saves a string to a text file.

    This node takes a string and saves it to the specified path as a text file.
    Optionally, you can choose to create the directory if it doesn't exist.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": (IO.STRING, {"default": ""}),
                "path": (IO.STRING, {"default": ""}),
            },
            "optional": {
                "create_dirs": (IO.BOOLEAN, {"default": True}),
                "encoding": (IO.STRING, {"default": "utf-8"}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN)
    RETURN_NAMES = ("success")
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "save_text"
    OUTPUT_NODE = True

    def save_text(self, text: str, path: str, create_dirs: bool = True, encoding: str = "utf-8"):
        if not path:
            return (False,)

        try:
            # Create directories if needed
            directory = os.path.dirname(path)
            if directory and create_dirs and not os.path.exists(directory):
                os.makedirs(directory)

            with open(path, "w", encoding=encoding) as f:
                f.write(text)

            return (True,)
        except Exception as e:
            print(f"Basic data handling: Error saving text file: {e}")
            return (False,)


class PathSaveImageRGB(ComfyNodeABC):
    """
    Saves an image to a file.

    This node takes an image tensor and saves it to the specified path.
    Supports various image formats like PNG, JPG, WEBP, JXL (if pillow-jxl is installed), etc.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": (IO.IMAGE,),
                "path": (IO.STRING, {"default": ""}),
            },
            "optional": {
                "format": (IO.STRING, {"default": "png"}),
                "quality": (IO.INT, {"default": 95, "min": 1, "max": 100}),
                "create_dirs": (IO.BOOLEAN, {"default": True}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN)
    RETURN_NAMES = ("success")
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "save_image"
    OUTPUT_NODE = True

    def save_image(self, images, path: str, format: str = "png", quality: int = 95, create_dirs: bool = True):
        if not path:
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
                import pillow_jxl
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

            # Save the image
            if format.lower() == "jpg" or format.lower() == "jpeg":
                pil_img.save(path, format="JPEG", quality=quality)
            elif format.lower() == "webp":
                pil_img.save(path, format="WEBP", quality=quality)
            elif format.lower() == "jxl" and has_jxl_support:
                # JPEG XL specific options
                pil_img.save(path, format="JXL", quality=quality)
            else:
                pil_img.save(path, format=format.upper())

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
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": (IO.IMAGE,),
                "mask": (IO.MASK,),
                "path": (IO.STRING, {"default": ""}),
            },
            "optional": {
                "format": (IO.STRING, {"default": "png"}),
                "quality": (IO.INT, {"default": 95, "min": 1, "max": 100}),
                "invert_mask": (IO.BOOLEAN, {"default": False}),
                "create_dirs": (IO.BOOLEAN, {"default": True}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN)
    RETURN_NAMES = ("success")
    CATEGORY = "Basic/Path"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "save_image_with_mask"
    OUTPUT_NODE = True

    def save_image_with_mask(self, images, mask, path: str, format: str = "png",
                            quality: int = 95, invert_mask: bool = False,
                            create_dirs: bool = True):
        if not path:
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
            import torch
            from PIL import Image

            # Check if pillow_jxl is available for JXL support
            has_jxl_support = False
            try:
                import pillow_jxl
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

            # Create alpha channel image
            alpha_img = Image.fromarray(alpha_np, mode='L')

            # Convert to RGBA and add alpha channel
            pil_img_rgba = pil_img.convert("RGBA")
            pil_img_rgba.putalpha(alpha_img)

            # Save the image
            if format.lower() == "webp":
                pil_img_rgba.save(path, format="WEBP", quality=quality)
            elif format.lower() == "jxl" and has_jxl_support:
                # JPEG XL supports alpha channel
                pil_img_rgba.save(path, format="JXL", quality=quality)
            else:
                pil_img_rgba.save(path, format=format.upper())

            return (True,)
        except Exception as e:
            print(f"Basic data handling: Error saving image with mask: {e}")
            return (False,)


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
    "Basic data handling: PathIsAbsolute": PathIsAbsolute,
    "Basic data handling: PathIsDir": PathIsDir,
    "Basic data handling: PathIsFile": PathIsFile,
    "Basic data handling: PathJoin": PathJoin,
    "Basic data handling: PathListDir": PathListDir,
    "Basic data handling: PathNormalize": PathNormalize,
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
    "Basic data handling: PathIsAbsolute": "is absolute",
    "Basic data handling: PathIsDir": "is dir",
    "Basic data handling: PathIsFile": "is file",
    "Basic data handling: PathJoin": "join",
    "Basic data handling: PathListDir": "list dir",
    "Basic data handling: PathNormalize": "normalize",
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
