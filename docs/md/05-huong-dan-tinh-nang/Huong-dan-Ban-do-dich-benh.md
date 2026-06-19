# Hướng dẫn & kịch bản: Tab "Bản đồ dịch bệnh" (heatmap thị trường)

> Tính năng của AI SalesMate giúp đội Sale **nhập thông tin dịch bệnh từ thực địa** → hiển thị **heatmap (bản đồ nhiệt) toàn quốc** → nhìn ra **điểm nóng** → **tạo chiến dịch gọi khách trong vùng** tư vấn nhập hàng phòng dịch (vaccine, sát trùng, bổ trợ).
> Tài liệu này gồm 2 phần: (A) Hướng dẫn sử dụng từng bước, (B) Kịch bản trình bày cho khách (SaigonVet).
> Tổng quan toàn bộ tính năng sản phẩm: xem **[Huong-dan-Tinh-nang-AI-SalesMate.md](Huong-dan-Tinh-nang-AI-SalesMate.md)**.

---

## A. HƯỚNG DẪN SỬ DỤNG

### 1. Tính năng giải quyết vấn đề gì?
- **Trước đây:** thông tin dịch bệnh nằm rải rác trong đầu từng Sale/tin nhắn → không ai có bức tranh tổng thể, phản ứng chậm, bỏ lỡ cơ hội bán hàng phòng dịch.
- **Bây giờ:** mọi Sale nhập nhanh ca dịch gặp ngoài thị trường → hệ thống gom lại thành **bản đồ nhiệt theo tỉnh** → cả đội thấy vùng nào đang "nóng", bệnh nào đang lan → **chủ động tư vấn khách nhập hàng đúng lúc**.

### 2. Mở tính năng
1. Trên thanh tiêu đề (góc phải), bấm tab **"Bản đồ dịch bệnh"** (cạnh tab "Trợ lý tư vấn").
2. Bản đồ Việt Nam hiện ra với các **vùng màu nóng** thể hiện mật độ cảnh báo dịch.
   - Bấm lại **"Trợ lý tư vấn"** để quay về phần chat tư vấn (4 năng lực cũ) bất cứ lúc nào — hai phần độc lập, không ảnh hưởng nhau.

### 3. Đọc bản đồ nhiệt (heatmap)
- **Màu sắc = mật độ/độ nặng cảnh báo** tại khu vực đó. Theo chú giải góc dưới trái:
  - Xanh dương → xanh nhạt → vàng → cam → **đỏ** = từ **Thấp đến Cao**.
  - Vùng càng đỏ/càng rộng → càng nhiều cảnh báo hoặc mức độ càng nặng → **ưu tiên chú ý trước**.
- **Thanh thống kê nhanh** (ngay trên bản đồ):
  - **Tổng cảnh báo** — số ca đang theo dõi.
  - **Bệnh nổi bật** — bệnh có nhiều cảnh báo nhất (vd: Dịch tả lợn châu Phi).
  - **Tỉnh nổi bật** — địa bàn nhiều cảnh báo nhất (vd: Đồng Nai).
  - **Cảnh báo mức nặng** — số ca mức "Nặng".
- Có thể **phóng to/thu nhỏ** (nút +/− hoặc cuộn chuột) và kéo bản đồ để xem từng vùng.

### 4. Nhập thông tin thị trường (cập nhật ca dịch mới)
1. Bấm nút **"＋ Nhập thông tin thị trường"** (góc phải trên bản đồ).
2. Điền popup:
   | Trường | Ý nghĩa | Ví dụ |
   |---|---|---|
   | **Loại vật nuôi** | Đối tượng mắc bệnh | Heo / Gà / Vịt / Trâu-Bò / Khác |
   | **Khu vực / Tỉnh thành** | Địa bàn ghi nhận (quyết định vị trí trên bản đồ) | Đồng Nai, Long An, Bắc Giang… |
   | **Loại dịch bệnh** | Chọn từ **danh mục bệnh chuẩn** (master data — 14 bệnh) để thống kê nhất quán | Dịch tả lợn châu Phi (ASF), Newcastle, Gumboro… |
   | **Mức độ** | Độ nặng để tô đậm điểm nóng | Nhẹ / Trung bình / Nặng |
   | **Ghi chú mô tả** | Mô tả triệu chứng, số ca, quy mô đàn | "Heo chết nhanh, da tai bụng tím, ~30 con" |
3. Bấm **"Lưu cảnh báo"** → điểm mới **xuất hiện ngay trên heatmap**, thống kê tự cập nhật.
   - Thiếu **Tỉnh/thành** hoặc **Loại dịch bệnh** sẽ được nhắc điền (2 trường bắt buộc để định vị + thống kê).

### 5. Tạo chiến dịch gọi khách từ cảnh báo (mới)
Mỗi mục trong **"Cảnh báo gần đây"** (thanh bên) giờ **bấm được**:
1. Bấm một cảnh báo → mở cửa sổ **"Chiến dịch theo cảnh báo"** (mã `CMP-…`).
2. Cửa sổ tự dựng sẵn:
   - **NPP / khách ưu tiên gọi** — lọc và **đánh dấu "trong vùng"** từ `distributors.json`.
   - **Sản phẩm nên chào** — theo đúng bệnh của cảnh báo (vd ASF → NAVET-ASFVAC + Iodine 10%).
   - **Tin nhắn mẫu** — soạn sẵn để gửi Zalo/SMS.
3. Bấm **Copy tin nhắn** hoặc **Lưu chiến dịch** (lưu localStorage, đếm vào dashboard).

> Đây là bước biến bản đồ từ "để xem" thành **hành động bán hàng cụ thể**.

### 6. Vì sao chọn bệnh từ "master data"?
Loại dịch bệnh lấy từ danh mục bệnh chuẩn của hệ thống (`diseases.json`) thay vì gõ tự do → tránh sai chính tả, **gộp đúng số liệu thống kê** (vd mọi cách viết "ASF / dịch tả lợn" đều quy về 1 bệnh) → biểu đồ và bản đồ chính xác.

### 7. Lưu ý
- Cần **kết nối Internet** để tải bản đồ nền (bản đồ là dữ liệu trực tuyến).
- Trong bản trình bày hiện tại, dữ liệu nhập là **trong phiên làm việc** (tải lại trang sẽ trở về dữ liệu mẫu). Khi triển khai thật, chỉ cần nối **API/cơ sở dữ liệu** để lưu vĩnh viễn và đồng bộ cho cả đội — giữ nguyên cấu trúc dữ liệu (`provinces_vn.json`, `market_alerts.json`).

---

## B. KỊCH BẢN TRÌNH BÀY CHO KHÁCH (SaigonVet)

> Mục tiêu: cho thấy tính năng biến **thông tin dịch tễ rời rạc** thành **hành động bán hàng cụ thể**, và **liên thông** với phần tư vấn AI.

### Bước 1 — Mở bức tranh toàn cảnh (10 giây gây ấn tượng)
- Bấm tab **"Bản đồ dịch bệnh"**. Chỉ vào các **điểm nóng đỏ ở Đông Nam Bộ & ĐBSCL** (Đồng Nai, Long An, Đồng Tháp…): *"Đây là bức tranh dịch theo thời gian thực do chính đội Sale nhập về."*
- Đọc nhanh thanh thống kê: *"Hệ thống tự tổng hợp: bệnh nổi bật là **Dịch tả lợn châu Phi**, nóng nhất ở **Đồng Nai**, có **6 ca mức nặng**."*

### Bước 2 — Nhập một ca mới ngay trước mặt khách (cho thấy sự đơn giản)
- Bấm **"＋ Nhập thông tin thị trường"**, điền: Heo · **Tiền Giang** · **Dịch tả lợn châu Phi (ASF)** · Nặng · "trại 200 con, heo chết nhanh".
- Bấm **Lưu** → *"Chỉ 10 giây, điểm nóng mới hiện ngay trên bản đồ và thống kê nhảy số. Mỗi Sale ngoài thị trường đều góp dữ liệu như vậy."*

### Bước 3 — Biến điểm nóng thành chiến dịch gọi khách (1 cú bấm)
- Ở thanh bên, **bấm cảnh báo ASF Đồng Nai** → cửa sổ **"Chiến dịch theo cảnh báo"** hiện ra với **NPP ưu tiên (đánh dấu trong vùng) + sản phẩm nên chào (NAVET-ASFVAC, Iodine 10%) + tin nhắn mẫu**.
- Chốt: *"Khi một vùng đỏ lên vì ASF, chỉ một cú bấm là có ngay **danh sách gọi + sản phẩm + tin nhắn** — bán đúng nhu cầu, đúng thời điểm."* Bấm **Lưu chiến dịch** để theo dõi.

### Bước 4 — Liên thông sang tư vấn chuyên sâu (sức mạnh kép)
- Bấm sang tab **"Trợ lý tư vấn"**, hỏi: *"Heo sốt cao, da tai bụng đỏ tím, chết nhanh — bệnh gì, xử lý và sản phẩm nào?"*
- → AI trả lời ASF kèm cơ chế bệnh sinh, cảnh báo "chuyển chuyên gia", và **gợi ý sản phẩm + 👉 Gợi ý cho Sales**.
- Chốt thông điệp: *"Bản đồ cho biết **ở đâu, đang nóng cái gì**; Trợ lý cho biết **tư vấn thế nào, bán gì** — khép kín từ phát hiện dịch đến chốt đơn phòng dịch."*

### Bước 5 — Mở rộng theo địa bàn của khách
- Hỏi khách họ mạnh ở vùng nào, nhập thử 1–2 ca ở vùng đó (vd gà ở **Bắc Giang — Gumboro**, hoặc **Hải Dương — Cúm gia cầm**) để bản đồ "sống" đúng địa bàn họ quan tâm.

---

## Tóm tắt 1 câu để chốt
> *"Bản đồ dịch bệnh biến mỗi nhân viên Sale thành một 'trạm quan trắc dịch tễ', gom thành bức tranh toàn quốc, để cả đội chủ động tư vấn khách nhập hàng phòng dịch — đúng vùng, đúng bệnh, đúng lúc."*
