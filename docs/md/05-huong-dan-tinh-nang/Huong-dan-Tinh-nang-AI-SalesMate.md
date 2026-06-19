# Hướng dẫn tính năng AI SalesMate (bản sản phẩm hóa)

> Tài liệu tổng hợp toàn bộ tính năng của AI SalesMate sau khi nâng từ "chatbot tra cứu" thành **trợ lý hiện trường có quy trình khép kín**. Dành cho đội Sale, quản lý và đội kỹ thuật/R&D.
> Tab **Bản đồ dịch bệnh** có hướng dẫn riêng: xem **[Huong-dan-Ban-do-dich-benh.md](Huong-dan-Ban-do-dich-benh.md)**.

---

## 0. Toàn cảnh: một vòng lặp công việc, không phải vài câu hỏi rời

```
[Trợ lý tư vấn]                                   [Bản đồ dịch bệnh]
 Tạo ca bệnh ─┐                                    Nhập cảnh báo ──┐
              ├─► Chẩn đoán sâu ─► Quick actions:                  ├─► Heatmap
              │    • Hồ sơ ca       • Tính số lượng                │
              │    • Mức rủi ro     • Tạo đơn nháp                 └─► Tạo chiến dịch
              │    • Cần hỏi thêm   • Tạo ticket chuyên gia            (NPP ưu tiên + SKU
              │    • Phác đồ đàn    • Soạn tin nhắn khách               + tin nhắn mẫu)
              │    • Bảng ảnh hưởng
              │    • SP theo vai trò
              └─► Ca gần đây (lưu lại) ─► NPP Cockpit ─► Dashboard theo vai trò
```

Mọi ca/đơn/ticket/chiến dịch được **lưu trong trình duyệt (localStorage)** → tải lại trang không mất.

---

## 1. Hai không gian làm việc

Trên thanh tiêu đề có 2 tab:
- **Trợ lý tư vấn** — chat + quy trình ca bệnh (4 năng lực: chẩn đoán, tra cứu thuốc, phân tích NPP, tra cứu tài liệu).
- **Bản đồ dịch bệnh** — heatmap thị trường + tạo chiến dịch (tài liệu riêng).

Hai tab độc lập, chuyển qua lại bất cứ lúc nào.

---

## 2. Tạo ca bệnh (Case Intake)

**Mục tiêu:** thay vì gõ chat tự do, Sale nhập nhanh một **ca có cấu trúc** để AI chẩn đoán sâu hơn và tạo được đơn/ticket.

### Cách dùng
1. Ở thanh bên trái (tab Trợ lý tư vấn), bấm **`＋ Tạo ca bệnh`**.
2. Điền form:

   | Trường | Ý nghĩa | Ví dụ |
   |---|---|---|
   | Khách / trại / NPP | Đối tượng của ca | Trại heo Long Thành |
   | Loài nuôi · Giai đoạn | Để gắn đúng phác đồ | Heo · Heo thịt |
   | Tỉnh / thành | Định vị, liên thông bản đồ | Đồng Nai |
   | Tổng đàn · Số mắc · Số chết | Tính **mức rủi ro** | 200 · 30 · 8 |
   | Bắt đầu từ | Diễn biến thời gian | 1–2 ngày trước |
   | **Triệu chứng** *(bắt buộc)* | Cơ sở để chẩn đoán | sốt 41°, da tai bụng tím, chết nhanh |
   | Đã dùng thuốc/vaccine | Tránh gợi ý trùng/sai | đã tiêm dịch tả cổ điển tháng trước |

   - Có **chip triệu chứng bấm nhanh** (sốt cao, tiêu chảy, da tím tái, chết nhanh…).
3. Bấm **`Tạo ca & chẩn đoán`** → AI tự push mô tả ca và trả về chẩn đoán sâu.

> Ca được lưu vào mục **"Ca bệnh gần đây"** ở thanh bên — bấm để mở lại bất kỳ lúc nào.

---

## 3. Chẩn đoán sâu — các khối trả lời (điểm nhấn với khách kỹ thuật)

Khi chẩn đoán (từ form hoặc gõ chat), câu trả lời gồm các khối xếp theo đúng tư duy lâm sàng:

1. **Hồ sơ ca bệnh** — snapshot khách/loài/đàn/mắc-chết/khởi phát + **% độ đầy đủ thông tin**.
2. **Bệnh khả năng nhất** — tên bệnh, **độ tin cậy**, mức độ, **chẩn đoán phân biệt** (các bệnh dễ nhầm).
3. **Mức rủi ro ca bệnh** — Khẩn cấp / Cao / Theo dõi / Thấp, kèm **lý do** (vd "bệnh nguy hiểm · chưa có thuốc đặc trị · đã có 8 con chết").
4. **Cảnh báo an toàn / chuyển chuyên gia** — với bệnh virus nguy hiểm, hiện cờ **"không tự kê đơn"**.
5. **Cần hỏi khách thêm** — 3–5 câu hỏi bổ sung dữ kiện; **bấm để đưa thẳng vào ô soạn chat**.
6. **Cơ sở khoa học & dịch tễ** — tác nhân, thời gian ủ bệnh, đường lây, **cơ chế bệnh sinh, bệnh tích, xét nghiệm xác chẩn**.
7. **Chỉ số cảnh báo sớm** — dấu hiệu phát hiện sớm tại trại.
8. **Bước xử lý đề xuất** + **Đối với trại này nên làm gì** — phác đồ tách 4 nhóm:
   - 🔴 **Đàn đang bệnh** · 🔵 **Đàn khỏe cùng trại** · 🟢 **Người · xe · dụng cụ** · 🟣 **Theo dõi tiếp**.
9. **Ảnh hưởng & lưu ý từng bước** — bảng *Bước | Tác dụng | Lưu ý* (vd vì sao dừng vận chuyển, vì sao không tiêm heo đang sốt).
10. **Sản phẩm Nova Consumer theo vai trò** — nhóm rõ: *Sát trùng · Hỗ trợ · Vaccine cho đàn khỏe · Điều trị* (với bệnh virus, vaccine ghi "đúng đối tượng", điều trị ghi "chỉ khi có chỉ định").
11. **Nguồn** — chip tài liệu + nhãn "R&D duyệt".
12. **👉 Gợi ý cho Sales** — lập luận chốt đơn.

> **Vì sao thuyết phục:** đây là sự khác biệt lớn nhất so với chatbot thường — trả lời **có cấu trúc lâm sàng + an toàn + dẫn nguồn**, không phải một đoạn văn chung chung.

---

## 4. Quick actions — biến tư vấn thành hành động

Ngay dưới câu trả lời chẩn đoán có hàng nút:

### 4.1 Tính số lượng sản phẩm
Mở máy tính: chọn sản phẩm, nhập **số con / trọng lượng / số ngày / hao hụt** → ra **ước tính nhu cầu + số quy cách + chi phí**.
- Quy tắc minh bạch theo loại (vaccine: 1 liều/con; kháng sinh theo kg; sát trùng/điện giải theo đàn).
- Luôn gắn nhãn **"ước tính demo"** — cho chỉnh tay, nhắc đối chiếu nhãn thật.

### 4.2 Tạo đơn nháp
Dựng **giỏ hàng đề xuất** từ ca: mỗi dòng có nhãn **Ưu tiên / Bán kèm / Có điều kiện / Cần chuyên gia** + số lượng + cảnh báo.
- **Guardrail:** với bệnh virus, **không đưa kháng sinh vào nhóm "chữa bệnh"**, vaccine chỉ "có điều kiện cho đàn khỏe".
- Nút **Copy đơn** / **Lưu đơn nháp** (lưu localStorage).

### 4.3 Tạo ticket chuyên gia
Tạo **ticket mock** chuyển R&D/thú y: **mã ticket + SLA** (2 giờ nếu khẩn cấp / 24 giờ) + người phụ trách + tóm tắt ca + khuyến nghị AI. Copy/Lưu được.

### 4.4 Soạn tin nhắn gửi khách
Sinh **tin nhắn Zalo/SMS** mẫu đã lồng guardrail an toàn (vd bệnh virus → cách ly + sát trùng + báo thú y, tránh "kháng sinh chữa"). Copy gửi ngay.

---

## 5. NPP Cockpit — khai thác nhà phân phối

Hỏi *"Phân tích Đại lý Minh Phát"* (hoặc bấm năng lực **Phân tích nhà phân phối**) → ngoài biểu đồ lịch sử, có thêm:
- **Bối cảnh dịch vùng** — tỉnh của NPP đang có cảnh báo gì (tự lồng vào lời tư vấn).
- **Đơn 3 mức** — *An toàn* (nhập lại theo nhịp) → *Đề xuất* (thêm combo phòng/hỗ trợ) → *Tăng trưởng* (mở SKU mới).
- **Script gọi NPP** — Mở đầu / Lý do theo dữ liệu / Đề xuất / Câu chốt.
- **Xử lý từ chối** — sợ tồn · giá cao · chưa có nhu cầu · công nợ.
- **Task follow-up** — nhắc gọi lại theo mốc.

---

## 6. Bản đồ dịch bệnh → Chiến dịch gọi khách

Ở tab **Bản đồ dịch bệnh**, bấm một **cảnh báo gần đây** (thanh bên) → mở **Chiến dịch theo cảnh báo**:
- **NPP/khách ưu tiên gọi** (đánh dấu "trong vùng"), **Sản phẩm nên chào** theo bệnh, **Tin nhắn mẫu**.
- Copy tin nhắn / **Lưu chiến dịch**.

Chi tiết tab bản đồ: **[Huong-dan-Ban-do-dich-benh.md](Huong-dan-Ban-do-dich-benh.md)**.

---

## 7. Hồ sơ người dùng — vai trò & dashboard

Bấm **avatar (NS)** góc phải trên:
- **Đổi vai trò mô phỏng** — Sales / Quản lý / R&D.
- **Bảng theo dõi** — số **Ca đang mở · Đơn nháp · Ticket chuyên gia · Chiến dịch · Cảnh báo nặng**.
- **Xuất JSON** (copy toàn bộ dữ liệu phiên) · **Reset demo** (xóa dữ liệu đã lưu, về dữ liệu mẫu).

---

## 8. Guardrails an toàn (luôn bật)

| Tình huống | Hành vi của trợ lý |
|---|---|
| Bệnh virus nguy hiểm (ASF, FMD, Newcastle, HPAI…) | Cờ **"chuyển chuyên gia — không tự kê đơn"**; không bán kháng sinh như thuốc "chữa" |
| Vaccine | Chỉ **đúng đối tượng** (không nái mang thai/heo-gà đang ốm) |
| Kháng sinh | Nhắc **thời gian ngừng thuốc** + nguyên tắc **dùng có trách nhiệm (AMR)** |
| Thiếu dữ kiện (trọng lượng/loài) | Không tính liều chắc chắn; gắn nhãn **"ước tính demo"** |
| Mọi câu trả lời | **Dẫn nguồn** tài liệu "R&D duyệt"; số liệu từ KB, không để mô hình bịa |

---

## 9. Lưu ý kỹ thuật

- **Mở qua máy chủ** (vd `python3 -m http.server` trong thư mục `AI4Sales/`) vì ứng dụng nạp `data/*.json`. Mở trực tiếp file sẽ không tải được dữ liệu.
- Cần **Internet** để tải React/bản đồ nền (CDN).
- Dữ liệu ca/đơn/ticket/chiến dịch lưu **localStorage** trên máy đang mở — chưa đồng bộ nhiều máy. Khi triển khai thật chỉ cần nối **API/CRM/DMS**, **giữ nguyên schema** (`cases`, `draft_orders`, `expert_tickets`, `campaigns`, `alerts`).

---

## 10. Bảng "tính năng → giá trị"

| Tính năng | Giải quyết nỗi đau | Giá trị thể hiện khi demo |
|---|---|---|
| Tạo ca bệnh + chẩn đoán sâu | Tư vấn phụ thuộc vài chuyên gia | Chuẩn hóa tư vấn lâm sàng cho mọi Sale |
| Phác đồ tách đàn + bảng ảnh hưởng | Lời khuyên chung chung | Hành động cụ thể theo đàn bệnh/khỏe |
| Tính số lượng + đơn nháp | Từ tư vấn không ra đơn | Nối kỹ thuật → doanh số đo được |
| Ticket chuyên gia (SLA) | Ca khó không có quy trình | Cơ chế an toàn, không bỏ rơi ca nặng |
| NPP Cockpit (3 mức + objection) | Chào hàng cảm tính | Chốt đơn dựa trên dữ liệu |
| Bản đồ → chiến dịch | Dịch tễ rời rạc | Phát hiện dịch → hành động bán hàng |
| Dashboard theo vai trò | Thiếu bức tranh quản trị | Quản lý nhìn được toàn cảnh |
| Guardrails + dẫn nguồn | AI bịa, bán bừa | An toàn, có trách nhiệm, truy xuất nguồn |
