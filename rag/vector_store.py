import faiss
import numpy as np


def create_index(embeddings):
    """
    Create a FAISS index from embedding vectors.
    """

    embeddings = embeddings.astype(np.float32)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def search_index(index, query_embedding, k=3):
    """
    Search the FAISS index for the top-k nearest vectors.
    """

    query_embedding = query_embedding.astype(np.float32)

    distances, indices = index.search(query_embedding, k)

    return distances, indices