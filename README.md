# Basic Data Handling

Basic Python functions for manipulating data that every programmer is used to. These nodes are very lightweight and
require no additional dependencies.

## Quickstart

### Recommended Installation

1. Install [ComfyUI](https://docs.comfy.org/get_started)
2. Install [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)
3. Look up the "Basic data handling" extension in ComfyUI-Manager
4. Restart ComfyUI

### Alternative (Manual Installation)

1. Install [ComfyUI](https://docs.comfy.org/get_started)
2. Clone this repository under `ComfyUI/custom_nodes`
3. Restart ComfyUI

## Node Categories

### BOOLEAN

Boolean logic operations:

- **Logic operations**: and, or, not, xor, nand, nor

### Cast

Type conversion nodes for ComfyUI data types:
to BOOLEAN, to FLOAT, to INT, to STRING, to DICT, to LIST, to SET

### Comparison

Value comparison nodes:

- **Basic comparisons**: equal (==), not equal (!=), greater than (>), greater than or equal (>=), less than (<), less
  than or equal (<=)
- **String comparison**: StringComparison with case-sensitive/insensitive options
- **Special comparisons**: NumberInRange, IsNull
- **Container operations**: CompareLength

### Control Flow

Mechanisms to direct workflow execution:

- **Conditional branching**:
    - if/else - Routes based on a boolean condition
    - if/elif/.../else - Supports multiple conditional branches
    - switch/case - Selects from options based on an index
- **Execution management**:
    - disable flow - Conditionally enables/disables a flow
    - flow select - Directs output to either "true" or "false" path
    - force calculation - Prevents caching and forces recalculation
    - force execution order - Controls node execution sequence

### Data List

ComfyUI list manipulation nodes (for processing individual items):

- **Creation**: create Data List (generic and type-specific versions)
- **Modification**: append, extend, insert, set item, remove, pop, pop random
- **Filtering**: filter, filter select
- **Access**: get item, first, last, slice, index, contains
- **Information**: length, count
- **Operations**: sort, reverse, zip, min, max
- **Conversion**: convert to LIST, convert to SET

### DICT

Dictionary manipulation nodes:

- **Creation**: create (generic and type-specific), create from items, create from lists, fromkeys
- **Access**: get, get_multiple, keys, values, items
- **Modification**: set, update, setdefault, merge
- **Removal**: pop, popitem, pop random, remove
- **Information**: length, contains_key
- **Operations**: filter_by_keys, exclude_keys, invert, compare
- **Conversion**: get_keys_values

### FLOAT

Floating-point operation nodes:

- **Creation**: create FLOAT from string
- **Basic arithmetic**: add, subtract, multiply, divide, divide (zero safe), power
- **Formatting**: round (to specified decimal places)
- **Conversion**: to_hex, from_hex
- **Analysis**: is_integer, as_integer_ratio

### INT

Integer operation nodes:

- **Creation**: create INT, create INT with base
- **Basic arithmetic**: add, subtract, multiply, divide, divide (zero safe), modulus, power
- **Bit operations**: bit_length, bit_count
- **Byte conversion**: to_bytes, from_bytes

### LIST

Python list manipulation nodes (as a single variable):

- **Creation**: create LIST (generic and type-specific versions)
- **Modification**: append, extend, insert, remove, pop, pop random, set_item
- **Access**: get_item, first, last, slice, index, contains
- **Information**: length, count
- **Operations**: sort, reverse, min, max
- **Conversion**: convert to data list, convert to SET

### Math

Mathematical operations:

- **Generic**: formula
- **Trigonometric functions**: sin, cos, tan, asin, acos, atan, atan2
- **Logarithmic/Exponential**: log, log10, exp, sqrt
- **Constants**: pi, e
- **Angle conversion**: degrees, radians
- **Rounding operations**: floor, ceil
- **Min/Max functions**: min, max
- **Other**: abs

### Path

File system path manipulation nodes:

- **Basic operations**: join, split, splitext, basename, dirname, normalize
- **Path information**: abspath, exists, is_file, is_dir, is_absolute, get_size, get_extension, set_extension, input_dir, output_dir
- **Directory operations**: list_dir, get_cwd
- **Path searching**: glob, common_prefix
- **Path conversions**: relative, expand_vars
- **File loading**: load STRING from file, load IMAGE from file, load IMAGE+MASK from file, load MASK from alpha
  channel, load MASK from greyscale/red
- **File saving**: save STRING to file, save IMAGE to file, save IMAGE+MASK to file

### SET

Python set manipulation nodes (as a single variable):

- **Creation**: create SET (generic and type-specific versions)
- **Modification**: add, remove, discard, pop, pop random
- **Information**: length, contains
- **Set operations**: union, intersection, difference, symmetric_difference
- **Set comparison**: is_subset, is_superset, is_disjoint
- **Conversion**: convert to data list, convert to LIST

### STRING

String manipulation nodes:

- **Text case conversion**: capitalize, casefold, lower, swapcase, title, upper
- **Text inspection**: contains, endswith, find, length, rfind, startswith
- **Character type checking**: isalnum, isalpha, isascii, isdecimal, isdigit, isidentifier, islower, isnumeric,
  isprintable, isspace, istitle, isupper
- **Text formatting**: center, expandtabs, ljust, rjust, zfill
- **Text splitting/joining**: join, split, rsplit, splitlines (with data list and LIST variants)
- **Text modification**: concat, count, replace, strip, lstrip, rstrip, removeprefix, removesuffix
- **Encoding/escaping**: decode, encode, escape, unescape, format_map

### Time

Date and time manipulation nodes:

- **DateTime creation/conversion**: TimeNow, TimeNowUTC, TimeToUnix, UnixToTime
- **String formatting/parsing**: TimeFormat, TimeParse
- **Time calculations**: TimeDelta, TimeAddDelta, TimeSubtractDelta, TimeDifference
- **Component extraction**: TimeExtract (year, month, day, hour, etc.)

## Understanding Data Types

ComfyUI provides three different collection types that serve distinct purposes:

### Collection Types and When to Choose Them

| Type          | Description                                                    | When to Choose                                                                                                                                                                     |
|---------------|----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **data list** | Native ComfyUI list where **items are processed individually** | • When you need ComfyUI to process each item individually<br>• For batch operations with parallel processing<br>• When connecting to nodes that expect individual inputs           |
| **LIST**      | Python list passed as a single variable                        | • When you need ordered collections with preserved duplicates<br>• When index-based access is important<br>• When you need to work with the collection as a complete unit          |
| **SET**       | Python set passed as a single variable                         | • When you need to ensure unique values only<br>• When you need fast membership testing<br>• For set operations (union, intersection, etc.)<br>• When element order doesn't matter |
