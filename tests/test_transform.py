import pytest
from app.transform import mirror_word

def test_foobar25_example():
    """The exact test case from the requirements"""
    assert mirror_word("fOoBar25") == "52RAbOoF"

def test_lowercase_word():
    """All lowercase should become uppercase reversed"""
    assert mirror_word("hello") == "OLLEH"

def test_uppercase_word():
    """All uppercase should become lowercase reversed"""
    assert mirror_word("WORLD") == "dlrow"

def test_mixed_case():
    """Mix of upper and lower"""
    # TeSt -> tEsT (case flip) -> TsEt (reverse)
    assert mirror_word("TeSt") == "TsEt"

def test_with_numbers():
    """Numbers stay as-is, just get reversed"""
    assert mirror_word("abc123") == "321CBA"

def test_with_special_chars():
    """Special characters don't change case, just reverse"""
    assert mirror_word("test@123") == "321@TSET"

def test_empty_string():
    """Edge case: empty string"""
    assert mirror_word("") == ""

def test_single_char():
    """Edge case: single character"""
    assert mirror_word("a") == "A"
    assert mirror_word("Z") == "z"
