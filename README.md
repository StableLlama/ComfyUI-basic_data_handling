# Basic data handling

Basic Python functions for manipulating data that every programmer is used to.

These nodes are very lightweight and require no additional dependencies.

> [!NOTE]
> This projected is in early development—do not use it in production, yet!

## Quickstart

1. Install [ComfyUI](https://docs.comfy.org/get_started).
1. Install [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)
1. Look up this extension in ComfyUI-Manager. If you are installing manually, clone this repository under `ComfyUI/custom_nodes`.
1. Restart ComfyUI.

# Features

- **STRING**: String manipulation nodes
  - Basic functions: capitalize, casefold, center, concat, count, encode/decode, find/rfind, join, lower/upper, replace, split, strip, etc.
  - String checking: contains, endswith, startswith
  - Case conversion: lower, upper, swapcase, title, capitalize
  - Validation: isalnum, isalpha, isdigit, isnumeric, etc.

- **LIST**: List manipulation nodes
  - Creation: create, create_empty
  - Modification: append, extend, insert, remove, pop, clear, set_item
  - Access: get_item, slice, index, contains
  - Information: length, count
  - Operations: sort, reverse, copy, join, zip, flatten
  - Unpacking: unpack

- **INT**: Integer operation nodes
  - Basic operations: add, subtract, multiply, divide, modulus, power
  - Bit operations: bit_length, to_bytes, from_bytes, bit_count

- **FLOAT**: Floating-point operation nodes
  - Basic operations: add, subtract, multiply, divide, power, round
  - Specialized: is_integer, as_integer_ratio, to_hex, from_hex

- **BOOLEAN**: Boolean logic nodes
  - Logic operations: and, or, not, xor, nand, nor

## Tests

This repo contains unit tests written in Pytest in the `tests/` directory. It is recommended to unit test your custom node.

- [build-pipeline.yml](.github/workflows/build-pipeline.yml) will run pytest and linter on any open PRs
- [validate.yml](.github/workflows/validate.yml) will run [node-diff](https://github.com/Comfy-Org/node-diff) to check for breaking changes
