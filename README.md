# Basic data handling

Basic Python functions for manipulating data that every programmer is used to.

These nodes are very lightweight and require no additional dependencies.

## Quickstart

### Recommended

1. Install [ComfyUI](https://docs.comfy.org/get_started).
1. Install [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)
1. Look up the "Basic data handling" extension in ComfyUI-Manager.
1. Restart ComfyUI.

### Alternative (manual installation)

1. Install [ComfyUI](https://docs.comfy.org/get_started).
1. Clone this repository under `ComfyUI/custom_nodes`.
1. Restart ComfyUI.

# Features

## Nodes

### BOOLEAN: Boolean logic nodes
- Logic operations: and, or, not, xor, nand, nor

### cast: Type conversion nodes for ComfyUI data types
- Basic data type conversions:
    - to BOOLEAN - Converts any input to a Boolean using Python's truthy/falsy rules
    - to FLOAT - Converts numeric input to a floating-point number (raises ValueError for invalid inputs)
    - to INT - Converts numeric input to an integer (raises ValueError for invalid inputs)
    - to STRING - Converts any input to a string using Python's str() function
- Collection type conversions:
    - to DICT - Converts compatible inputs (mappings or lists of key-value pairs) to a dictionary
    - to LIST - Converts input to a LIST (wraps single items in a list, preserves existing lists)
    - to SET - Converts input to a SET (creates a set from single items or collections, removing duplicates)

### Comparison: Value comparison nodes
- Basic comparisons: equal (==), not equal (!=), greater than (>), greater than or equal (>=), less than (<), less than or equal (<=)
- String comparison: StringComparison node with case-sensitive/insensitive options and various operators (==, !=, >, <, >=, <=)
- Special comparisons: NumberInRange (check if a value is within specified bounds), IsNull (check if a value is null)
- Container operations: CompareLength (compare the length of strings, lists, and other containers)

### data list: ComfyUI list manipulation nodes (for processing individual items)
- Creation:
    - create Data List - Generic creation from any type inputs (dynamically expandable)
    - Type-specific creation:
        - create Data List from BOOLEANs - Creates a data list from Boolean values
        - create Data List from FLOATs - Creates a data list from floating-point values
        - create Data List from INTs - Creates a data list from integer values
        - create Data List from STRINGs - Creates a data list from string values
- Modification:
    - append - Adds an item to the end of a data list
    - extend - Combines elements from multiple data lists
    - insert - Inserts an item at a specified position
    - set item - Replaces an item at a specified position
    - remove - Removes the first occurrence of a specified value
    - pop - Removes and returns an item at a specified position
    - pop random - Removes and returns a random element
- Filtering:
    - filter - Filters a data list using boolean values
    - filter select - Separates items into two lists based on boolean filters
- Access:
    - get item - Retrieves an item at a specified position
    - first - Returns the first element in a data list
    - last - Returns the last element in a data list
    - slice - Creates a subset of a data list using start/stop/step parameters
    - index - Finds the position of a value in a data list
    - contains - Checks if a data list contains a specified value
- Information:
    - length - Returns the number of items in a data list
    - count - Counts occurrences of a value in a data list
- Operations:
    - sort - Orders items (with optional reverse parameter)
    - reverse - Reverses the order of items
    - zip - Combines multiple data lists element-wise
    - min - Finds the minimum value in a list of numbers
    - max - Finds the maximum value in a list of numbers
- Conversion:
    - convert to LIST - Converts a data list to a LIST object
    - convert to SET - Converts a data list to a SET (removing duplicates)

### DICT: Dictionary manipulation nodes
- Creation: create (generic and type-specific versions), create from items (data list and LIST versions), create from lists, fromkeys
- Access: get, get_multiple, keys, values, items
- Modification: set, update, setdefault, merge
- Removal: pop, popitem, pop random, remove
- Information: length, contains_key
- Operations: filter_by_keys, exclude_keys, invert, compare
- Conversion: get_keys_values

### FLOAT: Floating-point operation nodes
- Creation: create FLOAT from string
- Basic arithmetic: add, subtract, multiply, divide, divide (zero safe), power
- Formatting: round (to specified decimal places)
- Conversion: to_hex (hexadecimal representation), from_hex (create from hex string)
- Analysis: is_integer (check if float has no fractional part), as_integer_ratio (get numerator/denominator)

### Flow Control: Workflow control nodes
- Conditional branching:
  - if/else - Basic conditional that returns one of two values based on a condition
  - if/elif/.../else - Extended conditional with multiple conditions and outcomes
- Selection:
  - switch/case - Selects from multiple options based on an integer index
  - flow select - Directs a value to either "true" or "false" output path based on a condition
- Execution control:
  - force execution order - Coordinates the execution sequence of nodes in a workflow

### INT: Integer operation nodes
- Creation: create INT (from string), create INT with base (convert string with specified base)
- Basic arithmetic: add, subtract, multiply, divide, divide (zero safe), modulus, power
- Bit operations: bit_length (bits needed to represent number), bit_count (count of 1 bits)
- Byte conversion: to_bytes (convert integer to bytes), from_bytes (convert bytes to integer)

### LIST: Python list manipulation nodes (as a single variable)
- Creation: create LIST (generic), create from type-specific values (BOOLEANs, FLOATs, INTs, STRINGs)
- Modification: append, extend, insert, remove, pop, pop random, set_item
- Access: get_item, first, last, slice, index, contains
- Information: length, count
- Operations: sort (with optional reverse), reverse, min, max
- Conversion: convert to data list, convert to SET

### Math: Mathematical operations
- Trigonometric functions:
  - Basic: sin, cos, tan - Calculate sine, cosine, and tangent of angles (in degrees or radians)
  - Inverse: asin, acos, atan - Calculate inverse sine, cosine, and tangent (returns degrees or radians)
  - Special: atan2 - Calculate arc tangent of y/x with correct quadrant handling
- Logarithmic/Exponential functions:
  - log - Natural logarithm (base e) with optional custom base
  - log10 - Base-10 logarithm
  - exp - Exponential function (e^x)
  - sqrt - Square root
- Constants:
  - pi - Mathematical constant π (3.14159...)
  - e - Mathematical constant e (2.71828...)
- Angle conversion:
  - degrees - Convert radians to degrees
  - radians - Convert degrees to radians
- Rounding operations:
  - floor - Return largest integer less than or equal to input
  - ceil - Return smallest integer greater than or equal to input
- Min/Max functions:
  - min - Return minimum of two values
  - max - Return maximum of two values
- Other:
  - abs - Absolute value (magnitude without sign)

### path: File system path manipulation nodes
- Basic operations:
    - join - Joins multiple path components intelligently with correct separators
    - split - Splits a path into directory and filename components
    - splitext - Splits a path into name and extension components
    - basename - Extracts the filename component from a path
    - dirname - Extracts the directory component from a path
    - normalize - Collapses redundant separators and resolves up-level references
- Path information:
    - abspath - Returns the absolute (full) path by resolving relative components
    - exists - Checks if a path exists in the filesystem
    - is_file - Checks if a path points to a regular file
    - is_dir - Checks if a path points to a directory
    - is_absolute - Checks if a path is absolute (begins at root directory)
    - get_size - Returns the size of a file in bytes
    - get_extension - Extracts the file extension from a path (including the dot)
    - set_extension - Replaces or adds a file extension to a path
- Directory operations:
    - list_dir - Lists files and directories in a specified path with filtering options
    - get_cwd - Returns the current working directory
- Path searching:
    - glob - Finds paths matching a pattern with wildcard support
    - common_prefix - Finds the longest common leading component of given paths
- Path conversions:
    - relative - Computes a relative path from a start path to a target path
    - expand_vars - Replaces environment variables in a path with their values
- File loading:
    - load STRING from file - Loads a text file and returns its content as a STRING
    - load IMAGE from file (RGB) - Loads an image and returns RGB channels as a tensor
    - load IMAGE+MASK from file (RGBA) - Loads an image and returns RGB channels as a tensor and alpha channel as a mask
    - load MASK from alpha channel - Loads an image and extracts its alpha channel as a mask
    - load MASK from greyscale/red - Loads an image and creates a mask from its greyscale or red channel
- File saving:
    - save STRING to file - Saves a string to a text file with optional directory creation
    - save IMAGE to file - Saves an image tensor to a file in various formats (PNG, JPG, WEBP, JXL)
    - save IMAGE+MASK to file - Saves an image with transparency using a mask as the alpha channel

### SET: Python set manipulation nodes (as a single variable)
- Creation:
    - create SET - Generic creation from any type inputs (dynamically expandable)
    - Type-specific creation:
        - create SET from BOOLEANs - Creates a set from Boolean values
        - create SET from FLOATs - Creates a set from floating-point values
        - create SET from INTs - Creates a set from integer values
        - create SET from STRINGs - Creates a set from string values
- Modification:
    - add - Adds an item to a set
    - remove - Removes an item from a set (raises error if not present)
    - discard - Removes an item if present (no error if missing)
    - pop - Removes and returns an arbitrary element
    - pop random - Removes and returns a random element
- Information:
    - length - Returns the number of items in a set
    - contains - Checks if a set contains a specified value
- Set operations:
    - union - Combines elements from multiple sets
    - intersection - Returns elements common to all input sets
    - difference - Returns elements in first set but not in second set
    - symmetric_difference - Returns elements in either set but not in both
- Set comparison:
    - is_subset - Checks if first set is a subset of second set
    - is_superset - Checks if first set is a superset of second set
    - is_disjoint - Checks if two sets have no common elements
- Conversion:
    - convert to data list - Converts a SET to a ComfyUI data list
    - convert to LIST - Converts a SET to a LIST

### STRING: String manipulation nodes
Available nodes grouped by functionality:

#### Text case conversion
- capitalize - Converts first character to uppercase, rest to lowercase
- casefold - Aggressive lowercase for case-insensitive comparisons
- lower - Converts string to lowercase
- swapcase - Swaps case of all characters
- title - Converts string to titlecase
- upper - Converts string to uppercase

#### Text inspection and validation
- contains (in) - Checks if string contains a substring
- endswith - Checks if string ends with a specific suffix
- find - Finds first occurrence of a substring
- length - Returns the number of characters in the string
- rfind - Finds last occurrence of a substring
- startswith - Checks if string starts with a specific prefix

#### Character type checking
- isalnum - Checks if all characters are alphanumeric
- isalpha - Checks if all characters are alphabetic
- isascii - Checks if all characters are ASCII
- isdecimal - Checks if all characters are decimal
- isdigit - Checks if all characters are digits
- isidentifier - Checks if string is a valid Python identifier
- islower - Checks if all characters are lowercase
- isnumeric - Checks if all characters are numeric
- isprintable - Checks if all characters are printable
- isspace - Checks if all characters are whitespace
- istitle - Checks if string is titlecased
- isupper - Checks if all characters are uppercase

#### Text formatting and alignment
- center - Centers text within specified width
- expandtabs - Replaces tabs with spaces
- ljust - Left-aligns text within specified width
- rjust - Right-aligns text within specified width
- zfill - Pads string with zeros on the left

#### Text splitting and joining
- join (from data list) - Joins strings from a data list
- join (from LIST) - Joins strings from a LIST
- rsplit (from data list) - Splits string from right into a data list
- rsplit (from LIST) - Splits string from right into a LIST
- split (to data list) - Splits string into a data list
- split (to LIST) - Splits string into a LIST
- splitlines (from data list) - Splits string at line boundaries into a data list
- splitlines (to LIST) - Splits string at line boundaries into a LIST

#### Text modification
- concat - Combines two strings together
- count - Counts occurrences of a substring
- replace - Replaces occurrences of a substring
- strip - Removes leading and trailing characters
- lstrip - Removes leading characters
- rstrip - Removes trailing characters
- removeprefix - Removes prefix if present
- removesuffix - Removes suffix if present

#### Encoding and escaping
- decode - Converts bytes-like string to text
- encode - Converts string to bytes
- escape - Converts special characters to escape sequences
- unescape - Converts escape sequences to actual characters
- format_map - Formats string using values from dictionary

## Understanding data list vs. LIST vs. SET

ComfyUI has different data types that serve different purposes:

### 1. data list
- A native ComfyUI list where **items are processed individually**
- Acts like a standard array/list in most programming contexts
- Items can be accessed individually by compatible nodes
- Supports built-in ComfyUI iteration over each item
- Best for:
    - Working directly with multiple items in parallel
    - Processing each item in a collection separately
    - When you need ComfyUI's automatic iteration functionality

### 2. LIST
- A Python list passed as a single ComfyUI variable
- Must be processed as a complete unit by compatible nodes
- Operations apply to the entire LIST at once
- Best for:
    - Storing and manipulating structured data as a single unit
    - When you need to preserve ordered collections
    - Passing complex data structures between nodes

### 3. SET
- A Python set passed as a single ComfyUI variable
- Unordered collection of unique items
- Useful for membership testing, removing duplicates, and set operations
- Best for:
    - When you need to ensure uniqueness of items
    - Performing mathematical set operations (union, intersection, difference)
    - Efficient membership testing (contains operation)
    - When item order doesn't matter

## Control Flow Nodes

Control flow nodes provide mechanisms to direct the flow of execution in your ComfyUI workflows, allowing for conditional processing and dynamic execution paths.

### Available Control Flow Nodes:

#### Conditional Processing
- **if/else** - Routes execution based on a boolean condition
- **if/elif/.../else** - Supports multiple conditional branches
- **switch/case** - Selects from multiple options based on an index

#### Execution Management
- **disable flow** - Conditionally enables or disables a flow
- **flow select** - Directs output to either "true" or "false" path
- **force calculation** - Prevents caching and forces recalculation
- **force execution order** - Controls the sequence of node execution

These control flow nodes enable building more complex, dynamic workflows with decision-making capabilities based on runtime conditions.
    - Batch processing scenarios
    - When you need to apply the same operation to multiple inputs
    - When your operation needs to work with individual items separately

### 2. LIST datatype
- A Python list represented as a **single variable** in the workflow
- Treated as a self-contained object that can be passed between nodes
- Cannot directly connect to nodes that expect individual items
- Best for:
  - Working with collections of data as a single unit
  - Storing intermediate results that need to be processed as a whole
  - Passing collections between different parts of your workflow
  - Complex data storage that shouldn't be split apart

### 3. SET datatype
- A Python set represented as a **single variable** in the workflow
- Stores unique values with no duplicates
- Supports mathematical set operations (union, intersection, etc.)
- Best for:
  - Eliminating duplicate values
  - Testing membership efficiently
  - Set operations (union, difference, etc.)
  - When element order doesn't matter

### When to use which type
- Use **data list** when you need to:
    - Process each item individually through ComfyUI nodes
    - Allow nodes to iterate through your items automatically
    - Connect to nodes that expect individual inputs
    - Perform batch processing operations
    -
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
