from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.chat import MessageRequest, ChatResponse
from app.dependencies import get_current_user
from app.database.db import get_db
from app.models.chat_history import ChatHistory
from app.core.vector_db import collection, model
from app.core.gemini import chain, settings


router = APIRouter(prefix="/chat", tags=["Chat"])

def retrieve_context(query: str, top_k: int = 4) -> str:
    query_emb = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k
    )
    return "\n".join(results['documents'][0]) if results['documents'] else ""

@router.post("/", response_model=ChatResponse)
async def chat(
    request: MessageRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # RAG: lấy context
    context_str = retrieve_context(request.content, top_k=4)

    try:
        # Gọi chain LangChain
        reply = await chain.ainvoke({
            "context": context_str,
            "question": request.content,
            "username": current_user.username  # truyền username vào prompt
        })
    except Exception as e:
        print(f"[LANGCHAIN ERROR] {e}")
        reply = "Xin lỗi, hệ thống đang gặp sự cố. Thử lại sau nhé!"

    # Lưu lịch sử chat
    chat_entry = ChatHistory(
        user_id=current_user.id,
        question=request.content,
        answer=reply,
        context=context_str
    )
    db.add(chat_entry)
    db.commit()

    return ChatResponse(reply=reply.strip())