# AI Personal Helper – Trợ lý AI chạy trên máy tính

Trợ lý ảo trên máy cá nhân, hiểu ngôn ngữ tự nhiên và thực hiện tác vụ thay người dùng (mở ứng dụng, quản lý file, chụp màn hình, mở website, chỉnh âm lượng…).

Hệ thống dùng kiến trúc **Hybrid**: **Cloud LLM (Groq API)** kết hợp **Tool Calling** để điều khiển máy local.

| Thông tin | Chi tiết |
|-----------|----------|
| **Môn học** | Introduction to Information Technology |
| **Giảng viên** | Nguyễn Đăng Quang |
| **Nhóm** | 3 |

---

## 1. Tính năng

- Chat với AI bằng tiếng Việt (ngôn ngữ tự nhiên)
- Mở ứng dụng trên máy (Chrome, Notepad, Discord…)
- Mở website (Google, YouTube…)
- Chụp màn hình và lưu vào thư mục `screenshot/`
- Đọc / ghi / thêm ghi chú file (thư mục `notes/`)
- Chỉnh âm lượng hệ thống (0–100)
- Xem ngày giờ hiện tại
- Giao diện chat (Gradio), có thể chạy dạng cửa sổ app (pywebview)

### Ví dụ lệnh

| Bạn gõ | Hệ thống làm |
|--------|----------------|
| `Mở Chrome giúp mình` | Mở Google Chrome |
| `Mở youtube.com` | Mở website YouTube |
| `Chụp màn hình` | Chụp màn hình, lưu file ảnh |
| `Chỉnh âm lượng 40` | Đặt volume = 40% |
| `Viết note: Họp nhóm lúc 8h` | Ghi chú vào `notes/` |
| `Bây giờ là mấy giờ?` | Trả về giờ hiện tại |

---

## 2. Công nghệ

| Thành phần | Công nghệ |
|------------|-----------|
| Ngôn ngữ | Python |
| Cloud LLM | Groq API (Tool Calling) |
| Giao diện | Gradio |
| Cửa sổ desktop | pywebview (tùy chọn) |
| Xử lý ảnh | Pillow |
| Âm lượng Windows | pycaw + comtypes |

### Luồng hoạt động (Tool Calling)

Người dùng nhập lệnh
        ↓
LLM (Groq) chọn tool phù hợp
        ↓
Python chạy hàm local trên máy
        ↓
Trả kết quả → LLM trả lời tự nhiên (hoặc hiện ảnh nếu screenshot)


---

## 3. Cấu trúc thư mục


aph/

├── main.py              # Backend: tools + chat_with_tools

├── app.py               # UI Gradio + cửa sổ desktop (pywebview)

├── requirements.txt     # Danh sách thư viện

├── .env                 # GROQ_API_KEY 

├── notes/               # File ghi chú

├── screenshot/          # Ảnh chụp màn hình

└── README.md



---

## 4. Cài đặt và chạy

### Bước 1 – Clone dự án

```bash
git clone https://github.com/phanhuyhoang4989clone-ux/ai-personal-helper.git
cd aph
```

### Bước 2 – Cài thư viện

```bash
python -m pip install -r requirements.txt
```

Nội dung `requirements.txt`:

```text
groq
python-dotenv
gradio
pillow
pycaw
comtypes
pywebview
AppOpener
```

### Bước 3 – Cấu hình API key

Tạo file `.env` trong thư mục dự án:

```env
GROQ_API_KEY=nhập_key_groq_của_bạn
```

Lấy key miễn phí tại: [https://console.groq.com](https://console.groq.com)


### Bước 4 – Chạy ứng dụng

**Cách 1 – Bằng file .bat (khuyến nghị):**

Ấn mở trực tiếp file Maph.bat ( có thể sử dụng cửa sổ đã mở hoặc web http://http://127.0.0.1:7860/ )

**Cách 2 – Cửa sổ app:**

```bash
python app.py 
```

## 5. Thành viên & phân công

| Họ tên | MSSV | Vai trò | Nhiệm vụ chính |
|--------|------|---------|----------------|
| Phan Huy Hoàng | 26110098 | Leader + Backend | Quản lý tiến độ; tích hợp Groq API + Tool Calling; quản lý GitHub |
| Nguyễn Hoàng Nhân | 26110157 | AI / Prompt Engineering | System prompt; thiết kế tool schema; tối ưu Tool Calling & edge case |
| Nguyễn Quang Huy | 26110106 | System Control (Local) | Hàm điều khiển máy: mở app/web, screenshot, file, volume |
| Nguyễn Trung Nguyên | 26110152 | Frontend / UI | Giao diện Gradio; kết nối backend; hiển thị chat & ảnh |
| Nguyễn Phước Hưng | 26110109 | Testing + Docs + Present | Kiểm thử; README & báo cáo; slide; video demo; thuyết trình |

---

## 6. Lưu ý

- Cần **kết nối internet** để gọi Groq API
- Một số tính năng tối ưu cho **Windows** (âm lượng, mở app)
- Nên dùng **Python 3.10 – 3.12** nếu gặp lỗi tương thích với bản quá mới
- Thư mục `notes/` và `screenshot/` được tạo tự động khi chạy

---

## 7. License

Đồ án môn học – chỉ sử dụng cho mục đích học tập.
