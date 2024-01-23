from glob_null import Any, Either, Lit, One, OneOrMore
from inspect import getmembers, isfunction
import sys

def test_literal_match_entire_string():
    # /abc/ matches "abc"
    assert Lit("abc").match("abc")

def test_literal_substring_alone_no_match():
    # /ab/ doesn't match "abc"
    assert not Lit("ab").match("abc")

def test_literal_superstring_no_match():
    # /abc/ doesn't match "ab"
    assert not Lit("abc").match("ab")

def test_any_matches_empty():
    # /*/ matches ""
    assert Any().match("")

def test_any_matches_entire_string():
    # /*/ matches "abc"
    assert Any().match("abc")

def test_any_matches_as_prefix():
    # /*def/ matches "abcdef"
    assert Any(Lit("def")).match("abcdef")

def test_any_matches_as_suffix():
    # /abc*/ matches "abcdef"
    assert Lit("abc", Any()).match("abcdef")

def test_any_matches_interior():
    # /a*c/ matches "abc"
    assert Lit("a", Any(Lit("c"))).match("abc")

def test_either_two_literals_first():
    # /{a,b}/ matches "a"
    assert Either(Lit("a"), Lit("b")).match("a")

def test_either_two_literals_second():
    # /{a,b}/ matches "b"
    assert Either(Lit("a"), Lit("b")).match("b")

def test_either_two_literals_neither():
    # /{a,b}/ doesn't match "c"
    assert not Either(Lit("a"), Lit("b")).match("c")

def test_either_two_literals_not_both():
    # /{a,b}/ doesn't match "ab"
    assert not Either(Lit("a"), Lit("b")).match("ab")

def test_either_after_any():
    # /*{x,y}/ matches "abcx"
    assert Any(Either(Lit("x"), Lit("y"))).match("abcx")

def test_either_leading_or_trailing():
    # /{*x,y*}/ matches "abx"
    # /{*x,y*}/ matches "yab"
    # /{*x,y*}/ matches "yabx"
    assert Either(Any(Lit("x")), Lit("y", Any())).match("abx")
    assert Either(Any(Lit("x")), Lit("y", Any())).match("yab")
    assert Either(Any(Lit("x")), Lit("y", Any())).match("yabx")

def test_match_one():
    assert One().match("x")
    assert not One().match("")
    assert not One().match("xxxx")
    assert One(Lit("x")).match("ax")
    assert not One(Lit("x")).match("x")
    
def test_match_one_or_more():
    assert OneOrMore().match("x")
    assert OneOrMore().match("xxxx")
    assert not OneOrMore().match("")
    assert OneOrMore(Lit("x")).match("ax")
    assert OneOrMore(Lit("x")).match("aaaax")    
    assert not OneOrMore(Lit("x")).match("x")
    

if __name__ == '__main__':
    for f in getmembers(sys.modules[__name__], isfunction):
        if f[0].startswith('test_'):
            f[1]()