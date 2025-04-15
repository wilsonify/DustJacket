"""
tests for normalize_author_names_difflib.py
"""
import pytest

from normalization_author.normalize_author_names_difflib import (
    normalize_name,
    get_similarity,
    group_similar_names
)


# --- Tests for normalize_name ---

@pytest.mark.parametrize("input_name, expected", [
    ("Rowling, J.K.", "rowling jk"),
    ("J.K. Rowling", "jk rowling"),
    ("Joanne Rowling", "joanne rowling"),
    ("Rowling ,   J.K.  ", "rowling jk"),
    ("Tolkien, J. R. R.", "tolkien j r r"),
    ("Isaac Asimov", "isaac asimov"),
    ("asimov, isaac", "asimov isaac"),
])
def test_normalize_name(input_name, expected):
    assert normalize_name(input_name) == expected


# --- Tests for get_similarity ---

@pytest.mark.parametrize("name1, name2, expected_min_score", [
    ("jk rowling", "joanne rowling", 0.7),
    ("isaac asimov", "isaac asimov", 1.0),
    ("george orwell", "orwell george", 0.4),  # directionally reversed
    ("tolkien", "j r r tolkien", 0.5),
])
def test_get_similarity(name1, name2, expected_min_score):
    score = get_similarity(name1, name2)
    assert score >= expected_min_score


# --- Tests for group_similar_names ---

def test_group_similar_names():
    names = [
        "jk rowling",
        "jo rowling",
        "isaac asimov",
        "george orwell",
        "george Orwelll",
        "isaac aasimov"
    ]
    groups = group_similar_names(names, threshold=0.75)

    # Flatten to lookup form: which group is each name in?
    name_to_group = {}
    for group in groups:
        for name in group:
            name_to_group[name] = group[0]

    assert name_to_group["jk rowling"] == name_to_group["jo rowling"]
    assert name_to_group["george orwell"] == name_to_group["george Orwelll"]
    assert name_to_group["isaac asimov"] == name_to_group["isaac aasimov"]
