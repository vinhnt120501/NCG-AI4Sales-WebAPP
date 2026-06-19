# Deploy AI SalesMate (web app) lên GitHub + GitHub Pages — Free

Mục tiêu: có một **link công khai** dạng `https://vinhnt120501.github.io/NCG-AI4Sales-WebAPP/` để gửi cho sếp/khách bấm vào là chạy ngay.

> **Vì sao GitHub Pages?** App `AI4Sales/` là **web tĩnh thuần** (HTML + JS + JSON), chạy hoàn toàn ở trình duyệt: không backend, **không API key**, không tốn quota. → Hosting **0đ**, không "ngủ", không cần cấu hình server.
> Repo đích: **https://github.com/vinhnt120501/NCG-AI4Sales-WebAPP**

---

## 0. Đã chuẩn bị sẵn trong dự án (không cần tạo lại)

| File | Vai trò |
|---|---|
| `.gitignore` | **Chặn `.env` (chứa key thật), `.DS_Store`, `*.bak`, `node_modules`, `.venv`** → không bao giờ rò rỉ lên GitHub |
| `.nojekyll` | Bắt GitHub Pages serve **nguyên file** `.md` và `.dc.html` (không cho Jekyll xử lý) — bắt buộc để RAG đọc được `data/knowledge/*.md` |
| `index.html` (ở gốc) | Trang chờ có thương hiệu, **tự chuyển** vào `AI4Sales/AI SalesMate.dc.html` (xử lý cả tên file có dấu cách) |

> ✅ **Đã kiểm thử**: serve từ thư mục gốc → mở `/` → redirect → app nạp đủ data/ảnh, chẩn đoán ASF chạy, **0 lỗi**.
> ✅ **Đã xác minh bảo mật**: `git check-ignore` xác nhận `ver/salemate-ver/.env` **bị loại** khỏi mọi commit.

---

## 1. Yêu cầu (1 lần)
- Cài **git**: kiểm tra bằng `git --version`.
- Tài khoản **GitHub** + đã tạo repo trống **NCG-AI4Sales-WebAPP** (đã có theo link trên).
- Đăng nhập git lần đầu (nếu chưa):
  ```bash
  git config --global user.name  "Vinh NT"
  git config --global user.email "ban@email.com"
  ```

## 2. Đẩy code lên GitHub

```bash
cd "/Users/vinhnt120501/Documents/fpd_fdx/8. NCG - AI4Sales"

git init                      # (có thể đã init sẵn — không sao)
git add .

# 🔒 KIỂM TRA AN TOÀN: lệnh dưới phải KHÔNG in ra dòng nào.
git status --short | grep -iE '\.env$'

git commit -m "Deploy AI SalesMate web app"
git branch -M main
git remote add origin https://github.com/vinhnt120501/NCG-AI4Sales-WebAPP.git
git push -u origin main
```

> Nếu push báo *"remote origin already exists"* → chạy `git remote set-url origin https://github.com/vinhnt120501/NCG-AI4Sales-WebAPP.git` rồi push lại.
> Nếu GitHub hỏi mật khẩu → dùng **Personal Access Token** (Settings → Developer settings → Tokens) thay cho mật khẩu, hoặc đăng nhập bằng `gh auth login`.

## 3. Bật GitHub Pages
1. Mở repo trên GitHub → tab **Settings** → mục **Pages** (cột trái).
2. **Source**: chọn **Deploy from a branch**.
3. **Branch**: `main` · **Folder**: **`/ (root)`** → bấm **Save**.
4. Chờ **1–2 phút**, tải lại trang Pages sẽ hiện link.

## 4. Link công khai
```
https://vinhnt120501.github.io/NCG-AI4Sales-WebAPP/
```
Mở thử: trang chờ Anova hiện ra rồi tự vào app. **Gửi link này cho sếp/khách.**

> Mỗi lần cập nhật code, chỉ cần:
> ```bash
> git add . && git commit -m "Cập nhật" && git push
> ```
> Pages tự build lại sau ~1–2 phút.

---

## 5. Xử lý sự cố thường gặp

| Hiện tượng | Nguyên nhân & cách sửa |
|---|---|
| Link 404 ngay sau khi Save | Pages chưa build xong — đợi 1–2 phút rồi tải lại. |
| Vào `/` bị trắng / không chuyển | Kiểm tra file `index.html` có ở **gốc repo** và Pages đang serve từ **/(root)**. |
| App mở nhưng **trống dữ liệu** (không có bệnh/sản phẩm) | Thiếu `.nojekyll` → `.md`/`json` bị Jekyll xử lý. Đảm bảo `.nojekyll` ở gốc repo và đã push. |
| Bản đồ không hiện | Cần Internet để tải bản đồ nền (OpenStreetMap) — bình thường. |
| Lỡ commit nhầm file `.env` | **Thu hồi key đó ngay** trên FPT Marketplace, tạo key mới, rồi xoá file khỏi lịch sử git. |

---

## 6. Tuỳ chọn

- **Repo gọn (chỉ web app + docs):** nếu không muốn đẩy cả `ver/` (bản Streamlit), `mobile-app/`, `AI4Sales-Mobile/` lên repo này, thêm chúng vào `.gitignore` trước khi `git add .`.
- **Tên miền riêng:** Settings → Pages → **Custom domain** (vd `salesmate.anova.vn`), trỏ DNS theo hướng dẫn GitHub.
- **Repo Private vẫn deploy Pages được** (với tài khoản hỗ trợ Pages cho private repo).

---

## Phụ lục — Bản chạy LLM thật (Streamlit)

Bản web tĩnh ở trên dùng dữ liệu mock, **không gọi LLM** → không tốn key. Nếu cần bản **gọi GLM-5.1 qua FPT Cloud** (thư mục `ver/salemate-ver/`), đó là app **Streamlit** cần backend + key → deploy lên **Streamlit Community Cloud** (https://share.streamlit.io): chọn repo, main file `app.py`, và dán key vào **Secrets** (`FPT_API_KEY`, `FPT_BASE_URL`, `FPT_MODEL`). Lưu ý: link công khai = ai cũng chat được và **tiêu quota key của bạn** → theo dõi/đổi key sau buổi demo.
