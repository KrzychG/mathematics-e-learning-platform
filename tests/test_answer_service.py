import pytest
from app.services.answer_service import answers_match, extract_choice_letter, resolve_choice_letter


@pytest.mark.parametrize('user_ans,correct_ans,opts,expected', [
    ('A', 'A', None, True),
    ('  b  ', 'B', None, True),
    ('(C)', 'c', None, True),
    ('A', '12', {"A": "12", "B": "14"}, True),
    ('0.5', 'A', {"A": "0.5", "B": "1.5"}, True),
    ('A', 'B', None, False),
    ('C', 'A', None, False),
])
def test_answers_matching(user_ans, correct_ans, opts, expected):
    assert answers_match(user_ans, correct_ans, options=opts) is expected


def test_invalid_and_empty_answers_rejected():
    assert answers_match("", "A") is False
    assert answers_match(None, "A") is False
    assert answers_match("A" * 300, "A") is False
    assert answers_match("niepoprawny_ciag_znakow", "A") is False


def test_choice_letter_extraction_and_resolution():
    assert extract_choice_letter(" A ") == "A"
    assert extract_choice_letter("(B)") == "B"
    assert extract_choice_letter("c.") == "C"
    assert extract_choice_letter("X") is None

    assert resolve_choice_letter("B", fallback="A") == "B"
    assert resolve_choice_letter("12", options={"A": "10", "B": "12"}, fallback="A") == "B"
    assert resolve_choice_letter(None, fallback="D") == "D"
