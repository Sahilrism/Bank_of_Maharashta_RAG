import os
import json
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

RAW_DATA_PATH = "data/raw_data/combined_bom_data.json"
EMBEDDINGS_DIR = "embeddings"
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)


def chunk_text(text, chunk_size=300):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


def clean_text(text):
    text = text.replace("\n", " ").replace("\r", " ")
    text = " ".join(text.split())
    return text


def main():
    print("Loading combined BOM data...")
    with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_chunks = []
    for entry in data:
        content = clean_text(entry.get("content", ""))
        if content:
            chunks = chunk_text(content)
            all_chunks.extend(chunks)

    print(f"Total text chunks: {len(all_chunks)}")

    print("Generating embeddings...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(all_chunks, convert_to_numpy=True, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    print("Building FAISS index...")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, os.path.join(EMBEDDINGS_DIR, "faiss_index.bin"))
    with open(os.path.join(EMBEDDINGS_DIR, "texts.pkl"), "wb") as f:
        pickle.dump(all_chunks, f)

    print("FAISS index and text chunks saved!")


if __name__ == "__main__":
    main()
