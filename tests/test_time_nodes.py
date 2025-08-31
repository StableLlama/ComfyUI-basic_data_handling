#import pytest

from datetime import datetime, timedelta
from ..src.basic_data_handling.time_nodes import (
    TimeNow,
    TimeToUnix,
    UnixToTime,
    TimeFormat,
    TimeParse,
    TimeDelta,
    TimeAddDelta,
    TimeSubtractDelta,
    TimeDifference,
    TimeExtract,
)

def test_time_now():
    node = TimeNow()
    result = node.get_now()
    assert isinstance(result, tuple)
    assert len(result) == 1
    assert isinstance(result[0], datetime)

    # Test with trigger parameter
    result_with_trigger = node.get_now(trigger="any value")
    assert isinstance(result_with_trigger, tuple)
    assert len(result_with_trigger) == 1
    assert isinstance(result_with_trigger[0], datetime)

def test_time_to_unix():
    node = TimeToUnix()
    test_datetime = datetime(2023, 1, 1, 12, 0, 0)
    result = node.to_unix(test_datetime)

    assert isinstance(result, tuple)
    assert len(result) == 1
    assert isinstance(result[0], float)
    # 2023-01-01 12:00:00 should convert to a specific timestamp
    expected_timestamp = test_datetime.timestamp()
    assert result[0] == expected_timestamp

def test_unix_to_time():
    node = UnixToTime()
    # Test with a specific timestamp (2023-01-01 12:00:00)
    test_timestamp = 1672574400.0  # This is 2023-01-01 12:00:00 in UTC
    result = node.from_unix(test_timestamp)

    assert isinstance(result, tuple)
    assert len(result) == 1
    assert isinstance(result[0], datetime)

    # The returned datetime will be in local timezone, so hours might differ
    # Just check that the date is correct and hours are reasonable
    returned_dt = result[0]
    assert returned_dt.year == 2023
    assert returned_dt.month == 1
    assert returned_dt.day == 1
    # Allow for timezone differences (typically within ±12 hours)
    assert 0 <= returned_dt.hour < 24
    assert returned_dt.minute == 0
    assert returned_dt.second == 0

def test_time_format():
    node = TimeFormat()
    test_datetime = datetime(2023, 1, 1, 12, 30, 45)

    # Test with default format
    result = node.format_time(test_datetime, "%Y-%m-%d %H:%M:%S")
    assert result == ("2023-01-01 12:30:45",)

    # Test with custom format
    result = node.format_time(test_datetime, "%d/%m/%Y")
    assert result == ("01/01/2023",)

    # Test with time-only format
    result = node.format_time(test_datetime, "%H:%M")
    assert result == ("12:30",)

def test_time_parse():
    node = TimeParse()

    # Test standard format
    result = node.parse_time("2023-01-01 12:30:45", "%Y-%m-%d %H:%M:%S")
    assert isinstance(result, tuple)
    assert len(result) == 1
    assert isinstance(result[0], datetime)
    assert result[0] == datetime(2023, 1, 1, 12, 30, 45)

    # Test custom format
    result = node.parse_time("01/01/2023", "%d/%m/%Y")
    assert result[0] == datetime(2023, 1, 1, 0, 0, 0)

    # Test time-only format
    result = node.parse_time("12:30", "%H:%M")
    parsed_datetime = result[0]
    assert parsed_datetime.hour == 12
    assert parsed_datetime.minute == 30

def test_time_delta():
    node = TimeDelta()

    # Test with days only
    result = node.create_delta(days=5)
    assert isinstance(result, tuple)
    assert len(result) == 1
    assert isinstance(result[0], timedelta)
    assert result[0].days == 5

    # Test with multiple parameters
    result = node.create_delta(days=1, hours=2, minutes=30)
    delta = result[0]
    # Convert to seconds for easier comparison
    total_seconds = delta.total_seconds()
    expected_seconds = 24*60*60 + 2*60*60 + 30*60  # 1 day, 2 hours, 30 minutes
    assert total_seconds == expected_seconds

    # Test with all parameters
    result = node.create_delta(
        days=1,
        seconds=30,
        microseconds=500,
        milliseconds=100,
        minutes=5,
        hours=2,
        weeks=1
    )
    delta = result[0]
    # A week plus a day
    assert delta.days == 8
    # Convert the remainder to seconds for comparison
    remainder_seconds = delta.seconds
    expected_remainder = 2*60*60 + 5*60 + 30 + 0.1  # 2 hours, 5 minutes, 30 seconds, 100 milliseconds
    assert abs(remainder_seconds - expected_remainder) < 1
    assert delta.microseconds == 100500

def test_time_add_delta():
    node = TimeAddDelta()
    test_datetime = datetime(2023, 1, 1, 12, 0, 0)
    test_delta = timedelta(days=1, hours=2, minutes=30)

    result = node.add(test_datetime, test_delta)
    assert isinstance(result, tuple)
    assert len(result) == 1
    assert isinstance(result[0], datetime)

    expected_datetime = datetime(2023, 1, 2, 14, 30, 0)  # 1 day, 2 hours, 30 minutes later
    assert result[0] == expected_datetime

def test_time_subtract_delta():
    node = TimeSubtractDelta()
    test_datetime = datetime(2023, 1, 2, 14, 30, 0)
    test_delta = timedelta(days=1, hours=2, minutes=30)

    result = node.subtract(test_datetime, test_delta)
    assert isinstance(result, tuple)
    assert len(result) == 1
    assert isinstance(result[0], datetime)

    expected_datetime = datetime(2023, 1, 1, 12, 0, 0)  # 1 day, 2 hours, 30 minutes earlier
    assert result[0] == expected_datetime

def test_time_difference():
    node = TimeDifference()
    datetime1 = datetime(2023, 1, 2, 14, 30, 0)
    datetime2 = datetime(2023, 1, 1, 12, 0, 0)

    result = node.difference(datetime1, datetime2)
    assert isinstance(result, tuple)
    assert len(result) == 1
    assert isinstance(result[0], timedelta)

    expected_delta = timedelta(days=1, hours=2, minutes=30)
    assert result[0] == expected_delta

    # Test reverse order (should give negative timedelta)
    result = node.difference(datetime2, datetime1)
    assert result[0] == -expected_delta

def test_time_extract():
    node = TimeExtract()
    test_datetime = datetime(2023, 1, 2, 14, 30, 45, 123456)

    result = node.extract(test_datetime)
    assert isinstance(result, tuple)
    assert len(result) == 8

    year, month, day, hour, minute, second, microsecond, weekday = result

    assert year == 2023
    assert month == 1
    assert day == 2
    assert hour == 14
    assert minute == 30
    assert second == 45
    assert microsecond == 123456
    # January 2, 2023 was a Monday (weekday 0)
    assert weekday == 0
