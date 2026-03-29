from unittest.mock import MagicMock, patch

from backend.services.reranker import rerank

def _chunks(contents: list[str]) -> list:
    # Build mock chunk objects with .content attribute
    return [MagicMock(content=c) for c in contents]

def test_returns_top_k():
    chunks = _chunks(["cats", "dogs", "cars", "ships", "planes", "trains"])
    result = rerank("cats", chunks, top_k=3)
    assert len(result) == 3

def test_fewer_chunks_than_top_k():
    # Should return all available chunks, not raise
    result = rerank("query", _chunks(["only one"]), top_k=5)
    assert len(result) == 1

def test_empty_chunks_returns_empty():
    assert rerank("query", [], top_k=5) == []

def test_most_relevant_chunk_is_first():
    # The chunk with highest score must be index 0
    chunks = _chunks(["about cats and kittens", "about cars and trucks"])
    result = rerank("cats", chunks, top_k=2)
    assert "cats" in result[0].content
