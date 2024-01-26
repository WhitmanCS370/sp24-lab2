import unittest

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

class Charset(Match):
    def __init__(self, charset, rest=None):
        super().__init__(rest)
        self.charset = set(charset)

    def _match(self, text, start):
        if start < len(text) and text[start] in self.charset:
            return start + 1
        else:
            return None
class Range(Match):
    def __init__(self, start, end, rest=None):
        super().__init__(rest)
        self.start = start
        self.end = end

    def _match(self, text, start):
        if start < len(text) and self.start <= text[start] <= self.end:
            return start + 1
        else:

            return None
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

# test cases
def test_one_or_more(self):
   matcher = OneOrMore(Charset('a'))
   self.assertEqual(matcher.match('aaa'), 3)
   self.assertEqual(matcher.match('baa'), None)
   self.assertEqual(matcher.match('aab'), 2)

def test_range(self):
   matcher = Range('a', 'z')
   self.assertEqual(matcher.match('a'), 1)
   self.assertEqual(matcher.match('z'), 1)
   self.assertEqual(matcher.match('m'), 1)
   self.assertEqual(matcher.match('A'), None)
   self.assertEqual(matcher.match('1'), None)

def test_charset(self):
    matcher = Charset('aeiou')
    self.assertEqual(matcher.match('a'), 1)
    self.assertEqual(matcher.match('e'), 1)
    self.assertEqual(matcher.match('i'), 1)
    self.assertEqual(matcher.match('o'), 1)
    self.assertEqual(matcher.match('u'), 1)
    self.assertEqual(matcher.match('b'), None)
    self.assertEqual(matcher.match('c'), None)

def test_either(self):
        matcher = Either([Lit('abc'), Lit('def')])
        self.assertEqual(matcher._match('abcdef', 0), None)
        self.assertEqual(matcher._match('abc', 0), 3)
        self.assertEqual(matcher._match('def', 0), 3)
