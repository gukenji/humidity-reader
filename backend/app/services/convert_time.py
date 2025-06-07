from db.models import HumidityReading
from typing import List


def convert_reading_timezone(reading: HumidityReading, target_tz):
    reading.timestamp = reading.timestamp.astimezone(target_tz)
    return reading


def convert_list_timezone(readings: List[HumidityReading], target_tz):
    return [convert_reading_timezone(r, target_tz) for r in readings]
