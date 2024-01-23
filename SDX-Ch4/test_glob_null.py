from glob_null import Any, Either, Lit,Nonempty,Charset,Range
from inspect import getmembers

def test_any_matches_nonempty():
    # /*/ matches ""
    assert Nonempty().match("a")

def test_any_matches_nonempty_empty():
    # /*/ matches ""
    assert not Nonempty().match("")

def test_charset_match():
    # /abc/ matches "abc"
    assert Charset("abc").match("a")

def test_range_match():
    # /abc/ matches "abc"
    assert Range("a","e").match("d")

def test_range_no_match():
    # /abc/ matches "abc"
    assert not Range("a","e").match("g")

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
    assert Either([Lit("a"), Lit("b")]).match("a")

def test_either_two_literals_second():
    # /{a,b}/ matches "b"
    assert Either([Lit("a"), Lit("b")]).match("b")

def test_either_two_literals_neither():
    # /{a,b}/ doesn't match "c"
    assert not Either([Lit("a"), Lit("b")]).match("c")

def test_either_two_literals_not_both():
    # /{a,b}/ doesn't match "ab"
    assert not Either([Lit("a"), Lit("b")]).match("ab")

def test_either_after_any():
    # /*{x,y}/ matches "abcx"
    assert Any(Either([Lit("x"), Lit("y")])).match("abcx")

def test_either_leading_or_trailing():
    # /{*x,y*}/ matches "abx"
    # /{*x,y*}/ matches "yab"
    # /{*x,y*}/ matches "yabx"
    assert Either([Any(Lit("x")), Lit("y", Any())]).match("abx")
    assert Either([Any(Lit("x")), Lit("y", Any())]).match("yab")
    assert Either([Any(Lit("x")), Lit("y", Any())]).match("yabx")


test_any_matches_nonempty()
test_any_matches_nonempty_empty()
test_charset_match()
test_range_match()
test_range_no_match()
test_literal_match_entire_string()
test_literal_substring_alone_no_match()
test_literal_superstring_no_match()
test_any_matches_empty()
test_any_matches_entire_string()
test_any_matches_as_prefix()
test_any_matches_as_suffix()
test_any_matches_interior()
test_either_two_literals_first()
test_either_two_literals_second()
test_either_two_literals_neither()
test_either_two_literals_not_both()
test_either_after_any()
test_either_leading_or_trailing()
