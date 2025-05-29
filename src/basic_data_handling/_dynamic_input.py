class ContainsDynamicDict(dict):
    """
    A custom dictionary that dynamically returns values for keys based on a pattern.
    - If a key in the passed dictionary has a value with `{"_dynamic": "number"}` in the tuple's second position,
      then any other key starting with the same string and ending with a number will return that value.
    - For other keys, normal dictionary lookup behavior applies.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store prefixes associated with `_dynamic` values for efficient lookup
        self._dynamic_prefixes = {
            key.rstrip("0123456789"): value
            for key, value in self.items()
            if isinstance(value, tuple) and len(value) > 1 and value[1].get("_dynamic") == "number"
        }

    def __contains__(self, key):
        # Check if key matches a dynamically handled prefix or exists normally
        return (
            any(key.startswith(prefix) and key[len(prefix):].isdigit() for prefix in self._dynamic_prefixes)
            or super().__contains__(key)
        )

    def __getitem__(self, key):
        # Dynamically return the value for keys matching a `prefix<number>` pattern
        for prefix, value in self._dynamic_prefixes.items():
            if key.startswith(prefix) and key[len(prefix):].isdigit():
                return value
        # Fallback to normal dictionary behavior for other keys
        return super().__getitem__(key)
