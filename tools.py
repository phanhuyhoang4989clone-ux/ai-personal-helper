from langchain_core.tools import tool
import subprocess

# Thêm app mới ở đây: "tên gọi": lệnh mở
DANH_SACH_APP = {
    "chrome": "chrome",
    "notepad": "notepad",
    "calc": "calc",
    "riot": [r"C:\Riot Games\Riot Client\RiotClientServices.exe"],
    "valorant": [
        r"C:\Riot Games\Riot Client\RiotClientServices.exe",
        "--launch-product=valorant",
        "--launch-patchline=live",
    ],
}

@tool
def mo_phan_mem(ten_phan_mem: str) -> str:
    """
    Hàm này dùng để mở một phần mềm hoặc game trên máy tính.
    KHI NÀO SỬ DỤNG: Khi người dùng yêu cầu "mở...", "bật...", "khởi động...".
    CÁCH TRUYỀN THAM SỐ (ten_phan_mem): Chỉ truyền tên tiếng Anh viết thường.
    - "Mở trình duyệt" -> "chrome"
    - "Mở ghi chú" -> "notepad"
    - "Bật máy tính bỏ túi" -> "calc"
    - "Mở Riot Client" -> "riot"
    - "Chơi Valorant" / "Mở Valorant" -> "valorant"
    """
    ten = ten_phan_mem.strip().lower()
    if ten not in DANH_SACH_APP:
        return f"Không có '{ten}' trong danh sách. Các app mở được: {', '.join(DANH_SACH_APP)}"
    try:
        lenh = DANH_SACH_APP[ten]
        if isinstance(lenh, str):
            subprocess.Popen(f"start {lenh}", shell=True)
        else:
            subprocess.Popen(lenh)
        return "Đã mở thành công."
    except Exception as e:
        return f"Bị lỗi, không mở được: {e}"

# Gom lại thành danh sách công cụ
danh_sach_cong_cu = [mo_phan_mem]