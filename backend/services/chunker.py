from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..utils.token_counter import count_tokens

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=100,
    length_function=count_tokens,
    is_separator_regex=False,
)

def chunk_text(text: str) -> list[str]:
    # Split into 512-token chunks with 100-token overlap
    return _splitter.split_text(text)
