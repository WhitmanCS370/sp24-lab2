# [parent]
class Match:
    def __init__(self, rest):
        self.rest = rest if rest is not None else Null()

    def match(self, text):
        result = self._match(text, 0)
        return result == len(text)
# [/parent]

# [null]
class Null(Match):
    def __init__(self):
        self.rest = None

    def _match(self, text, start):
        return start
# [/null]

# [any]
class Any(Match):
    def __init__(self, rest=None):
        super().__init__(rest)

    def _match(self, text, start):
        # We need the plus one here because we want to match at least one character.
        # If we didn't, then we would match the empty string, which is not what we want.
        for i in range(start, len(text) + 1):
            end = self.rest._match(text, i)
            if end == len(text):
                return end
        return None
# [/any]

# [either]
class Either(Match):
    def __init__(self, left, right, rest=None):
        super().__init__(rest)
        self.left = left
        self.right = right

    def _match(self, text, start):
        for pat in [self.left, self.right]:
            end = pat._match(text, start)
            if end is not None:
                end = self.rest._match(text, end)
                if end == len(text):
                    return end
        return None
# [/either]

# [lit]
class Lit(Match):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars

    def _match(self, text, start):
        end = start + len(self.chars)
        if text[start:end] != self.chars:
            return None
        return self.rest._match(text, end)
# [/lit]
    
# [AnyPlus]
class AnyPlus(Any):
    # should match for atleast one or more characters but not the empty string
    def __init__(self, rest=None):
        super().__init__(rest)

    def _match(self, text, start):
        if len(text) == 0:
            return None 
        # We need the plus one here because we want to match at least one character.
        # If we didn't, then we would match the empty string, which is not what we want.
        for i in range(start, len(text) + 1):
            end = self.rest._match(text, i)
            if end == len(text):
                return end
        return None
    
class Charset(Match):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars

    # checks that a character is in the set of characters
    def _match(self, text, start):
        end = start + 1
        if text[start:end] in self.chars:
            return self.rest._match(text, end)
        return None