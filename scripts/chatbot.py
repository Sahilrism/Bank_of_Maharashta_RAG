import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline


vector_db = "embeddings/faiss_index.bin"
text_path = "embeddings/texts.pkl"

print("Loading FAISS index and text chunks...")
index = faiss.read_index(vector_db)
with open(text_path, "rb") as f:
    texts = pickle.load(f)

print("Loading models...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
generator = pipeline("text2text-generation", model="google/flan-t5-base", device=-1)

print("\n Hello I am BOM ! A Chatbot for Bank of Maharashtra, ask me questions\n")

def retrieve_context(query, top_k=3):
    query_emb = embedder.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(query_emb, top_k)
    return [texts[i] for i in indices[0]]

def generate_answer(question, context):
    context = context[:1000]

    prompt = (
        f"You are a helpful banking assistant for Bank of Maharashtra.\n\n"
        f"Use the following information to answer accurately.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer in clear, concise English:"
    )

    result = generator(
        prompt, max_new_tokens=200, do_sample=False, truncation=True
    )[0]["generated_text"]

    return result.strip()


while True:
    question = input("Ask a question ==> ").strip()
    if question.lower() == "exit":
        print("Closing Chatbot. Goodbye!")
        break

    contexts = retrieve_context(question)

    if not contexts or len("".join(contexts).strip()) < 50:
        print("\n Sorry, I couldn’t find relevant information for that question.\n")
        continue

    combined_context = "\n\n".join(contexts)
    answer = generate_answer(question, combined_context)

    print(f"\n ===> {answer}\n")
