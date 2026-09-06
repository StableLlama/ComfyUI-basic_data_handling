from inspect import cleandoc
import datetime
import time

try:
    from comfy.comfy_types.node_typing import IO, ComfyNodeABC
except ImportError:
    # Define dummy classes if comfy is not available
    class IO:
        BOOLEAN = "BOOLEAN"
        INT = "INT"
        FLOAT = "FLOAT"
        STRING = "STRING"
        NUMBER = "FLOAT,INT"
        ANY = "*"
    ComfyNodeABC = object

# Add custom IO types for DATETIME and TIMEDELTA
IO.DATETIME = "DATETIME"
IO.TIMEDELTA = "TIMEDELTA"


class TimeNow(ComfyNodeABC):
    """
    Returns the current time and date as a DATETIME object.
    Note: Output changes for every run, providing a fresh timestamp each time.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "trigger": (IO.ANY, {"tooltip": "Optional input to trigger a fresh evaluation."})
            }
        }

    RETURN_TYPES = (IO.DATETIME,)
    RETURN_NAMES = ("now",)
    OUTPUT_TOOLTIPS = ("The current local date and time; a new value every run.",)
    CATEGORY = "Basic/time"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_now"

    @classmethod
    def IS_CHANGED(s, **kwargs):
        # Always return a changing value to indicate the output changes every run
        return time.time()

    def get_now(self, trigger=None) -> tuple[datetime.datetime]:
        """
        Retrieves the current system time.
        The optional trigger input can be used to trigger execution.
        """
        return (datetime.datetime.now(),)


class TimeNowUTC(ComfyNodeABC):
    """
    Returns the current time and date as a DATETIME object, in the UTC timezone.
    Note: Output changes for every run, providing a fresh timestamp each time.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "trigger": (IO.ANY, {"tooltip": "Optional input to trigger a fresh evaluation."})
            }
        }

    RETURN_TYPES = (IO.DATETIME,)
    RETURN_NAMES = ("now",)
    OUTPUT_TOOLTIPS = ("The current UTC date and time (timezone-aware); a new value every run.",)
    CATEGORY = "Basic/time"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_now_utc"

    @classmethod
    def IS_CHANGED(s, **kwargs):
        # Always return a changing value to indicate the output changes every run
        return time.time()

    def get_now_utc(self, trigger=None) -> tuple[datetime.datetime]:
        """
        Retrieves the current system time in the UTC timezone.
        The optional trigger input can be used to trigger execution.
        """
        return (datetime.datetime.now(datetime.timezone.utc),)


class TimeToUnix(ComfyNodeABC):
    """
    Converts a DATETIME object to a Unix timestamp (a float representing seconds since the epoch).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "datetime": (IO.DATETIME, {"tooltip": "The DATETIME to convert."}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    RETURN_NAMES = ("unix_timestamp",)
    OUTPUT_TOOLTIPS = ("Seconds since the Unix epoch (1970-01-01 UTC).",)
    CATEGORY = "Basic/time"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "to_unix"

    def to_unix(self, datetime: datetime.datetime) -> tuple[float]:
        """
        Converts the given datetime object to a Unix timestamp.
        """
        return (datetime.timestamp(),)


class UnixToTime(ComfyNodeABC):
    """
    Converts a Unix timestamp (float or int) to a DATETIME object.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "unix_timestamp": (IO.NUMBER, {"default": 0.0, "tooltip": "Seconds since the Unix epoch (float or int)."}),
            }
        }

    RETURN_TYPES = (IO.DATETIME,)
    RETURN_NAMES = ("datetime",)
    OUTPUT_TOOLTIPS = ("The DATETIME corresponding to the timestamp, in the local timezone.",)
    CATEGORY = "Basic/time"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "from_unix"

    def from_unix(self, unix_timestamp: float) -> tuple[datetime.datetime]:
        """
        Creates a datetime object from a Unix timestamp.
        """
        return (datetime.datetime.fromtimestamp(unix_timestamp),)


class TimeFormat(ComfyNodeABC):
    """
    Formats a DATETIME object into a string using a specified format code.
    Common format codes: %Y (year), %m (month), %d (day), %H (hour), %M (minute), %S (second).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "datetime": (IO.DATETIME, {"tooltip": "The DATETIME to format."}),
                "format_string": (IO.STRING, {"default": "%Y-%m-%d %H:%M:%S", "tooltip": "strftime format code, e.g. %Y-%m-%d %H:%M:%S."}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("formatted_string",)
    OUTPUT_TOOLTIPS = ("The DATETIME rendered as a string using the format code.",)
    CATEGORY = "Basic/time"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "format_time"

    def format_time(self, datetime: datetime.datetime, format_string: str) -> tuple[str]:
        """
        Formats a datetime object into a string.
        """
        return (datetime.strftime(format_string),)


class TimeParse(ComfyNodeABC):
    """
    Parses a string containing a date and time into a DATETIME object, using a specified format code.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "time_string": (IO.STRING, {"tooltip": "The date/time string to parse."}),
                "format_string": (IO.STRING, {"default": "%Y-%m-%d %H:%M:%S", "tooltip": "strptime format code matching the input string, e.g. %Y-%m-%d %H:%M:%S."}),
            }
        }

    RETURN_TYPES = (IO.DATETIME,)
    RETURN_NAMES = ("datetime",)
    OUTPUT_TOOLTIPS = ("The parsed DATETIME.",)
    CATEGORY = "Basic/time"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "parse_time"

    def parse_time(self, time_string: str, format_string: str) -> tuple[datetime.datetime]:
        """
        Parses a string into a datetime object.
        """
        return (datetime.datetime.strptime(time_string, format_string),)


class TimeDelta(ComfyNodeABC):
    """
    Creates a TIMEDELTA object, which represents a duration and can be used for date calculations.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "days": (IO.FLOAT, {"default": 0, "tooltip": "Number of days."}),
                "seconds": (IO.FLOAT, {"default": 0, "tooltip": "Number of seconds."}),
                "microseconds": (IO.FLOAT, {"default": 0, "tooltip": "Number of microseconds."}),
                "milliseconds": (IO.FLOAT, {"default": 0, "tooltip": "Number of milliseconds."}),
                "minutes": (IO.FLOAT, {"default": 0, "tooltip": "Number of minutes."}),
                "hours": (IO.FLOAT, {"default": 0, "tooltip": "Number of hours."}),
                "weeks": (IO.FLOAT, {"default": 0, "tooltip": "Number of weeks."}),
            }
        }

    RETURN_TYPES = (IO.TIMEDELTA,)
    RETURN_NAMES = ("delta",)
    OUTPUT_TOOLTIPS = ("A TIMEDELTA representing the combined duration.",)
    CATEGORY = "Basic/time"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_delta"

    def create_delta(self, **kwargs: float) -> tuple[datetime.timedelta]:
        """
        Creates a timedelta object from the given durations.
        """
        return (datetime.timedelta(**kwargs),)


class TimeAddDelta(ComfyNodeABC):
    """
    Adds a TIMEDELTA (duration) to a DATETIME object, resulting in a new DATETIME.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "datetime": (IO.DATETIME, {"tooltip": "The DATETIME to add the duration to."}),
                "delta": (IO.TIMEDELTA, {"tooltip": "The duration (TIMEDELTA) to add."}),
            }
        }

    RETURN_TYPES = (IO.DATETIME,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("The DATETIME advanced by the given duration.",)
    CATEGORY = "Basic/time"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "add"

    def add(self, datetime: datetime.datetime, delta: datetime.timedelta) -> tuple[datetime.datetime]:
        """
        Adds a timedelta to a datetime object.
        """
        return (datetime + delta,)


class TimeSubtractDelta(ComfyNodeABC):
    """
    Subtracts a TIMEDELTA (duration) from a DATETIME object, resulting in a new DATETIME.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "datetime": (IO.DATETIME, {"tooltip": "The DATETIME to subtract the duration from."}),
                "delta": (IO.TIMEDELTA, {"tooltip": "The duration (TIMEDELTA) to subtract."}),
            }
        }

    RETURN_TYPES = (IO.DATETIME,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("The DATETIME moved back by the given duration.",)
    CATEGORY = "Basic/time"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "subtract"

    def subtract(self, datetime: datetime.datetime, delta: datetime.timedelta) -> tuple[datetime.datetime]:
        """
        Subtracts a timedelta from a datetime object.
        """
        return (datetime - delta,)


class TimeDifference(ComfyNodeABC):
    """
    Calculates the difference between two DATETIME objects, returning a TIMEDELTA object.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "datetime1": (IO.DATETIME, {"tooltip": "First date/time (the minuend)."}),
                "datetime2": (IO.DATETIME, {"tooltip": "Second date/time, subtracted from the first."}),
            }
        }

    RETURN_TYPES = (IO.TIMEDELTA,)
    RETURN_NAMES = ("delta",)
    OUTPUT_TOOLTIPS = ("The duration datetime1 - datetime2 (negative when datetime1 is earlier).",)
    CATEGORY = "Basic/time"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "difference"

    def difference(self, datetime1: datetime.datetime, datetime2: datetime.datetime) -> tuple[datetime.timedelta]:
        """
        Calculates the duration between two datetime objects.
        """
        return (datetime1 - datetime2,)


class TimeExtract(ComfyNodeABC):
    """
    Extracts individual components (year, month, day, hour, etc.) from a DATETIME object.
    Weekday is returned as an integer, where Monday is 0 and Sunday is 6.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { "datetime": (IO.DATETIME, {"tooltip": "The DATETIME to decompose."}) }
        }

    RETURN_TYPES = (IO.INT, IO.INT, IO.INT, IO.INT, IO.INT, IO.INT, IO.INT, IO.INT)
    RETURN_NAMES = ("year", "month", "day", "hour", "minute", "second", "microsecond", "weekday")
    OUTPUT_TOOLTIPS = ("Year.", "Month (1-12).", "Day of the month.", "Hour (0-23).", "Minute (0-59).", "Second (0-59).", "Microsecond.", "Weekday (Monday = 0 .. Sunday = 6).")
    CATEGORY = "Basic/time"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "extract"

    def extract(self, datetime: datetime.datetime) -> tuple[int, int, int, int, int, int, int, int]:
        """
        Extracts all time components from a datetime object.
        """
        return (datetime.year, datetime.month, datetime.day, datetime.hour,
                datetime.minute, datetime.second, datetime.microsecond, datetime.weekday())


class TimeDeltaToSeconds(ComfyNodeABC):
    """
    Converts a TIMEDELTA object to a float representing its duration in seconds.
    A value of 1.0 corresponds to a time delta of one second.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "delta": (IO.TIMEDELTA, {"tooltip": "The duration to convert."}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    RETURN_NAMES = ("seconds",)
    OUTPUT_TOOLTIPS = ("The duration expressed as a float in seconds.",)
    CATEGORY = "Basic/time"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "to_seconds"

    def to_seconds(self, delta: datetime.timedelta) -> tuple[float]:
        """
        Converts a timedelta to a float value representing seconds.
        """
        return (delta.total_seconds(),)


class TimeDeltaToMilliseconds(ComfyNodeABC):
    """
    Converts a TIMEDELTA object to an integer representing its duration in milliseconds.
    A value of 1 corresponds to a time delta of one millisecond, rounded to the nearest millisecond.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "delta": (IO.TIMEDELTA, {"tooltip": "The duration to convert."}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    RETURN_NAMES = ("milliseconds",)
    OUTPUT_TOOLTIPS = ("The duration expressed as an integer number of milliseconds, rounded to the nearest millisecond.",)
    CATEGORY = "Basic/time"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "to_milliseconds"

    def to_milliseconds(self, delta: datetime.timedelta) -> tuple[int]:
        """
        Converts a timedelta to an integer value representing milliseconds,
        rounded to the nearest millisecond.
        """
        return (round(delta.total_seconds() * 1000),)


NODE_CLASS_MAPPINGS = {
    "Basic data handling: TimeNow": TimeNow,
    "Basic data handling: TimeNowUTC": TimeNowUTC,
    "Basic data handling: TimeToUnix": TimeToUnix,
    "Basic data handling: UnixToTime": UnixToTime,
    "Basic data handling: TimeFormat": TimeFormat,
    "Basic data handling: TimeParse": TimeParse,
    "Basic data handling: TimeDelta": TimeDelta,
    "Basic data handling: TimeAddDelta": TimeAddDelta,
    "Basic data handling: TimeSubtractDelta": TimeSubtractDelta,
    "Basic data handling: TimeDifference": TimeDifference,
    "Basic data handling: TimeExtract": TimeExtract,
    "Basic data handling: TimeDeltaToSeconds": TimeDeltaToSeconds,
    "Basic data handling: TimeDeltaToMilliseconds": TimeDeltaToMilliseconds,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: TimeNow": "Time Now",
    "Basic data handling: TimeNowUTC": "Time Now (UTC)",
    "Basic data handling: TimeToUnix": "Time to Unix Timestamp",
    "Basic data handling: UnixToTime": "Unix Timestamp to Time",
    "Basic data handling: TimeFormat": "Format Time String",
    "Basic data handling: TimeParse": "Parse Time String",
    "Basic data handling: TimeDelta": "Create Time Delta",
    "Basic data handling: TimeAddDelta": "Add Time Delta",
    "Basic data handling: TimeSubtractDelta": "Subtract Time Delta",
    "Basic data handling: TimeDifference": "Time Difference",
    "Basic data handling: TimeExtract": "Extract Time Components",
    "Basic data handling: TimeDeltaToSeconds": "Time Delta to Seconds",
    "Basic data handling: TimeDeltaToMilliseconds": "Time Delta to Milliseconds",
}
