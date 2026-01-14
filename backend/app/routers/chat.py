from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.chat import MessageRequest, ChatResponse
from app.dependencies import get_current_user
from app.database.db import get_db
from app.models.chat_history import ChatHistory
from app.core.gemini import chain
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: MessageRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:
        # Gọi RAG chain (gồm: classify → retrieve → answer → (suggest tạm thời commnet) )
        reply = await chain.ainvoke({
            "question": request.content,
            "username": current_user.username
        })
    except ChatGoogleGenerativeAIError as e:
        print("[GEMINI ERROR]", e)
        reply = "Hiện hệ thống đang quá tải, bạn vui lòng thử lại sau khoảng 1 phút nhé "
    except Exception as e:
        import traceback
        print("[CHAIN FULL ERROR]".center(80, "="))
        print(traceback.format_exc())
        print("[END ERROR]".center(80, "="))
        reply = "Xin lỗi, hệ thống đang gặp sự cố. Thử lại sau nhé!"

    chat_entry = ChatHistory(
        user_id=current_user.id,
        question=request.content,
        answer=reply,
    )
    db.add(chat_entry)
    db.commit()

    return ChatResponse(reply=reply.strip())