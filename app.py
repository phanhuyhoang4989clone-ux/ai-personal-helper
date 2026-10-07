"""
AI Personal Helper - Desktop App
Chạy: python app.py
"""

import os
import base64
import threading
import time
import ctypes
import webview
import gradio as gr
from main import chat_with_tools


def image_to_markdown(filepath: str) -> str:
    """Nhúng ảnh vào tin nhắn trả lời"""
    try:
        with open(filepath, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return (
            f"Đã chụp màn hình thành công!\n\n"
            f"![screenshot](data:image/png;base64,{b64})"
        )
    except Exception as e:
        return f"Đã chụp nhưng không hiện được ảnh: {e}"


def create_ui():
    with gr.Blocks(title="AI Personal Helper") as demo:
        gr.Markdown("# AI Personal Helper")
        gr.Markdown("Trợ lý cá nhân điều khiển máy tính")

        chatbot = gr.Chatbot(height=500, show_label=False)

        with gr.Row():
            msg = gr.Textbox(
                placeholder="Nhập yêu cầu của bạn...",
                show_label=False,
                scale=8,
                container=False
            )
            send_btn = gr.Button("Gửi", variant="primary", scale=1)

        gr.Examples(
            examples=[
                "Mở Chrome giúp mình",
                "Chụp màn hình",
                "Chỉnh âm lượng 40",
                "Xin chào"
            ],
            inputs=msg
        )

        def user_submit(message, history):
            if not message or not str(message).strip():
                return "", history
            if history is None:
                history = []
            history = history + [{"role": "user", "content": message}]
            return "", history

        def bot_respond(history):
            if not history:
                return history

            message = history[-1]["content"]
            try:
                bot_reply = chat_with_tools(message)
            except Exception as e:
                bot_reply = f"Lỗi: {str(e)}"

            # Ảnh hiện trong tin nhắn bot (không tạo mục riêng)
            if isinstance(bot_reply, str) and bot_reply.startswith("SCREENSHOT_PATH::"):
                filepath = bot_reply.replace("SCREENSHOT_PATH::", "").strip()
                if os.path.exists(filepath):
                    bot_reply = image_to_markdown(filepath)
                else:
                    bot_reply = f"Không tìm thấy file: {filepath}"

            history.append({"role": "assistant", "content": bot_reply})
            return history

        msg.submit(
            user_submit, [msg, chatbot], [msg, chatbot], queue=False
        ).then(
            bot_respond, chatbot, chatbot
        )

        send_btn.click(
            user_submit, [msg, chatbot], [msg, chatbot], queue=False
        ).then(
            bot_respond, chatbot, chatbot
        )

    return demo


def start_gradio():
    demo = create_ui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=False,
        prevent_thread_lock=True
    )


def set_window_icon():
    time.sleep(1.5)
    try:
        hwnd = ctypes.windll.user32.FindWindowW(None, "AI Personal Helper")
        if hwnd:
            hicon = ctypes.windll.user32.LoadImageW(
                0, "icon.ico", 1, 0, 0, 0x0010
            )
            if hicon:
                ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 0, hicon)
                ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 1, hicon)
    except Exception as e:
        print("Không đặt được icon:", e)


if __name__ == "__main__":
    t = threading.Thread(target=start_gradio, daemon=True)
    t.start()
    time.sleep(2)

    threading.Thread(target=set_window_icon, daemon=True).start()

    webview.create_window(
        title="AI Personal Helper",
        url="http://127.0.0.1:7860",
        width=900,
        height=650,
        resizable=True,
        min_size=(700, 500)
    )
    webview.start()