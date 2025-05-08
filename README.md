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

- **LIST**: Python list manipulation nodes (as a single variable)
  - Conversion: convert to data list
  - Creation: any to LIST
  - Modification: append, extend, insert, remove, pop, clear, set_item
  - Access: get_item, slice, index, contains
  - Information: length, count
  - Operations: sort, reverse, min, max

- **SET**: Python set manipulation nodes (as a single variable)
  - Conversion: convert to data list, to LIST
  - Creation: any to SET, LIST to SET
  - Modification: add, remove, discard, pop, clear
  - Information: length, contains
  - Set operations: union, intersection, difference, symmetric_difference
  - Comparison: is_subset, is_superset, is_disjoint

- **data list**: ComfyUI list manipulation nodes (for processing individual items)
  - Creation: create_empty
  - Modification: append, filter, extend, insert, remove, pop, clear, set_item
  - Access: get_item, slice, index, contains
  - Information: length, count
  - Operations: sort, reverse, copy, zip, min, max

- **cast**: Type conversion nodes for ComfyUI data types
  - Basic conversions: to STRING, to INT, to FLOAT, to BOOLEAN
  - Collection conversions: to LIST, to SET, to DICT
  - Special conversions: data list to LIST, data list to SET

- **DICT**: Dictionary manipulation nodes
  - Creation: create, from_items, from_lists, fromkeys, any_to_DICT
  - Access: get, get_multiple, keys, values, items
  - Modification: set, update, setdefault, merge
  - Removal: pop, popitem, remove, clear
  - Information: length, contains_key
  - Operations: copy, filter_by_keys, exclude_keys, invert, compare
  - Conversion: get_keys_values

- **INT**: Integer operation nodes
  - Basic operations: add, subtract, multiply, divide, modulus, power
  - Bit operations: bit_length, to_bytes, from_bytes, bit_count

- **FLOAT**: Floating-point operation nodes
  - Basic operations: add, subtract, multiply, divide, power, round
  - Specialized: is_integer, as_integer_ratio, to_hex, from_hex

- **BOOLEAN**: Boolean logic nodes
  - Logic operations: and, or, not, xor, nand, nor

- **Comparison**: Value comparison nodes
  - Basic comparisons: equal (==), not equal (!=), greater than (>), less than (<), etc.
  - String comparison: case-sensitive/insensitive string comparison with various operators
  - Special comparisons: number in range, is null, compare length
  - Container operations: length comparison for strings, lists, and other containers

- **Flow Control**: Workflow control nodes
  - Conditional: if/else for branching logic based on conditions
  - Selection: switch/case for selecting from multiple options based on an index

- **Math**: Mathematical operations
  - Trigonometric: sin, cos, tan, asin, acos, atan, atan2
  - Logarithmic/Exponential: log, log10, exp, sqrt
  - Numerical: min, max
  - Constants: pi, e
  - Conversion: degrees/radians
  - Rounding: floor, ceil
  - Other: abs (absolute value)

## Understanding LIST vs. data list vs. SET

ComfyUI has different data types that serve different purposes:

### 1. LIST datatype
- A Python list represented as a **single variable** in the workflow
- Treated as a self-contained object that can be passed between nodes
- Cannot directly connect to nodes that expect individual items
- Best for:
  - Working with collections of data as a single unit
  - Storing intermediate results that need to be processed as a whole
  - Passing collections between different parts of your workflow
  - Complex data storage that shouldn't be split apart

### 2. SET datatype
- A Python set represented as a **single variable** in the workflow
- Stores unique values with no duplicates
- Supports mathematical set operations (union, intersection, etc.)
- Best for:
  - Eliminating duplicate values
  - Testing membership efficiently
  - Set operations (union, difference, etc.)
  - When element order doesn't matter

### 3. data list
- A native ComfyUI list where **items are processed individually**
- Acts like a standard array/list in most programming contexts
- Items can be accessed individually by compatible nodes
- Supports built-in ComfyUI iteration over each item
- Best for:
  - Working directly with multiple items in parallel
  - Batch processing scenarios
  - When you need to apply the same operation to multiple inputs
  - When your operation needs to work with individual items separately

### Converting between types
- Use `convert to data list` node to transform a LIST or SET into a ComfyUI data list
- Use `convert to LIST` node to transform a ComfyUI data list into a LIST object
- Use `LIST to SET` to convert a LIST to a SET (removing duplicates)
- Use `SET to LIST` to convert a SET to a LIST

### When to use which type
- Use **LIST** when you need:
  - Ordered collection with potential duplicates
  - To preserve insertion order
  - To access elements by position/index
  - To use methods like append, extend, etc.

- Use **SET** when you need:
  - Collection of unique values (no duplicates)
  - Fast membership testing (x in set)
  - Set theory operations (union, intersection)
  - To eliminate duplicates from data

- Use **data list** when you need to:
  - Process each item individually through ComfyUI nodes
  - Allow nodes to iterate through your items automatically
  - Connect to nodes that expect individual inputs
  - Perform batch processing operations

## Tests

This repo contains unit tests written in Pytest in the `tests/` directory. It is recommended to unit test your custom node.

- [build-pipeline.yml](.github/workflows/build-pipeline.yml) will run pytest and linter on any open PRs
- [validate.yml](.github/workflows/validate.yml) will run [node-diff](https://github.com/Comfy-Org/node-diff) to check for breaking changes
