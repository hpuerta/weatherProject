class TextHelper():
    @staticmethod
    def getCloudinessText(percentage:float) -> str:
        if percentage == 0: return "Sky clear"
        elif 0 < percentage < 31.25: return "Few clouds"
        elif 31.25 <= percentage < 56.25: return "Scattered clouds"
        elif 56.25 <= percentage < 100: return "Broken clouds"
        else: return "Overcast"

    @staticmethod
    def __getWindSpeed(speed:float) ->str:
        if speed < 0.5 : return 'Calm'
        elif 0.5 <= speed <=1.5: return 'Light air'
        elif 1.5 < speed <=3.3: return 'Light breeze'
        elif 3.3 < speed <=5.5: return 'Gentle breeze'
        elif 5.5 < speed <=7.9: return 'Moderate breeze'
        elif 7.9 < speed <=10.7: return 'Fresh breeze'
        elif 10.7 < speed <=13.8: return 'Strong breeze'
        elif 13.8 < speed <=17.1: return 'Moderate gale'
        elif 17.1 < speed <=20.7: return 'Fresh gale'
        elif 20.7 < speed <=24.4: return 'Strong gale'
        elif 24.4 < speed <=28.4: return 'Whole gale'
        elif 28.4 < speed <=32.6: return 'Storm'
        else: return "Hurricane"
    @staticmethod
    def __getWindDirection(degrees:float)->str:
        if degrees>348 or degrees<=11: return 'North'
        elif 11<degrees<=33: return 'North-Northeast'
        elif 33<degrees<=56: return 'Northeast'
        elif 56<degrees<=78: return 'East-Northeast'
        elif 78<degrees<=101: return 'East'
        elif 101<degrees<=123: return 'East-Southeast'
        elif 123<degrees<=146: return 'Southeast'
        elif 146<degrees<=168: return 'South-Southeast'
        elif 168<degrees<=191: return 'South'
        elif 191<degrees<=213: return 'South-Southwest'
        elif 213<degrees<=236: return 'Southwest'
        elif 236<degrees<=258: return 'West-Southwest'
        elif 258<degrees<=281: return 'West'
        elif 281<degrees<=303: return 'West-Northwest'
        elif 303<degrees<=326: return 'Northwest'
        elif 326<degrees<=348: return 'North-Northwest'
    
    @staticmethod
    def getWindText(speed:float,degrees:float) -> str:
        breeze = TextHelper.__getWindSpeed(speed)
        direction = TextHelper.__getWindDirection(degrees)
        return breeze + ", " + str(speed) + " m/s, " + direction