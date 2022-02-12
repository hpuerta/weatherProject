class TextHelper():
    @staticmethod
    def getCloudinessText(percentage:float) -> str:
        if percentage == 0: return "Sky clear"
        elif 0 < percentage < 31.25: return "Few clouds"
        elif 31.25 <= percentage < 56.25: return "Scattered clouds"
        elif 56.25 <= percentage < 100: return "Broken clouds"
        else: return "Overcast"