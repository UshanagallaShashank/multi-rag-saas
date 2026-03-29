from backend.services.chunker import chunk_text

def test_short_text_is_single_chunk():
    # Text well below 512 tokens should not be split
    result = chunk_text("Hello world")
    assert len(result) == 1

def test_long_text_splits_into_multiple():
    # ~600 words should produce more than one chunk
    result = chunk_text("word " * 600)
    assert len(result) > 1

def test_chunks_preserve_content():
    # All words from original text must appear somewhere in chunks
    text = "The quick brown fox jumps over the lazy dog"
    joined = " ".join(chunk_text(text))
    assert "quick" in joined
    assert "lazy" in joined

def test_empty_text_returns_empty():
    assert chunk_text("") == []
