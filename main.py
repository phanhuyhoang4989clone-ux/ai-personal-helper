import os
import json
import webbrowser
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
import shutil
from AppOpener import open as open_app
import sys
import io

# Ép toàn bộ stdout/stderr dùng UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ====================== CÁC HÀM ĐIỀU KHIỂN MÁY (Local Tools) ======================

def open_website(url: str) -> str:
    """Mở một trang web bằng trình duyệt mặc định"""
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        webbrowser.open(url)
        return f"Đã mở website: {url}"
    except Exception as e:
        return f"Lỗi khi mở website: {str(e)}"




def open_application(app_name: str) -> str:
    """
    Tự động tìm và mở ứng dụng theo tên (hỗ trợ gần đúng)
    Không hardcode bất kỳ app cụ thể nào.
    """
    import os
    import subprocess
    from pathlib import Path

    name = app_name.strip().lower()
    
    search_dirs = [
        Path(os.environ["APPDATA"]) / r"Microsoft\Windows\Start Menu\Programs",
        Path(os.environ["PROGRAMDATA"]) / r"Microsoft\Windows\Start Menu\Programs",
        Path(os.environ["LOCALAPPDATA"]) / r"Microsoft\Windows\Start Menu\Programs",
    ]

    candidates = []

    for directory in search_dirs:
        if not directory.exists():
            continue
        for lnk in directory.rglob("*.lnk"):
            if name in lnk.stem.lower():
                candidates.append(lnk)

    if candidates:
        # Chọn cái có tên ngắn nhất (thường chính xác hơn)
        best = min(candidates, key=lambda x: len(x.stem))
        try:
            os.startfile(str(best))
            return f"Đã mở thành công: {best.stem}"
        except Exception as e:
            return f"Tìm thấy {best.stem} nhưng không mở được: {e}"

    # Thử lệnh start thông thường
    try:
        subprocess.Popen(f'start "" "{app_name}"', shell=True)
        return f"Đã thử mở '{app_name}' bằng lệnh hệ thống"
    except Exception:
        return f"Không tìm thấy ứng dụng nào khớp với: {app_name}"

def get_current_time() -> str:
    """Lấy thời gian hiện tại"""
    now = datetime.now()
    return now.strftime("%H:%M:%S ngày %d/%m/%Y")


def take_screenshot(**kwargs) -> str:
    try:
        from PIL import ImageGrab
        from datetime import datetime
        import os

        base_dir = os.path.dirname(os.path.abspath(__file__))
        screenshot_dir = os.path.join(base_dir, "screenshot")
        os.makedirs(screenshot_dir, exist_ok=True)

        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(screenshot_dir, filename)

        screenshot = ImageGrab.grab()
        screenshot.save(filepath)

        # Trả về dạng đặc biệt để UI nhận biết
        return f"SCREENSHOT_PATH::{filepath}"
    except Exception as e:
        return f"Lỗi khi chụp màn hình: {type(e).__name__}: {str(e)}"
    
def set_volume(level: int) -> str:
    """Chỉnh âm lượng hệ thống từ 0 đến 100"""
    try:
        from pycaw.pycaw import AudioUtilities

        level = max(0, min(100, int(level)))

        device = AudioUtilities.GetSpeakers()
        
        # Cách mới của pycaw
        device.volume_percent = level

        return f"Đã chỉnh âm lượng thành {level}%"
    except Exception as e:
        return f"Lỗi khi chỉnh âm lượng: {type(e).__name__}: {str(e)}"

# Thư mục mặc định để lưu ghi chú (aph)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTE_DIR = os.path.join(BASE_DIR, "notes")   # → aph/notes
os.makedirs(NOTE_DIR, exist_ok=True)

def read_file(file_path: str = None) -> str:
    """Đọc nội dung file. Mặc định đọc note hôm nay trong thư mục aph/notes"""
    try:
        if not file_path:
            today = datetime.now().strftime("%Y-%m-%d")
            file_path = os.path.join(NOTE_DIR, f"note_{today}.txt")

        if not os.path.exists(file_path):
            return f"Không tìm thấy file: {file_path}"

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"Nội dung file:\n{content}"
    except Exception as e:
        return f"Lỗi khi đọc file: {str(e)}"


def write_file(content: str, file_path: str = None) -> str:
    """Ghi đè hoặc tạo mới file. Mặc định lưu vào aph/notes"""
    try:
        if not file_path:
            today = datetime.now().strftime("%Y-%m-%d")
            file_path = os.path.join(NOTE_DIR, f"note_{today}.txt")
        else:
            # Nếu chỉ đưa tên file thì lưu vào thư mục notes
            if not os.path.isabs(file_path) and not file_path.startswith("notes"):
                file_path = os.path.join(NOTE_DIR, file_path)

        folder = os.path.dirname(file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Đã ghi thành công vào: {file_path}"
    except Exception as e:
        return f"Lỗi khi ghi file: {str(e)}"


def append_file(content: str, file_path: str = None) -> str:
    """Thêm nội dung vào cuối file. Mặc định lưu vào aph/notes theo ngày"""
    try:
        if not file_path:
            today = datetime.now().strftime("%Y-%m-%d")
            file_path = os.path.join(NOTE_DIR, f"note_{today}.txt")
        else:
            if not os.path.isabs(file_path) and not file_path.startswith("notes"):
                file_path = os.path.join(NOTE_DIR, file_path)

        folder = os.path.dirname(file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        line = f" {content}\n"

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(line)

        return f"Đã thêm ghi chú vào: {file_path}"
    except Exception as e:
        return f"Lỗi khi thêm nội dung: {str(e)}"
# Mapping tên tool → hàm thực thi
available_tools = {
    "open_website": open_website,
    "open_application": open_application,
    "get_current_time": get_current_time,
    "take_screenshot": take_screenshot,
    "set_volume": set_volume,
    "read_file": read_file,
    "write_file": write_file,
    "append_file": append_file,
}

# ====================== ĐỊNH NGHĨA TOOL CHO LLM ======================

tools = [
    {
        "type": "function",
        "function": {
            "name": "open_website",
            "description": "Mở một trang web trên trình duyệt. Dùng khi người dùng muốn mở website, google, youtube, facebook...",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Địa chỉ website cần mở (ví dụ: google.com, youtube.com)"
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_application",
            "description": "Mở ứng dụng trên máy tính (notepad, calculator, chrome, edge, explorer...)",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "Tên ứng dụng cần mở"
                    }
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Lấy thời gian và ngày hiện tại",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "take_screenshot",
            "description": "Chụp màn hình máy tính và lưu thành file ảnh",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_volume",
            "description": "Chỉnh âm lượng máy tính (0 đến 100)",
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "integer",
                        "description": "Mức âm lượng (0 = tắt tiếng, 100 = lớn nhất)"
                    }
                },
                "required": ["level"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Đọc nội dung file. Nếu không chỉ định file_path thì đọc note hôm nay.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Đường dẫn file (không bắt buộc)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Ghi đè hoặc tạo mới file. Nếu không chỉ định file_path thì lưu vào notes theo ngày.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Nội dung muốn ghi"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Đường dẫn file (không bắt buộc)"
                    }
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "append_file",
            "description": "Thêm ghi chú vào file. Nếu không chỉ định file_path thì tự lưu vào thư mục notes theo ngày.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Nội dung muốn ghi chú"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Đường dẫn file (không bắt buộc)"
                    }
                },
                "required": ["content"]
            }
        }
    }
]

# ====================== HÀM CHÍNH XỬ LÝ HỘI THOẠI ======================

def chat_with_tools(user_message: str, conversation_history: list = None):
    if conversation_history is None:
        conversation_history = []

    system_prompt = {
        "role": "system",
        "content": (
            "Bạn là AI Personal Helper - trợ lý ảo thông minh trên máy tính. "
            "Bạn có thể trò chuyện bình thường và điều khiển máy tính thông qua các công cụ. "
            "Khi người dùng yêu cầu mở web, mở ứng dụng, xem giờ, chụp màn hình... hãy dùng tool tương ứng. "
            "Trả lời bằng tiếng Việt, thân thiện và ngắn gọn."
        )
    }

    messages = [system_prompt] + conversation_history + [
        {"role": "user", "content": user_message}
    ]

    # Bước 1: Gọi model lần đầu
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",      # Model mạnh + hỗ trợ tool tốt
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.6,
        max_tokens=1024
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # Bước 2: Nếu model muốn gọi tool
    if tool_calls:
        messages.append({
            "role": "assistant",
            "content": response_message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in tool_calls
            ]
        })

        screenshot_path = None

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments or "{}")

            print(f"→ Đang gọi tool: {function_name} với args: {function_args}")

            if function_name in available_tools:
                function_response = available_tools[function_name](**function_args)
            else:
                function_response = f"Không tìm thấy tool: {function_name}"

            print(f"→ Kết quả tool: {function_response}")

            # Bắt path ảnh chụp màn hình
            if isinstance(function_response, str) and function_response.startswith("SCREENSHOT_PATH::"):
                screenshot_path = function_response.replace("SCREENSHOT_PATH::", "").strip()

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(function_response)
            })

        # Quan trọng: nếu là screenshot thì trả về path, KHÔNG gọi model lần 2
        if screenshot_path:
            return f"SCREENSHOT_PATH::{screenshot_path}"
        # Các tool khác mới gọi model lần 2
        messages.append({
            "role": "user",
            "content": (
                "Dựa trên kết quả các tool ở trên, hãy trả lời người dùng một cách tự nhiên, "
                "ngắn gọn bằng tiếng Việt. Tuyệt đối không được gọi tool nữa."
            )
        })

        second_response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.5,
            tool_choice="none"
        )
        final_answer = second_response.choices[0].message.content

    else:
        final_answer = response_message.content

    return final_answer


# ====================== TEST NHANH ======================
if __name__ == "__main__":
    print("=== AI Personal Helper (Groq + Tool Calling) ===")
    print("Gõ 'exit' để thoát\n")

    history = []

    while True:
        user_input = input("Bạn: ")
        if user_input.lower() in ["exit", "quit", "thoát"]:
            break

        answer = chat_with_tools(user_input, history)
        print(f"Assistant: {answer}\n")

        # Lưu lịch sử đơn giản
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": answer})

