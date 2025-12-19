from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.chat import MessageRequest, ChatResponse
from app.core.gemini import get_gemini_response, SYSTEM_PROMPT
from app.dependencies import get_current_user
from app.database.db import get_db
from app.models.chat_history import ChatHistory
from app.core.vector_db import collection, model


router = APIRouter(prefix="/chat", tags=["Chat"])

def retrieve_context(query: str, top_k: int = 3) -> str:
    query_emb = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k
    )
    contexts = results['documents'][0]
    return "\n".join(contexts)

@router.post("/", response_model=ChatResponse)
async def chat(
    request: MessageRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    context = retrieve_context(request.content, top_k=4) #khi đã thêm context retrieve
    # context = ""  #chưa có vector DB

    # bổ sung pormpt kiểu rag sau.
    full_prompt = f"""{SYSTEM_PROMPT.format(context=context)}

    User: {request.content}
    Assistant:"""

    reply = get_gemini_response(full_prompt)

    # Lưu lịch sử chat
    chat_entry = ChatHistory(
        user_id=current_user.id,  # current_user là object User, có .id
        question=request.content,
        answer=reply,
        context=context
    )
    db.add(chat_entry)
    db.commit()
    
    return ChatResponse(reply=reply)
def retrieve_context(query: str, top_k: int = 3) -> str:
    query_emb = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k
    )
    contexts = results['documents'][0]
    return "\n".join(contexts)