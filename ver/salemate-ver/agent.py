"""AI SalesMate agent — gọi LLM qua FPT Cloud (OpenAI-compatible) với tool use."""
import json

from openai import OpenAI

import tools as T

SYSTEM_PROMPT = """Bạn là "AI SalesMate" — trợ lý bán hàng & tư vấn thú y cho đội ngũ Sales/tư vấn viên của Nova Consumer (thuốc thú y Anova Pharma, vaccine Navetco/Vetvaco/Anova Biotech).

NĂNG LỰC:
- Chẩn đoán bệnh trên heo từ triệu chứng, kèm thông tin thị trường liên quan.
- Tra cứu thuốc/vaccine: công dụng, chỉ định, LIỀU LƯỢNG, đường dùng, thời gian ngừng thuốc.
- Phân tích nhà phân phối: lịch sử mua/bán, gợi ý đơn tiếp theo & sản phẩm nên bán.
- So sánh sản phẩm cám Anova với đối thủ theo đạm, xơ, năng lượng, FCR tham chiếu và giá/kg.

NGUYÊN TẮC:
1. Luôn dùng công cụ (tool) để lấy liều lượng, giá, lịch sử đơn, phác đồ — KHÔNG tự bịa số liệu.
1b. Khi so sánh đối thủ, PHẢI nêu rõ dữ liệu đối thủ là DEMO/chưa kiểm chứng nếu công cụ trả về lưu ý này.
2. AN TOÀN THÚ Y: với bệnh virus nguy hiểm (ASF/dịch tả lợn châu Phi, CSF, FMD, PRRS) hoặc khi công cụ báo cần-chuyển-chuyên-gia, PHẢI nêu rõ "chưa có thuốc đặc trị / cần thú y xác chẩn", nhấn mạnh an toàn sinh học + vaccine phòng, và KHÔNG tự kê đơn điều trị virus. Kháng sinh chỉ cho bệnh vi khuẩn.
3. Khi nêu liều lượng/đường dùng, lấy đúng từ công cụ và kèm khuyến cáo "theo chỉ định thú y, tuân thủ thời gian ngừng thuốc".
4. Khi tra cứu tài liệu: trích dẫn nguồn (tên file). Số liệu sản phẩm/giá là dữ liệu mẫu (DEMO).
5. KẾT THÚC mỗi câu trả lời bằng dòng "👉 Gợi ý cho Sales:" — luận điểm chốt đơn / sản phẩm nên chào / bước tiếp theo cụ thể.

PHONG CÁCH: tiếng Việt, ngắn gọn, có cấu trúc (gạch đầu dòng/bảng), đi thẳng vào điều Sales cần để chốt khách."""


def build_client(api_key: str, base_url: str) -> OpenAI:
    """Client OpenAI-compatible trỏ vào FPT Cloud.

    Gửi cả Authorization: Bearer và header api-key để tương thích cả hai cách FPT chấp nhận.
    """
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        default_headers={"api-key": api_key},
    )


def _openai_tools():
    """Chuyển schema tool (dạng Anthropic) sang định dạng tools của OpenAI."""
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["input_schema"],
            },
        }
        for t in T.TOOL_SCHEMAS
    ]


def run_agent(client, model, messages, on_event=None, max_steps=6):
    """Vòng lặp agent. `messages` là list OpenAI-format (KHÔNG chứa system).

    on_event(kind, name, payload): kind ∈ {"tool", "tool_done", "final"}.
    Trả về (text_tra_loi, messages).
    """
    tools = _openai_tools()
    for _ in range(max_steps):
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.3,
            max_tokens=2000,
        )
        msg = resp.choices[0].message
        tool_calls = msg.tool_calls or []

        # Lưu lại lượt trả lời của assistant (kèm tool_calls nếu có)
        assistant_entry = {"role": "assistant", "content": msg.content or ""}
        if tool_calls:
            assistant_entry["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in tool_calls
            ]
        messages.append(assistant_entry)

        if tool_calls:
            for tc in tool_calls:
                name = tc.function.name
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                if on_event:
                    on_event("tool", name, args)
                result = T.dispatch(name, args)
                if on_event:
                    on_event("tool_done", name, result)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )
            continue

        # Trả lời cuối
        if on_event:
            on_event("final", None, None)
        return (msg.content or "(không có nội dung)", messages)

    return ("⚠️ Đã đạt giới hạn số bước xử lý.", messages)
