# Bộ 10 câu hỏi demo AI SalesMate — thuyết phục đội ngũ khoa học SaigonVet

> ⚠️ **Bản cũ (lưu trữ).** Bản hiện hành đã cập nhật theo phiên bản sản phẩm hóa (quy trình ca bệnh, đơn nháp, ticket, chiến dịch, NPP cockpit, câu hỏi bẫy chuyên gia): xem **[Kich-ban-cau-hoi-SaigonVet-v2.md](Kich-ban-cau-hoi-SaigonVet-v2.md)**. File này giữ lại để tham chiếu lịch sử.

> **Bối cảnh:** SaigonVet là đơn vị phân phối/kinh doanh thuốc thú y, có đội ngũ chuyên gia (bác sĩ thú y, dược, R&D) nhiều năm kinh nghiệm.
> Vì vậy phần demo không chỉ "tra cứu" mà phải cho thấy chiều sâu **khoa học** (dịch tễ, cơ chế bệnh sinh, dược lý PK/PD, bằng chứng) + giá trị **kinh doanh** (khai thác NPP, ROI).
> Mỗi câu trả lời của trợ lý đều có: cấu trúc rõ, dẫn nguồn tài liệu đã duyệt, cảnh báo an toàn và dòng **👉 Gợi ý cho Sales**.
>
> Tất cả 10 câu dưới đây đã được kiểm thử: định tuyến đúng công cụ và trả về đúng nội dung. Có thể bấm nhanh ở phần **"Câu hỏi gợi ý cho buổi demo"** trên màn hình chào, hoặc gõ trực tiếp.

---

## Vẫn giữ nguyên 4 nhóm năng lực chính

| # | Năng lực | Công cụ | Đầu ra cốt lõi |
|---|---|---|---|
| 1 | **Chẩn đoán & dự đoán bệnh** | `chan_doan_benh` | Bệnh khả năng nhất + độ tin cậy + **cơ chế bệnh sinh** + **bệnh tích** + **xét nghiệm xác chẩn** + **chỉ số cảnh báo sớm** + bước xử lý + sản phẩm + cờ "chuyển chuyên gia" |
| 2 | **Tra cứu & phân tích thuốc/vaccine** | `tra_cuu_thuoc` | Hồ sơ sản phẩm: **cơ chế tác động**, **phổ tác động**, **dược động học (PK/PD)**, bằng chứng, tiêu chuẩn GMP, tương tác, bảo quản, liều, giá |
| 3 | **Phân tích nhà phân phối** | `phan_tich_nha_phan_phoi` | Lịch sử mua, sản phẩm chủ lực, **gợi ý đơn kế tiếp**, **cơ hội bán thêm** |
| 4 | **Tra cứu tài liệu khoa học (RAG)** | `tra_cuu_tai_lieu` | Trích đoạn có dẫn nguồn từ **11 tài liệu đã duyệt** (an toàn sinh học, kỹ thuật, chính sách, dịch tễ, AMR, dược lý, bằng chứng lâm sàng, kinh tế, tiêu chuẩn chất lượng) |

---

# NHÓM 1 — Đào sâu dữ liệu: chẩn đoán, dự đoán bệnh

### Câu 1. Chẩn đoán ASF kèm cơ chế bệnh sinh và xét nghiệm xác chẩn
> **"Heo sốt cao 41 độ, bỏ ăn, da vùng tai và bụng đỏ tím, nhiều con chết nhanh, tỷ lệ chết cao. Đây là bệnh gì, cơ chế bệnh sinh và cần xét nghiệm gì để xác chẩn?"**

- **Trợ lý trả lời:** Dịch tả lợn châu Phi (ASF) với độ tin cậy + chẩn đoán phân biệt (CSF, PRRS, tụ huyết trùng) → khối **Cơ sở khoa học & dịch tễ** (tác nhân ASFV, thời gian ủ bệnh, đường lây, cơ chế nhân lên trong đại thực bào gây rối loạn đông máu, bệnh tích lách nhồi huyết, **xét nghiệm Real-time PCR xác chẩn**) → **cảnh báo sớm** → bước xử lý → cờ **"chuyển chuyên gia — không tự kê đơn"** (bệnh virus) → vaccine ASF + sát trùng.
- **Điểm thuyết phục nhà khoa học:** trợ lý phân biệt rõ "nhiễm" vs "xác chẩn", không bán kháng sinh cho bệnh virus, và chỉ đúng phương pháp PCR — đúng tư duy thú y chuẩn mực.

### Câu 2. Chẩn đoán Newcastle trên gà + hướng xử lý
> **"Đàn gà giảm đẻ đột ngột, phân xanh, vài con vẹo cổ và liệt chân, chết nhanh. Đây là bệnh gì và hướng xử lý?"**

- **Trợ lý trả lời:** Newcastle (gà rù) — triệu chứng thần kinh đặc trưng, cơ chế virus xâm nhập thần kinh trung ương, bệnh tích xuất huyết dạ dày tuyến, xét nghiệm RT-PCR/HI; cảnh báo sớm "giảm đẻ + phân xanh + thần kinh ở đàn quá lịch vaccine"; nhấn mạnh **không có thuốc đặc trị virus**, phòng bằng vaccine + an toàn sinh học.
- **Điểm thuyết phục:** cho thấy năng lực trên cả **gà** (không chỉ heo) và tư duy phòng-bệnh-bằng-vaccine.

### Câu 3. Dự đoán hội chứng còi cọc PCV2 sau cai sữa
> **"Heo sau cai sữa còi cọc chậm lớn, gầy sút dù vẫn ăn, kém đồng đều, hạch sưng. Nghi bệnh gì và phòng thế nào?"**

- **Trợ lý trả lời:** Circovirus (PCV2 / PCVAD) — cơ chế suy giảm miễn dịch do cạn kiệt mô lympho, mở đường đồng nhiễm PRRS/Mycoplasma; xác chẩn bằng PCR định lượng + hóa mô miễn dịch; khuyến nghị **vaccine PCV2** (ROI cao) + kiểm soát đồng nhiễm.
- **Điểm thuyết phục:** đây là bệnh "thiệt hại ẩn" mà chỉ người làm chuyên môn mới nhận ra — trợ lý gọi tên đúng và đưa giải pháp phòng có hiệu quả kinh tế rõ.

---

# NHÓM 2 — Phân tích thuốc/vaccine ở mức dược lý

### Câu 4. Phân tích cơ chế & dược động học một kháng sinh
> **"Phân tích sản phẩm Anova Florfen-200: cơ chế tác động, phổ tác động, dược động học và lưu ý sử dụng."**

- **Trợ lý trả lời:** hồ sơ đầy đủ — Florfenicol ức chế ribosome 50S (không gây suy tủy như chloramphenicol), phổ rộng Gram±, thấm tốt mô phổi, phác đồ 2 mũi cách 48 giờ, thời gian ngừng thuốc 14 ngày, lưu ý không dùng cho đực giống. Dẫn nguồn **dược lý PK/PD** + **AMR**.
- **Điểm thuyết phục:** trả lời ở tầng **cơ chế phân tử & PK/PD**, không phải chỉ "công dụng — liều" — đúng "gu" của dược sĩ/R&D.

### Câu 5. Hồ sơ vaccine chủ lực
> **"Cho tôi hồ sơ vaccine NAVET-ASFVAC: cơ chế, đối tượng, bảo quản và giá bán."**

- **Trợ lý trả lời:** vaccine nhược độc đông khô, cơ chế tạo miễn dịch chủ động, chỉ dùng cho heo thịt khỏe đúng đối tượng, **chuỗi lạnh 2-8°C**, kiểm nghiệm từng lô (GMP), giá. Dẫn nguồn **tiêu chuẩn chất lượng & chuỗi lạnh**.
- **Điểm thuyết phục:** nhấn mạnh chuỗi lạnh & QA lô — yếu tố quyết định hiệu lực vaccine mà khách khoa học rất coi trọng.

---

# NHÓM 3 — Kiến thức khoa học & nguồn thông tin đa dạng (RAG)

### Câu 6. Sử dụng kháng sinh có trách nhiệm & AMR
> **"Nguyên tắc sử dụng kháng sinh có trách nhiệm và giảm kháng kháng sinh (AMR) trong chăn nuôi?"**

- **Trợ lý trả lời:** trích tài liệu AMR — 5 nguyên tắc, nhóm kháng sinh dự trữ (fluoroquinolone, colistin), giảm kháng sinh bằng phòng bệnh chủ động, tồn dư & an toàn thực phẩm.
- **Điểm thuyết phục:** thể hiện trợ lý "bán hàng có trách nhiệm", phù hợp xu hướng giảm kháng sinh — chạm đúng giá trị nghề nghiệp của chuyên gia.

### Câu 7. Nguyên lý dược lý PK/PD
> **"Giải thích nguyên lý dược động học và dược lực học (PK/PD) trong thú y: Cmax/MIC, T>MIC và cách phối hợp kháng sinh tránh đối kháng."**

- **Trợ lý trả lời:** trích tài liệu dược lý — diệt khuẩn phụ thuộc nồng độ vs thời gian, vì sao "đủ liều, đúng nhịp, đủ ngày", và các cặp phối hợp hiệp đồng/đối kháng.
- **Điểm thuyết phục:** đây là kiến thức hàn lâm — chứng minh trợ lý "nói cùng ngôn ngữ" với đội ngũ R&D.

### Câu 8. Dự đoán & cảnh báo sớm dịch theo dịch tễ học
> **"Làm sao dự đoán và cảnh báo sớm nguy cơ bùng dịch theo mùa và theo chỉ số R0?"**

- **Trợ lý trả lời:** trích tài liệu dịch tễ — ý nghĩa R0 và miễn dịch cộng đồng, đường cong dịch, yếu tố nguy cơ theo mùa, **bộ chỉ số cảnh báo sớm tại trại** và giám sát huyết thanh để phòng theo dữ liệu.
- **Điểm thuyết phục:** nâng AI từ "tra cứu" lên "**phân tích dự báo**" — đúng kỳ vọng "đào sâu dữ liệu".

---

# NHÓM 4 — Hỗ trợ bán hàng & kinh tế

### Câu 9. ROI của phòng bệnh (lập luận chốt đơn bằng con số)
> **"Phân tích hiệu quả kinh tế (ROI) của tiêm vaccine và an toàn sinh học so với chi phí một ổ dịch?"**

- **Trợ lý trả lời:** trích tài liệu kinh tế chăn nuôi — cấu trúc chi phí (cám 60-70%, FCR), ROI cao của vaccine/an toàn sinh học, chi phí một ổ dịch và giá trị phát hiện sớm, tư duy giỏ hàng theo phác đồ.
- **Điểm thuyết phục:** chuyển từ "giá thuốc" sang "**lợi nhuận trên đầu con**" — ngôn ngữ ra quyết định của ban lãnh đạo/khoa học.

### Câu 10. Khai thác nhà phân phối (bán hàng dựa trên dữ liệu)
> **"Phân tích nhà phân phối Đại lý Minh Phát và gợi ý đơn kế tiếp + cơ hội bán thêm."**

- **Trợ lý trả lời:** biểu đồ lịch sử mua theo tháng, sản phẩm chủ lực, **gợi ý đơn kế tiếp theo nhịp mua**, **cơ hội cross-sell** (ưu tiên vaccine ASF & sát trùng mà NPP chưa nhập), kèm cảnh báo công nợ.
- **Điểm thuyết phục:** biến lịch sử bán hàng thành hành động bán cụ thể — giá trị thương mại đo được ngay.

---

## Câu hỏi mở rộng (bonus — nếu khách muốn thử thêm)

- **Gumboro (gà):** *"Gà 3-6 tuần ủ rũ đột ngột, tiêu chảy phân trắng nhớt, run rẩy, tự mổ lỗ huyệt, chết tăng nhanh rồi giảm. Bệnh gì?"* → IBD, điểm nhấn **chọn thời điểm tiêm theo ELISA kháng thể mẹ truyền (công thức Deventer)** — kỹ thuật cao cấp.
- **Cúm gia cầm H5N1:** *"Gà chết đột ngột hàng loạt, mào tích tím tái, xuất huyết da chân, nghi cúm gia cầm H5N1. Xử lý?"* → HPAI, cảnh báo **bệnh phải công bố dịch + nguy cơ lây sang người**.
- **Tiêu chảy E.coli heo con:** *"Heo con sau cai sữa tiêu chảy phân trắng vàng, mất nước. Phác đồ và sản phẩm?"* → đặc trị + **bù điện giải + men vi sinh** (giảm kháng sinh).
- **Chính sách:** *"Chính sách chiết khấu và chương trình khuyến mãi hiện hành?"* → trích chính sách kinh doanh đã duyệt.

---

## Gợi ý kịch bản trình diễn (8-10 phút)

1. **Mở đầu bằng ASF (Câu 1)** — ca "đau" nhất, cho thấy chiều sâu khoa học + an toàn (không tự kê đơn).
2. **Phân tích thuốc (Câu 4)** — chứng minh tầng dược lý PK/PD.
3. **Kiến thức khoa học (Câu 6/7/8)** — khoe nguồn tài liệu đa dạng đã duyệt.
4. **Kinh tế + NPP (Câu 9 → 10)** — chốt bằng giá trị kinh doanh đo được.
5. **Bonus** theo câu hỏi tự do của khách để thể hiện độ phủ (gà, cúm, Gumboro…).

---

## Vì sao bộ câu hỏi này thuyết phục được nhà khoa học

- **Chiều sâu, không chỉ tra cứu:** mỗi câu đều chạm tới cơ chế bệnh sinh / dược lý / dịch tễ / bằng chứng — thay vì chỉ "công dụng — liều — giá".
- **Đa dạng nguồn thông tin:** 11 tài liệu đã duyệt (R&D & Kinh doanh) gồm cả dịch tễ học, AMR, dược lý PK/PD, bằng chứng lâm sàng, kinh tế chăn nuôi và tiêu chuẩn chất lượng — mọi câu trả lời đều **dẫn nguồn**.
- **An toàn & có trách nhiệm:** tự động gắn cờ "chuyển chuyên gia" với bệnh virus, nhắc thời gian ngừng thuốc và nguyên tắc giảm kháng sinh.
- **Gắn khoa học với kinh doanh:** kết mỗi câu bằng **👉 Gợi ý cho Sales** và lập luận ROI — đúng mục tiêu "đi bán hàng".

> *Lưu ý: số liệu định lượng (giá, tỷ lệ, dịch tễ) trong bản demo là dữ liệu mẫu (DEMO) để minh họa luồng xử lý. Khi triển khai thật chỉ cần thay bằng catalogue/KB/CRM thật — giữ nguyên schema và kiến trúc.*
