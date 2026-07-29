from rag.pdf_loader import extract_text_from_pdf
from rag.chunker import create_chunks
from rag.embeddings import create_embedding
from rag.vector_store import create_index, search_index

from chatbot import stream_gemini

import numpy as np


# ----------------------------------------
# Build RAG Index
# ----------------------------------------
def build_rag(pdf_path):

    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        raise ValueError("The PDF contains no readable text.")

    chunks = create_chunks(text)

    embeddings = []

    for chunk in chunks:
        embeddings.append(create_embedding(chunk))

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    index = create_index(embeddings)

    return index, chunks


# ----------------------------------------
# Retrieve Relevant Context
# ----------------------------------------
def retrieve_context(question, index, chunks, k=5):

    query_embedding = create_embedding(question)

    query_embedding = np.array(
        [query_embedding],
        dtype=np.float32
    )

    _, indices = search_index(
        index,
        query_embedding,
        k
    )

    retrieved_chunks = []

    for i in indices[0]:

        if 0 <= i < len(chunks):
            retrieved_chunks.append(chunks[i])

    return "\n\n".join(retrieved_chunks)


# ----------------------------------------
# Ask Question
# ----------------------------------------
def ask_pdf(question, index, chunks):

    context = retrieve_context(
        question,
        index,
        chunks
    )

    prompt = f"""
You are Nova AI.

A document is currently loaded.

Below is the most relevant information retrieved from that document.

---------------- DOCUMENT ----------------

{context}

------------------------------------------

User Question:
{question}

Instructions:

1. If the document clearly contains the answer, answer using the document.

2. If the document does NOT contain the answer, answer using your own knowledge.

3. Never say:
"I couldn't find that information in the document."

4. If you answer from the document, don't mention the document unless the user asks.

5. If the question is general knowledge (for example AI, Python, DBMS, C++, Java, networking, operating systems, etc.), simply answer normally.

Answer:
"""

    answer = stream_gemini(prompt)

    return answer