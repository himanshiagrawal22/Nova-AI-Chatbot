# ----------------------------------------
# Split text into overlapping chunks
# ----------------------------------------

def create_chunks(text, chunk_size=1000, overlap=200):
    """
    Splits extracted PDF text into overlapping chunks.

    Args:
        text (str): Extracted PDF text.
        chunk_size (int): Size of each chunk.
        overlap (int): Number of overlapping characters.

    Returns:
        list: List of text chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += (chunk_size - overlap)

    return chunks