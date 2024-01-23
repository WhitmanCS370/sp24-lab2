# [parent]
from typing import Any


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
        for i in range(start, len(text) + 1):
            end = self.rest._match(text, i)
            if end == len(text):
                return end
        return None
# [/any]

class One(Match):
    def __init__(self, rest=None):
        super().__init__(rest)
        
    def _match(self, text, start):
        if start < len(text):
            return self.rest._match(text, start+1)
        return None
        
class OneOrMore(One):
    def __init__(self, rest=None):
        super().__init__(Any(rest))

# [either]
class Either(Match):
    def __init__(self, options, rest=None):
        super().__init__(rest)
        self.options = options

    def _match(self, text, start):
        for pat in self.options:
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

class Charset(Match):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars
        
    def _match(self, text, start):
        if start < len(text) and text[start] in self.chars:
            return self.rest._match(text, start+1)
        return None

class Range(Match):
    def __init__(self, first, last, rest=None):
        super().__init__(rest)
        self.first = first 
        self.last = last
        
    def _match(self, text, start):
        if start < len(text) and self.first <= text[start] <= self.last:
            return self.rest._match(text, start+1)
        return None