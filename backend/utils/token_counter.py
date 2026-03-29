import tiktoken

_enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    # Count tokens in text using cl100k_base encoding
    return len(_enc.encode(text))

def truncate_to_tokens(text: str, max_tokens: int) -> str:
    # Truncate text to at most max_tokens tokens
    tokens = _enc.encode(text)
    return _enc.decode(tokens[:max_tokens])
