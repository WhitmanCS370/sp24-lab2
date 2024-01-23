class Any:
    def __init__(self, rest=None):
        self.rest = rest

    def match(self, text, start=0):
        if self.rest is None:
            return True
        for i in range(start, len(text)):
            if self.rest.match(text, i):
                return True
        return False

#len(text + 1 is because Any (*) could potentially look at the next character in the literal, taking up one or more spaces in the string so len(text+1) captures that addition