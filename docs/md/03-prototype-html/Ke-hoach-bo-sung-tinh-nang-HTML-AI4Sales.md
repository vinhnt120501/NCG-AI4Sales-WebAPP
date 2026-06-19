# Kế hoạch bổ sung tính năng cho bản HTML AI4Sales

> Ngày tạo: 19/06/2026  
> Phạm vi: chỉ dùng để nâng cấp bản mẫu đang chạy trong `AI4Sales/AI SalesMate.dc.html`.  
> Mục tiêu: dựng prototype nhìn như sản phẩm thật hơn, tận dụng dữ liệu hiện có trong `AI4Sales/data/*.json` và `AI4Sales/data/knowledge/*.md`, chưa cần backend, CRM, DMS, API thật.  
> Lưu ý quan trọng: file này **kế thừa toàn bộ thông tin, tính năng, logic sản phẩm và định hướng** trong `docs/md/02-ke-hoach-san-pham/De-xuat-nang-cap-AI4Sales-thanh-san-pham.md`; khác biệt chỉ nằm ở mức triển khai: production blueprint được chuyển thành phiên bản prototype/mock có thể dựng trong HTML tĩnh.

---

## 1. Hiểu đúng scope

File `docs/md/02-ke-hoach-san-pham/De-xuat-nang-cap-AI4Sales-thanh-san-pham.md` là blueprint cho sản phẩm production.

File này dùng để trả lời câu hỏi **"bây giờ nên thêm gì vào HTML demo đang chạy để nó trông giống sản phẩm thật hơn?"**, nhưng không được hiểu là bản cắt bớt. Mọi thông tin/tính năng trong blueprint production vẫn được giữ lại theo nguyên tắc:

- Tính năng production nào có backend/API thật thì trong HTML làm bằng state/localStorage/mock data.
- Quy trình production nào có chuyên gia/CRM/DMS thật thì trong HTML làm bằng ticket mock, đơn nháp, copy text/JSON.
- Dữ liệu production nào chưa có thì trong HTML dùng data hiện có hoặc demo mock có gắn nhãn minh họa.
- Guardrails production vẫn giữ nguyên trong câu trả lời và UI, chỉ khác là chưa có hệ thống phê duyệt thật.

Nguyên tắc:

- Không biến HTML demo thành hệ thống production.
- Không cần backend thật.
- Không cần đăng nhập thật.
- Không cần CRM/DMS/ERP thật.
- Vẫn dùng dữ liệu mẫu hiện có: bệnh, sản phẩm, NPP, cảnh báo thị trường, tỉnh thành, knowledge docs.
- Có thể thêm dữ liệu mock nhỏ nếu cần để UI đầy đủ hơn.
- Ưu tiên những tính năng tạo cảm giác sản phẩm thật: tạo ca bệnh, hỏi sâu, theo dõi, đơn nháp, campaign từ bản đồ, phân quyền giả lập, dashboard nhỏ.
- Không bỏ ý nào trong blueprint sản phẩm; nếu chưa làm được thật thì thể hiện bằng UI mock, checklist, cảnh báo hoặc placeholder rõ ràng.

---

## 2. Hiện trạng HTML đang có

`AI SalesMate.dc.html` hiện đã có:

| Nhóm | Đã có |
|---|---|
| Chat | Gửi câu hỏi, route intent, trả message theo 4 nhóm năng lực |
| Chẩn đoán | `buildDiagnose(query)` đối chiếu triệu chứng với `diseases.json`, trả bệnh, độ tin cậy, cảnh báo, bước xử lý, sản phẩm |
| Tra cứu sản phẩm | `buildDrug(query)` lấy thông tin từ `vet_products.json` |
| Phân tích NPP | `buildDistributor(query)` phân tích lịch sử mua từ `distributors.json` |
| RAG nhẹ | `buildRag(query)` tìm trong `knowledge/*.md` |
| Bản đồ dịch | Tab `market`, heatmap Leaflet, nhập cảnh báo, sidebar tóm tắt theo bệnh |
| Data | `diseases.json`, `vet_products.json`, `distributors.json`, `market_alerts.json`, `provinces_vn.json`, `knowledge/*.md` |

Điểm cần nâng:

- Chat hiện trả lời một lần, chưa có case workspace.
- Chẩn đoán có 6 bước xử lý nhưng chưa tách theo đàn bệnh/đàn khỏe/ảnh hưởng/lưu ý.
- Chưa có form tạo ca bệnh chuyên biệt.
- Chưa có follow-up questions/action buttons sau câu trả lời.
- Chưa tính đủ dữ kiện ca bệnh, risk score, missing questions.
- Chưa có tính số lượng sản phẩm/đơn nháp.
- Bản đồ mới hiển thị điểm nóng, chưa tạo campaign/call list.
- NPP phân tích còn đơn giản, chưa có 3 mức đơn, script gọi, objection.
- Dữ liệu nhập alert chỉ nằm trong state, reload mất.

---

## 3. Hướng nâng cấp prototype

Thay vì thêm một đống text vào câu trả lời chat, nên thêm các **khối giao diện sản phẩm**:

1. **Case Intake** - tạo ca bệnh có cấu trúc.
2. **Deep Diagnosis Card** - trả lời sâu theo ca, không chỉ 6 bước.
3. **Follow-up Actions** - nút hỏi tiếp nhanh.
4. **Step Impact Table** - phân tích ảnh hưởng/lưu ý từng bước.
5. **Dose/Quantity Calculator** - tính số lượng sản phẩm theo quy mô đàn.
6. **Draft Order** - đơn hàng nháp từ ca bệnh/NPP.
7. **Expert Ticket Mock** - tạo ticket chuyển chuyên gia giả lập.
8. **Market Campaign** - từ alert bản đồ tạo danh sách khách/NPP cần gọi.
9. **NPP Cockpit nâng cấp** - 3 mức đơn + script gọi + objection.
10. **Local Persistence** - lưu cases/alerts/draft orders vào `localStorage`.

Các tính năng này đủ làm bản mẫu trông như sản phẩm thật, nhưng vẫn chạy trong HTML tĩnh.

---

## 4. Feature 1 - Case Intake: tạo ca bệnh có cấu trúc

### 4.1. Mục tiêu

Sales không chỉ gõ chat tự do mà có thể bấm **"Tạo ca bệnh"** và nhập form nhanh.

### 4.2. UI đề xuất

Thêm nút ở sidebar hoặc welcome:

- `＋ Tạo ca bệnh`
- `＋ Nhập alert thị trường` giữ cho tab bản đồ.

Popup `Tạo ca bệnh` gồm:

| Trường | Kiểu UI | Ghi chú |
|---|---|---|
| Khách/trại/NPP | select/input | lấy từ `distributors.json` hoặc nhập tự do |
| Loài nuôi | select | Heo/Gà |
| Tỉnh/thành | select | lấy từ `provinces_vn.json` |
| Giai đoạn | select | heo con, heo thịt, nái, gà con, gà đẻ |
| Tổng đàn | number | dùng tính tỷ lệ |
| Số con mắc | number | dùng risk |
| Số con chết | number | dùng risk |
| Bắt đầu từ | select/input | hôm nay, 1-2 ngày, 3-7 ngày |
| Triệu chứng | textarea + chips | sốt, tiêu chảy, ho, da tím, chết nhanh |
| Đã dùng thuốc/vaccine | textarea | tránh gợi ý trùng/sai |
| Ghi chú | textarea | thông tin tự do |

### 4.3. State cần thêm

```js
state = {
  ...
  cases: [],
  showCaseForm: false,
  caseForm: {
    customer: '',
    species: '',
    province: '',
    stage: '',
    herdSize: '',
    affectedCount: '',
    deadCount: '',
    started: '',
    symptoms: '',
    usedProducts: '',
    note: ''
  },
  selectedCaseId: null
}
```

### 4.4. Function cần thêm

```js
createCaseFromForm()
buildCaseSummary(caseObj)
calcCaseCompleteness(caseObj)
calcCaseRisk(caseObj, diagnosis)
getMissingQuestions(caseObj, diagnosis)
persistCases()
loadCases()
```

### 4.5. Output sau khi tạo ca

Sau khi lưu form, chat tự động push một message user:

```text
Tạo ca bệnh: Heo thịt tại Đồng Nai, tổng đàn 200 con, 30 con sốt/bỏ ăn, 5 con chết, da tai bụng tím, bắt đầu từ hôm qua.
```

Sau đó gọi `buildDiagnose()` nhưng truyền thêm context từ case để trả lời sâu hơn.

---

## 5. Feature 2 - Deep Diagnosis Card

### 5.1. Mục tiêu

Nâng `buildDiagnose(query)` từ câu trả lời demo thành card giống sản phẩm thật:

- Có tình trạng ca.
- Có risk level.
- Có dữ kiện thiếu.
- Có hành động theo đàn đang bệnh/đàn khỏe.
- Có phân tích ảnh hưởng từng bước.
- Có follow-up.
- Có sản phẩm liên quan phân nhóm đúng.

### 5.2. Message object mở rộng

Hiện message chẩn đoán có:

```js
{
  diagnosis,
  escalation,
  earlyWarning,
  science,
  steps,
  products,
  marketInfo,
  sources,
  suggestion
}
```

Nên bổ sung:

```js
{
  caseSummary: {},
  riskBadge: { label, color, reason },
  completeness: { score, missing },
  missingQuestions: [],
  actionPlan: {
    sickHerd: [],
    healthyHerd: [],
    farmBiosecurity: [],
    followUp: []
  },
  impactTable: [],
  productGroups: {
    prevention: [],
    disinfection: [],
    support: [],
    treatment: [],
    conditional: []
  },
  quickActions: [],
  draftOrderSeed: {}
}
```

### 5.3. UI khối trả lời

Trong phần BOT message, thêm các card:

1. **Case Snapshot**
   - Loài, vùng, tổng đàn, mắc/chết, bắt đầu, completeness.

2. **Risk Badge**
   - Đỏ/Cam/Vàng/Xanh.
   - Lý do: "chết nhanh + da tím + sốt cao".

3. **Cần hỏi thêm**
   - 3-5 câu.
   - Mỗi câu có nút copy hoặc click để gửi vào chat.

4. **Đối với đàn này nên làm gì**
   - Tab hoặc nhóm:
     - Đàn đang bệnh.
     - Đàn khỏe cùng trại.
     - Người/xe/dụng cụ.
     - Theo dõi tiếp.

5. **Ảnh hưởng/lưu ý từng bước**
   - Bảng `Bước | Tác dụng | Lưu ý`.

6. **Sản phẩm liên quan**
   - Nhóm rõ:
     - Phòng bệnh.
     - Sát trùng.
     - Hỗ trợ.
     - Điều trị kế phát nếu có chỉ định.

7. **Quick actions**
   - `Phân tích từng bước`
   - `Tính số lượng sản phẩm`
   - `Tạo đơn nháp`
   - `Tạo ticket chuyên gia`
   - `Soạn tin nhắn gửi khách`

### 5.4. Rule dựng `actionPlan`

Với bệnh virus không có đặc trị:

```js
actionPlan.sickHerd = [
  'Cách ly ô/chuồng nghi bệnh',
  'Dừng di chuyển, xuất bán, nhập đàn mới',
  'Báo thú y/chuyên gia và lấy mẫu xét nghiệm',
  'Không dùng kháng sinh như thuốc chữa bệnh virus'
]

actionPlan.healthyHerd = [
  'Tách luồng chăm sóc đàn khỏe và đàn bệnh',
  'Tăng sát trùng, giảm người/xe vào trại',
  'Rà soát lịch vaccine; vaccine chỉ dùng cho con khỏe đúng đối tượng',
  'Bổ sung điện giải/vitamin nếu cần để giảm stress'
]
```

Với bệnh vi khuẩn/ký sinh có thuốc:

```js
actionPlan.sickHerd = [
  'Tách con bệnh nặng',
  'Bù nước/điện giải nếu tiêu chảy hoặc sốt',
  'Dùng thuốc đúng chỉ định, đủ liệu trình',
  'Theo dõi đáp ứng sau 24-48 giờ'
]
```

### 5.5. Rule dựng `impactTable`

Ví dụ ASF:

| Bước | Tác dụng | Lưu ý |
|---|---|---|
| Cách ly | Giảm lây trực tiếp | Không gom đàn lung tung làm tăng stress |
| Dừng vận chuyển | Giảm lan ra ngoài | Ảnh hưởng kế hoạch bán nhưng giảm thiệt hại lớn hơn |
| Sát trùng | Cắt lây gián tiếp | Dọn chất hữu cơ trước, pha đúng nồng độ |
| Lấy mẫu | Xác chẩn, phân biệt CSF/PRRS | Mẫu sai làm chậm kết quả |
| Vaccine đàn khỏe | Phòng bệnh nếu đúng đối tượng | Không tiêm heo đang sốt/ốm |

---

## 6. Feature 3 - Quick follow-up actions trong chat

### 6.1. Mục tiêu

Sau mỗi câu trả lời, người dùng không phải nghĩ "hỏi gì tiếp", mà có nút bấm sẵn.

### 6.2. Quick actions theo loại message

Chẩn đoán:

- `Hỏi thêm dữ kiện còn thiếu`
- `Phân tích ảnh hưởng từng bước`
- `Đối với đàn khỏe thì làm gì`
- `Tính sản phẩm theo quy mô đàn`
- `Tạo đơn nháp`
- `Tạo tin nhắn gửi khách`
- `Chuyển chuyên gia`

Sản phẩm:

- `Tính liều/số lượng`
- `Kiểm tra chống chỉ định`
- `So sánh sản phẩm thay thế`
- `Tạo hướng dẫn bảo quản`
- `Tạo câu chốt sales`

NPP:

- `Tạo đơn 3 mức`
- `Soạn script gọi NPP`
- `Xử lý objection`
- `Tạo task follow-up`

Bản đồ dịch:

- `Tạo chiến dịch gọi khách`
- `Lọc NPP trong vùng`
- `Gợi ý SKU phòng dịch`
- `Tạo tin nhắn cảnh báo`

### 6.3. Cách implement trong HTML

Thêm trong message:

```js
quickActions: [
  { label: 'Tính sản phẩm', action: 'calc_quantity', payload: {...} },
  { label: 'Tạo đơn nháp', action: 'create_order', payload: {...} }
]
```

Thêm function:

```js
handleQuickAction(action, payload)
```

Function này push user message giả lập rồi gọi builder phù hợp.

---

## 7. Feature 4 - Dose/Quantity Calculator

### 7.1. Mục tiêu

Prototype phải trả lời được câu thực tế:

> "Đàn 200 con thì cần bao nhiêu chai/gói/lọ?"

### 7.2. Dữ liệu lấy từ đâu

Dùng `vet_products.json`:

- `lieu_luong`
- `duong_dung`
- `quy_cach`
- `gia_vnd`
- `doi_tuong`
- `chong_chi_dinh`

Do liều đang là text, prototype có thể tính đơn giản theo rule mẫu:

- Vaccine: `số liều = số con`.
- Sát trùng: hỏi diện tích hoặc dùng mức minh họa.
- Điện giải/vitamin pha nước: hỏi số lít nước/ngày hoặc dùng mức minh họa.
- Kháng sinh theo kg: cần `avgWeightKg`.

### 7.3. UI calculator

Popup hoặc inline card:

| Trường | Kiểu |
|---|---|
| Sản phẩm | select từ sản phẩm liên quan |
| Số con | number |
| Trọng lượng TB | number |
| Số ngày/mũi | number/select |
| Hao hụt dự phòng | 0%, 3%, 5%, 10% |

Output:

```md
Ước tính bản mẫu:
- Tổng đàn: 200 con
- Trọng lượng TB: 30 kg/con
- Tổng trọng lượng: 6.000 kg
- Sản phẩm: Anova Electrolyte-Plus
- Nhu cầu ước tính: ...
- Số quy cách cần chuẩn bị: ...
- Chi phí ước tính: ...
- Lưu ý: số liệu demo, cần kiểm nhãn thật khi production.
```

### 7.4. Function

```js
buildQuantityEstimate(product, caseObj, options)
parseDoseText(product.lieu_luong)
estimatePacks(quantity, product.quy_cach)
```

Vì liều text khó parse chính xác, bản mẫu nên hiển thị `Ước tính demo` và cho người dùng chỉnh tay.

---

## 8. Feature 5 - Draft Order từ ca bệnh

### 8.1. Mục tiêu

Từ chẩn đoán, bấm **"Tạo đơn nháp"** để ra giỏ hàng đề xuất.

### 8.2. Rule gợi ý đơn

Với bệnh virus:

- Không đưa kháng sinh vào nhóm "chữa bệnh".
- Đưa sát trùng vào nhóm ưu tiên.
- Đưa hỗ trợ điện giải/vitamin nếu có.
- Vaccine chỉ ở nhóm "cho đàn khỏe đúng đối tượng/kiểm tra thêm".

Với bệnh vi khuẩn/ký sinh:

- Kháng sinh/đặc trị phù hợp.
- Điện giải/hỗ trợ.
- Men vi sinh phục hồi nếu tiêu chảy.
- Vaccine phòng tái phát nếu có.

### 8.3. UI Draft Order

Card gồm:

- Khách/trại.
- Lý do tạo đơn.
- Danh sách sản phẩm.
- Nhãn: `Ưu tiên`, `Có điều kiện`, `Bán kèm`, `Cần chuyên gia`.
- Số lượng ước tính.
- Chi phí ước tính.
- Cảnh báo.
- Nút: `Copy đơn`, `Lưu nháp`, `Xóa`.

### 8.4. State

```js
draftOrders: []
```

### 8.5. Function

```js
buildDraftOrderFromDiagnosis(caseObj, diagnosisMsg)
saveDraftOrder(order)
copyDraftOrder(order)
```

---

## 9. Feature 6 - Expert Ticket Mock

### 9.1. Mục tiêu

Ca đỏ/cam nhìn phải có workflow chuyển chuyên gia, không chỉ text cảnh báo.

### 9.2. UI

Khi `escalation` có:

- Hiển thị box `Cần chuyển chuyên gia`.
- Nút `Tạo ticket chuyên gia`.
- Sau khi bấm, tạo ticket mock:
  - Mã ticket.
  - SLA.
  - Chuyên gia phụ trách giả lập.
  - Trạng thái: `Đang chờ phản hồi`.

### 9.3. State

```js
expertTickets: []
```

### 9.4. Function

```js
createExpertTicket(caseObj, diagnosisMsg)
getTicketSla(riskLevel)
```

### 9.5. Nội dung ticket

```md
Ticket chuyên gia
- Ca: CASE-...
- Khách/trại: ...
- Loài/giai đoạn: ...
- Triệu chứng: ...
- Số mắc/chết/tổng đàn: ...
- Bệnh nghi ngờ: ...
- Dữ kiện còn thiếu: ...
- Khuyến nghị AI đã đưa: ...
```

---

## 10. Feature 7 - Bản đồ dịch: Alert detail + Campaign

### 10.1. Hiện trạng

Tab bản đồ hiện có:

- Heatmap.
- Form nhập cảnh báo.
- Sidebar bệnh nổi bật, cảnh báo gần đây.

### 10.2. Cần thêm

1. **Alert Detail Panel**
   - Click cảnh báo gần đây hoặc marker/heat point để xem chi tiết.
   - Bệnh, tỉnh, mức độ, ghi chú, nguồn, trạng thái xác minh.

2. **Verification Status**
   - `Chưa xác minh`
   - `Sales xác nhận`
   - `Chuyên gia xác nhận`
   - `Có xét nghiệm`

3. **Create Campaign**
   - Bấm từ alert để tạo chiến dịch.
   - Lọc NPP/khách trong cùng tỉnh/vùng từ `distributors.json`.
   - Gợi ý SKU theo bệnh.
   - Tạo script gọi.

4. **Campaign Card**
   - Tên chiến dịch.
   - Bệnh/vùng.
   - Khách/NPP ưu tiên.
   - Sản phẩm nên chào.
   - Tin nhắn mẫu.
   - Tiến độ giả lập.

### 10.3. State

```js
selectedAlertId: null,
campaigns: []
```

### 10.4. Function

```js
selectAlert(alertId)
buildCampaignFromAlert(alert)
rankDistributorsForAlert(alert)
buildCampaignScript(alert, products)
```

### 10.5. Rule gợi ý campaign theo bệnh

- ASF: sát trùng + vaccine cho đàn khỏe đúng điều kiện + điện giải/vitamin.
- Newcastle/Gumboro/HPAI: vaccine liên quan + sát trùng + vitamin.
- E.coli/Salmonella: kháng sinh đúng chỉ định + điện giải + men vi sinh.
- Suyễn/CRD: kháng sinh hô hấp + vitamin + cải thiện môi trường.

---

## 11. Feature 8 - NPP Cockpit nâng cấp

### 11.1. Mục tiêu

`buildDistributor()` hiện có lịch sử mua, đơn kế tiếp, cross-sell. Cần làm cho giống công cụ sales hơn.

### 11.2. Bổ sung output

```js
distributorPlus: {
  riskContext: [],
  orderOptions: {
    safe: [],
    recommended: [],
    growth: []
  },
  objections: [],
  callScript: '',
  followUpTask: ''
}
```

### 11.3. UI

Thêm các khối:

- **Bối cảnh vùng**: tỉnh này đang có alert gì.
- **Đơn 3 mức**:
  - Mức an toàn: nhập lại sản phẩm bán đều.
  - Mức đề xuất: thêm combo phòng/điều trị.
  - Mức tăng trưởng: mở SKU mới.
- **Script gọi NPP**:
  - Mở đầu.
  - Lý do theo dữ liệu.
  - Đề xuất.
  - Câu chốt.
- **Objection handling**:
  - Khách sợ tồn.
  - Giá cao.
  - Chưa có nhu cầu.
  - Công nợ.

### 11.4. Function

```js
buildOrderOptions(distributor)
buildObjections(distributor, crossSell)
buildDistributorCallScript(distributor, orderOptions)
```

---

## 12. Feature 9 - Source & Knowledge Drawer

### 12.1. Mục tiêu

Khi câu trả lời có nguồn, người dùng bấm để xem đoạn nguồn, tăng cảm giác "tri thức đã duyệt".

### 12.2. UI

Hiện sources chỉ là chip. Nên thêm drawer/modal:

- Tên file.
- Loại nguồn: R&D duyệt.
- Đoạn trích liên quan.
- Dùng cho câu trả lời nào.

### 12.3. Function

```js
openSourceDrawer(source)
findKnowledgeChunk(source, query)
```

Nếu chưa muốn phức tạp, chỉ cần hiển thị tên file + nhãn `R&D duyệt` + mô tả ngắn.

---

## 13. Feature 10 - Local persistence

### 13.1. Mục tiêu

Reload trang không mất alert/case/order vừa tạo, giúp demo giống app thật.

### 13.2. Lưu vào `localStorage`

Các key:

```text
ai4sales_cases
ai4sales_alerts
ai4sales_draft_orders
ai4sales_expert_tickets
ai4sales_campaigns
```

### 13.3. Function

```js
saveLocal(key, value)
loadLocal(key, fallback)
clearDemoData()
```

### 13.4. UI

Thêm nút nhỏ trong avatar/user menu:

- `Reset dữ liệu demo`
- `Xuất dữ liệu demo JSON`

---

## 14. Data mock nên thêm cho prototype

Không bắt buộc, nhưng nếu muốn UI đầy đủ hơn, thêm các file nhỏ:

### 14.1. `AI4Sales/data/demo_cases.json`

Chứa 3-5 ca mẫu:

- Nghi ASF heo.
- Tiêu chảy E.coli heo con.
- Newcastle gà.
- Cầu trùng gà.
- Suyễn heo.

### 14.2. `AI4Sales/data/product_bundles.json`

Mapping bệnh -> combo:

```json
{
  "D01": {
    "name": "Combo phòng dịch ASF",
    "items": [
      { "ma_sp": "ST01", "role": "sat_trung", "priority": "high" },
      { "ma_sp": "BT01", "role": "ho_tro", "priority": "medium" },
      { "ma_sp": "VX01", "role": "phong_benh_dan_khoe", "priority": "conditional" }
    ]
  }
}
```

### 14.3. `AI4Sales/data/demo_campaign_rules.json`

Mapping alert -> campaign:

```json
{
  "ASF": {
    "target_species": "heo",
    "priority_products": ["ST01", "VX01", "BT01", "TP05"],
    "message_template": "Khu vực đang có cảnh báo ASF..."
  }
}
```

Nếu muốn giữ đơn giản, có thể hard-code các rule này trong HTML trước.

---

## 15. Thứ tự triển khai prototype

### Phase A - Làm sâu câu trả lời chẩn đoán

Ưu tiên cao nhất vì đúng yêu cầu "ngoài 6 bước thì trả lời thêm".

Làm:

- Thêm `caseSummary`, `riskBadge`, `missingQuestions`.
- Thêm `actionPlan` tách đàn bệnh/đàn khỏe.
- Thêm `impactTable`.
- Thêm quick actions.

Kết quả demo:

- Hỏi ASF sẽ thấy câu trả lời sâu, giống bác sĩ tư vấn hơn.

### Phase B - Case form + localStorage

Làm:

- Popup tạo ca bệnh.
- Lưu ca vào state/localStorage.
- Sidebar `Ca gần đây`.
- Tạo ca xong tự sinh chẩn đoán.

Kết quả demo:

- App không chỉ là chat; có cảm giác case management.

### Phase C - Draft order + quantity estimate

Làm:

- Nút `Tạo đơn nháp`.
- Card đơn nháp.
- Tính số lượng đơn giản.
- Copy đơn.

Kết quả demo:

- Nối kỹ thuật sang sales action rõ ràng.

### Phase D - Market campaign

Làm:

- Alert detail.
- Verification status.
- Create campaign.
- Danh sách NPP/khách ưu tiên.
- Script gọi.

Kết quả demo:

- Bản đồ dịch không chỉ để xem, mà tạo hành động bán hàng.

### Phase E - NPP cockpit nâng cấp

Làm:

- Đơn 3 mức.
- Script gọi.
- Objection handling.
- Task follow-up.

Kết quả demo:

- Phân tích NPP giống công cụ sales thật.

---

## 16. Demo script sau khi bổ sung

### Cảnh 1 - Tạo ca ASF

1. Bấm `Tạo ca bệnh`.
2. Nhập:
   - Heo thịt.
   - Đồng Nai.
   - Tổng đàn 200.
   - Mắc 30.
   - Chết 8.
   - Sốt 41, da tai bụng tím, chết nhanh.
3. AI trả:
   - Risk đỏ.
   - Cần hỏi thêm.
   - Đối với đàn bệnh.
   - Đối với đàn khỏe.
   - Ảnh hưởng từng bước.
   - Sản phẩm liên quan.
4. Bấm `Tạo ticket chuyên gia`.
5. Bấm `Tạo đơn nháp`.

Thông điệp: không chỉ demo chẩn đoán, mà đã có workflow ca bệnh.

### Cảnh 2 - Tính sản phẩm

1. Từ ca ASF, bấm `Tính sản phẩm theo quy mô đàn`.
2. Chọn sát trùng hoặc điện giải.
3. AI trả số lượng ước tính và cảnh báo.

Thông điệp: AI chuyển từ lời khuyên sang số lượng có thể bán.

### Cảnh 3 - Bản đồ dịch tạo campaign

1. Sang `Bản đồ dịch bệnh`.
2. Chọn cảnh báo ASF Đồng Nai.
3. Bấm `Tạo chiến dịch`.
4. AI trả NPP ưu tiên, SKU đề xuất, script gọi.

Thông điệp: bản đồ biến thành hành động sales.

### Cảnh 4 - NPP cockpit

1. Hỏi: "Phân tích Đại lý Minh Phát".
2. AI trả thêm:
   - Đơn an toàn.
   - Đơn đề xuất.
   - Đơn tăng trưởng.
   - Objection handling.
   - Script gọi.

Thông điệp: AI giúp sales chốt đơn có dữ liệu.

---

## 17. Mapping từ product blueprint sang HTML prototype

| Blueprint production | HTML prototype nên làm |
|---|---|
| Case management đầy đủ | Case form + case cards + localStorage |
| Expert workflow thật | Ticket mock + SLA giả lập |
| CRM/DMS integration | Draft order card + copy JSON/text |
| Knowledge governance | Source drawer hiển thị file R&D duyệt |
| Dose calculator chính xác | Calculator demo có cảnh báo "ước tính" |
| Market intelligence | Campaign mock từ alert + distributors |
| Role-based permission | User menu giả lập vai trò Sales/Manager/R&D |
| Evaluation dashboard | Mini dashboard count cases/orders/campaigns |

---

## 18. Rủi ro khi làm trong HTML tĩnh

| Rủi ro | Cách xử lý trong prototype |
|---|---|
| Liều lượng text khó parse | Chỉ tính demo, yêu cầu người dùng nhập/chỉnh tay |
| Không có CRM thật | Dùng `localStorage` và `Copy JSON` |
| Không có tồn kho thật | Gắn nhãn "tồn kho minh họa" hoặc không hiển thị tồn |
| Không có chuyên gia thật | Ticket mock, trạng thái giả lập |
| Data cook | Luôn hiển thị nhãn "Dữ liệu minh họa" |
| HTML quá dài | Ưu tiên helper function nhỏ, tránh refactor lớn |
| UI bị rối | Dùng collapsible sections/tabs cho card dài |

---

## 19. Checklist triển khai trong `AI SalesMate.dc.html`

### 19.1. State

- [ ] `cases`
- [ ] `showCaseForm`
- [ ] `caseForm`
- [ ] `selectedCaseId`
- [ ] `draftOrders`
- [ ] `expertTickets`
- [ ] `selectedAlertId`
- [ ] `campaigns`
- [ ] `showQuantityCalc`
- [ ] `quantityForm`

### 19.2. Helper logic

- [ ] `calcCaseCompleteness`
- [ ] `calcCaseRisk`
- [ ] `getMissingQuestions`
- [ ] `buildActionPlan`
- [ ] `buildImpactTable`
- [ ] `groupProductsByRole`
- [ ] `buildQuantityEstimate`
- [ ] `buildDraftOrderFromDiagnosis`
- [ ] `createExpertTicket`
- [ ] `buildCampaignFromAlert`
- [ ] `buildDistributorPlus`
- [ ] `saveLocal/loadLocal`

### 19.3. UI blocks

- [ ] Case form modal.
- [ ] Case snapshot card.
- [ ] Missing questions card.
- [ ] Action plan card.
- [ ] Impact table.
- [ ] Quick actions row.
- [ ] Quantity calculator modal.
- [ ] Draft order card.
- [ ] Expert ticket card.
- [ ] Alert detail panel.
- [ ] Campaign card.
- [ ] NPP order options.
- [ ] Source drawer.

### 19.4. Demo data

- [ ] Có ít nhất 3 case mẫu.
- [ ] Có mapping bệnh -> combo sản phẩm.
- [ ] Có campaign rule cho ASF/Newcastle/E.coli.
- [ ] Có trạng thái xác minh cho alert.

---

## 20. Ưu tiên nếu chỉ có thời gian làm nhanh

Nếu chỉ làm 1 ngày:

1. Deep Diagnosis Card.
2. Missing Questions.
3. Action Plan tách đàn bệnh/đàn khỏe.
4. Impact Table.
5. Quick Actions.

Nếu có 2-3 ngày:

6. Case Form.
7. Draft Order.
8. Expert Ticket Mock.
9. LocalStorage.

Nếu có 1 tuần:

10. Market Campaign.
11. NPP Cockpit nâng cấp.
12. Quantity Calculator.
13. Source Drawer.
14. Mini dashboard.

---

## 21. Kế thừa đầy đủ từ blueprint sản phẩm

Mục này dùng để đảm bảo file HTML-plan **không bị thiếu thông tin/tính năng** so với `docs/md/02-ke-hoach-san-pham/De-xuat-nang-cap-AI4Sales-thanh-san-pham.md`. Mỗi phần của blueprint production đều phải có phiên bản thể hiện trong HTML prototype, dù chỉ là mock UI, localStorage, demo data hoặc placeholder.

| Phần trong blueprint production | Cách đưa vào HTML prototype |
|---|---|
| Hiện trạng đang có | Giữ nguyên các năng lực hiện tại: chat, diagnosis, drug lookup, distributor, RAG, market map |
| Định vị sản phẩm | UI phải thể hiện AI4Sales là trợ lý hiện trường cho sales thú y, không chỉ chatbot |
| Người dùng thật | Thêm role giả lập Sales/Manager/R&D trong user menu hoặc dashboard |
| Mức drill câu trả lời | Deep Diagnosis Card, action plan, impact table, missing questions |
| Chuẩn output production | Message object mở rộng + các card UI tương ứng |
| Ví dụ ASF sâu hơn 6 bước | Là use case demo ưu tiên số 1 trong HTML |
| Dữ liệu cần bổ sung | Dùng form case + demo fields; phần chưa có backend thì lưu localStorage |
| Bản đồ dịch đi xa hơn heatmap | Alert detail + campaign builder + call list mock |
| Nâng cấp hội thoại | Quick follow-up actions sau mỗi câu trả lời |
| Guardrails | Giữ trong text/UI: không chữa virus bằng kháng sinh, không vaccine cho con ốm, chuyển chuyên gia |
| Quản trị tri thức | Source drawer + nhãn R&D duyệt + placeholder version/source |
| NPP/order nâng cấp | NPP cockpit: đơn 3 mức, script gọi, objection handling |
| Roadmap production | Chuyển thành phase A-E cho HTML prototype |
| Tiêu chí nghiệm thu | Chuyển thành checklist demo acceptance |
| Quyết định cần chốt | Đưa vào notes/placeholder nếu chưa có câu trả lời |
| Product canvas | Giữ nguyên lời hứa 60 giây dưới dạng case intake + recommendation + order draft |
| Module sản phẩm | Dựng đủ module mock: case, triage, diagnosis, product advisor, dose, sales copilot, expert queue, campaign, knowledge |
| Hành trình người dùng | Demo script 4 cảnh: ca ASF, tính sản phẩm, bản đồ campaign, NPP cockpit |
| Bộ câu hỏi follow-up | Quick actions + missing questions bank |
| Công thức scoring | `calcCaseCompleteness`, `calcCaseRisk`, risk badge, priority score mock |
| Schema dữ liệu | State/localStorage schema tương ứng: cases, tickets, orders, campaigns |
| API/tool agent | Helper functions trong HTML thay cho API thật |
| Prompt policy | Rule trả lời trong builders: diagnosis/drug/distributor/rag |
| Giao diện sản phẩm thật | Thêm tab/card/modal để có cảm giác app: case, order, campaign, ticket |
| Phân quyền và SLA | Role switch mock + SLA badge trong expert ticket |
| Test/evaluation | Checklist test câu hỏi golden path cho HTML |
| Tích hợp hệ thống | Copy JSON/text mock thay cho CRM/DMS/ERP |
| Non-functional requirements | LocalStorage, basic fallback, reset demo data |
| Backlog epic | Checklist triển khai section 19 |
| MVP 8-12 tuần | Rút thành ưu tiên 1 ngày, 2-3 ngày, 1 tuần |
| Ví dụ output khác ngoài ASF | Thêm demo outputs: E.coli, vaccine, NPP vùng dịch |
| Câu hỏi cần hỏi nội bộ | Giữ làm phần notes trong tài liệu, chưa cần UI |
| Nguồn tham khảo | Source drawer/knowledge chips; không cần web trong HTML |

---

## 22. Danh sách tính năng đầy đủ cần có trong HTML prototype

Danh sách dưới đây gom lại toàn bộ tính năng từ blueprint production, nhưng diễn giải theo cách có thể dựng bản mẫu trong `AI SalesMate.dc.html`.

### 22.1. Tư vấn bệnh và case management

- Tạo ca bệnh từ form.
- Tạo ca bệnh từ chat tự do.
- Case snapshot: khách/trại, loài, tỉnh, tổng đàn, mắc/chết, timeline.
- Case completeness score.
- Risk badge đỏ/cam/vàng/xanh.
- Bệnh khả năng cao nhất và chẩn đoán phân biệt.
- Dữ kiện còn thiếu.
- Câu hỏi follow-up theo bệnh/loài.
- Kế hoạch hành động 0-2 giờ, 24 giờ, 3-7 ngày.
- Tách hành động cho đàn đang bệnh, đàn khỏe, người/xe/dụng cụ.
- Impact table: bước, tác dụng, lưu ý.
- Theo dõi tiếp: số chết, số mắc, ăn uống, nhiệt độ, đáp ứng.
- Lưu case vào localStorage.
- Sidebar danh sách ca gần đây.

### 22.2. An toàn thú y và guardrails

- Với virus nguy hiểm: không gợi ý kháng sinh như thuốc chữa.
- Với ASF/HPAI/FMD/Newcastle nặng: hiển thị bắt buộc chuyển chuyên gia.
- Vaccine chỉ hiện ở nhóm phòng cho đàn khỏe đúng điều kiện.
- Kháng sinh luôn có nhắc thời gian ngừng thuốc.
- Nếu thiếu trọng lượng/loài/sản phẩm thì không tính liều chắc chắn.
- Câu trả lời có nhãn "dữ liệu minh họa" khi dùng data demo.
- Card "Không nên làm" cho ca đỏ.

### 22.3. Sản phẩm, liều lượng và đơn nháp

- Product detail card giữ toàn bộ thông tin hiện có.
- Product grouping theo vai trò: phòng, sát trùng, hỗ trợ, điều trị, có điều kiện.
- Dose/quantity calculator demo.
- Người dùng chỉnh số con, trọng lượng, số ngày/mũi, hao hụt.
- Tạo draft order từ diagnosis.
- Tạo draft order từ NPP.
- Card cảnh báo sản phẩm: chống chỉ định, chuỗi lạnh, thời gian ngừng thuốc.
- Copy order dạng text/JSON.
- Lưu draft order vào localStorage.

### 22.4. Expert workflow mock

- Tạo ticket chuyên gia từ ca đỏ/cam.
- Ticket có mã, SLA, người phụ trách giả lập.
- Ticket chứa summary ca, triệu chứng, nghi bệnh, missing questions, sản phẩm đã gợi ý.
- Trạng thái ticket: chờ chuyên gia, đang xử lý, cần bổ sung, đã phản hồi.
- Follow-up task sau 2 giờ/24 giờ/3 ngày.

### 22.5. Bản đồ dịch và campaign

- Alert detail panel.
- Verification status cho alert.
- Duplicate warning đơn giản nếu cùng tỉnh + cùng bệnh.
- Tạo campaign từ alert.
- Lọc NPP/khách theo tỉnh/vùng từ `distributors.json`.
- Gợi ý SKU theo bệnh.
- Script gọi khách/NPP.
- Tin nhắn Zalo/SMS mẫu.
- Campaign card: mục tiêu, khách ưu tiên, sản phẩm, tiến độ mock.
- Lưu campaign vào localStorage.

### 22.6. NPP cockpit

- Tóm tắt doanh số/lịch sử mua hiện có.
- Bối cảnh vùng dịch liên quan.
- Đơn 3 mức:
  - Mức an toàn.
  - Mức đề xuất.
  - Mức tăng trưởng.
- Cross-sell theo sản phẩm chưa mua.
- Objection handling:
  - Sợ tồn.
  - Giá cao.
  - Chưa có nhu cầu.
  - Công nợ.
  - Nghi ngại vaccine.
- Script gọi NPP.
- Follow-up task.

### 22.7. Knowledge/source

- Source chips hiện có.
- Source drawer/modal.
- Nhãn `R&D duyệt`.
- Hiển thị tên file nguồn.
- Hiển thị mô tả ngắn của nguồn.
- Placeholder version/effective date nếu cần.
- Nếu không tìm thấy nguồn, nói rõ không tìm thấy.

### 22.8. Dashboard/role mock

- User menu chọn vai trò giả lập: Sales, Manager, R&D.
- Mini dashboard:
  - Số ca đang mở.
  - Số ticket chuyên gia.
  - Số đơn nháp.
  - Số campaign.
  - Alert nặng.
- Manager view mock: ưu tiên campaign/NPP.
- R&D view mock: ticket cần duyệt.

### 22.9. Dữ liệu và lưu trữ

- Dùng `diseases.json`, `vet_products.json`, `distributors.json`, `market_alerts.json`, `provinces_vn.json`.
- Có thể thêm `demo_cases.json`, `product_bundles.json`, `demo_campaign_rules.json`.
- localStorage keys:
  - `ai4sales_cases`
  - `ai4sales_alerts`
  - `ai4sales_draft_orders`
  - `ai4sales_expert_tickets`
  - `ai4sales_campaigns`
- Có nút reset demo data.
- Có nút export demo data JSON.

### 22.10. Acceptance checklist cho bản HTML

- Hỏi ASF trả lời sâu hơn 6 bước và có action plan theo đàn.
- Có missing questions rõ ràng.
- Có impact table.
- Có quick actions.
- Tạo được ca bệnh từ form.
- Tạo được ticket chuyên gia mock.
- Tạo được đơn nháp từ ca bệnh.
- Từ bản đồ tạo được campaign mock.
- Phân tích NPP có đơn 3 mức và script gọi.
- Reload trang không mất ca/alert/order/campaign vừa tạo.
- UI vẫn đọc được trên màn hình laptop và không quá rối.

---

## 23. Cách hiểu khi triển khai

Khi code HTML, nếu gặp một ý trong blueprint production mà không thể làm thật ngay, không bỏ ý đó. Chuyển nó thành một trong bốn dạng:

1. **Mock UI**  
   Ví dụ expert workflow thành ticket giả lập.

2. **Local state/localStorage**  
   Ví dụ case management, draft order, campaign.

3. **Computed helper**  
   Ví dụ scoring, missing questions, risk badge.

4. **Placeholder có cảnh báo**  
   Ví dụ CRM/DMS/ERP, tồn kho realtime, lab result thật.

Mục tiêu của bản HTML là **chứng minh luồng sản phẩm và cảm giác sử dụng**, không chứng minh hạ tầng production. Vì vậy cần ưu tiên những phần nhìn thấy được trong demo: case, action plan, order, campaign, ticket, dashboard.

---

## 24. Kết luận

Bản HTML hiện tại đã có nền tốt: data, chat, chẩn đoán, sản phẩm, NPP, bản đồ. Để nó trông như sản phẩm thật hơn trong phạm vi prototype, không cần làm backend ngay. Cần thêm các lớp **workflow**:

- Từ chat sang case.
- Từ chẩn đoán sang hành động theo đàn.
- Từ sản phẩm sang đơn nháp.
- Từ bản đồ sang campaign.
- Từ cảnh báo sang ticket chuyên gia/follow-up.

Ưu tiên đầu tiên nên là **làm sâu câu trả lời chẩn đoán ASF và các bệnh tương tự**, vì đây là điểm người dùng đang cảm thấy "gợi ý chung chung". Sau đó mới mở sang draft order, campaign và NPP cockpit.
