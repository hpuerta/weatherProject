from datetime import datetime
from zoneinfo import ZoneInfo
class DateFormatting():
    '''This class deliver static methods to format dates
    '''
    @staticmethod
    def fromTimestampToLocalDateTime(timestamp:int,timezone:str)->str:
        '''This function gets the unix timepestamp and timezone, 
        to return the local date and time formatted
        '''
        return datetime.fromtimestamp(timestamp).astimezone(ZoneInfo(timezone)).strftime("%Y-%m-%d %H:%M:%S")
    @staticmethod
    def fromTimestampToLocalTime(timestamp:int,timezone:str)->str:
        '''This function gets the unix timepestamp and timezone, 
        to return the local time formatted
        '''
        return datetime.fromtimestamp(timestamp).astimezone(ZoneInfo(timezone)).strftime("%H:%M:%S")
