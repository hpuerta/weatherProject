from datetime import datetime
from zoneinfo import ZoneInfo
class DateFormatting():
    @staticmethod
    def fromTimestampToLocalDateTime(timestamp:int,timezone:str)->str:
        return datetime.fromtimestamp(timestamp).astimezone(ZoneInfo(timezone)).strftime("%Y-%m-%d %H:%M:%S")
    @staticmethod
    def fromTimestampToLocalTime(timestamp:int,timezone:str)->str:
        return datetime.fromtimestamp(timestamp).astimezone(ZoneInfo(timezone)).strftime("%H:%M:%S")
