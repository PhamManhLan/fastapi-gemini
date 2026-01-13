# app/core/llm.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic_settings import BaseSettings
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda, RunnableBranch
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from app.core.vector_db import collection, model

class Settings(BaseSettings):
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra="ignore"

settings = Settings()

# Khởi tạo LLM (Gemini) qua LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.7,
    max_output_tokens=600,
)

classification_prompt = ChatPromptTemplate.from_template(
    """Phân loại nhanh câu hỏi sau có liên quan đến du lịch, văn hóa, ẩm thực, lịch sử, địa điểm tại Thừa Thiên Huế không?

Câu hỏi: {question}

Chỉ trả về đúng 1 từ: YES hoặc NO
Không giải thích gì thêm."""
)
main_prompt = ChatPromptTemplate.from_messages([
    ("system", """
Bạn là hướng dẫn viên du lịch chuyên nghiệp tại Thừa Thiên Huế, thân thiện, nhiệt tình, am hiểu sâu về lịch sử, văn hóa, ẩm thực và các địa điểm.

**Quy tắc trả lời nghiêm ngặt:**
- Ưu tiên và chỉ sử dụng thông tin từ phần "Context liên quan" để trả lời chính xác, tránh bịa đặt.
- Trả lời bằng tiếng Việt, ngắn gọn (3–8 câu), tự nhiên, gần gũi như đang trò chuyện.
- Nếu không có thông tin phù hợp trong context → trả lời trung thực: "Hiện tại mình chưa có thông tin chi tiết về phần này ạ..."
- KHÔNG tự gợi ý thêm ở đây (gợi ý sẽ được thêm riêng ở bước sau).
- Giữ giọng điệu vui vẻ, chào đón du khách.

Context liên quan (Nguồn kiến thức chính từ RAG):
{context}

Hiện tại đang trò chuyện với: {username}
    """),
    ("human", "{question}")
])
suggestion_prompt = ChatPromptTemplate.from_messages([
    ("system", """
Dựa trên câu hỏi của du khách: "{question}"

Hãy gợi ý NGẮN GỌN (1–2 câu) **một** địa điểm, món ăn, hoạt động, hoặc trải nghiệm liên quan tại Huế để họ khám phá thêm.
Ví dụ:
- Hỏi về lăng tẩm → gợi ý ăn cơm hến hoặc chùa Thiên Mụ gần đó
- Hỏi về ẩm thực → gợi ý chợ Đông Ba hoặc quán bún bò Huế nổi tiếng

Chỉ trả về nội dung gợi ý, không nói thêm gì khác (không dùng "Tôi gợi ý", "Bạn nên", chỉ nội dung thuần).
    """),
    ("human", "Gợi ý cho tôi nhé!")
])
def retrieve_context_fn(inputs: dict) -> str:
    question = inputs.get("question", "")
    if not isinstance(question, str):
        return ""
    query = question.strip().lower()
    if not query:
        return ""
    try:
        query_emb = model.encode([query]).tolist()
        results = collection.query(
                query_embeddings=[query_emb],
                n_results=5
            )
        docs = results.get("documents", [[]])[0]
        return "\n".join(docs) if docs else ""
    except Exception as e:
            print(f"[VectorDB][ERROR] {e}")
            return "" # Trả về "" tốt hơn vì LLM có bắt lỗi không có thông tin phù hợp context

retriever = RunnableLambda(retrieve_context_fn)
def format_output(x: dict) -> str:
    answer = x.get("answer", "").strip()
    suggestion = x.get("suggestion", "").strip() or "Hiện chưa có gợi ý phù hợp ạ~"

    source = ""
    context = x.get("context", "")
    if context:
        ctx = context[:350].replace("\n", " ")
        source = f"\n\n(Nguồn tham khảo: {ctx}...)"

    return f"{answer}\n\n**Gợi ý thêm:** {suggestion}{source}"
yes_branch = (
    RunnableParallel(
        # question=itemgetter("question"),
        # username=itemgetter("username"),
        # context=itemgetter("context"),
        # answer=main_prompt | llm | StrOutputParser(),
        # suggestion=suggestion_prompt | llm | StrOutputParser(),
        question=itemgetter("question"),
        username=itemgetter("username"),
        context=itemgetter("context"),
        answer=main_prompt | llm | StrOutputParser(),
        suggestion=RunnableLambda(lambda _: ""), #giảm request tránh crash server/ keyfree.
    )
)
no_branch = RunnableLambda(
    lambda x: {
        "question": x["question"],
        "username": x["username"],
        "context": "",
        "answer": "Mình hiện chỉ hỗ trợ thông tin du lịch tại Huế thôi ạ 😊 Bạn muốn hỏi về địa điểm, ẩm thực hay trải nghiệm nào ở Huế không?",
        "suggestion": "",
    }
)


chain = (
    # Bước 1: Nhận input
    RunnableParallel(
        question=itemgetter("question"),  #bug dict != string
        username = itemgetter("username") #username=RunnableLambda(lambda x: x.get("username", "du khách")), ##đồng bộ với question
    )

    # Bước 2: Lấy context + phân loại
    | RunnableParallel(
        question=itemgetter("question"),
        username=itemgetter("username"),
        context=retriever,
        is_hue=classification_prompt | llm | StrOutputParser(),
    )

    # Bước 3: Rẽ nhánh theo phân loại
    | RunnableBranch(
        (
            lambda x: x["is_hue"].strip().upper() == "YES",
            yes_branch,
        ),
        no_branch
    )

    # Bước 4: Format output cuối
    | RunnableLambda(format_output)
)