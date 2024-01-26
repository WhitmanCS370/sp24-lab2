# [parent]
class Match:
    def __init__(self, rest):
        self.rest = rest if rest is not None else Null()

    def match(self, text):
        result = self._match(text, 0)
        return result == len(text)
# [/parent]

class OneOrMore(Match):
    def __init__(self, rest=None):
        super().__init__(rest)

    def _match(self, text, start):
        end = start
        while True:
            next_end = self.rest._match(text, end)
            if next_end is None: # we need at least one match
                break
            end = next_end
        return end if end > start else None

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

# Why does the upper bound of the loop in the final version of Any run to len(text) + 1?
#  A: in order to include the last character of the string in the text to be matched.

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
