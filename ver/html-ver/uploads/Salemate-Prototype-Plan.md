# Kế hoạch xây dựng Prototype — "Salemate" (Trợ lý bán hàng & tư vấn kỹ thuật chăn nuôi)

> Mục tiêu prototype: **DEMO để pitch Anova Feed**. Ưu tiên trải nghiệm "wow", chạy được vài kịch bản thật, đánh trúng pain point. KHÔNG cần độ chính xác/độ phủ production.
> Phạm vi: làm **cả 4 tính năng** nhưng theo thứ tự ưu tiên + 1 "golden path" demo xuyên suốt.

---

## 0. Hiểu lại "nỗi đau" để mọi thứ phục vụ nó

| # | Pain point của Anova | Tính năng đánh vào |
|---|----------------------|--------------------|
| P1 | Sales phụ thuộc chuyên gia kỹ thuật/thú y; tri thức nằm trong đầu vài người | Tư vấn kỹ thuật + chẩn đoán bệnh nhẹ |
| P2 | Tra cứu thủ công ~150 SP, chính sách, khuyến mãi → chậm, không nhất quán | Tra cứu SP & chính sách (RAG) |
| P3 | Yếu thế khi khách so sánh với đối thủ → khó chốt đơn | So sánh đối thủ + sinh kịch bản chốt |
| P4 | Gợi ý sản phẩm theo từng khách/trang trại còn cảm tính | Gợi ý cá nhân hóa + cross-sell |

**Nguyên tắc xuyên suốt:** mỗi tính năng trong demo phải kết thúc bằng "câu chốt giúp Sales" (luận điểm bán hàng, phác đồ, kịch bản) — không chỉ trả lời thông tin.

---

## 1. Kiến trúc tổng thể (đủ cho demo, không over-engineer)

```
┌─────────────┐     ┌──────────────────────────────────────────┐     ┌─────────────────┐
│  Giao diện  │ ──▶ │           AI Agent (Claude)              │ ──▶ │   Nguồn dữ liệu  │
│  Chat web   │     │  Router (Haiku) → Reasoner (Opus 4.8)    │     │  - Vector store  │
│  (Streamlit │     │  + Tools:                                │     │    (RAG docs)    │
│   /Next.js) │ ◀── │   • rag_search (tra cứu tài liệu)        │ ◀── │  - JSON/SQLite   │
└─────────────┘     │   • product_lookup (catalogue có cấu trúc)│     │    (SP, đối thủ) │
                    │   • compare_competitor                   │     │  - Tri thức KT/   │
                    │   • recommend_products                   │     │    phác đồ (RAG)  │
                    │   • diagnose (+ confidence + escalation) │     └─────────────────┘
                    └──────────────────────────────────────────┘
```

**Vì sao kiến trúc này:**
- **RAG** cho tài liệu phi cấu trúc (hướng dẫn kỹ thuật, phác đồ, chính sách) → trả lời có dẫn nguồn, chống "bịa".
- **JSON/SQLite có cấu trúc** cho catalogue & đối thủ → so sánh **chính xác, đối chiếu được** (không để LLM tự nhớ số liệu).
- **Tool calling**: Claude tự quyết gọi tool nào theo câu hỏi → đúng tinh thần "AI Agent" trong slide.
- **Confidence + escalation**: ca thú y khó → bot tự gắn cờ "chuyển R&D/thú y" → thể hiện cơ chế an toàn mà slide nhấn mạnh.

> Knowledge Graph trong slide: với prototype **chưa cần**. RAG + bảng so sánh có cấu trúc đã đủ tạo "wow". Để KG vào phần "lộ trình production".

---

## 2. Dữ liệu — thu thập & chuẩn bị như thế nào

Đây là phần xương sống. Chia 2 loại: **có cấu trúc** (để tra cứu/so sánh chính xác) và **phi cấu trúc** (để RAG).

### 2.1 Catalogue ~150 SP — *có cấu trúc*
- **Nguồn:** website Anova (anovafeed.vn), datasheet PDF/Excel nội bộ, bảng giá.
- **Cách làm:** trích thành JSON, mỗi SKU 1 bản ghi. Trường gợi ý:
  ```json
  {
    "ma_sp": "A101", "ten": "...", "vat_nuoi": "heo|gà|...",
    "giai_doan": "heo con|heo thịt|nái...", "thanh_phan_dinh_duong": {"dam": 18, "xo": 5, ...},
    "fcr_tham_chieu": 2.4, "huong_dan_dung": "...", "gia": 0, "ghi_chu": "..."
  }
  ```
- Với demo: chuẩn hóa **20–30 SP chủ lực** là đủ (phần còn lại điền tối thiểu). Slide cũng đề xuất giai đoạn 1 phạm vi hẹp.

### 2.2 Chính sách & khuyến mãi — *phi cấu trúc → RAG*
- **Nguồn:** tài liệu chính sách bán hàng, chương trình khuyến mãi/tích lũy hiện hành.
- **Cách làm:** convert sang Markdown sạch → cắt chunk (≈300–500 token) → embed → vector store. Gắn metadata `{loai: "chinh_sach", hieu_luc: "...", vat_nuoi: "..."}`.

### 2.3 Tài liệu kỹ thuật / phác đồ — *phi cấu trúc → RAG (quan trọng nhất)*
- **Nguồn:** hướng dẫn chăm sóc, kỹ thuật chăn nuôi, triệu chứng bệnh, phác đồ điều trị.
- **Cách làm:** chunk theo chủ đề; **gắn cờ `r&d_approved: true/false`** cho từng tài liệu. Demo chỉ cho bot dùng tri thức `approved` → thể hiện "tri thức được R&D kiểm duyệt".
- Riêng phác đồ bệnh: cấu trúc nhẹ `{trieu_chung: [...], chan_doan: "...", phac_do: "...", san_pham_lien_quan: [...], do_nghiem_trong: "nhẹ|cần chuyên gia"}` để bot truy xuất "ca tương tự".

### 2.4 Dữ liệu đối thủ — *web search + sinh data demo bằng Claude*
- **Nguồn:** search thông tin công khai các đối thủ (De Heus, GreenFeed, CP, Cargill, Japfa, Haid/Hi‑Gro, Uni‑President...). Lấy thông số/giá/thành phần ở đâu có.
- **Chỗ thiếu:** dùng Claude **sinh dữ liệu mẫu hợp lý** (thành phần dinh dưỡng, giá ước tính, FCR) → **gắn nhãn rõ "DỮ LIỆU DEMO"** trong UI và file, tránh hiểu nhầm là số liệu thật.
- Lưu **có cấu trúc** (JSON) giống schema catalogue để `compare_competitor` đối chiếu trực tiếp.

### 2.5 Pipeline xử lý (chạy 1 lần, offline)
```
Raw (PDF/Excel/web)
  → Clean/OCR/parse
  → [Có cấu trúc]   → JSON / SQLite   (product_lookup, compare_competitor, recommend)
  → [Phi cấu trúc]  → chunk → embed → vector store   (rag_search)
  → Tạo "golden Q&A set" (~40–50 câu) để test nhanh
```

> Mẹo demo: chuẩn bị sẵn **bộ 40–50 câu hỏi mẫu** + đáp án kỳ vọng. Vừa để test, vừa để show "độ chính xác X%" lúc pitch.

---

## 3. Các bước làm (phased, ~2.5–3 tuần)

### Phase 0 — Dữ liệu & khung dự án (2–3 ngày)
- Thu thập 4 nhóm dữ liệu ở Mục 2; chuẩn hóa 20–30 SP chủ lực + 5–10 SP đối thủ + 50 mục tài liệu.
- Dựng vector store + nạp embeddings; tạo JSON/SQLite cho SP & đối thủ.
- **Output:** dữ liệu sẵn sàng, golden Q&A set v1.

### Phase 1 — RAG core + Tra cứu (P2) (3–4 ngày)
- Tool `rag_search` + `product_lookup`. Agent trả lời thông số/hướng dẫn/chính sách, **có trích nguồn**.
- **Output:** demo được "hỏi sản phẩm/chính sách → trả lời nhanh, dẫn nguồn".

### Phase 2 — So sánh đối thủ (P3) + Gợi ý cá nhân hóa (P4) (3–4 ngày)
- `compare_competitor`: sinh **bảng so sánh dinh dưỡng/giá/FCR + 2–3 luận điểm chốt đơn**.
- `recommend_products`: nhập bối cảnh khách (vật nuôi, độ tuổi, quy mô) → gợi ý SP + cross-sell.
- **Output:** demo được "khách đang dùng cám X → bảng so sánh + kịch bản chào bán".

### Phase 3 — Tư vấn kỹ thuật + Chẩn đoán bệnh nhẹ (P1) (3–4 ngày)
- `diagnose`: nhận mô tả triệu chứng (text, +ảnh nếu kịp) → truy xuất ca/phác đồ tương tự → đề xuất sơ bộ + SP liên quan.
- **Cơ chế an toàn:** mỗi câu trả lời thú y có **confidence score**; thấp hoặc ca nặng → "⚠️ Chuyển chuyên gia R&D/thú y". Có disclaimer.
- **Output:** demo được pain sâu nhất một cách an toàn.

### Phase 4 — UI polish + kịch bản demo + tổng duyệt (2–3 ngày)
- Style giao diện theo brand FPT/Anova; thêm badge "nguồn", "DEMO data", "confidence".
- Hard-code/tinh chỉnh 4 kịch bản golden path; tổng duyệt, đo thời gian phản hồi.

---

## 4. Kịch bản demo (Golden Path) — bán câu chuyện, không bán tính năng

Dựng 1 nhân vật Sales đi gặp khách, 4 cảnh nối tiếp:

1. **Tra cứu (P2):** *"Khách nuôi heo thịt ~30kg, cho tôi SP phù hợp + thông số."* → bot tra cứu + dẫn nguồn trong vài giây.
2. **So sánh (P3):** *"Khách đang dùng cám [Đối thủ X], so sánh giúp tôi."* → bảng so sánh + 3 luận điểm chốt đơn.
3. **Cá nhân hóa + cross-sell (P4):** *"Trang trại 200 con, gợi ý thêm gì?"* → SP theo giai đoạn + gợi ý vaccine/thuốc + chương trình KM phù hợp.
4. **Tư vấn kỹ thuật (P1):** *"Heo tiêu chảy, phân trắng, bỏ ăn 2 ngày."* → bot phân tích → ca tương tự + phác đồ sơ bộ + SP; nếu confidence thấp → **"chuyển chuyên gia R&D"** (chốt thông điệp an toàn).

> Mỗi cảnh để lại 1 con số "before/after": *"trước đây Sales mất 10–15 phút lục tài liệu, giờ < 10 giây"*.

---

## 5. Tech stack (bản hiện thực)

> Cập nhật theo bản đã build: pivot sang mảng thú y (**AI SalesMate**) và gọi LLM qua **FPT Cloud** thay vì Anthropic trực tiếp. Chi tiết kỹ thuật xem **Mục 9**.

| Lớp | Đang dùng | Ghi chú |
|-----|-----------|---------|
| LLM | **GLM-5.1 qua FPT Cloud** (FPT AI Marketplace, OpenAI-compatible) | Endpoint `https://mkp-api.fptcloud.com`, gọi bằng `openai` SDK. Model đổi ở `.env` `FPT_MODEL`. Phải hỗ trợ function calling. |
| Orchestration | **Python + OpenAI SDK** (function calling) | Vòng lặp agent tự gọi tool → trả kết quả → lặp tới khi xong (`agent.py`). |
| RAG (tài liệu) | Truy xuất **từ vựng + IDF**, chuẩn hóa dấu tiếng Việt (`retrieval.py`) | Nhẹ, chạy ngay, không cần model embedding. Production thay bằng vector embeddings. |
| Dữ liệu có cấu trúc | **JSON** (sản phẩm, bệnh, nhà phân phối) | Số liệu (liều lượng/giá/lịch sử đơn) lấy từ đây, không để LLM bịa. |
| Giao diện | **Streamlit** (full-width, brand Anova) | Logo + màu thật từ anovafeed.vn. |
| Cấu hình | **.env** (backend) + `.streamlit/config.toml` (theme) | Key/model/endpoint ở backend, không nhập trên UI. |

**Lưu ý kỹ thuật:**
- Số liệu lấy từ **tool (dữ liệu cấu trúc)**, KHÔNG để LLM tự bịa.
- Parse tool input bằng `json.loads()` (không string-match).
- Model bắt buộc hỗ trợ **function calling**; số liệu/độ tin cậy tính ở Python, LLM chỉ diễn giải.

---

## 6. Guardrails cho phần tư vấn thú y (bắt buộc, vì là pitch về chăn nuôi)

- Chỉ dùng tri thức `r&d_approved` trong vector store.
- Mọi đề xuất phác đồ kèm **disclaimer** + **confidence**; ca nặng/độ tin thấp → **escalation** sang chuyên gia.
- Không tự kê liều cho ca phức tạp; chỉ "gợi ý sơ bộ + SP phù hợp".
- UI hiển thị rõ nguồn trích dẫn → tăng độ tin khi pitch.

---

## 7. Cách đo lường để pitch (nhẹ nhưng thuyết phục)

- Chạy golden Q&A set (40–50 câu) → báo "đúng X%, có dẫn nguồn".
- Đo thời gian phản hồi trung bình (mục tiêu < 5–8s/câu).
- So sánh "before/after" thời gian tra cứu của Sales.
- Tổng hợp thành 1 slide "kết quả prototype" để gắn vào bộ đề xuất.

---

## 8. Việc để dành cho production (nói rõ trong pitch, không làm trong prototype)

- Knowledge Graph + escalation workflow đầy đủ.
- Tích hợp CRM/ERP/DMS (bối cảnh khách, lịch sử mua, tác động doanh số).
- Mở rộng full ~150 SP + toàn bộ chương trình KM; quy trình duyệt & versioning tri thức.
- Triển khai On-Cloud/On-Premise hạ tầng riêng Anova.

---

### Checklist khởi động nhanh
- [ ] Gom 4 nhóm dữ liệu (catalogue, chính sách, kỹ thuật/phác đồ, đối thủ)
- [ ] Chuẩn hóa 20–30 SP chủ lực + 5–10 SP đối thủ + 50 mục tài liệu
- [ ] Dựng vector store + JSON/SQLite + golden Q&A set
- [ ] Code 5 tool + agent (Opus 4.8 / Haiku 4.5)
- [ ] UI chat + badge nguồn/DEMO/confidence
- [ ] 4 kịch bản golden path + tổng duyệt

---

## 9. Công nghệ & kiến trúc kỹ thuật (chi tiết bản hiện thực)

### 9.1 Sơ đồ kiến trúc

```
┌──────────────┐   câu hỏi    ┌─────────────────────────────┐   tool call   ┌──────────────────┐
│  Streamlit   │ ───────────▶ │  AI Agent (agent.py)        │ ────────────▶ │  Tools (tools.py) │
│  app.py      │              │  - System prompt + lịch sử  │               │  4 hàm Python     │
│  (giao diện) │ ◀─────────── │  - Vòng lặp function calling│ ◀──────────── │  + dữ liệu JSON   │
└──────────────┘   trả lời    └──────────────┬──────────────┘   kết quả      └────────┬─────────┘
                                             │ HTTPS (OpenAI-compatible)               │
                                             ▼                                         ▼
                                   ┌────────────────────┐                  ┌────────────────────────┐
                                   │   FPT Cloud LLM    │                  │  data/*.json + RAG      │
                                   │   GLM-5.1          │                  │  retrieval.py (IDF)     │
                                   └────────────────────┘                  └────────────────────────┘
```

- **3 lớp tách bạch:** Giao diện (Streamlit) · Bộ não (Agent + LLM) · Tri thức (dữ liệu cấu trúc + RAG).
- LLM **không giữ số liệu** — mọi liều lượng/giá/lịch sử đơn/độ tin cậy đều tính ở Python rồi đưa vào ngữ cảnh.

### 9.2 Luồng xử lý một câu hỏi (agent loop)

1. Người dùng gửi câu hỏi (hoặc bấm 1 trong 4 nút kịch bản).
2. Agent gọi FPT/GLM với: `system prompt` + lịch sử hội thoại + **danh sách 4 tool**.
3. Nếu LLM trả về `tool_calls` → Python **thực thi tool** (truy vấn JSON/RAG) → đưa kết quả (JSON) trở lại LLM → lặp lại bước 2.
4. Khi LLM không gọi tool nữa → trả về câu trả lời cuối (tiếng Việt, có cấu trúc, kết bằng "👉 Gợi ý cho Sales").
5. Giới hạn an toàn: tối đa **6 vòng** lặp (`max_steps`) tránh lặp vô hạn.

UI hiển thị realtime các tool được gọi (khối "Salemate đang xử lý...") để minh bạch khi demo.

### 9.3 Cơ chế Tool Use (function calling)

- Chuẩn **OpenAI function calling** (FPT tương thích). 4 tool khai báo trong `tools.py` (`TOOL_SCHEMAS`), convert sang định dạng `{"type":"function","function":{name,description,parameters}}`.
- 4 tool: `chan_doan_benh`, `tra_cuu_thuoc`, `phan_tich_nha_phan_phoi`, `tra_cuu_tai_lieu`.
- Tham số do LLM sinh được parse bằng `json.loads()`; điều phối qua `dispatch(name, args)`; mỗi hàm trả về `dict` JSON-serializable.
- **Vì sao tách tool:** đảm bảo số liệu chính xác & kiểm soát được (LLM không tự bịa liều/giá), đồng thời gắn được logic an toàn (escalation) ở tầng code.

### 9.4 RAG — truy xuất tài liệu (`retrieval.py`)

- Nạp các file `data/knowledge/*.md` → cắt chunk theo heading → tập token.
- **Chuẩn hóa tiếng Việt:** bỏ dấu (NFD + loại dấu) + `đ→d` để khớp bền (vd "tiêu chảy" ≈ "tieu chay").
- **Xếp hạng bằng IDF:** ưu tiên từ hiếm/đặc trưng (vd "chiết khấu", "an toàn sinh học") hơn từ phổ biến → đúng tài liệu lên top.
- Cờ `r&d_approved`: chỉ trả tài liệu đã duyệt.
- **Tradeoff:** đây là retrieval từ vựng (lexical) — chạy ngay, 0 phụ thuộc model embedding, đủ cho corpus nhỏ. Production: nâng lên **vector embeddings** (multilingual-e5 / Vietnamese-SBERT) + vector DB + reranker khi dữ liệu lớn.

### 9.5 Lớp dữ liệu (schema)

| File | Vai trò | Trường chính |
|---|---|---|
| `vet_products.json` | Catalogue thuốc/vaccine | `ma_sp, ten, hang, loai, cong_dung, chi_dinh, lieu_luong, duong_dung, thoi_gian_ngung, gia_vnd` |
| `diseases.json` | KB bệnh + thị trường | `ten_benh, tac_nhan, trieu_chung[], muc_do, co_thuoc_dac_tri, buoc_xu_ly, vaccine_phong, san_pham_lien_quan[], thong_tin_thi_truong, can_chuyen_gia` |
| `distributors.json` | NPP + lịch sử đơn | `ten, khu_vuc, loai_hinh, cong_no_vnd, lich_su_don[{thang, ma_sp, so_luong, gia_tri_vnd}]` |
| `knowledge/*.md` | RAG | tài liệu an toàn sinh học/ASF, vaccine, chính sách, khuyến mãi |

Số liệu là **DEMO cook**; production thay bằng dữ liệu thật (giữ nguyên schema → không phải sửa code).

### 9.6 Tích hợp FPT Cloud

- SDK: `openai` (Python), trỏ `base_url = https://mkp-api.fptcloud.com`.
- Xác thực: gửi **cả** `Authorization: Bearer <key>` **và** header `api-key: <key>` (tương thích 2 cách FPT chấp nhận).
- Model: `FPT_MODEL` (mặc định `GLM-5.1`) — phải khớp đúng id trên FPT Marketplace và **hỗ trợ function calling**. Nếu model không có tool → đổi sang model có tool (vd `Llama-3.3-70B-Instruct`, `DeepSeek-R1`).
- Tham số gọi: `temperature=0.3`, `max_tokens=2000`, `tool_choice="auto"`.

### 9.7 Cấu hình & bảo mật

- Toàn bộ cấu hình ở **backend `.env`**: `FPT_API_KEY`, `FPT_BASE_URL`, `FPT_MODEL`. UI không yêu cầu nhập key.
- API key **không** nằm trong code, không in ra UI; `.env` cần được loại khỏi git (`.gitignore`) khi đưa lên repo.
- Theme/màu thương hiệu tách ở `.streamlit/config.toml`.

### 9.8 Guardrails kỹ thuật (an toàn thú y)

- **Độ tin cậy** = số triệu chứng khớp / tổng triệu chứng của bệnh (tính ở Python).
- **Tự động escalation** (cờ `can_chuyen_chuyen_gia=true`) khi: độ tin cậy < 0.4 **hoặc** mức độ ∈ {nặng, nguy hiểm} **hoặc** bệnh đánh dấu cần chuyên gia **hoặc** không có thuốc đặc trị (bệnh virus như ASF).
- System prompt ràng buộc: không tự kê đơn điều trị virus; kháng sinh chỉ cho bệnh vi khuẩn; luôn kèm khuyến cáo "theo chỉ định thú y, tuân thủ thời gian ngừng thuốc".

### 9.9 Hiệu năng & chi phí

- Độ trễ phụ thuộc model GLM-5.1 trên FPT + số vòng tool (thường 1–2 vòng/câu).
- Corpus nhỏ → truy xuất/truy vấn JSON gần như tức thời; chi phí chủ yếu ở token LLM.
- Tối ưu khi mở rộng: cache kết quả tool tĩnh, rút gọn ngữ cảnh, giảm `max_tokens` cho câu đơn giản.

### 9.10 Triển khai

- **Local/demo:** `streamlit run app.py` (đã có sẵn `.venv`).
- **Kiểm thử logic không cần key:** `python test_tools.py` (4 tool).
- **Production gợi ý:** đóng gói **Docker** → deploy lên FPT Cloud/máy chủ nội bộ; secret qua secret manager; đặt sau reverse proxy + xác thực người dùng nội bộ.

### 9.11 Lộ trình công nghệ production

| Hạng mục | Công nghệ |
|---|---|
| Đa phương thức input | Vision (upload ảnh ca bệnh, model đa phương thức) · Voice (speech-to-text) |
| RAG nâng cao | Vector embeddings (multilingual-e5/Vietnamese-SBERT) + vector DB (pgvector/Qdrant) + reranker |
| Tri thức | Knowledge Graph bệnh–triệu chứng–sản phẩm; quy trình duyệt & versioning |
| Tích hợp nghiệp vụ | Connector **CRM/ERP/DMS** cho lịch sử nhà phân phối; nguồn **dữ liệu thị trường** (giá heo, diễn biến dịch) cập nhật tự động |
| Vận hành | Logging/observability, bộ **eval** (golden Q&A) đo độ chính xác, guard model kiểm soát đầu ra |
