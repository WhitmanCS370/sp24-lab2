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

# [any
# The upper bound needs to be what it is, because if we stop at just
# len(text), then we won't actually be reaching the end of the text.
class Any(Match):
    def __init__(self, rest=None):
        super().__init__(rest)

    def _match(self, text, start):
        for i in range(start, len(text) + 1):
            end = self.rest._match(text, i)
            if end == len(text):
                return end
        return None
# [/any]

# [either]
class Either(Match):
    def __init__(self, patterns, rest=None):
        super().__init__(rest)
        self.patterns = patterns

    def _match(self, text, start):
        for pat in self.patterns:
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

# [nonempty]
class Nonempty(Match):
    def __init__(self, rest=None):
        super().__init__(rest)

    def _match(self, text, start):
        for i in range(start + 1, len(text) + 1):
            end = self.rest._match(text, i)
            if end == len(text):
                return end
        return None
# [/nonempty]
    
# [charset]
class Charset(Match):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars

    def _match(self, text, start):
        end = start + 1
        if text[start] not in self.chars:
            return None
        return self.rest._match(text, end)
# [/charset]
    
# [range]
class Range(Match):
    def __init__(self, startchar, endchar, rest=None):
        super().__init__(rest)
        self.startchar = startchar
        self.endchar = endchar

    def _match(self, text, start):
        end = start + 1
        if not (self.startchar <= text[start] <= self.endchar):
            return None
        return self.rest._match(text, end)
# [/range]
