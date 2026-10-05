"""
AI Personal Helper - Frontend (Gradio 6)
Bố cục màu:  nền ĐEN  |  lịch sử chat chữ TRẮNG  |  ô nhập văn bản CAM

Chạy:  python UI.py
Mở:    http://127.0.0.1:7860   (nhấn Ctrl+F5 để tải lại sạch cache)
"""
import time
import gradio as gr


# ---------------------------------------------------------------
# 1. BACKEND GIẢ LẬP (mock)
#    Sau này thay bằng hàm thật của bạn backend, giữ nguyên chữ ký:
#    backend_chat(message, history) -> generator các "sự kiện"
#      {"type": "tool_start", "name": ..., "args": ...}
#      {"type": "tool_end",   "name": ..., "result": ...}
#      {"type": "text",       "content": ...}   (từng đoạn câu trả lời)
# ---------------------------------------------------------------
def backend_chat(message, history):
    if "mở" in message.lower():
        yield {"type": "tool_start", "name": "open_app", "args": {"app": "Chrome"}}
        time.sleep(1)
        yield {"type": "tool_end", "name": "open_app", "result": "Đã mở Chrome"}
    for ch in f"Mình đã nhận được: {message}":
        time.sleep(0.02)
        yield {"type": "text", "content": ch}


# ---------------------------------------------------------------
# 2. UI: chuyển các sự kiện của backend thành tin nhắn trong khung chat
# ---------------------------------------------------------------
def respond(message, history):
    msgs = []          # danh sách tin nhắn của lượt trả lời này
    tools = {}         # tên tool -> tin nhắn đang hiển thị
    answer = None

    try:
        for ev in backend_chat(message, history):
            if ev["type"] == "tool_start":
                m = gr.ChatMessage(
                    content=f"Tham số: `{ev['args']}`",
                    metadata={"title": f"🛠️ {ev['name']}", "status": "pending"},
                )
                tools[ev["name"]] = m
                msgs.append(m)
            elif ev["type"] == "tool_end":
                m = tools[ev["name"]]
                m.content += f"\n\nKết quả: {ev['result']}"
                m.metadata["status"] = "done"
            elif ev["type"] == "text":
                if answer is None:
                    answer = gr.ChatMessage(content="")
                    msgs.append(answer)
                answer.content += ev["content"]
            yield msgs
    except Exception as e:
        msgs.append(gr.ChatMessage(content=f"⚠️ Lỗi: {e}"))
        yield msgs


# ---------------------------------------------------------------
# 3. GIAO DIỆN: nền đen - chữ lịch sử chat trắng - ô nhập cam
#    CSS nhúng thẳng vào trang (gr.HTML) nên chạy ở mọi bản Gradio.
#    Dùng elem_id (#chat-area, #msg-box) để nhắm đúng phần tử.
# ---------------------------------------------------------------
CSS = """
/* ===== 1. NỀN NGOÀI: ĐEN ===== */
:root, .dark, gradio-app, body, .gradio-container {
    color-scheme: dark !important;
    --body-background-fill: #000000;
    --body-text-color: #FFFFFF;
    --body-text-color-subdued: #A3A3A3;
    --color-accent: #FE7C00;
    --link-text-color: #FB923C;
}
body, gradio-app, .gradio-container { background: #000000 !important; }
.gradio-container, .fillable, .app, main {
    width: 100% !important;
    max-width: 900px !important;
    margin: 0 auto !important;
}

/* Tiêu đề trắng, mô tả xám */
.gradio-container h1 {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    text-align: center !important;
}
.gradio-container .prose p, .gradio-container p { text-align: center; color: #A3A3A3; }

/* ===== 2. KHUNG LỊCH SỬ TRÒ CHUYỆN: nền đen, CHỮ TRẮNG ===== */
#chat-area {
    color-scheme: dark !important;
    --body-text-color: #FFFFFF;
    --body-text-color-subdued: #D4D4D4;
    --background-fill-primary: #000000;
    --background-fill-secondary: #000000;
    --block-background-fill: #000000;
    --panel-background-fill: #000000;
    --border-color-primary: #262626;
    --block-border-color: #262626;
    background: #000000 !important;
    border: 1px solid #262626 !important;
    border-radius: 16px !important;
    color: #FFFFFF !important;
}
#chat-area .bubble-wrap, #chat-area .wrapper, #chat-area [role="log"],
#chat-area .placeholder, #chat-area .placeholder-content {
    background: #000000 !important;
    color: #FFFFFF !important;
}

/* Tin nhắn của bạn: cam, chữ trắng */
#chat-area .message.user, #chat-area .user .message {
    background: #FE7C00 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
}
#chat-area .message.user *, #chat-area .user .message * { color: #FFFFFF !important; }

/* Tin nhắn bot: xám đen, chữ trắng */
#chat-area .message.bot, #chat-area .bot .message {
    background: #1A1A1A !important;
    color: #FFFFFF !important;
    border: 1px solid #333333 !important;
    border-radius: 14px !important;
}
#chat-area .message.bot *, #chat-area .bot .message * { color: #FFFFFF !important; }

/* Gợi ý ví dụ: thẻ đen, viền cam, chữ trắng */
#chat-area .examples button, #chat-area button.example, #chat-area .gr-examples button,
#chat-area .placeholder button {
    background: #111111 !important;
    border: 1px solid #FE7C00 !important;
    color: #FFFFFF !important;
    border-radius: 12px !important;
}
#chat-area .examples button:hover, #chat-area button.example:hover,
#chat-area .placeholder button:hover {
    background: #FE7C00 !important;
    color: #FFFFFF !important;
}

/* ===== 3. Ô NHẬP VĂN BẢN: CAM ===== */
#msg-box, #msg-box > *, #msg-box label, #msg-box .container, #msg-box .wrap {
    background: #FE7C00 !important;
    border-radius: 14px !important;
}
#msg-box textarea, #msg-box input {
    background: #FE7C00 !important;
    color: #FFFFFF !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 16px !important;
}
#msg-box textarea::placeholder, #msg-box input::placeholder {
    color: rgba(255, 255, 255, 0.8) !important;
}
#msg-box:focus-within { box-shadow: 0 0 0 3px rgba(254, 124, 0, 0.45) !important; }

/* Nút gửi: trắng, chữ cam, nổi trên nền cam */
button.primary, button[variant="primary"] {
    background: #FFFFFF !important;
    color: #FE7C00 !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
}
button.primary:hover { background: #FFEDD5 !important; }

footer { visibility: hidden; }
"""

# Theme mô phỏng "deepkyu/compact-theme" (Hugging Face), viết sẵn trong code
# nên không cần mạng để tải theme.
#   Primary #d0670c | Accent #fe7c00 | Neutral #737373 | Nền #000000 / #0b0f19
#   Font chính: Gabarito | Font mono: Roboto Mono
_primary = gr.themes.Color(
    c50="#fff6ec", c100="#ffe9d2", c200="#fdd0a0", c300="#f9b06a", c400="#f38d3a",
    c500="#e47a1c", c600="#d0670c", c700="#a8520b", c800="#86420d", c900="#6e380f",
    c950="#3d1d06", name="compact_primary",
)
_accent = gr.themes.Color(
    c50="#fff4e6", c100="#ffe5c2", c200="#ffcb85", c300="#ffab47", c400="#ff9019",
    c500="#fe7c00", c600="#e06300", c700="#b84b02", c800="#953b09", c900="#7a320b",
    c950="#451803", name="compact_accent",
)

_local_theme = gr.themes.Base(
    primary_hue=_primary,
    secondary_hue=_accent,
    neutral_hue="neutral",
    font=[gr.themes.GoogleFont("Gabarito"), "ui-sans-serif", "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("Roboto Mono"), "ui-monospace", "monospace"],
    radius_size=gr.themes.sizes.radius_md,
    spacing_size=gr.themes.sizes.spacing_sm,   # "compact": khoảng cách nhỏ gọn
    text_size=gr.themes.sizes.text_md,
).set(
    body_background_fill="#000000",
    body_background_fill_dark="#000000",
    button_primary_background_fill="#d0670c",
    button_primary_background_fill_dark="#d0670c",
    button_primary_background_fill_hover="#fe7c00",
    button_primary_background_fill_hover_dark="#fe7c00",
    button_primary_text_color="#FFFFFF",
    button_primary_text_color_dark="#FFFFFF",
)

# Ưu tiên tải đúng theme gốc "deepkyu/compact-theme" từ Hugging Face Hub
# (cần mạng). Nếu không tải được thì dùng bản mô phỏng ở trên.
try:
    theme = gr.Theme.from_hub("deepkyu/compact-theme")
except Exception as e:
    print(f"[UI] Không tải được theme từ Hub ({type(e).__name__}), dùng theme local.")
    theme = _local_theme

with gr.Blocks(title="AI Personal Helper") as demo:
    gr.HTML(f"<style>{CSS}</style>")
    gr.ChatInterface(
        fn=respond,
        title="AI Personal Helper",
        description="Trợ lý cá nhân điều khiển máy tính của bạn.",
        chatbot=gr.Chatbot(
            elem_id="chat-area",
            height=520,
            show_label=False,
            placeholder="👋 Xin chào! Hãy nhập yêu cầu để mình giúp bạn.",
        ),
        textbox=gr.Textbox(
            elem_id="msg-box",
            placeholder="Nhập yêu cầu của bạn...",
            container=False,
            scale=7,
        ),
        examples=["Mở Chrome giúp mình", "Chụp màn hình", "Xin chào"],
    )

if __name__ == "__main__":
    try:
        # Gradio 6: theme và css truyền vào launch()
        demo.launch(theme=theme, css=CSS)
    except TypeError:
        # Bản Gradio cũ hơn không nhận tham số này, CSS nhúng ở trên vẫn hoạt động
        demo.launch()