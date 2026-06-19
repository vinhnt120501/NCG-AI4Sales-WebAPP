"""Salemate — Trợ lý bán hàng & tư vấn kỹ thuật chăn nuôi (Anova Feed).

Giao diện hoàn chỉnh, cấu hình API key ở backend (.env).
"""
import os
import html
import base64
import time
import streamlit as st
from dotenv import load_dotenv

from agent import build_client, run_agent
import tools as T

load_dotenv()

st.set_page_config(
    page_title="AI SalesMate · Nova Consumer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ===========================================================================
# THEME / CSS — nhận diện Anova (xanh lá nông nghiệp) + font tiếng Việt
# ===========================================================================
st.markdown(
    """
<style>
html, body, [class*="css"], button, input, textarea {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif !important;
}
:root {
  --sm-green: #6DBB45;
  --sm-blue: #0070B0;
  --sm-ink: #1E241F;
  --sm-muted: #66736A;
  --sm-line: #D8E2D5;
  --sm-soft: #F7FAF6;
}

/* Ẩn chrome mặc định của Streamlit */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; height: 0; }
header[data-testid="stHeader"] { background: transparent; height: 0; }
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stDecoration"] {
  background: #FFFFFF !important;
}
.block-container {
  padding-top: 0;
  padding-bottom: 7rem;
  max-width: none;
  padding-left: clamp(24px, 4vw, 72px);
  padding-right: clamp(24px, 4vw, 72px);
}
.stApp { background: #FFFFFF; }

.sm-topbar {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  max-width: none;
  margin: 0 auto;
}
.sm-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}
.sm-logo {
  height: 38px;
  width: auto;
  display: block;
}
.sm-brand-name {
  color: var(--sm-ink);
  font-size: 15px;
  font-weight: 700;
  line-height: 1.15;
}
.sm-brand-sub {
  color: var(--sm-muted);
  font-size: 12px;
  margin-top: 2px;
}
.sm-empty-shell {
  min-height: 360px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  text-align: center;
  padding-bottom: 42px;
}
.sm-empty-logo {
  height: 48px;
  width: auto;
  margin-bottom: 16px;
}
.sm-ready {
  color: var(--sm-ink);
  font-size: clamp(28px, 2.2vw, 40px);
  font-weight: 700;
  letter-spacing: 0;
  line-height: 1.08;
  margin-bottom: 12px;
}
.sm-ready-sub {
  color: var(--sm-muted);
  font-size: clamp(15px, 1vw, 19px);
  margin-bottom: 0;
}
.sm-chat-shell {
  width: min(980px, calc(100vw - 18vw));
  margin: 0 auto;
  padding-top: 56px;
}
.sm-user-row {
  display: flex;
  justify-content: flex-end;
  margin: 10px 0 34px;
}
.sm-user-bubble {
  max-width: min(76%, 560px);
  background: var(--sm-soft);
  color: var(--sm-ink);
  border: 1px solid var(--sm-line);
  border-radius: 24px;
  padding: 12px 18px;
  font-size: 16px;
  line-height: 1.55;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
.sm-bot-row {
  display: grid;
  grid-template-columns: 44px minmax(0, 680px) 1fr;
  column-gap: 14px;
  align-items: flex-start;
  margin: 0 0 36px;
}
.sm-bot-avatar {
  width: 38px;
  height: 38px;
  border: 1px solid var(--sm-line);
  border-radius: 50%;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.sm-bot-avatar img {
  width: 32px;
  height: auto;
  display: block;
}
.sm-bot-content {
  color: var(--sm-ink);
  font-size: 16px;
  line-height: 1.7;
  padding-top: 5px;
}
.sm-bot-content p:first-child {
  margin-top: 0;
}
.sm-bot-content p:last-child {
  margin-bottom: 0;
}
.sm-bot-pending {
  color: var(--sm-muted);
}

/* Chat bubble */
[data-testid="stChatMessage"] {
  background: transparent !important;
  padding: 0;
  margin-bottom: 32px;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
  border: 0;
}
[data-testid="stChatMessageAvatarAssistant"] {
  display: none;
}
[data-testid="stChatMessageContent"] {
  font-size: 16px;
  line-height: 1.7;
}

/* Input giống chat app */
[data-testid="stBottom"], [data-testid="stBottomBlockContainer"], [data-testid="stChatInput"] {
  background: #FFFFFF !important;
  background-color: #FFFFFF !important;
  background-image: none !important;
}
[data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] > div {
  background: #FFFFFF !important;
  background-color: #FFFFFF !important;
  background-image: none !important;
}
[data-testid="stBottom"]::before {
  content: "";
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 130px;
  background: #FFFFFF;
  z-index: -1;
}
[data-testid="stChatInput"] {
  width: min(980px, calc(100vw - 18vw));
  max-width: none;
  margin: 0 auto;
}
[data-testid="stChatInput"] > div {
  border-radius: 999px !important;
  border: 1px solid #E4E7E3 !important;
  box-shadow: 0 10px 28px rgba(30,36,31,.06);
  background: #FFFFFF !important;
}
[data-testid="stChatInput"] > div:focus-within {
  border-color: #D7DED5 !important;
  box-shadow: 0 10px 28px rgba(30,36,31,.07);
}
[data-testid="stChatInput"] textarea {
  font-size: 16px !important;
  color: var(--sm-ink) !important;
  background: #FFFFFF !important;
  caret-color: var(--sm-ink) !important;
}
[data-testid="stChatInput"] textarea::placeholder {
  color: #8A938D !important;
  opacity: 1 !important;
}
[data-testid="stChatInput"] button {
  background: var(--sm-green) !important;
  border: 1px solid var(--sm-green) !important;
  color: #FFFFFF !important;
}
.stApp:has(.sm-empty-shell) [data-testid="stChatInput"] {
  position: fixed;
  top: 53%;
  bottom: auto;
  left: 50%;
  transform: translate(-50%, 0);
  width: min(980px, calc(100vw - 18vw));
  z-index: 20;
}

/* Sidebar */
[data-testid="stSidebar"] {
  background: #F8FBF7;
  border-right: 1px solid var(--sm-line);
}
[data-testid="stSidebar"] * { color: var(--sm-ink); }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label {
  color: var(--sm-muted) !important;
}

.sm-pill { display:inline-block; padding:2px 9px; border-radius:999px; font-size:11px; font-weight:600; }
.sm-pill.ok { background:#EAF6E5; color:#2E6B1F; border: 1px solid #CEE8C5; }
.sm-pill.warn { background:#FDEFD0; color:#8a5a00; }
</style>
""",
    unsafe_allow_html=True,
)

# ===========================================================================
# CẤU HÌNH BACKEND
# ===========================================================================
def get_api_key() -> str:
    for k in (st.session_state.get("api_key_session", ""), os.getenv("FPT_API_KEY", "")):
        k = (k or "").strip()
        if k:
            return k
    return ""


DEFAULT_MODEL = os.getenv("FPT_MODEL", "GLM-5.1")
BASE_URL = os.getenv("FPT_BASE_URL", "https://mkp-api.fptcloud.com")

# Trạng thái hội thoại
if "display" not in st.session_state:
    st.session_state.display = []
if "api_messages" not in st.session_state:
    st.session_state.api_messages = []

api_key = get_api_key()


def _logo_uri() -> str:
    path = os.path.join(os.path.dirname(__file__), "assets", "anova-logo.png")
    try:
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    except OSError:
        return ""


LOGO_URI = _logo_uri()
LOGO_HTML = f'<img class="sm-logo" src="{LOGO_URI}" alt="Anova"/>' if LOGO_URI else ""
BOT_AVATAR_HTML = f'<img src="{LOGO_URI}" alt="Anova"/>' if LOGO_URI else "A"


def stream_text(slot, text: str, chunk_size: int = 4, delay: float = 0.012) -> None:
    """Render text progressively for a chat-like typing effect."""
    if not text:
        slot.markdown("")
        return

    rendered = ""
    for i in range(0, len(text), chunk_size):
        rendered += text[i : i + chunk_size]
        slot.markdown(rendered + "▌")
        time.sleep(delay)
    slot.markdown(text)

# ===========================================================================
# SIDEBAR
# ===========================================================================
with st.sidebar:
    st.markdown("### ⚙️ Bảng điều khiển")
    if api_key:
        st.markdown('Backend: <span class="sm-pill ok">● FPT Cloud · đã có key</span>', unsafe_allow_html=True)
    else:
        st.markdown('Backend: <span class="sm-pill warn">● Chưa có key FPT</span>', unsafe_allow_html=True)
        with st.expander("Cấu hình nhanh (tạm cho phiên này)"):
            tmp = st.text_input("Dán FPT API Key", type="password")
            if tmp:
                st.session_state.api_key_session = tmp
                st.rerun()
        st.caption("Khuyến nghị: điền key 1 lần vào `.env` (FPT_API_KEY=...) để backend tự chạy.")

    model = st.text_input(
        "Model (FPT Cloud)",
        value=DEFAULT_MODEL,
        help="ID model đúng như trên FPT Marketplace, vd GLM-5.1 / GLM-4.6 / DeepSeek-R1 / Llama-3.3-70B-Instruct.",
    )
    st.caption(f"Endpoint: {BASE_URL}")

    st.divider()
    st.markdown("**📦 Dữ liệu đang nạp**")
    n_vaccine = len([p for p in T.VET_PRODUCTS if p["loai"] == "vaccine"])
    st.markdown(
        f"- {len(T.VET_PRODUCTS)} thuốc/vaccine ({n_vaccine} vaccine)\n"
        f"- {len(T.DISEASES)} bệnh trong knowledge base\n"
        f"- {len(T.DISTRIBUTORS)} nhà phân phối\n"
        f"- {len(T.RETRIEVER.chunks)} đoạn tài liệu (RAG)"
    )
    st.divider()
    if st.button("🗑️ Xóa hội thoại", use_container_width=True):
        st.session_state.display = []
        st.session_state.api_messages = []
        st.rerun()

# ===========================================================================
# HỘI THOẠI
# ===========================================================================
st.markdown(
    f"""
<div class="sm-topbar">
  <div class="sm-brand">
    {LOGO_HTML}
    <div>
      <div class="sm-brand-name">AI SalesMate</div>
      <div class="sm-brand-sub">Nova Consumer · Anova Pharma · Navetco · Vetvaco</div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

prompt = st.chat_input("Ask anything")
pending_prompt = ""
if prompt:
    pending_prompt = prompt.strip()
    if pending_prompt:
        if not api_key:
            st.error("Chưa có API key FPT ở backend. Điền `FPT_API_KEY` vào file `.env` (hoặc dùng 'Cấu hình nhanh' ở thanh bên).")
            st.stop()
        st.session_state.display.append({"role": "user", "text": pending_prompt})
        st.session_state.api_messages.append({"role": "user", "content": pending_prompt})

if not st.session_state.display:
    st.markdown(
        f"""
<div class="sm-empty-shell">
  <div>
    {LOGO_HTML.replace('class="sm-logo"', 'class="sm-empty-logo"')}
    <div class="sm-ready">SalesMate sẵn sàng hỗ trợ.</div>
    <div class="sm-ready-sub">Hỏi về bệnh, thuốc, vaccine, liều dùng hoặc nhà phân phối.</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
else:
    st.markdown('<div class="sm-chat-shell">', unsafe_allow_html=True)
    for m in st.session_state.display:
        if m["role"] == "user":
            safe_text = html.escape(m["text"])
            st.markdown(
                f'<div class="sm-user-row"><div class="sm-user-bubble">{safe_text}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            bot_cols = st.columns([0.05, 0.62, 0.33], gap="small")
            with bot_cols[0]:
                st.markdown(f'<div class="sm-bot-avatar">{BOT_AVATAR_HTML}</div>', unsafe_allow_html=True)
            with bot_cols[1]:
                st.markdown(m["text"])

    if pending_prompt:
        bot_cols = st.columns([0.05, 0.62, 0.33], gap="small")
        with bot_cols[0]:
            st.markdown(f'<div class="sm-bot-avatar">{BOT_AVATAR_HTML}</div>', unsafe_allow_html=True)
        with bot_cols[1]:
            message_slot = st.empty()
            message_slot.markdown('<span class="sm-bot-pending">Đang xử lý...</span>', unsafe_allow_html=True)

            def on_event(kind, name, payload):
                return None

            try:
                client = build_client(api_key, BASE_URL)
                text, st.session_state.api_messages = run_agent(
                    client, model, st.session_state.api_messages, on_event=on_event
                )
            except Exception as e:  # noqa: BLE001
                text = f"Lỗi gọi API: {e}"

            stream_text(message_slot, text)
        st.session_state.display.append({"role": "assistant", "text": text})
    st.markdown("</div>", unsafe_allow_html=True)
