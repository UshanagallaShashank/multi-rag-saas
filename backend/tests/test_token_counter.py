from backend.utils.token_counter import count_tokens, truncate_to_tokens

def test_count_returns_positive():
    assert count_tokens("hello world") > 0

def test_count_empty_is_zero():
    assert count_tokens("") == 0

def test_truncate_respects_limit():
    # Truncated result must not exceed max_tokens
    result = truncate_to_tokens("word " * 200, 10)
    assert count_tokens(result) <= 10

def test_truncate_no_op_within_limit():
    # Short text within limit should be returned unchanged
    assert truncate_to_tokens("hi there", 100) == "hi there"
