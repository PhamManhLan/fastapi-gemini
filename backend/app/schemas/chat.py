from pydantic import BaseModel

class MessageRequest(BaseModel):
    content: str

class ChatResponse(BaseModel):
    reply: str