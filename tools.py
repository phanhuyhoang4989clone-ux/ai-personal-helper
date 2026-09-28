from langchain_core.tools import tool
import subprocess # Thư viện để mở app (Huy sẽ lo cái này)

# Từ @tool báo cho AI biết đây là món đồ chơi của nó
@tool
def mo_phan_mem(ten_phan_mem: str) -> str:
    """
    Hàm này dùng để mở một phần mềm trên máy tính.
    KHI NÀO SỬ DỤNG: Khi người dùng yêu cầu "mở...", "bật...", "khởi động...".
    CÁCH TRUYỀN THAM SỐ (ten_phan_mem): Chỉ truyền vào tên tiếng Anh viết thường.
    - Nếu người dùng bảo "Mở trình duyệt", truyền vào "chrome"
    - Nếu người dùng bảo "Mở ghi chú", truyền vào "notepad"
    - Nếu người dùng bảo "Bật máy tính bỏ túi", truyền vào "calc"
    """
    # Khúc dưới này là code của Quang Huy, bạn không cần quan tâm lắm
    try:
        subprocess.Popen(f"start {ten_phan_mem}", shell=True)
        return "Đã mở thành công."
    except Exception:
        return "Bị lỗi, không mở được."

# Gom lại thành 1 hộp công cụ
danh_sach_cong_cu = [mo_phan_mem]