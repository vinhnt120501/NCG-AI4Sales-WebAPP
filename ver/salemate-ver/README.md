# AI SalesMate — Prototype trợ lý thú y & bán hàng (Nova Consumer)

Bản prototype **chạy thật** (không phải mockup) cho mảng **thuốc thú y / vaccine**: bấm nút → gọi Claude (tool use) → tra dữ liệu thật → trả lời.

## 3 chức năng chính (nút bấm hoạt động)
1. **🩺 Chẩn đoán bệnh** — mô tả triệu chứng (text) → bệnh khả năng nhất + độ tin cậy + tác nhân + bước xử lý + **sản phẩm Nova Consumer** + **thông tin thị trường** + cờ **chuyển chuyên gia** (ASF/CSF/FMD/PRRS không tự kê đơn).
2. **💉 Tra cứu thuốc / vaccine** — công dụng, chỉ định, **liều lượng**, đường dùng, thời gian ngừng thuốc (Anova Pharma, Navetco, Vetvaco, Anova Biotech).
3. **📊 Phân tích nhà phân phối** — lịch sử mua/bán → sản phẩm chủ lực, **gợi ý đơn tiếp theo**, **cơ hội bán thêm** (ưu tiên vaccine ASF & sát trùng).

Bao phủ 4 câu hỏi "cook": *(1) bệnh gì? (2) xử lý thế nào? (3) sản phẩm Nova Consumer nào? (4) công dụng/liều lượng?*

## Cài đặt & chạy
```bash
cd "salemate"
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Điền key FPT 1 lần vào .env: FPT_API_KEY=...   (tạo tại marketplace.fptcloud.com)
streamlit run app.py
```
Mở http://localhost:8501. Cấu hình (key FPT, model) đọc từ backend `.env` — không cần nhập trên UI.

## Kiểm thử logic không cần API key
```bash
python test_tools.py
```

## Cấu trúc
```
salemate/
  app.py            # Giao diện Streamlit (full-width, brand Anova/Nova Consumer)
  agent.py          # Vòng lặp AI Agent (Claude + tool use)
  tools.py          # 4 tool: chan_doan_benh, tra_cuu_thuoc, phan_tich_nha_phan_phoi, tra_cuu_tai_lieu
  retrieval.py      # RAG nhẹ (truy xuất từ vựng + IDF, chuẩn hóa dấu tiếng Việt)
  .env / .streamlit/config.toml   # cấu hình backend (API key, theme màu thương hiệu)
  assets/anova-logo.png           # logo thật của Anova
  data/
    vet_products.json   # thuốc/vaccine Nova Consumer (DEMO, có liều lượng)
    diseases.json       # knowledge base bệnh heo (gồm ASF) + thông tin thị trường
    distributors.json   # nhà phân phối + lịch sử đơn (DEMO)
    knowledge/*.md      # an toàn sinh học/ASF, vaccine, chính sách, khuyến mãi (RAG)
```

## LLM & màu
- Gọi qua **FPT Cloud (FPT AI Marketplace, OpenAI-compatible)** — `FPT_BASE_URL=https://mkp-api.fptcloud.com`.
- Model mặc định `GLM-5.1` (đổi ở sidebar / `.env` `FPT_MODEL`). Model phải hỗ trợ function calling và khớp đúng id trên FPT Marketplace.
- Màu trích từ logo Anova thật: xanh lá #80C040 + xanh dương #0070B0.

## Lộ trình production (chưa làm trong prototype)
- Đa phương thức input: **hình ảnh** (Claude vision) + **giọng nói** (speech-to-text).
- Dữ liệu thật: catalogue thú y/vaccine thật, KB bệnh đầy đủ, tích hợp CRM/ERP cho lịch sử nhà phân phối.
- Nguồn dữ liệu thị trường (giá heo, diễn biến dịch) cập nhật tự động.
