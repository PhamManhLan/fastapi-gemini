import chromadb
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer('keepitreal/vietnamese-sbert')

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="hue_knowledge")

def load_knowledge_if_empty():
    if collection.count() == 0:
        with open("data/hue_knowledge.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        chunks = [line.strip() for line in lines if line.strip()]
        embeddings = model.encode(chunks).tolist()
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        collection.add(
            embeddings=embeddings,
            documents=chunks,
            ids=ids
        )
        print("Loaded knowledge into Chroma")

# load_knowledge_if_empty()  # gọi khi start app