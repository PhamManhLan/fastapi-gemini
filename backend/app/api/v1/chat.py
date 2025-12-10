from fastapi import APIRouter, Depends
from ...schemas.chat import MessageRequest, ChatResponse
from ...core.gemini import get_gemini_response
from ...dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
async def chat(
    request: MessageRequest,
    current_user=Depends(get_current_user)
):
    reply = await get_gemini_response(request.content)
    return ChatResponse(reply=reply)