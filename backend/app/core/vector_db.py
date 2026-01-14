import os
import torch
from typing import List

import chromadb
from langchain_community.document_loaders import (
    TextLoader,
    DirectoryLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

device = "cuda" if torch.cuda.is_available() else "cpu" #check máy có gpu không

embedding_model = HuggingFaceEmbeddings(
    model_name="keepitreal/vietnamese-sbert",
    model_kwargs={"device": device},          # cuda = gpu, cpu = cpu
    encode_kwargs={"normalize_embeddings": True}
)

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "hue_knowledge"

def load_and_split_documents(
    data_dir: str = "data",
    chunk_size: int = 600,
    chunk_overlap: int = 120
) -> List[Document]:
    """
    Load tất cả file .txt trong thư mục data/ và chia nhỏ thành chunks
    """
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Thư mục {data_dir} không tồn tại")

    loader = DirectoryLoader(
        data_dir,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    raw_documents = loader.load()

    if not raw_documents:
        print("[VectorDB] Không tìm thấy file .txt nào để load")
        return []

    print(f"[VectorDB] Đã load {len(raw_documents)} file")

    # Chia nhỏ văn bản
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],  # ưu tiên chia theo đoạn, câu
        add_start_index=True
    )

    chunks = text_splitter.split_documents(raw_documents)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
    print(f"[VectorDB] Đã chia thành {len(chunks)} chunks")
    return chunks


def get_or_create_vectorstore(force_reload: bool = False) -> Chroma:
    """
    Tạo hoặc lấy Chroma vectorstore.
    Nếu force_reload=True → xóa và tạo lại.
    """
    if force_reload and os.path.exists(CHROMA_PATH):
        import shutil
        shutil.rmtree(CHROMA_PATH)
        print("[VectorDB] Đã xóa Chroma cũ để reload")

    # Kiểm tra xem đã có collection chưa
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    existing_collections = client.list_collections()
    collection_names = [c.name for c in existing_collections]

    if COLLECTION_NAME in collection_names and not force_reload:
        print(f"[VectorDB] Collection '{COLLECTION_NAME}' đã tồn tại → load lại")
        vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embedding_model,
            persist_directory=CHROMA_PATH
        )
        print(f"[VectorDB] Đã load {vectorstore._collection.count()} documents")
        return vectorstore

    # Load và chia tài liệu
    chunks = load_and_split_documents()

    if not chunks:
        raise ValueError("Không có dữ liệu nào để đưa vào vectorstore")

    # Tạo mới vectorstore
    print("[VectorDB] Đang tạo vectorstore mới từ chunks...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH
    )

    print(f"[VectorDB] Đã lưu thành công {len(chunks)} chunks vào Chroma")
    return vectorstore


_vectorstore = None
_retriever = None


def get_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = get_or_create_vectorstore(force_reload=False)
    return _vectorstore


def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = get_vectorstore().as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
    return _retriever