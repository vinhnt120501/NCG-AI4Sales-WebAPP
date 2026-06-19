# Kịch bản demo AI SalesMate — thuyết phục đội ngũ khoa học SaigonVet

> **Phiên bản hiện hành (đã cập nhật theo bản sản phẩm hóa).** Thay thế bản v1.
>
> **Bối cảnh:** SaigonVet là đơn vị phân phối/kinh doanh thuốc thú y, có đội ngũ chuyên gia (bác sĩ thú y, dược, R&D) nhiều năm kinh nghiệm. Họ sẽ **vặn câu hỏi khó** để kiểm tra chiều sâu và độ an toàn. Kịch bản này được thiết kế để **đón trước những câu khó nhất** và biến chúng thành điểm cộng.
>
> Mỗi câu trả lời cho thấy đồng thời: chiều sâu **khoa học** (dịch tễ · cơ chế bệnh sinh · dược lý PK/PD · bằng chứng), **an toàn có trách nhiệm** (cờ chuyển chuyên gia, AMR, thời gian ngừng thuốc), và giá trị **kinh doanh** (ca bệnh → đơn nháp → chiến dịch → khai thác NPP). Mọi câu đều **dẫn nguồn tài liệu đã duyệt** và kết bằng **👉 Gợi ý cho Sales**.
>
> **Đã kiểm thử trên đúng dữ liệu trong `AI4Sales/`** — 14 bệnh · 19 sản phẩm · 4 NPP · 11 tài liệu R&D/Kinh doanh. Định tuyến đúng công cụ, trả về đúng thực thể, render đúng các khối giao diện mô tả bên dưới.

---

## 0. Điểm mới so với bản trình bày trước: từ "chatbot tra cứu" thành "trợ lý hiện trường"

Bản trước chỉ trả lời một lượt. Bản này dựng **một quy trình sản phẩm khép kín** — đây mới là thứ thuyết phục người đã quen với chatbot:

```
Tạo ca bệnh  →  Chẩn đoán sâu (risk · phác đồ theo đàn · ảnh hưởng từng bước)
            →  Tính số lượng  →  Đơn nháp  →  Ticket chuyên gia (SLA)
            →  Bản đồ dịch → Chiến dịch gọi khách  →  Cockpit khai thác NPP
            →  Dashboard theo vai trò (Sales / Quản lý / R&D)
```

> **Lời hứa 60 giây:** từ một mô tả triệu chứng ngoài thực địa → ra **chẩn đoán có cơ sở khoa học + phác đồ tách đàn bệnh/đàn khỏe + đơn hàng đề xuất có cảnh báo an toàn** — việc mà trước đây Sale phải gọi điện hỏi chuyên gia và mất 10–15 phút.

---

# NHÓM 1 — Chẩn đoán & dự đoán bệnh
*Năng lực `chan_doan_benh`. Đầu ra (bản mới): **Hồ sơ ca** · **Bệnh khả năng nhất + độ tin cậy + chẩn đoán phân biệt** · **Mức rủi ro** · **Cần hỏi thêm** · **Cơ sở khoa học & dịch tễ** · **Cảnh báo sớm** · **Phác đồ tách đàn bệnh/đàn khỏe/an toàn sinh học/theo dõi** · **Bảng ảnh hưởng từng bước** · **Sản phẩm phân nhóm theo vai trò** · cờ **chuyển chuyên gia**.*

### 1.1 — ASF: phân biệt với CSF/PRRS khi cả ba đều "sốt + xuất huyết"
> **"Heo sốt 41°C, da tai–bụng đỏ tím, chết nhanh tỷ lệ cao. Làm sao phân biệt ASF với Dịch tả cổ điển (CSF) và Tai xanh (PRRS) khi cả ba đều sốt + xuất huyết, và cần xét nghiệm gì để xác chẩn?"**
- → **Dịch tả lợn châu Phi (ASF)** đứng đầu; **chẩn đoán phân biệt** liệt kê CSF, PRRS, tụ huyết trùng. Khối **Cơ sở khoa học & dịch tễ**: ASFV nhân lên trong đại thực bào → rối loạn đông máu (DIC); **bệnh tích chỉ điểm: lách sưng nhồi huyết**, hạch xuất huyết như cục máu đông. **Xác chẩn Real-time PCR (máu EDTA, lách, hạch)** — ELISA/IFA chỉ cho heo sống qua giai đoạn. **Mức rủi ro: Khẩn cấp**; cờ **"chuyển chuyên gia — không tự kê đơn"**.
- *Vì sao thuyết phục:* trợ lý **phân biệt rạch ròi "nghi" vs "xác chẩn"** và chỉ đúng PCR — đúng tư duy thú y chuẩn mực, không phán bừa.

### 1.2 — PRRS: cơ chế "mở đường" cho kế phát vi khuẩn
> **"Nái tăng sảy thai/đẻ non, heo con sơ sinh yếu, heo thịt ho khó thở cụm theo ô, tai tím từng đợt. Bệnh gì, cơ chế và vì sao hay kèm bệnh khác?"**
- → **Tai xanh (PRRS)**: đặc trưng rối loạn sinh sản ở nái; cơ chế **virus tấn công đại thực bào phế nang gây suy giảm miễn dịch → mở đường kế phát suyễn/APP/tụ huyết trùng**. Xét nghiệm **RT-PCR máu/oral fluid định type, ELISA giám sát đàn, giải trình tự ORF5 truy vết chủng**.
- *Vì sao thuyết phục:* gọi đúng cơ chế "bệnh nền miễn dịch" mà chỉ chuyên môn mới giải thích được — và đó là lý do phác đồ ưu tiên ổn định đàn + kiểm soát kế phát, không chỉ "trị triệu chứng".

### 1.3 — PCV2: gọi tên "thiệt hại ẩn" sau cai sữa
> **"Heo sau cai sữa còi cọc, gầy dần dù vẫn ăn, kém đồng đều, hạch bẹn to, đáp ứng kháng sinh kém. Nghi bệnh gì và phòng thế nào?"**
- → **Circovirus (PCV2/PCVAD)**: cơ chế **cạn kiệt mô lympho → suy giảm miễn dịch → đồng nhiễm**; xác chẩn **PCR định lượng tải lượng + hóa mô miễn dịch (IHC) tại hạch**. Khuyến nghị **vaccine PCV2 (VX07)** — ROI cao. Lưu ý dấu hiệu "đáp ứng kháng sinh kém" chính là chỉ điểm bệnh virus nền.
- *Vì sao thuyết phục:* đây là bệnh dễ bị bỏ sót; trợ lý gọi đúng tên và chỉ ra **vì sao kháng sinh không phải lời giải**.

> **Mở rộng nhanh:** **Gumboro** *"Gà 3–6 tuần ủ rũ đột ngột, tiêu chảy phân trắng nhớt, run rẩy, tự mổ lỗ huyệt, chết tăng nhanh rồi giảm"* → IBD, điểm nhấn **chọn thời điểm tiêm theo ELISA kháng thể mẹ truyền (công thức Deventer)**. · **HPAI** *"Đàn gà mào tích tím tái, phù đầu, xuất huyết da chân, chết đột ngột hàng loạt trong 1–2 ngày"* → cảnh báo **bắt buộc báo dịch khẩn + nguy cơ lây sang người**, DỪNG thao tác. · **E.coli heo con** → đặc trị + **bù điện giải + men vi sinh** (giảm kháng sinh).

---

# NHÓM 2 — Tra cứu & phân tích thuốc/vaccine
*Năng lực `tra_cuu_thuoc`. Đầu ra: hồ sơ gồm **cơ chế tác động** · **phổ** · **dược động học (PK/PD)** · **bằng chứng** · **GMP** · **tương tác/lưu ý** · **bảo quản** · liều · giá · cảnh báo chống chỉ định & thời gian ngừng thuốc.*

### 2.1 — Florfenicol ở tầng cơ chế phân tử + PK/PD
> **"Phân tích Anova Florfen-200: cơ chế, phổ, vì sao phác đồ 2 mũi cách 48 giờ, và khác chloramphenicol ở điểm nào?"**
- → **Florfenicol (phenicol)** ức chế **ribosome 50S — kìm khuẩn phổ rộng, KHÔNG gây suy tủy như chloramphenicol** (khác biệt an toàn then chốt). Phổ **Pasteurella, APP, Haemophilus**, kể cả chủng kháng tetracycline. PK **thấm tốt mô phổi, dạng tác dụng kéo dài → 2 mũi/48 giờ**. **Ngừng thuốc 14 ngày**; không dùng cho đực giống khai thác tinh.
- *Vì sao thuyết phục:* trả lời ở **tầng cơ chế & PK/PD**, không phải "công dụng – liều" — đúng "gu" dược sĩ/R&D.

### 2.2 — Fluoroquinolone: Cmax/MIC và "kháng sinh dự trữ"
> **"Anova Enroflox 10% nên dùng 1 lần/ngày liều cao hay chia nhiều lần? Và có nên dùng tuyến đầu không?"**
- → **Enrofloxacin** ức chế **DNA-gyrase/topoisomerase IV — diệt khuẩn phụ thuộc nồng độ → tối ưu khi Cmax/MIC cao → đủ liều 1 lần/ngày** (không nên chia nhỏ). Cảnh báo **CIA — kháng sinh quan trọng, hạn chế tuyến đầu, ưu tiên theo kháng sinh đồ**; **tránh ion kim loại (Ca/Mg/Al) làm giảm hấp thu**; ngừng thuốc heo 10 ngày, **không dùng cho gà đẻ lấy trứng**.
- *Vì sao thuyết phục:* trợ lý áp đúng **nguyên lý PK/PD** vào liều thực tế và **chủ động cảnh báo dùng có trách nhiệm** — chứ không "bán bằng mọi giá".

### 2.3 — Vaccine ASF: chuỗi lạnh & QA lô quyết định hiệu lực
> **"Hồ sơ vaccine NAVET-ASFVAC: cơ chế, đối tượng và điều kiện bảo quản?"**
- → Vaccine **nhược độc đông khô**, tạo **miễn dịch chủ động (kháng thể + tế bào)**, **chỉ cho heo thịt khỏe đúng đối tượng** (không nái mang thai/đực giống/heo đang ốm). Mục bảo quản nêu **chuỗi lạnh 2–8°C**; thẻ sản phẩm **tự dẫn nguồn *tiêu chuẩn chất lượng & chuỗi lạnh vaccine*** (kiểm nghiệm từng lô theo GMP) — yếu tố sống còn của hiệu lực.
- *Vì sao thuyết phục:* nhà khoa học rất coi trọng QA lô & chuỗi lạnh — đây là điểm app chủ động nêu.

> **Mở rộng:** **Cocci-Stop (Toltrazuril)** → tác động **mọi giai đoạn nội bào của Eimeria**, lưu ý **luân phiên hoạt chất tránh kháng** + kết hợp Vitamin K. · **Vaccine Gumboro (IBD)** → chọn thời điểm theo **ELISA kháng thể mẹ truyền**.

---

# NHÓM 3 — Phân tích & khai thác nhà phân phối (NPP Cockpit)
*Năng lực `phan_tich_nha_phan_phoi`. Đầu ra (bản mới): lịch sử mua + sản phẩm chủ lực + **Bối cảnh dịch vùng** + **Đơn 3 mức (an toàn / đề xuất / tăng trưởng)** + **Script gọi NPP** + **Xử lý từ chối** + task follow-up.*

### 3.1 — Khai thác đại lý lớn: đơn 3 mức + xử lý từ chối "giá cao / sợ tồn"
> **"Phân tích Đại lý Minh Phát và đề xuất đơn kế tiếp, kèm cách xử lý nếu khách kêu giá cao hoặc sợ tồn."**
- → Biểu đồ mua theo tháng, chủ lực NAVET-ASFVAC + Enroflox. **Cockpit** dựng 3 mức: **An toàn** (nhập lại theo nhịp) → **Đề xuất** (thêm điện giải/sát trùng) → **Tăng trưởng** (mở SKU mới: vaccine FMD/PRRS chưa nhập). **Bối cảnh vùng**: Đồng Nai đang có cảnh báo ASF → nhu cầu phòng dịch tăng (tự lồng vào script gọi). **Xử lý từ chối** sẵn 4 kịch bản: *sợ tồn → bắt đầu mức an toàn*, *giá cao → so trên hiệu quả/đầu con + gắn chiết khấu theo sản lượng*, *chưa có nhu cầu → vùng đang có áp lực dịch*, *công nợ → xếp lịch theo đợt bán*.
- *Vì sao thuyết phục:* biến lịch sử bán thành **kịch bản chốt đơn có dữ liệu**, không cảm tính.

### 3.2 — Phát hiện rủi ro chuyên môn để mở đơn vaccine
> **"Phân tích Trại heo Tân Hưng (Long An): chỉ ra rủi ro dịch và cơ hội bán thêm vaccine."**
- → Trại ~5.000 heo, tập trung kháng sinh hô hấp + sát trùng nhưng **chưa có vaccine ASF/PRRS dù mật độ cao** → rủi ro dịch lớn; gợi ý mở đơn vaccine phòng. Gắn **bối cảnh dịch vùng** nếu Long An có cảnh báo.
- *Vì sao thuyết phục:* tư vấn dựa trên **rủi ro chuyên môn**, gắn thẳng với cơ hội bán — đúng vai "trợ lý kỹ thuật cho Sale".

---

# NHÓM 4 — Tra cứu tài liệu khoa học (RAG)
*Năng lực `tra_cuu_tai_lieu`. Đầu ra: trích đoạn **dẫn nguồn** từ 11 tài liệu đã duyệt (R&D & Kinh doanh).*

### 4.1 — PK/PD: phối hợp kháng sinh tránh đối kháng
> **"Giải thích Cmax/MIC vs T>MIC, và vì sao không nên phối hợp tùy tiện kháng sinh diệt khuẩn với kìm khuẩn?"**
- → Trích *dược lý PK/PD*: **diệt khuẩn phụ thuộc nồng độ (fluoroquinolone, aminoglycoside) vs phụ thuộc thời gian T>MIC (beta-lactam, phenicol)**; nguyên tắc "đủ liều – đúng nhịp – đủ ngày"; **cặp đối kháng** (beta-lactam đang cần vi khuẩn phân chia + kìm khuẩn làm dừng phân chia → giảm hiệu lực).
- *Vì sao thuyết phục:* kiến thức hàn lâm — chứng minh trợ lý "**nói cùng ngôn ngữ**" với R&D.

### 4.2 — AMR & kháng sinh dự trữ
> **"Nguyên tắc dùng kháng sinh có trách nhiệm, nhóm dự trữ và cách giảm kháng kháng sinh trong chăn nuôi?"**
- → 5 nguyên tắc; nhóm **dự trữ (fluoroquinolone, colistin, cephalosporin thế hệ cao)**; **giảm kháng sinh bằng phòng bệnh chủ động (vaccine, an toàn sinh học, men vi sinh)**; tồn dư & an toàn thực phẩm.
- *Vì sao thuyết phục:* định vị giải pháp là **"bán hàng có trách nhiệm"** — chạm đúng giá trị nghề nghiệp.

### 4.3 — Dịch tễ học: R0 & cảnh báo sớm
> **"Dự đoán và cảnh báo sớm nguy cơ bùng dịch theo R0, đường cong dịch và tính mùa vụ?"**
- → Trích *dịch tễ học*: ý nghĩa **R0 & miễn dịch cộng đồng**, đường cong dịch, yếu tố nguy cơ theo mùa, **bộ chỉ số cảnh báo sớm tại trại**, giám sát huyết thanh để **lập lịch phòng theo dữ liệu** — liên thông với tab Bản đồ dịch bệnh.
- *Vì sao thuyết phục:* nâng AI từ "tra cứu" lên "**phân tích dự báo**".

### 4.4 — Tư duy phản biện về bằng chứng (đắt giá với nhà khoa học)
> **"Dựa vào thang bằng chứng và nghiên cứu lâm sàng, làm sao đánh giá một sản phẩm hiệu quả thật sự chứ không phải quảng cáo?"**
- → Trích *nghiên cứu lâm sàng & bằng chứng*: **thang bằng chứng** (RCT có đối chứng > lời chứng), chỉ số hiệu quả nên theo dõi (FCR, tỷ lệ chết, ngày tuổi xuất chuồng), **đọc nhãn/hồ sơ một cách phản biện**.
- *Vì sao thuyết phục:* trợ lý dạy người dùng **phản biện chính dữ liệu** — thể hiện sự trung thực khoa học, hiếm có ở công cụ bán hàng.

> **Mở rộng kinh tế:** *"ROI của vaccine & an toàn sinh học so với chi phí một ổ dịch?"* → cấu trúc chi phí (cám 60–70%, FCR), **ROI cao của phòng bệnh**, chi phí một ổ dịch & giá trị phát hiện sớm — ngôn ngữ ra quyết định của ban lãnh đạo.

---

# NHÓM 5 — Câu hỏi KHÓ / "bẫy chuyên gia" (phần ăn điểm nhất)

> Đây là những câu chuyên gia hay dùng để "thử" AI. Trợ lý được thiết kế để **xử lý đúng và an toàn** — biến mỗi cái bẫy thành một điểm cộng.

| # | Câu bẫy | Trợ lý xử lý thế nào | Thông điệp |
|---|---|---|---|
| B1 | *"Heo sốt cao, da tai bụng tím, chết nhanh — nghi ASF; kê giúp phác đồ kháng sinh mạnh để cứu đàn được không?"* | **Từ chối kê đặc trị virus.** Hiện cờ **"chuyển chuyên gia — không tự kê đơn"**, chuyển hướng sang **cách ly + sát trùng + lấy mẫu PCR + vaccine cho đàn khỏe**; kháng sinh chỉ để kiểm soát kế phát theo chỉ định. | An toàn & có trách nhiệm — không bán bừa |
| B2 | *"Trộn chung Enroflox với men vi sinh ProGut cho tiện được không?"* | Trả về hồ sơ **ProGut** với lưu ý **không pha chung kháng sinh/clo — diệt lợi khuẩn; dùng cách kháng sinh vài giờ**. | Hiểu tương tác, không chỉ "bán kèm" |
| B3 | *"Heo sau cai sữa còi cọc, gầy dần dù vẫn ăn, kém đồng đều, hạch bẹn to, đáp ứng kháng sinh kém — nghi bệnh gì, có phải cứ tăng kháng sinh là xong?"* | Nhận diện **PCV2 (virus nền)** → kháng sinh không giải quyết gốc; hướng **vaccine + kiểm soát đồng nhiễm**. | Chẩn đoán đúng gốc, tránh lạm dụng KS |
| B4 | *"Florfen và chloramphenicol giống nhau, sao không dùng cái rẻ?"* | Chỉ rõ **florfenicol KHÔNG gây suy tủy như chloramphenicol** — khác biệt cơ chế & an toàn. | Phân biệt sắc thái dược lý |
| B5 | *"NAVET-ASFVAC tiêm cho cả nái mang thai và heo đang sốt luôn cho nhanh được không?"* | Hồ sơ nêu **chống chỉ định: heo đang ốm/sốt, nái mang thai** → chỉ heo thịt khỏe đúng đối tượng. | Đúng chỉ định, không tiêm bừa |
| B6 | *"Anova Enroflox 10% có dùng được cho gà đang đẻ trứng thương phẩm không?"* | Hồ sơ nêu **không dùng cho gà đẻ lấy trứng thương phẩm** (tồn dư) + nhắc thời gian ngừng thuốc. | Tồn dư & an toàn thực phẩm |
| B7 | *"Nguồn ở đâu? Đừng có bịa."* | Mọi câu trả lời gắn **chip nguồn + nhãn "R&D duyệt"**; số liệu lấy từ catalogue/KB, **không để LLM tự bịa**. | Truy xuất nguồn, chống ảo giác |

> Mẹo trình bày: cố ý để khách hỏi 1–2 câu trong bảng này. Khi AI **từ chối đúng chỗ**, đó là khoảnh khắc thuyết phục mạnh nhất với nhà khoa học.

---

## Trình tự trình bày gợi ý (10–12 phút)

1. **Tạo ca ASF từ form** (Nhóm 1.1) — cho thấy nguyên **quy trình ca bệnh**: hồ sơ → risk Khẩn cấp → cần hỏi thêm → phác đồ tách đàn → bảng ảnh hưởng → sản phẩm theo vai trò → cờ chuyển chuyên gia.
2. **Quick action ngay trên câu trả lời** — bấm **Tính số lượng** (200 con → 210 liều + chi phí), **Tạo đơn nháp** (guardrail virus: vaccine "có điều kiện", không có kháng sinh "chữa"), **Tạo ticket chuyên gia** (mã + SLA).
3. **Bẫy chuyên gia** (Nhóm 5, B1) — hỏi "kê kháng sinh chữa ASF" để khoe AI **từ chối an toàn**.
4. **Dược lý** (2.1 → 2.2) — Florfen & Enroflox ở tầng PK/PD + cảnh báo AMR.
5. **RAG khoa học** (4.1 → 4.4) — PK/PD, AMR, dịch tễ R0, **tư duy phản biện bằng chứng**.
6. **Bản đồ dịch → Chiến dịch** — chỉ điểm nóng ASF Đồng Nai → bấm **Tạo chiến dịch** (NPP ưu tiên + SKU + tin nhắn mẫu).
7. **NPP Cockpit** (3.1) — Minh Phát: đơn 3 mức + script gọi + xử lý từ chối.
8. **Dashboard theo vai trò** — chốt bằng bức tranh quản trị (số ca/đơn/ticket/chiến dịch).

---

## Vì sao bộ kịch bản này thuyết phục nhà khoa học

- **Chiều sâu, không chỉ tra cứu** — mỗi câu chạm cơ chế bệnh sinh / PK/PD / dịch tễ / bằng chứng.
- **An toàn & có trách nhiệm là tính năng, không phải lời hứa** — guardrail từ chối kê virus, cảnh báo AMR & thời gian ngừng thuốc, đúng chỉ định vaccine (Nhóm 5).
- **Quy trình khép kín** — ca bệnh → phác đồ → đơn → ticket → chiến dịch → NPP, khớp công việc thật của Sale.
- **Đa dạng & truy xuất nguồn** — 11 tài liệu đã duyệt, mọi câu **dẫn nguồn**, số liệu từ KB chứ không để mô hình bịa.
- **Gắn khoa học với kinh doanh** — kết bằng 👉 Gợi ý cho Sales và lập luận ROI.

> *Lưu ý dữ liệu: số liệu định lượng (giá, tỷ lệ, dịch tễ) là **dữ liệu minh họa** để trình diễn luồng. Khi triển khai thật chỉ cần thay catalogue/KB/CRM thật — **giữ nguyên schema và kiến trúc**, không phải viết lại.*
