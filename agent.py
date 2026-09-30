import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

# Lấy các công cụ và nội quy bạn đã làm ở 2 file kia
from tools import danh_sach_cong_cu, DANH_SACH_APP, mo_phan_mem
from prompts import lay_noi_quy

# 1. Nạp chìa khóa từ két sắt .env
load_dotenv()

# 2. Kết nối với bộ não Gemini trên Cloud
bo_nao_ai = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)

# 3. Lắp ráp Nội quy + Công cụ + Bộ não
noi_quy = lay_noi_quy()
ai_agent = create_tool_calling_agent(bo_nao_ai, danh_sach_cong_cu, noi_quy)
dieu_hanh = AgentExecutor(agent=ai_agent, tools=danh_sach_cong_cu, verbose=True)

# 4. Vòng lặp trò chuyện
print("\n=== TRỢ LÝ AI ĐÃ SẴN SÀNG! (Gõ 'thoat' để dừng) ===\n")

while True:
    cau_hoi = input("Bạn muốn AI làm gì: ")
    if cau_hoi.strip().lower() == "thoat":
        break

    # Kiểm tra nhanh: câu có chứa tên app nào không -> mở thẳng, khỏi tốn lượt gọi AI
    cau_hoi_thuong = cau_hoi.lower()
    ten_tim_thay = None
    for ten_app in DANH_SACH_APP:
        if ten_app in cau_hoi_thuong:
            ten_tim_thay = ten_app
            break

    if ten_tim_thay:
        ket_qua = mo_phan_mem.func(ten_tim_thay)
        print(ket_qua)
    else:
        # Câu phức tạp, không khớp tên app nào -> mới nhờ AI xử lý
        ket_qua = dieu_hanh.invoke({"input": cau_hoi})
        print(ket_qua["output"])