# AI SalesMate — Tổng quan dự án

> Prototype trợ lý thú y & bán hàng cho **Nova Consumer** (pivot từ bản mảng cám của Anova Feed).
> Cập nhật: 18/06/2026.

---

## 1. Dự án giải quyết vấn đề gì?

**AI SalesMate** số hóa tri thức thú y + bán hàng của Nova Consumer thành 1 trợ lý cho đội ngũ tư vấn viên/Sales, nhắm vào các "nỗi đau":

- **Phụ thuộc chuyên gia thú y**: kiến thức chẩn đoán bệnh + phác đồ nằm trong đầu vài người → nghỉ việc là mất, khó nhân rộng cho cả đội Sales.
- **Chẩn đoán & xử lý chậm khi gặp ca bệnh** (vd dịch tả lợn châu Phi - ASF): tư vấn viên khó nhận diện bệnh và đề xuất đúng sản phẩm tại hiện trường.
- **Tra cứu thuốc/vaccine thủ công**: công dụng, **liều lượng**, chỉ định, đường dùng dễ nhớ sai → tư vấn không nhất quán, rủi ro.
- **Khai thác nhà phân phối còn cảm tính**: không biết NPP nào nên chào sản phẩm gì, đơn kế tiếp ra sao.

→ **Mục tiêu:** chuẩn hóa + tăng tốc tư vấn, bán hàng có trách nhiệm (an toàn thú y), và khai thác sâu nhà phân phối.

---

## 2. Các vấn đề & kết quả đầu ra SalesMate hỗ trợ

| Vấn đề | Đầu vào | Kết quả đầu ra |
|---|---|---|
| **Chẩn đoán bệnh** | Mô tả triệu chứng (text) | Bệnh khả năng nhất + **độ tin cậy** + tác nhân + chẩn đoán phân biệt + **bước xử lý** + sản phẩm Nova Consumer + **thông tin thị trường** + cờ **"chuyển chuyên gia thú y"** (bệnh virus như ASF: không tự kê đơn) |
| **Tra cứu thuốc/vaccine** | Hỏi sản phẩm/bệnh | Công dụng, chỉ định, **liều lượng**, đường dùng, **thời gian ngừng thuốc**, giá |
| **Phân tích nhà phân phối** | Tên/mã NPP | Tổng quan mua hàng, sản phẩm chủ lực, **gợi ý đơn tiếp theo (số lượng)**, **cơ hội bán thêm** (cross-sell, ưu tiên vaccine ASF & sát trùng) |

Mỗi câu trả lời kết bằng dòng **"👉 Gợi ý cho Sales"** (luận điểm chốt đơn). Định dạng: chat tiếng Việt có cấu trúc, dẫn nguồn tài liệu, gắn nhãn **minh họa**, cảnh báo an toàn.

4 câu hỏi kịch bản "cook" đều được phủ:
1. Đây là bệnh gì?
2. Xử lý bệnh này thế nào?
3. Sản phẩm nào của Nova Consumer dùng được?
4. Thông tin chi tiết (công dụng, liều lượng) của sản phẩm đó?

---

## 3. Dữ liệu lấy từ đâu?

| Nhóm dữ liệu | File | Nguồn | Tính chất |
|---|---|---|---|
| Catalogue thuốc/vaccine | `data/vet_products.json` | Cook bằng AI, bám thương hiệu thật (Anova Pharma, **Navetco/NAVET-ASFVAC**, Vetvaco, Anova Biotech) — web-search xác thực cấu trúc nhóm cty + vaccine ASF VN | Cấu trúc thật, **số liệu liều lượng/giá là minh họa** |
| KB bệnh | `data/diseases.json` | Cook từ kiến thức thú y phổ thông + web-search ASF 2025 (NAVET-ASFVAC, AVAC, diễn biến dịch) | Minh họa, định hướng đúng |
| Thông tin thị trường | (trong `diseases.json`) | Cook từ tin tức ASF 2025 | Minh họa |
| Nhà phân phối + lịch sử đơn | `data/distributors.json` | Cook hoàn toàn (giả lập) | Minh họa |
| Tài liệu RAG | `data/knowledge/*.md` | Cook (an toàn sinh học/ASF, vaccine, chính sách, khuyến mãi) | Minh họa |
| Logo + màu thương hiệu | `assets/anova-logo.png` | **Thật** — tải từ anovafeed.vn, trích màu từ logo (#80C040 xanh lá, #0070B0 xanh dương) | Thật |

**Tóm lại:** kiến trúc/luồng xử lý là **thật và chạy được**; dữ liệu nghiệp vụ là **mẫu (cook)** để minh họa. Lên production chỉ cần thay bằng catalogue/KB/CRM thật (giữ nguyên schema).

---

## 4. Đã đáp ứng đủ yêu cầu chưa?

Đối chiếu với **spec pivot thú y** (yêu cầu mới nhất, thay cho deck mảng cám):

| Yêu cầu | Đáp ứng |
|---|---|
| Chuyển hướng cám → thuốc thú y/vaccine | ✅ |
| KB bệnh trên lợn (gồm ASF) | ✅ 8 bệnh |
| Nhập văn bản | ✅ |
| Nhập giọng nói | ❌ chưa (phạm vi chọn "chỉ Text") |
| Nhập hình ảnh | ❌ chưa (phạm vi chọn "chỉ Text") |
| AI phân tích/chẩn đoán bệnh | ✅ |
| Thông tin thị trường liên quan | ✅ (cook) |
| Đề xuất bước xử lý + sản phẩm Nova Consumer | ✅ |
| Phân tích lịch sử mua/bán NPP | ✅ |
| Gợi ý đơn tiếp theo / sản phẩm nên bán | ✅ |
| Giao diện chat đơn giản | ✅ (thực tế: UI branded full-width) |
| Data cook theo 4 câu kịch bản | ✅ cả 4 |

**Kết luận:** đáp ứng **gần đủ** spec đã thống nhất. Hai khoảng còn lại là **chủ ý theo phạm vi đã chọn**, không phải thiếu sót:
1. **Đa phương thức (giọng nói + hình ảnh)** — chọn "chỉ Text" giai đoạn này.
2. **Dữ liệu thật** — đang là dữ liệu minh họa (cook); cần nối catalogue/KB thật + CRM/ERP cho lịch sử NPP.

---

## 5. Kiến trúc & cấu hình (tham khảo)

- **Giao diện:** Streamlit (`salemate/app.py`) — full-width, brand Anova/Nova Consumer.
- **Agent:** tool use qua **FPT Cloud** (FPT AI Marketplace, OpenAI-compatible) — `salemate/agent.py`.
  - Endpoint mặc định: `https://mkp-api.fptcloud.com`
  - Model: **GLM-5.1** (cấu hình ở `.env` `FPT_MODEL` hoặc sidebar; phải khớp đúng id trên FPT Marketplace và hỗ trợ function calling).
  - Cấu hình backend: `salemate/.env` (`FPT_API_KEY`, `FPT_BASE_URL`, `FPT_MODEL`).
- **4 công cụ (tool):** `chan_doan_benh`, `tra_cuu_thuoc`, `phan_tich_nha_phan_phoi`, `tra_cuu_tai_lieu` (RAG) — `salemate/tools.py`.
- **RAG:** truy xuất từ vựng + IDF, chuẩn hóa dấu tiếng Việt — `salemate/retrieval.py`.
- **Chạy:** `cd salemate && source .venv/bin/activate && streamlit run app.py` → http://localhost:8501
- **Test logic không cần API key:** `python test_tools.py`

---

## 6. Lộ trình production (chưa làm trong prototype)

- Đa phương thức input: **hình ảnh** (vision) + **giọng nói** (speech-to-text).
- Dữ liệu thật: catalogue thú y/vaccine thật, KB bệnh đầy đủ (R&D/thú y duyệt), tích hợp **CRM/ERP/DMS** cho lịch sử nhà phân phối.
- Nguồn **dữ liệu thị trường** (giá heo, diễn biến dịch) cập nhật tự động.
- Knowledge Graph + quy trình duyệt & versioning tri thức; cơ chế escalation R&D/thú y hoàn chỉnh.
