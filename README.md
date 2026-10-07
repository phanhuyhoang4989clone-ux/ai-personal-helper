# [TÊN PROJECT] - Trợ lý AI chạy trên máy tính

Trợ lý AI chạy trên máy cá nhân, hiểu ngôn ngữ tự nhiên và thực hiện tác vụ thay người dùng (mở ứng dụng, quản lý file, chụp màn hình, mở website...), tương tự Copilot của Microsoft. Hệ thống dùng **Cloud API (Groq)** kết hợp **Tool Calling** để điều khiển máy.

**Môn học:** Introduction to Information Technology | **Giảng viên:** Nguyễn Đăng Quang | **Nhóm:** 3

## Tính năng dự kiến

- Chat với AI bằng ngôn ngữ tự nhiên
- Mở ứng dụng, thao tác file, chụp màn hình, mở website

*(Cập nhật lại khi các tính năng hoàn thành.)*

## Công nghệ

- Python
- Cloud API: Groq 
- Giao diện: Gradio

## Cài đặt và chạy

*(Sẽ bổ sung chi tiết khi project hoàn thiện.)*

```bash
git clone [URL_REPO]
cd [TEN_THU_MUC]
pip install -r requirements.txt
# Tạo file .env từ .env.example và điền API key của Grok (xAI)
```

Chạy ứng dụng (giao diện Gradio):

```bash
python app.py
```

> Không commit file `.env` (chứa API key) lên GitHub.

## Thành viên

| Họ tên | MSSV | Vai trò |
|---|---|---|
| Phan Huy Hoàng | 26110098 | Leader + Backend |
| Nguyễn Hoàng Nhân | 26110157 | AI / Prompt Engineering |
| Nguyễn Quang Huy | 26110106 | System Control (Local) |
| Nguyễn Trung Nguyên | 26110152 | Frontend / UI |
| Nguyễn Phước Hưng | 26110109 | Testing + Documentation + Present |
