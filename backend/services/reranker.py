from sentence_transformers import CrossEncoder

_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, chunks: list, top_k: int = 5) -> list:
    # Score all chunks against query, return top_k highest-scored
    if not chunks:
        return []
    pairs = [(query, c.content) for c in chunks]
    scores = _model.predict(pairs)
    ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)
    return [c for _, c in ranked[:top_k]]
