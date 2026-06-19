# Đề xuất nâng cấp AI4Sales thành sản phẩm thật

> Ngày tạo: 19/06/2026  
> Phạm vi đọc: `docs/md/*.md`, `AI4Sales/data/*.json`, `AI4Sales/data/knowledge/*.md`, `AI4Sales/AI SalesMate.dc.html`.  
> Kết luận ngắn: bản hiện tại đã đủ tốt để demo năng lực "AI tư vấn + sales intelligence", nhưng để thành sản phẩm cho người dùng thật cần nâng cấp từ "trả lời thông tin" sang "quản lý ca tư vấn, hỏi sâu theo ngữ cảnh, khuyến nghị hành động theo đàn/trại, theo dõi kết quả và có kiểm soát an toàn".

---

## 1. Hiện trạng đang có

AI4Sales hiện đã có các năng lực chính:

- Chẩn đoán bệnh từ triệu chứng, có độ tin cậy, chẩn đoán phân biệt, cơ chế bệnh sinh, xét nghiệm xác chẩn, bước xử lý, sản phẩm liên quan và cờ chuyển chuyên gia.
- Tra cứu thuốc/vaccine theo catalogue, có công dụng, liều lượng, đường dùng, chống chỉ định, thời gian ngừng thuốc, giá, cơ chế tác động, PK/PD, bảo quản.
- Phân tích nhà phân phối, lịch sử mua, gợi ý đơn kế tiếp, cross-sell.
- Tra cứu tài liệu RAG gồm an toàn sinh học, vaccine, AMR, PK/PD, kinh tế phòng bệnh, chuỗi lạnh, chính sách bán hàng.
- Bản đồ dịch bệnh cho phép nhập cảnh báo thị trường và xem heatmap theo tỉnh.

Điểm mạnh của demo:

- Đúng câu chuyện pain point: sales phụ thuộc chuyên gia, tra cứu chậm, tư vấn không nhất quán, khai thác NPP cảm tính.
- Có cấu trúc dữ liệu tốt: bệnh, sản phẩm, NPP, knowledge docs tách riêng.
- Có guardrail sơ bộ: bệnh virus không kê kháng sinh như thuốc chữa, ca nặng chuyển chuyên gia.
- Có gắn khoa học với bán hàng: câu trả lời không chỉ nói bệnh mà còn gợi ý sản phẩm và luận điểm chốt đơn.

Khoảng thiếu lớn nhất khi lên production:

- Câu trả lời vẫn thiên về "thông tin chung + 6 bước xử lý"; chưa đủ cá nhân hóa theo đàn cụ thể.
- Chưa có cơ chế hỏi tiếp bắt buộc khi thiếu dữ kiện quan trọng.
- Chưa có output theo vai trò: chủ trại cần làm gì, sales cần bán gì, thú y cần xác minh gì, quản lý vùng cần điều phối gì.
- Chưa có quản lý vòng đời ca bệnh: tiếp nhận, phân loại nguy cơ, khuyến nghị, chuyển chuyên gia, theo dõi, kết quả.
- Chưa có quản trị tri thức production: nguồn chính thức, ngày hiệu lực, phạm vi quốc gia, người duyệt, phiên bản, log thay đổi.
- Dữ liệu hiện là minh họa; production bắt buộc thay bằng catalogue thật, CRM/DMS/ERP thật, tồn kho thật, giá thật, chính sách thật, nguồn dịch tễ thật.

---

## 2. Định vị sản phẩm nên đi theo hướng nào

Không nên định vị AI4Sales chỉ là chatbot tra cứu. Sản phẩm nên là:

**Trợ lý hiện trường cho sales thú y, vừa tư vấn kỹ thuật an toàn, vừa biến tình huống trại/NPP/thị trường thành hành động bán hàng có thể theo dõi.**

Ba trục giá trị:

1. **Tư vấn kỹ thuật đáng tin**  
   Nhận ca, hỏi đủ thông tin, phân loại nguy cơ, đưa kế hoạch xử lý theo đàn/trại, biết khi nào phải chuyển bác sĩ thú y.

2. **Sales execution**  
   Từ ca bệnh hoặc điểm nóng dịch, sinh gợi ý đơn hàng, combo sản phẩm, số lượng ước tính, kịch bản gọi khách, phản biện objection và lịch follow-up.

3. **Tri thức tổ chức**  
   Chuẩn hóa kiến thức R&D, catalogue, chính sách, dữ liệu thị trường và kinh nghiệm hiện trường thành tài sản dùng lại được.

---

## 3. Người dùng thật và kết quả họ cần

| Nhóm người dùng | Nhu cầu thật | Output sản phẩm cần trả |
|---|---|---|
| Sales hiện trường | Đứng trước khách/trại, cần trả lời nhanh và đúng | Tóm tắt ca, hỏi thêm 3-5 câu quan trọng, hành động ngay, sản phẩm phù hợp, kịch bản nói với khách |
| Bác sĩ thú y/R&D | Cần ca được mô tả đủ dữ liệu để xác chẩn | Phiếu ca chuẩn, triệu chứng, timeline, mẫu cần lấy, chẩn đoán phân biệt, lý do escalation |
| Quản lý sales vùng | Muốn biết vùng nào nóng, đội nào cần gọi khách nào | Danh sách khách ưu tiên, sản phẩm nên đẩy, tồn kho cần chuẩn bị, dự báo doanh số |
| Nhà phân phối | Cần quyết định nhập hàng, không chỉ nghe "nên nhập" | Đơn gợi ý theo nhịp bán, combo theo mùa/dịch, biên lợi nhuận, rủi ro tồn kho, chương trình khuyến mãi |
| Chủ trại/hộ nuôi | Muốn biết đàn này làm gì ngay, tránh mất đàn | Kế hoạch 0-2 giờ, 24 giờ, 3-7 ngày; điều không được làm; khi nào gọi thú y |
| Chính quyền/phường/xã nếu có dùng | Cần tuyên truyền và khoanh vùng, không phải chốt đơn | Thông báo ngắn, checklist tuyên truyền, vùng nguy cơ, hướng dẫn báo cáo và an toàn sinh học |

Điểm cần quyết định: AI4Sales có phục vụ trực tiếp chủ trại/chính quyền không, hay chỉ phục vụ nội bộ sales. Nếu chỉ nội bộ sales thì mọi output vẫn cần có phần "nói thế nào với khách" và "ghi nhận lại gì vào CRM".

---

## 4. Cần drill sâu đến mức nào

### 4.1. Mức drill mặc định cho mọi câu hỏi bệnh

Khi người dùng hỏi bệnh hoặc mô tả triệu chứng, câu trả lời production nên đi qua 6 tầng:

1. **Triage nhanh**  
   Nghi bệnh gì, mức nguy cơ đỏ/cam/vàng/xanh, có cần chuyển chuyên gia ngay không.

2. **Dữ kiện còn thiếu**  
   Hỏi thêm tối đa 3-5 câu quan trọng nhất. Không hỏi lan man.

3. **Kế hoạch hành động theo đàn cụ thể**  
   Tách rõ: đàn đang bệnh, đàn khỏe cùng trại, đàn/trại lân cận, người và phương tiện.

4. **Phân tích ảnh hưởng và lưu ý của từng bước**  
   Ví dụ cách ly ảnh hưởng mật độ/stress, sát trùng bị giảm hiệu lực khi có chất hữu cơ, vaccine chỉ cho con khỏe, kháng sinh có thời gian ngừng thuốc.

5. **Sản phẩm và sales action**  
   Sản phẩm nào dùng để phòng, hỗ trợ, sát trùng, điều trị kế phát; không nói quá công dụng. Có gợi ý số lượng nếu biết quy mô đàn.

6. **Theo dõi sau tư vấn**  
   Cần ghi chỉ số nào, khi nào hỏi lại, điều kiện dừng/đổi phác đồ/chuyển chuyên gia.

### 4.2. Quy tắc hỏi tiếp

AI không nên chỉ trả lời một lần rồi kết thúc. Sau câu trả lời đầu, luôn gợi ý các câu hỏi tiếp theo theo kiểu bác sĩ:

- "Phân tích từng bước này có rủi ro/ảnh hưởng gì?"
- "Với đàn 200 con thì cần chuẩn bị bao nhiêu sát trùng, điện giải, vaccine?"
- "Tôi nên nói thế nào để khách hiểu đây là phòng dịch, không phải bán thuốc chữa?"
- "Cần hỏi khách thêm gì trước khi tư vấn đơn hàng?"
- "Tạo phiếu chuyển bác sĩ thú y cho ca này."

### 4.3. Khi nào không hỏi thêm mà phải hành động ngay

Với ca đỏ như nghi ASF, HPAI, FMD, Newcastle độc lực cao, nhiều con chết nhanh, AI phải vừa hỏi thêm vừa đưa hành động tối thiểu ngay:

- Cách ly ô/chuồng nghi bệnh.
- Ngừng xuất bán, vận chuyển, nhập đàn mới.
- Báo thú y/chuyên gia theo quy định nội bộ và địa phương.
- Lấy mẫu xét nghiệm theo hướng dẫn chuyên môn.
- Sát trùng, kiểm soát người/xe/dụng cụ.
- Không tự kê kháng sinh như thuốc chữa bệnh virus.

---

## 5. Chuẩn output câu trả lời production

### 5.1. Output người dùng nhìn thấy

Mẫu trả lời nên cố định cho nhóm bệnh:

```md
Kết luận sơ bộ
- Nghi bệnh: ...
- Mức nguy cơ: Đỏ/Cam/Vàng/Xanh
- Độ tin cậy: ...
- Cần chuyển chuyên gia: Có/Không, lý do ...

Cần hỏi thêm ngay
1. ...
2. ...
3. ...

Đối với đàn đang bệnh
- Làm ngay trong 0-2 giờ: ...
- Trong 24 giờ: ...
- Trong 3-7 ngày: ...

Đối với đàn khỏe cùng trại
- ...

Không nên làm
- ...

Vì sao làm như vậy
- Bước 1: tác dụng, ảnh hưởng, lưu ý.
- Bước 2: tác dụng, ảnh hưởng, lưu ý.

Sản phẩm liên quan
- Phòng bệnh: ...
- Sát trùng/an toàn sinh học: ...
- Hỗ trợ hồi phục: ...
- Điều trị kế phát nếu có chỉ định: ...

Theo dõi tiếp
- Ghi mỗi ngày: số con sốt, bỏ ăn, chết, tiêu chảy, ho, ăn uống.
- Hỏi lại sau: ...

Gợi ý cho Sales
- Câu nói với khách: ...
- Đơn gợi ý: ...
- Lưu ý đạo đức/an toàn: ...
```

### 5.2. Output máy đọc được

Ngoài Markdown, backend nên sinh thêm JSON để lưu CRM, tạo ticket và đo chất lượng:

```json
{
  "intent": "disease_triage",
  "species": "heo",
  "risk_level": "red",
  "suspected_diagnoses": [
    {
      "disease_id": "D01",
      "name": "Dịch tả lợn châu Phi (ASF)",
      "confidence": 0.78,
      "reason": ["sốt cao", "da tai bụng đỏ tím", "chết nhanh"]
    }
  ],
  "must_escalate": true,
  "missing_questions": [],
  "immediate_actions": [],
  "do_not_do": [],
  "recommended_products": [],
  "follow_up": {
    "next_check_hours": 24,
    "metrics_to_record": ["affected_count", "dead_count", "feed_drop", "temperature"]
  },
  "sources": [],
  "safety_flags": ["not_definitive_diagnosis", "reportable_disease", "no_antibiotic_for_virus"]
}
```

Lý do cần JSON: demo chỉ cần chat đẹp, nhưng production cần lưu case, audit, đo hiệu quả, kích hoạt workflow, tạo đơn hàng và chuyển chuyên gia.

---

## 6. Ví dụ ASF: câu trả lời nên sâu hơn "6 bước"

### Câu hỏi

> Heo sốt cao 41 độ, bỏ ăn, da tai bụng đỏ tím, chết nhanh. Nghi ASF. Đối với đàn lợn này nên làm gì?

### Câu trả lời mong muốn

**Kết luận sơ bộ**

- Đây là ca nghi ASF mức nguy cơ đỏ vì có cụm dấu hiệu sốt cao, da đỏ/tím vùng tai/bụng, chết nhanh.
- Chưa được gọi là xác chẩn nếu chưa có xét nghiệm. Cần xử lý như ca nghi nguy hiểm trong lúc chờ thú y/xét nghiệm.
- Cần chuyển chuyên gia thú y ngay. Sales không được tư vấn kháng sinh như thuốc chữa ASF.

**Cần hỏi thêm ngay**

1. Đàn bao nhiêu con, đã chết/mắc bao nhiêu con, tăng theo ngày như thế nào?
2. Heo ở giai đoạn nào: heo con, heo thịt, nái, đực giống?
3. Trong 7-14 ngày gần đây có nhập heo, bán chạy, xe cám/xe thương lái/người lạ vào trại không?
4. Đàn đã tiêm vaccine gì, ngày tiêm gần nhất, lô vaccine, bảo quản ra sao?
5. Đã lấy mẫu PCR hoặc báo thú y địa phương/chuyên gia công ty chưa?

**Đối với đàn đang bệnh**

- Trong 0-2 giờ: cách ly ô/chuồng nghi bệnh, dừng di chuyển heo giữa các ô, dừng bán/xuất heo, hạn chế người vào khu bệnh.
- Trong 0-2 giờ: đặt lối đi riêng cho khu nghi bệnh, sát trùng ủng, quần áo, dụng cụ, xe ra vào.
- Trong 24 giờ: báo thú y/chuyên gia phụ trách, lấy mẫu theo hướng dẫn, ưu tiên mẫu máu EDTA giai đoạn sốt sớm và mẫu mô phù hợp nếu có heo chết.
- Trong 24 giờ: ghi nhật ký số con sốt, bỏ ăn, chết, vị trí chuồng, thời điểm phát hiện để phục vụ truy vết.
- Sau xác chẩn: xử lý theo chỉ đạo thú y và quy định địa phương; không tự tiêu hủy/chôn lấp tùy tiện nếu chưa có hướng dẫn.

**Đối với đàn khỏe cùng trại**

- Tách luồng chăm sóc: người chăm đàn khỏe trước, khu nghi bệnh sau; không dùng chung dụng cụ.
- Tăng sát trùng, giảm khách/xe vào trại, dừng nhập đàn mới.
- Rà soát lịch tiêm phòng và tình trạng sức khỏe. Vaccine phòng chỉ cân nhắc cho heo khỏe, đúng đối tượng, theo hướng dẫn thú y; không tiêm cho heo đang sốt/ốm.
- Bổ sung điện giải, vitamin, giảm stress nhiệt, giữ chuồng khô sạch để đàn khỏe chống chịu tốt hơn. Đây là hỗ trợ, không phải thuốc chữa ASF.

**Không nên làm**

- Không bán chạy heo bệnh hoặc heo nghi bệnh.
- Không chuyển heo từ ô bệnh sang ô khác.
- Không dùng kháng sinh để quảng bá là "chữa ASF".
- Không tiêm vaccine cho heo đang sốt/ốm/stress nặng.
- Không để xe, người, dụng cụ từ khu nghi bệnh đi thẳng sang khu khỏe.

**Phân tích ảnh hưởng và lưu ý từng bước**

| Bước | Tác dụng | Ảnh hưởng/lưu ý |
|---|---|---|
| Cách ly ô bệnh | Giảm lây trực tiếp | Có thể tăng mật độ/stress nếu dồn sai; cần tách luồng chăm sóc, không gom đàn lung tung |
| Dừng vận chuyển | Giảm nguy cơ lan ra ngoài | Ảnh hưởng kế hoạch bán heo; cần giải thích đây là giảm thiệt hại lớn hơn |
| Sát trùng | Cắt lây gián tiếp qua xe, ủng, dụng cụ | Chất hữu cơ làm giảm hiệu lực; phải dọn phân/rác trước, pha đúng nồng độ, đủ thời gian tiếp xúc |
| Lấy mẫu xét nghiệm | Phân biệt ASF với CSF/PRRS/tụ huyết trùng | Chẩn đoán lâm sàng không đủ chắc; mẫu sai thời điểm hoặc bảo quản sai có thể làm chậm xác chẩn |
| Vaccine cho đàn khỏe | Tăng miễn dịch phòng bệnh nếu đúng đối tượng | Không dùng như điều trị; cần chuỗi lạnh, đúng tuổi, đúng loại heo, đúng hướng dẫn địa phương |
| Điện giải/vitamin | Hỗ trợ ăn uống, giảm stress | Không thay thế xử lý dịch; chỉ là hỗ trợ cho đàn khỏe/đàn phục hồi |

**Sản phẩm liên quan**

- Sát trùng/an toàn sinh học: Iodine hoặc sản phẩm sát trùng phù hợp danh mục công ty.
- Phòng bệnh cho heo khỏe đúng đối tượng: vaccine ASF nếu được phép dùng trong bối cảnh địa phương và có chỉ định/giám sát thú y.
- Hỗ trợ: điện giải, vitamin, hạ sốt theo chỉ định. Không định vị là thuốc chữa ASF.

**Gợi ý cho Sales**

- Câu nói với khách: "Ca này cần xử lý như nghi ASF cho đến khi có xét nghiệm. Em không tư vấn thuốc chữa virus. Việc quan trọng nhất là giữ đàn khỏe chưa bệnh và tránh lan ra cả trại. Mình ưu tiên bộ sát trùng, kiểm soát ra vào, hỗ trợ điện giải/vitamin và rà lại lịch vaccine cho đàn khỏe theo hướng dẫn thú y."
- Hỏi tiếp để chốt đúng đơn: "Trại mình còn bao nhiêu con khỏe, chia mấy dãy chuồng, mỗi ngày dùng bao nhiêu nước sát trùng, và còn tồn bao nhiêu sản phẩm?"

---

## 7. Thông tin cần bổ sung để sản phẩm dùng được thật

### 7.1. Dữ liệu hồ sơ trại/khách hàng

| Nhóm dữ liệu | Trường nên có |
|---|---|
| Định danh | `customer_id`, tên trại/NPP, người liên hệ, số điện thoại, sales phụ trách, bác sĩ phụ trách |
| Địa bàn | tỉnh, huyện/xã, tọa độ, vùng bán hàng, vùng dịch liên quan |
| Quy mô | loài nuôi, tổng đàn, số ô/chuồng, giai đoạn nuôi, mô hình nuôi |
| Lịch sử mua | SKU, số lượng, ngày mua, giá, chiết khấu, công nợ, tần suất mua |
| Tồn kho tại khách | thuốc/vaccine/sát trùng còn tồn, hạn dùng, lô, điều kiện bảo quản |
| Lịch vaccine | bệnh, sản phẩm, ngày tiêm, mũi, lô vaccine, phản ứng sau tiêm |
| Lịch bệnh | ca bệnh cũ, kết quả xét nghiệm, tỷ lệ chết, phác đồ đã dùng, kết quả |
| An toàn sinh học | mức kiểm soát người/xe, cách ly heo mới, sát trùng, nguồn thức ăn/nước, quản lý xác chết |

### 7.2. Dữ liệu ca bệnh

Một ca bệnh phải có form riêng, không chỉ là một dòng chat:

- Loài nuôi, giai đoạn tuổi, trọng lượng ước tính.
- Quy mô đàn, số con mắc, số con chết, số con bỏ ăn.
- Timeline: bắt đầu khi nào, tăng nhanh hay chậm, lan theo ô nào.
- Triệu chứng chính: sốt, tiêu chảy, ho, thần kinh, da tím/xuất huyết, giảm đẻ, sảy thai.
- Dấu hiệu định lượng: nhiệt độ, tỷ lệ chết/ngày, tỷ lệ ăn giảm, FCR nếu có.
- Ảnh/video nếu triển khai multimodal.
- Điều trị đã dùng: tên thuốc, liều, ngày dùng, đáp ứng.
- Vaccine đã tiêm: ngày, lô, bảo quản, đối tượng tiêm.
- Dữ kiện dịch tễ: nhập đàn, xe cám, thương lái, giết mổ, trại lân cận, nguồn nước/thức ăn.
- Xét nghiệm: loại mẫu, ngày gửi, phòng lab, kết quả.
- Kết quả sau tư vấn: khỏi, chết thêm, phải tiêu hủy, mua sản phẩm, không mua, lý do.

### 7.3. Dữ liệu sản phẩm production

Catalogue hiện đã có nền tốt, nhưng production cần thêm:

- Số đăng ký lưu hành, quốc gia/phạm vi được phép bán.
- Loại pháp lý: OTC, cần chỉ định thú y, vaccine cần giám sát, sản phẩm hạn chế.
- Loài/giai đoạn được dùng và không được dùng.
- Liều theo kg thể trọng, theo nước uống/thức ăn, theo con, theo lứa.
- Chống chỉ định, phản ứng bất lợi, tương tác.
- Thời gian ngừng thuốc theo loài và sản phẩm.
- Chuỗi lạnh, nhiệt độ, thời gian sau pha, điều kiện vận chuyển.
- Tồn kho theo kho/NPP, hạn dùng, số lô.
- Giá bán, chiết khấu, margin, chương trình khuyến mãi, min order.
- Sản phẩm thay thế khi hết hàng.
- Claims được phép nói và claims không được nói.

### 7.4. Dữ liệu thị trường và dịch bệnh

Bản đồ dịch bệnh production cần thêm:

- Nguồn cảnh báo: sales nhập, NPP nhập, thú y xác nhận, tin công khai, dữ liệu cơ quan quản lý.
- Trạng thái xác minh: chưa xác minh, đã kiểm tra nội bộ, đã có lab, đã có thông báo chính thức.
- Mức tin cậy và lý do.
- Cơ chế chống trùng lặp nhiều sales nhập cùng một ổ dịch.
- Phạm vi ảnh hưởng: xã/huyện/tỉnh, bán kính, tuyến vận chuyển.
- Thời gian hiệu lực cảnh báo và tự hết hạn nếu không cập nhật.
- Liên kết với danh sách khách/NPP trong vùng.
- Gợi ý hành động theo vai trò: sales gọi khách nào, quản lý điều phối tồn kho nào, chính quyền cần thông báo gì nếu có.

---

## 8. Bản đồ dịch bệnh phải đi xa hơn heatmap

Hiện heatmap chủ yếu cho thấy "ở đâu đang nóng". Sản phẩm thật cần biến bản đồ thành workflow:

1. **Phát hiện điểm nóng**  
   Tỉnh/huyện nào có bệnh gì, mức tin cậy bao nhiêu.

2. **Tạo danh sách hành động**  
   Khách/NPP trong vùng nguy cơ, ưu tiên theo quy mô đàn, lịch sử mua, chưa mua vaccine/sát trùng, công nợ, tồn kho.

3. **Gợi ý chiến dịch gọi khách**  
   Script 30 giây, nội dung Zalo/SMS, tài liệu gửi kèm, objection handling.

4. **Gợi ý đơn hàng theo quy mô**  
   Ví dụ trại 200 con, 1.000 con, NPP cấp 1: cần bao nhiêu sát trùng, điện giải, vaccine, combo gì.

5. **Theo dõi chuyển đổi**  
   Đã gọi chưa, khách phản hồi gì, đã đặt hàng chưa, sau 3 ngày tình hình ra sao.

6. **Phân biệt tuyên truyền và bán hàng**  
   Với phường/xã: output là checklist tuyên truyền, mẫu thông báo, quy trình báo cáo. Với sales/NPP: output là call list, đơn gợi ý, tồn kho cần chuẩn bị.

---

## 9. Nâng cấp trải nghiệm hội thoại

### 9.1. Không chỉ chat tự do

Nên có thêm các luồng có cấu trúc:

- **Tạo ca bệnh mới**: form nhanh 60 giây.
- **Hỏi tiếp theo ca**: AI nhớ ngữ cảnh ca đó, không bắt nhập lại.
- **Chuyển chuyên gia**: tạo ticket kèm toàn bộ dữ kiện.
- **Tạo đơn gợi ý**: từ ca bệnh hoặc chiến dịch vùng.
- **Theo dõi sau tư vấn**: nhắc sales hỏi lại khách sau 24 giờ/3 ngày/7 ngày.

### 9.2. Các nút hỏi tiếp nên có

Sau câu trả lời bệnh:

- "Hỏi thêm dữ kiện còn thiếu"
- "Phân tích ảnh hưởng từng bước"
- "Lập kế hoạch cho đàn khỏe"
- "Tính sản phẩm theo quy mô đàn"
- "Tạo tin nhắn gửi khách"
- "Chuyển bác sĩ thú y"
- "Tạo đơn hàng gợi ý"

Sau câu trả lời sản phẩm:

- "Tính liều theo trọng lượng đàn"
- "So sánh với sản phẩm thay thế"
- "Kiểm tra chống chỉ định"
- "Tạo hướng dẫn bảo quản/giao hàng"
- "Tạo luận điểm chốt đơn"

Sau phân tích NPP:

- "Tạo đơn đề xuất"
- "Tính tồn kho cần nhập"
- "Soạn kịch bản gọi NPP"
- "Kiểm tra công nợ trước khi chào"
- "Tạo chiến dịch cross-sell"

---

## 10. Guardrails bắt buộc

### 10.1. Guardrails thú y

- Không khẳng định xác chẩn nếu chưa có lab hoặc nguồn xác nhận.
- Không kê kháng sinh cho bệnh virus như thuốc chữa nguyên nhân.
- Với bệnh nguy hiểm/phải báo cáo: luôn có cờ chuyển chuyên gia và nhắc tuân thủ quy định địa phương.
- Không khuyến nghị vaccine cho con đang bệnh/sốt/stress nặng.
- Không bỏ qua thời gian ngừng thuốc.
- Không đưa liều nếu thiếu loài, trọng lượng, đường dùng hoặc sản phẩm không rõ.
- Luôn phân biệt "phòng", "hỗ trợ", "điều trị kế phát", "đặc trị".

### 10.2. Guardrails bán hàng

- Không nói quá claim sản phẩm.
- Không biến cảnh báo dịch thành bán hàng gây hoảng sợ.
- Không chào vaccine/thuốc sai đối tượng chỉ vì có hàng tồn.
- Nếu công nợ vượt ngưỡng, gợi ý sales xử lý công nợ trước khi đẩy đơn lớn.
- Với sản phẩm cần chuỗi lạnh, không gợi ý giao nếu kho/NPP không đảm bảo điều kiện bảo quản.

### 10.3. Guardrails AI

- Mỗi câu trả lời quan trọng phải có nguồn và phiên bản tri thức.
- Với dữ liệu xung đột, AI phải nói rõ nguồn nào áp dụng cho quốc gia/thời điểm nào.
- Log toàn bộ câu hỏi, nguồn dùng, tool call, output, user feedback.
- Có chế độ "draft for expert review" cho ca đỏ.
- Có danh sách câu cấm hoặc claim cần duyệt bởi R&D/pháp chế.

---

## 11. Quản trị tri thức production

Mỗi mẩu tri thức nên có metadata:

```json
{
  "knowledge_id": "ASF_VN_2026_001",
  "topic": "african_swine_fever",
  "country": "VN",
  "species": ["heo"],
  "effective_from": "2026-06-01",
  "effective_to": null,
  "source_type": "official|rd_internal|manufacturer|field_report",
  "source_url": "",
  "approved_by": "R&D",
  "approval_status": "approved",
  "version": "1.0.0",
  "allowed_claims": [],
  "forbidden_claims": []
}
```

Lưu ý rất quan trọng: nguồn quốc tế có thể khác nguồn Việt Nam và khác thời điểm. Ví dụ WOAH technical disease card cập nhật trước khi một số vaccine ASF thương mại ở Việt Nam được nhắc trong dữ liệu demo. Production phải ưu tiên nguồn chính thức theo quốc gia, ngày hiệu lực và người duyệt, không dùng một câu trả lời global cho mọi thị trường.

---

## 12. Nâng cấp phân tích NPP và đơn hàng

Hiện phân tích NPP mới dựa vào lịch sử mua và cross-sell. Production cần thêm:

- Sell-in và sell-out nếu có: NPP nhập nhiều nhưng bán ra chậm thì không nên đẩy thêm.
- Tồn kho tại NPP và hạn dùng.
- Công nợ, hạn mức tín dụng, lịch thanh toán.
- Vùng khách hàng của NPP và dịch bệnh đang nóng quanh vùng đó.
- Năng lực bảo quản vaccine/chuỗi lạnh.
- Biên lợi nhuận theo SKU và chương trình khuyến mãi.
- Tần suất mua bình thường và dấu hiệu giảm mua bất thường.
- Gợi ý đơn theo 3 mức: an toàn, đề xuất, tăng trưởng.
- Kịch bản objection: đắt, sợ tồn, khách chưa hỏi, chưa tin vaccine, công nợ.

Output NPP nên trả:

```md
Tóm tắt NPP
- Doanh số 3 tháng, nhóm chủ lực, công nợ, tồn kho.

Cơ hội
- SKU nên nhập lại.
- SKU nên bán thêm.
- Lý do theo dữ liệu.

Đơn gợi ý
- Mức an toàn: ...
- Mức đề xuất: ...
- Mức tăng trưởng: ...

Kịch bản gọi
- Câu mở đầu.
- Luận điểm theo vùng dịch/nhu cầu.
- Phản biện objection.

Rủi ro
- Công nợ, tồn kho, chuỗi lạnh, hạn dùng.
```

---

## 13. Roadmap nâng cấp

### Phase 1 - Product foundation

- Chuẩn hóa schema ca bệnh, khách hàng, trại, NPP, sản phẩm.
- Thay dữ liệu cook bằng catalogue/chính sách/CRM thật ở phạm vi nhỏ.
- Thêm output JSON song song với chat.
- Thêm workflow tạo ca, chuyển chuyên gia, follow-up.
- Thêm guardrails claim sản phẩm và an toàn thú y.

### Phase 2 - Field workflow

- Guided intake form cho sales.
- Nút hỏi tiếp theo ca.
- Tính liều/số lượng theo quy mô đàn.
- Tạo tin nhắn gửi khách/NPP.
- Tạo đơn gợi ý và đẩy sang CRM/DMS.
- Theo dõi outcome sau tư vấn.

### Phase 3 - Market intelligence

- Heatmap có xác minh, chống trùng lặp, thời gian hiệu lực.
- Tự tạo danh sách khách/NPP ưu tiên theo vùng dịch.
- Chiến dịch gọi khách theo bệnh/vùng/SKU.
- Dự báo nhu cầu tồn kho theo vùng.

### Phase 4 - Advanced intelligence

- Ảnh/video triệu chứng và bệnh tích, có guardrail chuyển chuyên gia.
- Speech-to-text cho sales hiện trường.
- Vector RAG + reranker + knowledge graph.
- Model đánh giá rủi ro dịch theo mùa, mật độ, lịch vaccine, lịch mua.
- Dashboard đo hiệu quả tư vấn và doanh số.

---

## 14. Tiêu chí nghiệm thu sản phẩm thật

### Chất lượng tư vấn

- Tỷ lệ câu trả lời có nguồn đúng: >= 95%.
- Tỷ lệ ca đỏ được escalation: 100%.
- Tỷ lệ claim sai về thuốc/vaccine: 0 lỗi nghiêm trọng.
- Tỷ lệ câu trả lời hỏi đủ dữ kiện quan trọng khi thiếu thông tin: >= 90%.
- Không có câu trả lời kháng sinh chữa bệnh virus.

### Hiệu quả sales

- Giảm thời gian tra cứu sản phẩm/chính sách.
- Tăng tỷ lệ follow-up đúng hạn sau ca bệnh.
- Tăng giá trị đơn trung bình ở nhóm có gợi ý combo.
- Tăng tỷ lệ cross-sell có lý do dữ liệu.
- Giảm số case phải hỏi lại R&D vì thiếu thông tin đầu vào.

### Vận hành

- Mỗi câu trả lời quan trọng có log, nguồn, phiên bản tri thức.
- Có quy trình duyệt nội dung mới bởi R&D/pháp chế/sales ops.
- Có dashboard cảnh báo tri thức hết hiệu lực.
- Có cơ chế thu feedback từ sales và bác sĩ thú y.

---

## 15. Các quyết định sản phẩm nên chốt sớm

1. AI4Sales phục vụ nội bộ sales hay mở cho NPP/chủ trại dùng trực tiếp?
2. Ai chịu trách nhiệm duyệt tri thức: R&D, pháp chế, marketing, sales ops?
3. Ca nào bắt buộc chuyển bác sĩ thú y và SLA phản hồi là bao lâu?
4. Danh mục sản phẩm nào được phép AI gợi ý, sản phẩm nào chỉ được hiển thị khi có chỉ định?
5. Có tích hợp CRM/DMS/ERP ngay không, hay import CSV theo giai đoạn đầu?
6. Bản đồ dịch bệnh lấy nguồn từ sales nhập, nguồn chính thức, hay cả hai?
7. AI có được tạo đơn hàng nháp không, hay chỉ gợi ý để sales xác nhận?
8. Có lưu dữ liệu trại/ca bệnh nhạy cảm không, và phân quyền xem thế nào?
9. Với vaccine/thuốc cần chuỗi lạnh, có dữ liệu tồn kho và điều kiện vận chuyển chưa?
10. Có đo outcome sau tư vấn để AI học lại không?

---

## 16. Product canvas chi tiết

### 16.1. Vấn đề cốt lõi

AI4Sales không chỉ giải quyết chuyện "hỏi AI cho nhanh". Sản phẩm thật phải xử lý 5 vấn đề vận hành:

1. **Thiếu dữ kiện đầu vào chuẩn**  
   Sales hỏi khách qua điện thoại/Zalo, thông tin rời rạc, không đủ tuổi đàn, số con chết, lịch vaccine, thuốc đã dùng. AI nếu trả lời ngay sẽ dễ thành trả lời chung chung.

2. **Thiếu quy trình xử lý theo mức nguy cơ**  
   Ca nhẹ, ca vừa, ca đỏ phải có workflow khác nhau. ASF/HPAI/FMD không thể xử lý giống tiêu chảy E.coli.

3. **Thiếu chuyển tiếp giữa tư vấn kỹ thuật và hành động bán hàng**  
   AI biết bệnh nhưng chưa tự tạo call list, đơn gợi ý, follow-up task, hoặc cảnh báo tồn kho.

4. **Thiếu bằng chứng và trách nhiệm**  
   Với thuốc/vaccine, mọi claim phải có nguồn, ngày hiệu lực, người duyệt. Nếu sai liều hoặc sai đối tượng, rủi ro rất lớn.

5. **Thiếu học lại từ hiện trường**  
   Sau tư vấn, không biết khách làm gì, có mua không, đàn hồi phục không, có chết thêm không. Không có outcome thì AI chỉ là chatbot, không thành hệ thống học nghiệp vụ.

### 16.2. Lời hứa sản phẩm

**Trong 60 giây, sales có thể ghi nhận một ca bệnh/nhu cầu khách hàng đủ chuẩn, nhận khuyến nghị an toàn đã được kiểm soát, tạo hành động bán hàng phù hợp và theo dõi kết quả.**

### 16.3. Phạm vi nên làm trước

| Giai đoạn | Phạm vi | Lý do |
|---|---|---|
| MVP | Sales nội bộ dùng cho heo/gà, bệnh phổ biến, catalogue thật, NPP thật | Dễ kiểm soát rủi ro, dữ liệu sẵn hơn, tạo giá trị nhanh |
| V1 | Thêm workflow chuyển bác sĩ thú y, follow-up, đơn hàng nháp, bản đồ dịch theo vùng | Bắt đầu thành sản phẩm vận hành |
| V2 | Mở cho NPP/chủ trại giới hạn, có mobile, ảnh/giọng nói, campaign tự động | Cần guardrails và dữ liệu mạnh hơn |
| V3 | Dự báo dịch, tối ưu tồn kho, học từ outcome, scoring khách hàng | Tạo lợi thế dữ liệu dài hạn |

### 16.4. Các nguyên tắc thiết kế

- **Hỏi ít nhưng đúng**: mỗi lượt chỉ hỏi 3-5 câu có tác động lớn nhất đến quyết định.
- **Trả lời theo hành động**: mọi câu trả lời phải nói "làm gì tiếp", không chỉ giải thích.
- **Tách kỹ thuật và bán hàng**: kỹ thuật phải đúng trước, sales action đi sau.
- **Không che giấu độ không chắc chắn**: nếu thiếu dữ kiện, nói rõ thiếu gì và ảnh hưởng ra sao.
- **Dùng được ngoài hiện trường**: nhanh, mobile-first, hỗ trợ nhập giọng nói sau này, lưu nháp khi mạng yếu.
- **Audit được**: mọi khuyến nghị quan trọng phải truy vết được nguồn, phiên bản, tool, người duyệt.

---

## 17. Module sản phẩm cần có

### 17.1. Case Intake - tạo ca bệnh/nhu cầu

Mục tiêu: biến hội thoại rời rạc thành phiếu ca chuẩn.

Chức năng:

- Tạo ca mới từ chat, form, ảnh, giọng nói hoặc alert bản đồ.
- Tự nhận diện loài nuôi, bệnh nghi ngờ, mức nguy cơ.
- Tự hỏi bổ sung dữ kiện còn thiếu.
- Lưu trạng thái ca: mới, đang hỏi thêm, cần chuyên gia, đã có khuyến nghị, đang theo dõi, đóng ca.
- Gắn ca với khách hàng, trại, NPP, địa bàn, sales phụ trách.

Trường tối thiểu trong MVP:

| Trường | Bắt buộc | Ghi chú |
|---|---|---|
| Loài nuôi | Có | Heo/gà trước |
| Giai đoạn/tuổi | Có nếu tính liều/vaccine | Heo con, heo thịt, nái, gà con, gà đẻ |
| Tổng đàn | Có | Để tính tỷ lệ mắc/chết và sản phẩm |
| Số con mắc | Có | Nếu không biết thì hỏi lại |
| Số con chết | Có với ca đỏ | Triage nguy cơ |
| Thời gian bắt đầu | Có | Phân biệt cấp tính/mạn |
| Triệu chứng | Có | Text + chọn nhanh |
| Địa điểm | Có | Bản đồ dịch, sales territory |
| Đã dùng thuốc/vaccine gì | Nên có | Tránh khuyến nghị lặp/sai |

### 17.2. Triage Engine - phân loại nguy cơ

Mục tiêu: quyết định AI được trả lời tới đâu và khi nào phải chuyển chuyên gia.

Mức nguy cơ:

| Mức | Ý nghĩa | Ví dụ | AI được làm |
|---|---|---|---|
| Đỏ | Bệnh nguy hiểm, chết nhanh, phải báo/chuyển | ASF, HPAI, FMD, chết hàng loạt | Hướng dẫn hành động tối thiểu, hỏi dữ kiện, tạo ticket chuyên gia, không kê đơn điều trị nguyên nhân |
| Cam | Ca nặng hoặc thiếu dữ kiện nhưng chưa chắc bệnh phải báo | Tụ huyết trùng cấp, PRRS nghi nặng | Tư vấn sơ bộ, đề nghị xác chẩn, sản phẩm hỗ trợ/điều trị kế phát có điều kiện |
| Vàng | Bệnh phổ biến, có thể xử lý nếu đủ dữ kiện | E.coli, cầu trùng, CRD | Đề xuất phác đồ theo tài liệu duyệt, tính liều nếu đủ thông tin |
| Xanh | Tra cứu hoặc phòng bệnh thông thường | Lịch vaccine, liều sản phẩm, chính sách | Trả lời trực tiếp có nguồn |

Rule gợi ý:

```text
risk_level = max(
  disease_base_risk,
  mortality_signal,
  spread_signal,
  reportable_signal,
  missing_data_risk
)
```

Trong đó:

- `disease_base_risk`: mức nguy hiểm mặc định trong KB bệnh.
- `mortality_signal`: tăng nếu chết nhanh, tỷ lệ chết cao, nhiều ô chuồng.
- `spread_signal`: tăng nếu lan nhanh trong 24-48 giờ.
- `reportable_signal`: tăng nếu bệnh thuộc nhóm cần báo/có quy định kiểm soát.
- `missing_data_risk`: tăng nếu thiếu loài, tuổi, số mắc/chết, thuốc đã dùng.

### 17.3. Diagnosis Assistant - trợ lý chẩn đoán

Mục tiêu: không thay bác sĩ thú y, nhưng giúp sales nhận diện nguy cơ và chuẩn bị dữ kiện đúng.

Chức năng:

- Xếp hạng 3 bệnh nghi ngờ nhất.
- Giải thích vì sao khớp và vì sao chưa chắc.
- Chẩn đoán phân biệt.
- Xét nghiệm/ảnh/bệnh tích cần xác nhận.
- Mẫu cần lấy, bảo quản mẫu, người cần liên hệ.
- Cảnh báo điều không được làm.

Output nên có:

| Khối | Nội dung |
|---|---|
| Kết luận sơ bộ | Bệnh nghi ngờ, mức nguy cơ, độ tin cậy |
| Vì sao nghi | Triệu chứng khớp, dịch tễ khớp |
| Chưa chắc vì | Dữ kiện thiếu, bệnh phân biệt |
| Hỏi thêm | 3-5 câu quan trọng |
| Xác chẩn | Mẫu, xét nghiệm, người chịu trách nhiệm |
| Hành động ngay | 0-2 giờ, 24 giờ, 3-7 ngày |

### 17.4. Treatment/Product Advisor - khuyến nghị sản phẩm có kiểm soát

Mục tiêu: chuyển từ bệnh/nhu cầu sang sản phẩm phù hợp nhưng không nói quá claim.

Rule bắt buộc:

- Với bệnh virus: sản phẩm chỉ được phân loại là phòng bệnh, sát trùng, hỗ trợ, kiểm soát kế phát; không ghi "đặc trị virus" nếu không có nguồn duyệt.
- Với bệnh vi khuẩn/ký sinh: được gợi ý thuốc nếu có đủ loài, tuổi/trọng lượng, chỉ định và không có chống chỉ định.
- Với vaccine: chỉ cho con khỏe, đúng tuổi/giai đoạn, bảo quản đúng, có lịch tiêm.
- Với kháng sinh: nhắc kháng sinh đồ khi cần, thời gian ngừng thuốc, không dùng kéo dài dự phòng.

### 17.5. Dose & Quantity Calculator - tính liều và số lượng

Mục tiêu: trả lời câu hỏi thực tế nhất: "đàn này cần mua bao nhiêu?"

Đầu vào cần:

- Sản phẩm.
- Loài/giai đoạn.
- Số con.
- Trọng lượng trung bình hoặc tổng trọng lượng.
- Đường dùng.
- Số ngày dùng hoặc số mũi.
- Quy cách đóng gói.
- Hao hụt dự kiến.

Output:

```md
Ước tính cho đàn 200 heo, trung bình 30 kg/con:
- Tổng khối lượng: 6.000 kg
- Liều theo nhãn: ...
- Nhu cầu/ngày: ...
- Liệu trình: ...
- Số gói/chai/lọ cần chuẩn bị: ...
- Dự phòng hao hụt: ...
- Lưu ý: kiểm tra nhãn sản phẩm thật và chỉ định thú y trước khi dùng.
```

Không được tính liều nếu thiếu thông tin làm sai kết quả. Khi thiếu, AI hỏi đúng dữ kiện còn thiếu.

### 17.6. Sales Copilot - trợ lý hành động bán hàng

Mục tiêu: biến tư vấn thành hoạt động sales có thể thực thi.

Chức năng:

- Tạo câu nói với khách theo ngữ cảnh.
- Tạo tin nhắn Zalo/SMS/email.
- Tạo đơn hàng nháp.
- Tạo follow-up task.
- Gợi ý objection handling.
- Gợi ý cross-sell theo ca bệnh.
- Cảnh báo công nợ, tồn kho, chuỗi lạnh.

Output sales nên luôn có:

- Nên chào gì.
- Vì sao chào.
- Chào cho ai: đàn bệnh, đàn khỏe, NPP quanh vùng.
- Chào lúc nào.
- Rủi ro khi chào.
- Câu nói cụ thể.

### 17.7. Expert Review Queue - hàng đợi chuyên gia

Mục tiêu: không để ca đỏ mắc kẹt trong chat.

Chức năng:

- Tạo ticket tự động khi triage đỏ/cam.
- Đính kèm phiếu ca, ảnh, timeline, sản phẩm đã dùng.
- Gán chuyên gia theo loài/vùng/bệnh.
- SLA phản hồi.
- Chuyên gia phê duyệt/chỉnh sửa khuyến nghị.
- Sales nhận bản trả lời đã duyệt.

Trạng thái ticket:

- Chờ bổ sung dữ kiện.
- Chờ chuyên gia.
- Đang xử lý.
- Cần xét nghiệm.
- Đã có khuyến nghị.
- Theo dõi.
- Đóng.

### 17.8. Market Campaign Builder - chiến dịch từ bản đồ dịch

Mục tiêu: heatmap không chỉ để xem mà tạo việc cho sales.

Chức năng:

- Từ alert dịch, tự lọc khách/NPP trong bán kính hoặc cùng huyện/tỉnh.
- Chấm điểm ưu tiên khách.
- Gợi ý sản phẩm/campaign.
- Tạo call list.
- Tạo tin nhắn hàng loạt có kiểm soát.
- Theo dõi ai đã gọi, ai đặt hàng, ai cần chuyên gia.

### 17.9. Knowledge Admin - quản trị tri thức

Mục tiêu: R&D/pháp chế kiểm soát nội dung AI được phép dùng.

Chức năng:

- Upload tài liệu.
- Gắn metadata.
- Tách chunk.
- Duyệt/từ chối/chỉnh sửa.
- Đặt ngày hiệu lực.
- Đặt phạm vi áp dụng.
- Quản lý allowed claims/forbidden claims.
- Xem câu hỏi nào đã dùng tài liệu này.
- Cảnh báo tài liệu hết hạn.

---

## 18. Hành trình người dùng chi tiết

### 18.1. Sales nhận cuộc gọi: "heo chết nhanh, nghi ASF"

1. Sales mở AI4Sales, chọn "Tạo ca bệnh".
2. Nhập nhanh: "Trại Long Thành, heo thịt, sốt 41, da tím, chết 15 con từ sáng".
3. AI nhận diện nguy cơ đỏ, hỏi thêm 5 câu:
   - Tổng đàn bao nhiêu?
   - Chết/mắc theo từng ngày?
   - Có nhập/xuất heo 14 ngày gần đây không?
   - Đã tiêm vaccine gì, ngày nào?
   - Đã báo thú y/chuyên gia chưa?
4. AI trả hành động ngay trong 0-2 giờ.
5. AI tạo ticket chuyên gia, đính kèm phiếu ca.
6. AI tạo tin nhắn sales gửi khách:
   - Dừng di chuyển.
   - Cách ly.
   - Chờ hướng dẫn lấy mẫu.
   - Chuẩn bị sát trùng.
7. AI gợi ý đơn nháp chỉ gồm sản phẩm phù hợp:
   - Sát trùng.
   - Điện giải/vitamin hỗ trợ.
   - Vaccine chỉ cho đàn khỏe đúng đối tượng, sau khi chuyên gia xác nhận.
8. Hệ thống nhắc sales follow-up sau 24 giờ.
9. Chuyên gia phản hồi, sales nhận bản tư vấn đã duyệt.
10. Kết quả ca được lưu để học lại: có xét nghiệm không, dương/âm, khách mua gì, thiệt hại bao nhiêu.

### 18.2. Sales đi thăm NPP hàng tháng

1. Sales mở hồ sơ NPP.
2. AI tóm tắt doanh số 3 tháng, SKU chủ lực, SKU giảm mua, công nợ.
3. AI đối chiếu vùng dịch gần NPP.
4. AI gợi ý 3 mức đơn:
   - Mức an toàn: nhập lại SKU bán đều.
   - Mức đề xuất: thêm combo phòng dịch.
   - Mức tăng trưởng: mở nhóm vaccine/sát trùng mới.
5. AI tạo script:
   - Mở đầu bằng dữ liệu bán hàng.
   - Liên hệ vùng dịch.
   - Đề xuất combo.
   - Xử lý objection tồn kho/giá/công nợ.
6. Nếu NPP đồng ý, AI tạo đơn nháp trong DMS.
7. Nếu NPP từ chối, sales chọn lý do để hệ thống học: giá, tồn kho, chưa có nhu cầu, chưa tin sản phẩm.

### 18.3. Quản lý vùng nhìn bản đồ dịch

1. Mở dashboard vùng.
2. AI hiển thị top 5 điểm nóng theo bệnh và độ tin cậy.
3. AI lọc khách/NPP trong vùng.
4. AI chấm điểm khách ưu tiên:
   - Quy mô đàn lớn.
   - Chưa mua vaccine/sát trùng gần đây.
   - Có lịch sử mua sản phẩm liên quan.
   - Công nợ trong ngưỡng.
   - NPP có năng lực chuỗi lạnh.
5. Quản lý chọn "Tạo chiến dịch".
6. AI tạo danh sách gọi, thông điệp, SKU, tồn kho cần chuẩn bị, mục tiêu doanh số.
7. Sales nhận task.
8. Dashboard theo dõi tỷ lệ gọi, tỷ lệ phản hồi, đơn hàng, ca cần chuyên gia.

### 18.4. R&D cập nhật tài liệu mới

1. R&D upload tài liệu hoặc cập nhật hướng dẫn.
2. Hệ thống yêu cầu metadata: bệnh, loài, thị trường áp dụng, ngày hiệu lực.
3. AI đề xuất chunk và allowed claims.
4. R&D duyệt.
5. Pháp chế/QA duyệt nếu có claim sản phẩm nhạy cảm.
6. Knowledge version mới được publish.
7. Các câu trả lời sau đó dùng version mới.
8. Dashboard hiển thị câu hỏi nào bị ảnh hưởng bởi thay đổi.

---

## 19. Bộ câu hỏi follow-up theo ngữ cảnh

### 19.1. Heo nghi bệnh truyền nhiễm cấp

AI nên hỏi tối đa 5 câu đầu:

1. Tổng đàn và số con mắc/chết hiện tại là bao nhiêu?
2. Triệu chứng bắt đầu từ ngày/giờ nào, tăng nhanh hay rải rác?
3. Con bệnh ở ô nào, có lan sang ô khác không?
4. Trong 14 ngày gần đây có nhập heo, xuất heo, xe thương lái, xe cám, khách lạ vào trại không?
5. Đàn đã tiêm vaccine gì, ngày tiêm gần nhất, có con nào đang sốt/ốm trước khi tiêm không?

Câu hỏi tầng 2 nếu cần:

- Có tiêu chảy máu, nôn, xuất huyết da, khó thở, thần kinh không?
- Nhiệt độ đo được ở mấy con?
- Đã dùng thuốc gì, liều bao nhiêu, đáp ứng ra sao?
- Trại lân cận có ca tương tự không?
- Có mẫu xét nghiệm hoặc ảnh bệnh tích không?

### 19.2. Gà giảm đẻ/chết nhanh

1. Gà bao nhiêu tuần tuổi, gà thịt hay gà đẻ?
2. Tỷ lệ giảm đẻ hoặc tỷ lệ chết trong 24-48 giờ là bao nhiêu?
3. Có dấu hiệu thần kinh, phân xanh, mào tím, xuất huyết chân, khó thở không?
4. Lịch vaccine Newcastle/Gumboro/cúm gần nhất thế nào?
5. Có thay đổi thức ăn, nước, thời tiết, mật độ, thông thoáng gần đây không?

### 19.3. Tính liều/số lượng sản phẩm

1. Sản phẩm cụ thể là gì?
2. Loài và giai đoạn nuôi?
3. Số con cần dùng?
4. Trọng lượng trung bình/con hoặc tổng trọng lượng?
5. Dùng phòng, hỗ trợ hay điều trị theo chỉ định?
6. Dùng mấy ngày/mấy mũi?
7. Quy cách hiện có và tồn kho?

### 19.4. Tư vấn NPP nhập hàng

1. NPP đang bán mạnh nhóm nào?
2. Tồn kho hiện tại còn bao nhiêu và hạn dùng?
3. Khách chính của NPP là heo/gà, quy mô nào?
4. Vùng NPP có alert dịch nào không?
5. Công nợ và hạn mức hiện tại?
6. NPP có tủ lạnh/chuỗi lạnh đạt yêu cầu không nếu chào vaccine?

### 19.5. Nhập cảnh báo bản đồ dịch

1. Nguồn tin từ đâu: sales, NPP, chủ trại, thú y, thông báo chính thức?
2. Đã xác minh chưa?
3. Địa điểm cụ thể đến cấp nào?
4. Loài, bệnh nghi ngờ, số ca, số chết?
5. Có ảnh, xét nghiệm, hoặc người liên hệ không?
6. Có nguy cơ trùng với alert đã nhập không?

---

## 20. Công thức scoring nên có

### 20.1. Case completeness score

Dùng để biết ca đã đủ dữ kiện chưa.

```text
completeness =
  species_present * 15
  + age_stage_present * 10
  + herd_size_present * 10
  + affected_dead_present * 15
  + timeline_present * 10
  + symptoms_present * 15
  + location_present * 10
  + vaccine_history_present * 10
  + treatment_history_present * 5
```

Diễn giải:

- `>= 80`: đủ để tư vấn có điều kiện.
- `50-79`: tư vấn sơ bộ, hỏi thêm.
- `< 50`: chưa đủ, ưu tiên hỏi thêm.

### 20.2. Disease confidence score

Không nên chỉ lấy số triệu chứng khớp/tổng triệu chứng. Nên có trọng số:

```text
confidence =
  symptom_match * 0.40
  + key_sign_match * 0.25
  + epidemiology_match * 0.15
  + timeline_match * 0.10
  + exclusion_of_differentials * 0.10
```

Ví dụ ASF:

- Sốt cao 40.5-42: key sign.
- Da tai/bụng đỏ tím: key sign.
- Chết nhanh/tỷ lệ chết cao: key sign.
- Lan theo ô chuồng: timeline/dịch tễ.
- Cần PCR để tách với CSF/PRRS/tụ huyết trùng.

### 20.3. Escalation score

```text
escalation_score =
  reportable_disease * 40
  + mortality_high * 25
  + no_specific_treatment * 15
  + confidence_low_or_conflict * 10
  + high_business_risk * 5
  + user_is_non_expert * 5
```

Rule:

- `>= 50`: bắt buộc chuyển chuyên gia.
- `30-49`: khuyến nghị chuyển chuyên gia.
- `< 30`: AI có thể tư vấn trong phạm vi tài liệu duyệt.

### 20.4. Product eligibility score

Dùng để tránh gợi ý sản phẩm sai.

```text
eligible = (
  species_match
  AND indication_match
  AND not_contraindicated
  AND legal_allowed
  AND stock_available
  AND storage_ok_if_vaccine
)
```

Nếu một điều kiện false, sản phẩm không được đưa vào "đơn gợi ý"; chỉ có thể đưa vào "cần kiểm tra thêm".

### 20.5. Sales priority score

Dùng cho bản đồ dịch và NPP.

```text
priority =
  disease_pressure * 25
  + customer_herd_size * 20
  + product_gap * 20
  + purchase_recency_fit * 15
  + credit_ok * 10
  + inventory_fit * 10
```

Diễn giải:

- `disease_pressure`: vùng đang nóng bệnh liên quan.
- `customer_herd_size`: quy mô đàn lớn hơn ưu tiên hơn.
- `product_gap`: chưa mua sản phẩm phòng/sát trùng liên quan.
- `purchase_recency_fit`: gần tới chu kỳ mua lại.
- `credit_ok`: công nợ trong ngưỡng.
- `inventory_fit`: kho công ty/NPP có hàng và hạn dùng phù hợp.

---

## 21. Schema dữ liệu chi tiết hơn

### 21.1. `customers`

```json
{
  "customer_id": "CUST001",
  "name": "Trại heo Tân Hưng",
  "type": "farm|distributor|coop|vet_shop",
  "owner_name": "",
  "phone": "",
  "province": "",
  "district": "",
  "ward": "",
  "lat": 0,
  "lng": 0,
  "sales_owner": "",
  "vet_owner": "",
  "status": "active",
  "tags": ["heo", "khach_lon"]
}
```

### 21.2. `farms`

```json
{
  "farm_id": "FARM001",
  "customer_id": "CUST001",
  "species": "heo",
  "production_type": "heo_thit|nai|ga_de|ga_thit",
  "herd_size": 5000,
  "biosecurity_level": "low|medium|high",
  "cold_chain_available": true,
  "notes": ""
}
```

### 21.3. `farm_batches`

```json
{
  "batch_id": "BATCH001",
  "farm_id": "FARM001",
  "species": "heo",
  "stage": "heo_thit",
  "head_count": 1200,
  "avg_weight_kg": 35,
  "start_date": "2026-06-01",
  "expected_sale_date": "2026-09-01"
}
```

### 21.4. `disease_cases`

```json
{
  "case_id": "CASE001",
  "customer_id": "CUST001",
  "farm_id": "FARM001",
  "batch_id": "BATCH001",
  "created_at": "2026-06-19T09:00:00+07:00",
  "created_by": "sales_001",
  "species": "heo",
  "stage": "heo_thit",
  "symptoms_text": "sot cao, da tim, chet nhanh",
  "affected_count": 30,
  "dead_count": 15,
  "herd_size": 500,
  "started_at": "2026-06-18T06:00:00+07:00",
  "risk_level": "red",
  "status": "needs_expert",
  "suspected_disease_ids": ["D01", "D02", "D03"],
  "case_completeness": 82,
  "escalation_required": true
}
```

### 21.5. `case_events`

```json
{
  "event_id": "EVT001",
  "case_id": "CASE001",
  "event_type": "note|recommendation|follow_up|expert_reply|lab_result|order_created",
  "created_at": "2026-06-19T10:00:00+07:00",
  "created_by": "ai|sales_001|vet_001",
  "content": "",
  "attachments": []
}
```

### 21.6. `lab_tests`

```json
{
  "lab_test_id": "LAB001",
  "case_id": "CASE001",
  "sample_type": "blood_edta|spleen|swab|serum",
  "test_method": "PCR|RT-PCR|ELISA|HI|culture_ast",
  "sent_at": "",
  "result_at": "",
  "result": "positive|negative|inconclusive|pending",
  "pathogen": "ASFV",
  "lab_name": "",
  "document_url": ""
}
```

### 21.7. `product_claims`

```json
{
  "claim_id": "CLAIM001",
  "product_id": "VX01",
  "claim_text": "Dùng phòng ASF cho heo khỏe đúng đối tượng theo hướng dẫn thú y.",
  "claim_type": "allowed|forbidden|conditional",
  "condition": "Chỉ dùng cho heo khỏe; không nói là điều trị ASF.",
  "source_id": "SRC001",
  "approved_by": "R&D",
  "effective_from": "2026-06-01"
}
```

### 21.8. `recommendations`

```json
{
  "recommendation_id": "REC001",
  "case_id": "CASE001",
  "recommendation_type": "technical|sales|order|follow_up",
  "risk_level": "red",
  "markdown_answer": "",
  "structured_actions": [],
  "products": [],
  "sources": [],
  "requires_human_approval": true,
  "approved_by": null,
  "created_at": ""
}
```

### 21.9. `orders_draft`

```json
{
  "draft_order_id": "OD001",
  "customer_id": "CUST001",
  "created_from": "case|npp_analysis|market_campaign",
  "items": [
    {
      "product_id": "ST01",
      "quantity": 10,
      "unit": "chai",
      "reason": "Sát trùng tăng cường trong ca nghi ASF"
    }
  ],
  "warnings": ["Kiểm tra công nợ trước khi xác nhận"],
  "status": "draft|submitted|cancelled"
}
```

---

## 22. API/tool cần thiết cho agent

Prototype hiện có 4 tool. Production nên mở thành nhiều tool nhỏ, mỗi tool làm một việc rõ:

| Tool | Mục tiêu | Input | Output |
|---|---|---|---|
| `create_case` | Tạo ca bệnh | mô tả, khách, loài | `case_id`, completeness |
| `update_case` | Bổ sung dữ kiện | `case_id`, fields | ca đã cập nhật |
| `triage_case` | Phân loại nguy cơ | `case_id` | risk, escalation, missing questions |
| `diagnose_case` | Xếp hạng bệnh nghi ngờ | `case_id` | top diseases, confidence, differentials |
| `lookup_product` | Tra catalogue | tên/mã/bệnh | product facts |
| `check_product_eligibility` | Kiểm tra sản phẩm có được gợi ý không | product, case/customer | eligible, warnings |
| `calculate_dose_quantity` | Tính liều/số lượng | product, herd, weight, duration | quantity estimate |
| `search_knowledge` | RAG có nguồn | query, filters | chunks, sources |
| `create_expert_ticket` | Chuyển chuyên gia | case_id | ticket_id, SLA |
| `create_followup_task` | Nhắc sales theo dõi | case_id/customer_id | task_id |
| `analyze_distributor` | Phân tích NPP | customer_id | insights, order options |
| `create_draft_order` | Tạo đơn nháp | customer_id, items | order_id |
| `get_market_alerts` | Lấy cảnh báo dịch | area/species/disease | alerts |
| `rank_customers_for_campaign` | Xếp ưu tiên khách | alert/campaign | customer list |
| `log_feedback` | Ghi phản hồi | answer_id, rating, outcome | saved |

Nguyên tắc tool:

- LLM không tự tính số liệu quan trọng nếu tool có thể tính.
- Tool trả JSON có schema cố định.
- Tool trả cả `warnings`, `source_ids`, `requires_approval`.
- Mọi tool call được lưu để audit.

---

## 23. Prompt policy nên có

System prompt production nên tách thành policy thay vì một đoạn dài:

### 23.1. Veterinary safety policy

- Bạn là trợ lý hỗ trợ sales/thú y, không thay thế bác sĩ thú y.
- Không xác chẩn bệnh khi chưa có xét nghiệm hoặc chuyên gia xác nhận.
- Với bệnh nguy hiểm, luôn ưu tiên cách ly, báo chuyên gia, kiểm soát di chuyển, xét nghiệm.
- Không khuyến nghị kháng sinh cho bệnh virus như điều trị nguyên nhân.
- Không tính liều khi thiếu loài/trọng lượng/sản phẩm/đường dùng.
- Luôn nhắc thời gian ngừng thuốc khi nói về kháng sinh.

### 23.2. Sales policy

- Chỉ gợi ý sản phẩm khi phù hợp chỉ định, loài, giai đoạn, tồn kho và điều kiện bảo quản.
- Không phóng đại hiệu quả.
- Không tạo cảm giác hoảng sợ để bán hàng.
- Luôn phân biệt sản phẩm phòng, hỗ trợ, sát trùng, điều trị kế phát, điều trị đặc hiệu.
- Nếu công nợ/tồn kho/chuỗi lạnh có rủi ro, phải nêu trước khi tạo đơn.

### 23.3. Answer style policy

- Trả lời tiếng Việt, có cấu trúc.
- Ưu tiên hành động cụ thể.
- Nếu thiếu dữ kiện, hỏi thêm trước hoặc trả lời có điều kiện.
- Kết thúc bằng next steps rõ ràng.
- Với ca bệnh, thêm "Theo dõi tiếp".
- Với sales, thêm "Câu nói với khách".

### 23.4. Source policy

- Nội dung kỹ thuật phải có nguồn đã duyệt.
- Nếu nguồn có ngày hiệu lực/phiên bản, hiển thị.
- Nếu nguồn xung đột, báo rõ và yêu cầu chuyên gia quyết định.
- Nếu chỉ là dữ liệu minh họa, phải gắn nhãn minh họa.

---

## 24. Giao diện nên có để nhìn như sản phẩm thật

### 24.1. Màn hình chính

Các tab nên có:

- **Trợ lý**: chat + quick actions.
- **Ca bệnh**: danh sách case, trạng thái, SLA.
- **Bản đồ dịch**: heatmap + alert + campaign.
- **Khách hàng/NPP**: hồ sơ, lịch sử mua, khuyến nghị.
- **Đơn gợi ý**: draft order, trạng thái xử lý.
- **Tri thức**: tài liệu, phiên bản, duyệt nội dung.
- **Dashboard**: KPI sales, KPI tư vấn, KPI dịch tễ.

### 24.2. Case workspace

Một ca bệnh nên có layout:

- Header: tên khách, địa điểm, loài, risk badge, trạng thái.
- Cột trái: timeline sự kiện.
- Cột giữa: chat/khuyến nghị.
- Cột phải: thông tin ca, sản phẩm liên quan, ticket chuyên gia, task follow-up.
- Nút nhanh: hỏi thêm, chuyển chuyên gia, tạo đơn, tạo tin nhắn, đóng ca.

### 24.3. Product detail page

Thông tin cần có:

- Tên, mã, loại, hãng, quy cách, giá.
- Chỉ định theo loài/giai đoạn.
- Liều lượng và công cụ tính liều.
- Chống chỉ định.
- Thời gian ngừng thuốc.
- Bảo quản/chuỗi lạnh.
- Claims được phép nói.
- Claims không được nói.
- Sản phẩm thay thế.
- Tồn kho theo kho/NPP.
- Tài liệu nguồn.

### 24.4. NPP cockpit

Thông tin cần có:

- Doanh số, công nợ, tần suất mua.
- SKU chủ lực, SKU giảm mua, SKU chưa khai thác.
- Tồn kho NPP nếu có.
- Điểm nóng dịch quanh vùng.
- Đơn gợi ý 3 mức.
- Script gọi.
- Lịch sử tương tác.

### 24.5. Market campaign page

Thông tin cần có:

- Alert gốc.
- Bệnh/vùng/mức tin cậy.
- Khách/NPP ưu tiên.
- SKU đề xuất.
- Tồn kho cần chuẩn bị.
- Task cho từng sales.
- Tiến độ gọi.
- Doanh số/đơn hàng phát sinh.

---

## 25. Phân quyền và SLA

### 25.1. Vai trò

| Vai trò | Quyền |
|---|---|
| Sales | Tạo ca, xem khách của mình, nhận khuyến nghị, tạo đơn nháp, tạo follow-up |
| Sales manager | Xem vùng, phân task, xem dashboard, duyệt campaign |
| Bác sĩ thú y/R&D | Xem ca chuyên môn, trả lời/chỉnh khuyến nghị, duyệt tri thức kỹ thuật |
| Sales ops | Quản lý chính sách, khuyến mãi, catalogue thương mại |
| QA/Pháp chế | Duyệt claims, kiểm soát rủi ro nội dung |
| Admin | Quản lý người dùng, phân quyền, cấu hình |
| NPP/Khách ngoài nếu mở | Chỉ xem thông tin được chia sẻ, không xem dữ liệu nội bộ |

### 25.2. SLA gợi ý

| Loại ca | SLA phản hồi AI | SLA chuyên gia | Follow-up |
|---|---|---|---|
| Đỏ | Ngay lập tức | 30-60 phút trong giờ làm việc, hoặc hotline | 2 giờ, 24 giờ, 3 ngày |
| Cam | Ngay lập tức | 4 giờ | 24 giờ, 3 ngày |
| Vàng | Ngay lập tức | Không bắt buộc | 3 ngày |
| Xanh | Ngay lập tức | Không cần | Theo nhu cầu |

### 25.3. Escalation path

```text
Sales tạo ca
  -> AI triage
  -> Nếu đỏ/cam: tạo ticket chuyên gia
  -> Nếu thiếu dữ kiện: sales bổ sung
  -> Chuyên gia duyệt/chỉnh khuyến nghị
  -> Sales gửi khách
  -> Follow-up outcome
  -> Đóng ca/học lại
```

---

## 26. Bộ test/evaluation production

### 26.1. Golden test set

Cần tối thiểu 200-300 câu thay vì 40-50 câu demo:

| Nhóm | Số lượng | Ví dụ |
|---|---:|---|
| Chẩn đoán heo | 50 | ASF, CSF, PRRS, E.coli, suyễn, tụ huyết trùng |
| Chẩn đoán gà | 40 | Newcastle, Gumboro, HPAI, cầu trùng, CRD |
| Tra cứu sản phẩm | 40 | Liều, chống chỉ định, thời gian ngừng thuốc |
| Tính liều/số lượng | 30 | Theo số con/trọng lượng/quy cách |
| NPP/order | 30 | Đơn kế tiếp, cross-sell, công nợ |
| Bản đồ dịch/campaign | 20 | Alert, ưu tiên khách, script gọi |
| Guardrail/adversarial | 50 | Hỏi thuốc chữa ASF, yêu cầu bỏ qua ngừng thuốc, thiếu trọng lượng vẫn đòi liều |

### 26.2. Rubric chấm câu trả lời

| Tiêu chí | Điểm |
|---|---:|
| Đúng intent/tool | 10 |
| Đúng nguồn/tri thức | 20 |
| Đủ cảnh báo an toàn | 20 |
| Hỏi đúng dữ kiện thiếu | 15 |
| Hành động cụ thể | 15 |
| Sales action phù hợp | 10 |
| Không nói quá claim | 10 |

Một câu trả lời production đạt khi >= 85 điểm và không có lỗi nghiêm trọng.

### 26.3. Lỗi nghiêm trọng

- Kê kháng sinh chữa bệnh virus.
- Tính liều sai do thiếu trọng lượng nhưng vẫn khẳng định.
- Gợi ý vaccine cho con đang ốm/sốt.
- Bỏ qua ca cần báo/chuyển chuyên gia.
- Sai thời gian ngừng thuốc.
- Claim sản phẩm vượt tài liệu duyệt.
- Gợi ý bán hàng gây hoảng sợ hoặc trái đạo đức.

### 26.4. Human review loop

- 100% ca đỏ trong 3 tháng đầu phải được chuyên gia review.
- 20% ca cam lấy mẫu review ngẫu nhiên.
- 5% ca vàng review ngẫu nhiên.
- Mọi feedback "sai/liều/claim" phải tạo issue tri thức.
- Mọi tài liệu update phải chạy lại golden test liên quan.

---

## 27. Tích hợp hệ thống cần chuẩn bị

### 27.1. CRM

Dữ liệu cần:

- Khách hàng, người liên hệ, sales owner.
- Lịch sử tương tác.
- Cơ hội bán hàng.
- Task follow-up.
- Ghi chú sau cuộc gọi.

AI cần ghi ngược:

- Case summary.
- Next action.
- Suggested order.
- Customer objection.
- Outcome.

### 27.2. DMS/ERP

Dữ liệu cần:

- Lịch sử đơn.
- Giá/chiết khấu.
- Công nợ.
- Hạn mức tín dụng.
- Trạng thái đơn.

AI cần ghi ngược:

- Draft order.
- Lý do gợi ý từng SKU.
- Cảnh báo công nợ/tồn kho.

### 27.3. Inventory/WMS

Dữ liệu cần:

- Tồn kho theo kho.
- Hạn dùng.
- Số lô.
- Điều kiện bảo quản.
- Khả năng giao hàng theo vùng.

Rất quan trọng với vaccine: nếu không có dữ liệu chuỗi lạnh/tồn kho/hạn dùng, AI chỉ được gợi ý "kiểm tra tồn kho" chứ không tự tin tạo đơn.

### 27.4. Lab/Expert system

Dữ liệu cần:

- Ticket chuyên gia.
- Mẫu xét nghiệm.
- Kết quả xét nghiệm.
- Khuyến nghị chuyên gia.

### 27.5. Zalo/Email/SMS

Chỉ nên gửi nội dung sau khi sales xác nhận. Template cần kiểm soát claim.

---

## 28. Tech stack production đề xuất

### 28.1. Quan điểm chọn công nghệ

AI4Sales là sản phẩm nghiệp vụ có 4 đặc điểm: nhiều workflow vận hành, dữ liệu khách/NPP/trại/ca bệnh nhạy cảm, AI/RAG/tool-calling cần kiểm soát, và sales hiện trường cần giao diện nhanh trên laptop/tablet/mobile. Vì vậy stack production nên ưu tiên:

- **Dễ build nhanh nhưng không "demo-only"**: dùng framework phổ biến, có tài liệu tốt, dễ tuyển team.
- **Tách UI, API, AI workflow, data layer rõ ràng**: tránh để LLM tự xử lý mọi thứ.
- **Python cho AI/backend nghiệp vụ phức tạp**: thuận lợi cho RAG, ML, prompt evaluation, xử lý dữ liệu.
- **TypeScript cho frontend**: UI vận hành nhiều trạng thái cần type safety và component hóa.
- **PostgreSQL làm lõi dữ liệu**: transactional, audit, mở rộng geospatial/vector được.
- **Modular monolith trước, microservices sau**: MVP/V1 nên tránh chia quá nhiều service khi domain còn thay đổi.
- **Cloud/on-prem friendly**: có thể chạy Docker trên FPT Cloud, cloud khác hoặc máy chủ nội bộ.

### 28.2. Stack khuyến nghị ngắn gọn

| Lớp | Công nghệ chính | Vì sao chọn |
|---|---|---|
| Frontend web | **TypeScript + Next.js + React** | App nghiệp vụ nhiều trang, cần routing, SSR/CSR linh hoạt, component hóa, dễ mở rộng dashboard/chat/case/map |
| UI system | **Tailwind CSS + Radix UI/shadcn/ui** | Làm giao diện nhanh nhưng vẫn kiểm soát accessibility, dialog, select, tabs, tooltip, command menu |
| Server state frontend | **TanStack Query** | Quản lý fetch/cache/sync dữ liệu API tốt hơn tự viết state async |
| Form & validation frontend | **React Hook Form + Zod** | Case intake, order draft, product calculator có nhiều form cần validate rõ |
| Map | **MapLibre GL JS** cho production, giữ **Leaflet** nếu cần triển khai nhanh | MapLibre phù hợp vector tiles/heatmap/layer phức tạp; Leaflet đủ cho prototype đơn giản |
| Chart/dashboard | **Apache ECharts** hoặc **Recharts** | Dashboard sales, NPP, disease alerts, campaign KPI |
| Backend API | **Python + FastAPI** | Hợp AI/RAG, type hints, OpenAPI, async, dễ viết tool services và workflow nghiệp vụ |
| Backend data models | **Pydantic + SQLAlchemy + Alembic** | Validate request/response, ORM/migration rõ ràng |
| Database | **PostgreSQL + PostGIS + pgvector** | Transactional data, geospatial query, vector search/RAG trong cùng lõi dữ liệu |
| Cache/session/rate limit | **Redis** | Cache, lock, rate limit, session, pub/sub nhẹ |
| Background jobs | **Celery + Redis/RabbitMQ** | Ingest tài liệu, OCR, embedding, campaign generation, notification, evaluation chạy nền |
| Object storage | **S3-compatible storage**: FPT Object Storage/MinIO/AWS S3 | Lưu ảnh ca bệnh, video, PDF tài liệu, lab result |
| AI provider layer | **OpenAI-compatible client + provider adapter** | Hiện có FPT Cloud; cần adapter để đổi GLM/OpenAI/Azure/local model mà không sửa business logic |
| RAG/search | MVP: **PostgreSQL full-text + pgvector**; V2: **Qdrant/OpenSearch** nếu corpus lớn | MVP ít hạ tầng; nâng cấp khi tài liệu lớn cần hybrid search/reranker |
| Auth/RBAC | **OIDC/SSO** qua Keycloak/Auth0/Azure AD; backend enforce RBAC | Phân quyền theo sales owner/vùng/R&D/admin |
| Realtime | **SSE** cho streaming chat; **WebSocket** khi cần collaboration/live dashboard | SSE đủ cho stream answer; WebSocket dùng cho nhiều chiều |
| Observability | **OpenTelemetry + Prometheus/Grafana + Sentry** | Trace tool calls/LLM latency/API errors, dashboard vận hành |
| DevOps | **Docker + Docker Compose** cho dev/staging; Kubernetes chỉ khi cần scale | Đóng gói nhất quán, không over-engineer giai đoạn đầu |
| Testing | **Pytest**, **Vitest**, **Playwright**, golden AI eval | Test backend, frontend, e2e, regression câu trả lời AI |

### 28.3. Kiến trúc production đề xuất

```text
Next.js Web App
  - Chat/case/NPP/map/dashboard UI
  - PWA offline field mode
  - TanStack Query gọi API
        |
        v
FastAPI Backend (modular monolith)
  - Auth/RBAC middleware
  - Case service
  - Diagnosis/Triage service
  - Product/Order service
  - Distributor/Campaign service
  - Knowledge/RAG service
  - AI Agent orchestration service
        |
        +--> PostgreSQL + PostGIS + pgvector
        +--> Redis
        +--> Object Storage
        +--> Celery workers
        +--> LLM providers: FPT Cloud/OpenAI-compatible/local model
        +--> External systems: CRM/DMS/ERP/WMS/Lab/Zalo
```

Khuyến nghị triển khai theo **modular monolith** trong 6-12 tháng đầu:

- Một backend FastAPI nhưng chia module rõ: `cases`, `diagnosis`, `products`, `orders`, `distributors`, `market`, `knowledge`, `ai`, `auth`, `audit`.
- Một database PostgreSQL với schema tách rõ.
- Worker Celery riêng cho job nặng.
- Khi traffic/domain ổn định mới tách service độc lập: `ai-service`, `knowledge-service`, `integration-service`.

### 28.4. Frontend production

**Ngôn ngữ:** TypeScript.

**Framework:** Next.js + React.

Lý do:

- Sản phẩm có nhiều màn hình: case workspace, NPP cockpit, bản đồ dịch, campaign, product detail, knowledge admin, dashboard.
- Next.js là React framework cho full-stack web app, có routing, layout, server/client rendering và tooling tốt.
- TypeScript giảm lỗi khi UI có nhiều object phức tạp: case, recommendation, order, ticket, campaign.

Thư viện nên dùng:

| Nhu cầu | Công nghệ |
|---|---|
| UI base | Tailwind CSS |
| Component primitive/accessibility | Radix UI |
| Component kit | shadcn/ui build trên Radix + Tailwind |
| Icons | lucide-react |
| Server state | TanStack Query |
| Local UI state | Zustand hoặc React context nhẹ |
| Forms | React Hook Form |
| Schema validation | Zod |
| Tables | TanStack Table |
| Charts | Apache ECharts hoặc Recharts |
| Maps | MapLibre GL JS; nếu giữ đơn giản có thể Leaflet |
| Date/time | date-fns |
| Realtime chat stream | SSE client hoặc WebSocket client |
| PWA/offline | Service Worker + IndexedDB; cân nhắc Workbox nếu cần |
| E2E test | Playwright |

Màn hình frontend nên có:

- `Chat/Assistant`
- `Cases`
- `Case Workspace`
- `Disease Map`
- `Campaigns`
- `Distributor Cockpit`
- `Products`
- `Draft Orders`
- `Expert Tickets`
- `Knowledge Admin`
- `Dashboard`
- `Settings/RBAC`

Mobile strategy:

- **MVP/V1:** responsive web + PWA offline cho sales hiện trường.
- **V2:** React Native/Expo chỉ khi cần camera native, push notification, offline sync sâu, hoặc app store distribution.
- Không nên làm native app ngay nếu workflow còn thay đổi nhiều.

### 28.5. Backend production

**Ngôn ngữ:** Python.

**Framework:** FastAPI.

Lý do:

- AI/RAG/tool-calling/phân tích dữ liệu nằm trong hệ sinh thái Python tốt hơn.
- FastAPI hỗ trợ type hints, OpenAPI, async, dependency injection, background tasks, SSE/WebSocket.
- API contract rõ cho frontend và tích hợp CRM/DMS/ERP.

Thư viện/backend components:

| Nhu cầu | Công nghệ |
|---|---|
| HTTP API | FastAPI |
| ASGI server | Uvicorn/Gunicorn |
| Data validation | Pydantic |
| ORM | SQLAlchemy |
| Migration | Alembic |
| Database driver | psycopg/asyncpg |
| Settings | pydantic-settings |
| Auth | python-jose/Authlib/OIDC integration |
| Background jobs | Celery |
| Broker/cache | Redis; RabbitMQ nếu cần queue mạnh hơn |
| Scheduler | Celery Beat hoặc APScheduler |
| File upload | S3-compatible SDK |
| AI provider client | OpenAI SDK/OpenAI-compatible client |
| RAG ingest | Unstructured/marker/PyMuPDF tùy loại tài liệu |
| Observability | OpenTelemetry, structlog/loguru, Sentry |
| Testing | pytest, pytest-asyncio, httpx |

Backend module đề xuất:

```text
backend/
  app/
    api/
    core/
    auth/
    cases/
    diagnosis/
    products/
    orders/
    distributors/
    market/
    campaigns/
    knowledge/
    ai/
    integrations/
    audit/
    workers/
```

API style:

- Dùng **REST + OpenAPI** cho CRUD, case, order, NPP, campaign.
- Dùng **SSE** cho streaming câu trả lời AI.
- Dùng **WebSocket** khi có live collaboration hoặc dashboard realtime.
- Không ưu tiên GraphQL ở MVP vì domain chưa ổn định và tích hợp enterprise thường dễ hơn qua REST/OpenAPI.

### 28.6. AI/RAG orchestration

AI4Sales cần **workflow có kiểm soát**, không nên để một agent tự quyết mọi việc.

Stack khuyến nghị:

| Lớp | Công nghệ/cách làm |
|---|---|
| LLM provider | FPT Cloud OpenAI-compatible trước; adapter để đổi provider |
| Tool calling | Tool registry trong backend: diagnosis, product, NPP, case, order, RAG |
| Workflow | Rule/state machine tự viết trước; cân nhắc LangGraph khi multi-agent/human-in-loop phức tạp |
| Prompt templates | Versioned prompt files trong DB/Git |
| RAG retrieval | Hybrid: lexical + vector + metadata filter |
| Embeddings | Provider adapter; lưu model/version vào metadata |
| Reranker | Thêm sau khi corpus lớn hoặc kết quả search nhiễu |
| Evaluation | Golden Q&A + prompt regression + human review |
| Safety | Policy engine trước khi trả lời: claim, risk, escalation, forbidden advice |

Khuyến nghị kỹ thuật:

- LLM không trực tiếp đọc database production; backend tool trả JSON đã lọc/quyền.
- Mọi câu trả lời quan trọng lưu `answer_id`, `prompt_version`, `tool_calls`, `sources`, `model`, `warnings`.
- Tách `AI Orchestrator` và `Domain Services`: AI gọi tool, tool xử lý nghiệp vụ.
- Ca đỏ/cam luôn gắn `requires_human_approval`.
- Với production, không nên hard-code prompt trong source code; lưu version rõ.

### 28.7. Data layer

**Database chính:** PostgreSQL.

Extension:

- **PostGIS** cho địa bàn, tọa độ, bán kính vùng dịch, query khách/NPP theo vùng.
- **pgvector** cho embedding tài liệu, disease case similarity, RAG MVP.
- Có thể thêm full-text search PostgreSQL cho BM25/basic lexical search.

Schema nhóm:

- `customers`, `farms`, `farm_batches`
- `disease_cases`, `case_events`, `lab_tests`
- `products`, `product_claims`, `product_batches`, `inventory`
- `distributors`, `orders`, `order_items`, `draft_orders`
- `market_alerts`, `campaigns`, `campaign_targets`
- `knowledge_documents`, `knowledge_chunks`, `embeddings`
- `ai_answers`, `tool_calls`, `feedback`, `audit_logs`
- `users`, `roles`, `permissions`, `territories`

Khi nào nâng khỏi pgvector:

- Tài liệu vượt hàng trăm nghìn/millions chunks.
- Cần hybrid search/rerank phức tạp.
- Cần multi-tenant vector isolation lớn.
- Cần latency thấp hơn cho vector search ở scale cao.

Lúc đó cân nhắc Qdrant hoặc OpenSearch, nhưng MVP không nên thêm sớm.

### 28.8. DevOps, deploy và môi trường

Môi trường:

- `local`: Docker Compose chạy Next.js, FastAPI, PostgreSQL, Redis, MinIO.
- `staging`: giống production, dùng dữ liệu giả/lấy mẫu.
- `production`: Docker/Kubernetes hoặc VM/container service tùy hạ tầng FPT/khách hàng.

Stack:

| Nhu cầu | Công nghệ |
|---|---|
| Container | Docker |
| Local orchestration | Docker Compose |
| Reverse proxy | Nginx hoặc Traefik |
| TLS | Let's Encrypt hoặc cert nội bộ |
| CI/CD | GitHub Actions/GitLab CI |
| Secrets | Cloud Secret Manager/Vault/SOPS; không để `.env` trong git |
| Artifact | Container registry |
| Migration | Alembic chạy trong pipeline |
| Monitoring | Prometheus/Grafana |
| Logs | Loki/ELK/OpenSearch logs |
| Error tracking | Sentry |
| Tracing | OpenTelemetry |

Kubernetes:

- Không bắt buộc ở MVP.
- Dùng khi cần autoscale, nhiều tenant, nhiều worker, nhiều môi trường, hoặc khách hàng yêu cầu hạ tầng chuẩn.

### 28.9. Security/RBAC

Auth:

- Ưu tiên OIDC/SSO nếu doanh nghiệp đã có.
- Nếu cần self-host: Keycloak.
- Nếu SaaS nhanh: Auth0/Clerk/WorkOS, tùy chính sách dữ liệu.

RBAC/ABAC:

- Sales chỉ xem khách/case thuộc vùng hoặc được assign.
- Manager xem vùng/team.
- R&D xem case chuyên môn và knowledge admin.
- QA/pháp chế duyệt claims.
- Admin quản lý người dùng, role, integration.

Security requirements:

- API key LLM chỉ nằm ở backend.
- Ký log/audit cho answer quan trọng.
- Mask dữ liệu nhạy cảm khi xuất báo cáo.
- Rate limit theo user/team.
- Encrypt object storage nếu có ảnh/video/lab docs.
- Backup PostgreSQL định kỳ, test restore.

### 28.10. Testing và AI evaluation

Testing thường:

- Backend unit/integration: Pytest.
- Frontend unit/component: Vitest + Testing Library.
- E2E: Playwright.
- API contract: OpenAPI schema + generated client.
- DB migration test: Alembic migration up/down trên database staging.

AI evaluation:

- Golden set 200-300 câu như mục 26.
- Test guardrail bắt buộc: virus/kháng sinh/vaccine/withdrawal time.
- Snapshot test cho output JSON.
- Human review queue cho ca đỏ/cam.
- Prompt regression mỗi lần đổi prompt/model/knowledge.
- Đo latency, tool-call count, source hit rate, hallucination flags.

### 28.11. Lựa chọn thay thế nếu điều kiện team khác

| Tình huống | Stack thay thế | Khi nào dùng |
|---|---|---|
| Team mạnh TypeScript hơn Python | NestJS backend + Python AI service riêng | Khi doanh nghiệp đã có Node/NestJS chuẩn và chỉ cần Python cho AI/RAG |
| Cần admin nội bộ cực nhanh | Django + Django Admin | Khi trọng tâm là CRUD/backoffice, ít realtime chat |
| Cần mobile native sớm | React Native/Expo + FastAPI | Khi sales bắt buộc dùng app offline/camera/push native |
| Corpus RAG rất lớn | Qdrant/OpenSearch + reranker | Khi pgvector không đáp ứng latency/scale |
| On-prem nghiêm ngặt | Docker Compose/Kubernetes + MinIO + Keycloak | Khi không được dùng SaaS/cloud bên ngoài |

Khuyến nghị cuối cùng vẫn là:

```text
Frontend: TypeScript + Next.js + React + Tailwind + Radix/shadcn + TanStack Query
Backend: Python + FastAPI + Pydantic + SQLAlchemy + Celery
Data: PostgreSQL + PostGIS + pgvector + Redis + S3-compatible object storage
AI: FPT Cloud/OpenAI-compatible provider adapter + controlled tool workflow + RAG
DevOps: Docker first, Kubernetes later only when thật sự cần
```

### 28.12. Công nghệ không nên dùng làm production core

| Công nghệ/cách làm | Lý do |
|---|---|
| Streamlit làm frontend chính | Rất tốt cho demo/internal tool, nhưng khó làm sản phẩm multi-role, offline, dashboard phức tạp, UI/UX enterprise |
| HTML tĩnh làm app chính | Hợp prototype, không đủ auth, state, routing, data sync, testing |
| LLM gọi thẳng từ frontend | Lộ API key, không kiểm soát tool/data/RBAC |
| Chỉ dùng file JSON làm database | Không có transaction, audit, phân quyền, query phức tạp |
| Microservices quá sớm | Tăng DevOps/observability complexity khi domain chưa ổn |
| Vector DB riêng ngay từ ngày đầu | Tăng hạ tầng; pgvector đủ cho MVP nếu corpus chưa lớn |
| Tự build UI primitive từ đầu | Tốn thời gian, dễ sai accessibility |

### 28.13. Nguồn công nghệ đã kiểm tra

- Next.js docs: https://nextjs.org/docs
- FastAPI docs: https://fastapi.tiangolo.com/
- PostgreSQL docs: https://www.postgresql.org/docs/current/intro-whatis.html
- PostGIS: https://postgis.net/
- pgvector: https://github.com/pgvector/pgvector
- Redis docs: https://redis.io/docs/latest/
- Celery docs: https://docs.celeryq.dev/en/stable/getting-started/introduction.html
- MapLibre GL JS docs: https://maplibre.org/maplibre-gl-js/docs/
- TanStack Query docs: https://tanstack.com/query/latest/docs/framework/react/overview
- Radix UI docs: https://www.radix-ui.com/primitives/docs/overview/introduction
- Tailwind CSS docs: https://tailwindcss.com/docs/styling-with-utility-classes

---

## 29. Non-functional requirements

### 29.1. Hiệu năng

- Chat trả phản hồi đầu tiên trong < 3 giây với câu đơn giản.
- Triage ca bệnh trong < 5 giây.
- Tạo đơn nháp trong < 10 giây nếu dữ liệu đủ.
- Dashboard vùng tải trong < 5 giây với dữ liệu đã cache.

### 29.2. Độ tin cậy

- Hệ thống vẫn tạo nháp ca khi mất mạng, đồng bộ sau.
- Nếu LLM lỗi, các tool tra cứu sản phẩm/khách/NPP vẫn dùng được ở chế độ basic.
- Nếu RAG không có nguồn, AI phải nói không tìm thấy thay vì bịa.

### 29.3. Bảo mật và dữ liệu

- Phân quyền theo vùng/sales owner.
- Log truy cập hồ sơ khách.
- Ẩn thông tin nhạy cảm khi chia sẻ ra ngoài.
- API key không nằm trong frontend.
- Có chính sách lưu trữ ảnh/video/ca bệnh.

### 29.4. Audit

Mỗi câu trả lời cần lưu:

- User input.
- Case/customer context.
- Tool calls.
- Knowledge chunks.
- Product data version.
- Model/version.
- Answer final.
- Warnings.
- User feedback/outcome.

### 29.5. Offline/field mode

Sales hiện trường có thể mạng yếu. Nên có:

- Form tạo ca offline.
- Cache catalogue sản phẩm cơ bản.
- Cache checklist xử lý ca đỏ.
- Đồng bộ khi có mạng.

---

## 30. Backlog chi tiết theo epic

### Epic 1 - Chuẩn hóa dữ liệu production

- Import catalogue thật.
- Import khách/NPP thật.
- Import lịch sử đơn.
- Import chính sách/khuyến mãi.
- Gắn metadata nguồn, ngày hiệu lực, người duyệt.
- Làm mapping SKU cũ/mới.

### Epic 2 - Case management

- Tạo ca bệnh.
- Case completeness score.
- Triage risk.
- Missing question generator.
- Case timeline.
- Follow-up tasks.
- Đóng ca và outcome.

### Epic 3 - Expert workflow

- Expert ticket.
- Gán chuyên gia.
- SLA.
- Chuyên gia comment/approve.
- Trả bản tư vấn đã duyệt cho sales.

### Epic 4 - Product recommendation

- Product eligibility.
- Dose/quantity calculator.
- Claim guardrails.
- Stock/cold-chain check.
- Draft order.

### Epic 5 - Distributor intelligence

- NPP profile.
- Sales history analysis.
- Cross-sell.
- Three-level order recommendation.
- Objection script.
- DMS integration.

### Epic 6 - Market intelligence

- Alert verification.
- Duplicate detection.
- Risk map.
- Customer priority list.
- Campaign builder.
- Campaign dashboard.

### Epic 7 - Knowledge governance

- Upload docs.
- Chunking.
- Approval workflow.
- Versioning.
- Expiry alerts.
- Golden test rerun.

### Epic 8 - Observability & evaluation

- Answer logging.
- Feedback button.
- Expert review sampling.
- KPI dashboard.
- Error taxonomy.
- Regression test.

---

## 31. MVP 8-12 tuần gợi ý

### Tuần 1-2: Data foundation

- Chốt schema khách, trại, ca bệnh, sản phẩm.
- Nạp 20-30 sản phẩm thật.
- Nạp 10-15 bệnh thật được R&D duyệt.
- Nạp 50-100 khách/NPP mẫu thật.
- Gắn nguồn và metadata.

### Tuần 3-4: Case workflow

- Tạo ca bệnh.
- Triage đỏ/cam/vàng/xanh.
- Hỏi thêm dữ kiện.
- Case timeline.
- Expert ticket cơ bản.

### Tuần 5-6: Product & order

- Tra cứu sản phẩm production.
- Eligibility check.
- Tính số lượng cơ bản.
- Đơn nháp.
- Tin nhắn gửi khách.

### Tuần 7-8: NPP & map

- NPP cockpit.
- Gợi ý đơn 3 mức.
- Heatmap có verification status.
- Customer priority list từ alert.

### Tuần 9-10: Governance & QA

- Knowledge admin cơ bản.
- Golden test 200 câu.
- Audit log.
- Feedback loop.

### Tuần 11-12: Pilot

- Pilot 5-10 sales, 1-2 vùng.
- Review 100% ca đỏ/cam.
- Đo thời gian tư vấn, tỷ lệ tạo follow-up, tỷ lệ chốt đơn.
- Chốt backlog V1.

---

## 32. Ví dụ output khác ngoài ASF

### 32.1. Ca tiêu chảy heo con nghi E.coli

```md
Kết luận sơ bộ
- Nghi tiêu chảy heo con do E.coli, mức nguy cơ vàng/cam tùy tỷ lệ mất nước.
- Có thể điều trị nếu đủ dữ kiện, nhưng nên hỏi thêm tuổi heo, số con mắc, mức mất nước và thuốc đã dùng.

Cần hỏi thêm
1. Heo bao nhiêu ngày tuổi hoặc sau cai sữa mấy ngày?
2. Phân trắng/vàng hay tóe nước, có máu không?
3. Bao nhiêu con tiêu chảy, bao nhiêu con mất nước/chết?
4. Đã dùng kháng sinh/điện giải gì chưa?
5. Chuồng có lạnh/ẩm, đổi cám gần đây không?

Đối với đàn đang bệnh
- Bù nước điện giải ngay, giữ ấm, làm khô nền.
- Nếu nghi vi khuẩn và đủ chỉ định, dùng kháng sinh đường ruột theo hướng dẫn thú y/kháng sinh đồ.
- Chia nhỏ bữa ăn, giảm stress cai sữa.

Lưu ý
- Điện giải là then chốt để giảm chết, không chỉ bán kháng sinh.
- Nếu tiêu chảy tóe nước lan rất nhanh cả đàn, cần phân biệt PED/TGE.

Gợi ý cho Sales
- Chào combo điều trị + hồi phục: kháng sinh phù hợp + điện giải + men vi sinh.
- Câu nói: "Mình xử lý mất nước trước để giữ heo, sau đó mới kiểm soát vi khuẩn và phục hồi ruột."
```

### 32.2. Tra cứu vaccine và tính kế hoạch

```md
Bạn đang hỏi NAVET-ASFVAC cho đàn 500 heo thịt khỏe.

Cần xác nhận trước
1. Heo bao nhiêu tuần tuổi?
2. Có con nào đang sốt/ốm không?
3. Trại có đang trong vùng có chỉ đạo/giám sát thú y không?
4. Có đảm bảo chuỗi lạnh 2-8°C đến lúc tiêm không?

Nếu đủ điều kiện
- Nhu cầu cơ bản: 500 liều.
- Dự phòng hao hụt/lỗi thao tác: 3-5% tùy quy trình.
- Số lọ cần tính theo quy cách thực tế.

Lưu ý
- Vaccine dùng để phòng cho heo khỏe, không dùng điều trị heo đang bệnh.
- Cần kiểm tra nhãn, lô, hạn dùng, hướng dẫn nhà sản xuất và chỉ đạo thú y.
```

### 32.3. NPP trong vùng ASF nóng

```md
Tóm tắt NPP
- Doanh số 3 tháng gần đây ổn định nhưng chưa nhập nhóm sát trùng/vaccine ASF.
- Khu vực đang có alert ASF mức tin cậy trung bình-cao.
- Công nợ trong ngưỡng, có thể chào đơn vừa.

Đơn gợi ý
- Mức an toàn: nhập lại SKU bán đều.
- Mức đề xuất: thêm sát trùng + điện giải/vitamin.
- Mức tăng trưởng: vaccine cho đàn khỏe đúng đối tượng nếu NPP có chuỗi lạnh và khách có nhu cầu.

Script gọi
- "Em thấy khu vực mình đang có nhiều cảnh báo ASF. Mình không bán thuốc chữa ASF, nhưng nên chuẩn bị bộ phòng dịch cho khách: sát trùng, hỗ trợ đàn khỏe và rà lại lịch vaccine. Em đề xuất anh nhập mức vừa để không ôm tồn."

Rủi ro
- Không chào vaccine nếu NPP không đảm bảo tủ lạnh/chuỗi lạnh.
- Không dùng thông tin alert chưa xác minh để gây hoang mang.
```

---

## 33. Những thứ còn thiếu cần đi hỏi nội bộ

Đây là danh sách nên hỏi Nova/Anova/SaigonVet trước khi build production:

### 33.1. R&D/thú y

- Danh sách bệnh ưu tiên theo loài và vùng.
- Phác đồ nào được phép AI tư vấn, phác đồ nào chỉ chuyên gia trả lời.
- Bệnh nào bắt buộc chuyển chuyên gia.
- Mẫu xét nghiệm và quy trình gửi mẫu.
- Lịch vaccine chuẩn theo giai đoạn.
- Allowed/forbidden claims cho từng sản phẩm.

### 33.2. Kinh doanh

- Danh mục SKU ưu tiên.
- SKU nào biên lợi nhuận tốt nhưng phải bán có điều kiện.
- Chính sách giá/chiết khấu/công nợ.
- Cách tính đơn gợi ý theo NPP.
- Ngưỡng công nợ không được tạo đơn.
- Chương trình khuyến mãi hiện hành.

### 33.3. Vận hành/kho

- Tồn kho realtime có sẵn không?
- Có dữ liệu hạn dùng/lô không?
- Vaccine giao theo chuỗi lạnh ra sao?
- NPP nào đủ năng lực bảo quản lạnh?
- Lead time giao hàng theo vùng?

### 33.4. IT/data

- CRM/DMS/ERP đang dùng gì?
- Có API không hay cần import file?
- User/role lấy từ đâu?
- Có SSO không?
- Log và phân quyền dữ liệu nhạy cảm thế nào?

### 33.5. Pháp chế/QA

- Câu disclaimer bắt buộc.
- Claim nào bị cấm.
- Quy định lưu dữ liệu ca bệnh/khách hàng.
- Quy trình duyệt tài liệu.
- Quy trình xử lý khi AI trả lời sai.

---

## 34. Nguồn tham khảo chính thức đã kiểm tra

- WOAH - African swine fever: https://www.woah.org/en/disease/african-swine-fever/
- WOAH - Technical Disease Card: African swine fever: https://www.woah.org/app/uploads/2021/03/a-african-swine-fever-v2-0.pdf
- USDA APHIS - African Swine Fever: https://www.aphis.usda.gov/livestock-poultry-disease/swine/african-swine-fever
- WOAH - Antimicrobial resistance: https://www.woah.org/en/what-we-do/global-initiatives/antimicrobial-resistance/
- NIST - AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework

Các nguồn trên dùng để củng cố nguyên tắc thiết kế: ASF là bệnh nguy hiểm cần phát hiện sớm, biosecurity, xét nghiệm và kiểm soát di chuyển; kháng sinh không dùng cho bệnh virus; antimicrobial phải dùng có trách nhiệm; hệ thống AI production cần quản trị rủi ro, nguồn, phiên bản và giám sát.
