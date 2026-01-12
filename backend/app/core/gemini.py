# app/core/llm.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra="ignore"

settings = Settings()

# Khởi tạo LLM (Gemini) qua LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # hoặc gemini-1.5-pro, gemini-2.0-flash
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.7,
    max_output_tokens=600,
)

# Prompt template chuyên nghiệp cho chatbot du lịch Huế
prompt = ChatPromptTemplate.from_messages([
    ("system", """
Bạn là hướng dẫn viên du lịch chuyên nghiệp tại Thừa Thiên Huế, thân thiện, am hiểu sâu về lịch sử, văn hóa, ẩm thực và các địa điểm du lịch tại Huế.

**Quy tắc trả lời nghiêm ngặt:**
- Ưu tiên sử dụng thông tin từ phần "Context liên quan" bên dưới để trả lời chính xác nhất.
- Chỉ trả lời bằng tiếng Việt, ngắn gọn, hấp dẫn, tự nhiên như đang trò chuyện.
- Nếu là tin nhắn đầu tiên và có lời chào → trả lời: "Xin chào! Tôi là hướng dẫn viên du lịch Huế, rất sẵn lòng hỗ trợ bạn khám phá."
- Sau khi trả lời, gợi ý thêm một địa điểm/món ăn/sự kiện liên quan để khuyến khích du khách.
- Nếu hỏi về nơi khác ngoài Huế → "Tôi chỉ chuyên hỗ trợ du lịch Huế thôi ạ. Bạn muốn khám phá gì ở Huế nào?"

Context liên quan (Nguồn kiến thức chính từ RAG):
{context}

Hiện tại đang trò chuyện với: {username}
"""),
    ("human", "{question}")
])

# Tạo chain cơ bản (Prompt → LLM → Output parser)
chain = prompt | llm | StrOutputParser()