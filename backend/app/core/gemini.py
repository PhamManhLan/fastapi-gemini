import google.generativeai as genai
from ..core.config import get_settings

settings = get_settings()
genai.configure(api_key=settings.GEMINI_API_KEY)

SYSTEM_PROMPT = """
            "-Bạn là **hướng dẫn viên du lịch chuyên nghiệp tại Thừa Thiên Huế** dành cho du khách Việt Nam"
            "-Đến thăm tỉnh Thừa Thiên Huế"
            "-**Giới thiệu**: Chỉ khi nhận được lời chào (Ví dụ: 'Xin chào', 'Hello') **ở lần tương tác đầu tiên**, hãy trả lời chính xác: 'Tôi là hướng dẫn viên du lịch Huế, rất sẵn lòng hỗ trợ bạn khám phá.'"
            "-**Nói ngắn gọn, bằng tiếng Việt** về Huế khi có người hỏi gợi ý thêm **một điều khác** liên quan đến Huế liên quan đến Huế (ví dụ: một địa điểm, một món ăn, hoặc một sự kiện)."
            "-Nếu có câu hỏi về địa điểm nào khác tỉnh Thừa Thiên Huế hãy trả lời: 'Tôi chỉ nói về Huế.'"
""".strip()

async def get_gemini_response(user_message: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = await model.generate_content_async(
            [SYSTEM_PROMPT, user_message],
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=512,
            )
        )
        return response.text.strip()
    except Exception as e:
        return "Lỗi. Thử lại sau!"