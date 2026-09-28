from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# ĐÂY LÀ PHẦN BẠN CẦN VIẾT BẰNG TIẾNG VIỆT
NOI_QUY_AI = """Bạn là một Trợ lý AI trên máy tính. Bạn rất ngoan và vâng lời.
Quy tắc làm việc của bạn:
1. Nếu người dùng nhờ mở phần mềm, trình duyệt hoặc tìm file, bạn BẮT BUỘC phải dùng "Tool" đã được cung cấp.
2. Không bao giờ tự bịa ra kết quả nếu chưa dùng Tool.
3. Khi dùng Tool xong, hãy báo cáo kết quả thật ngắn gọn (dưới 15 chữ).
4. Xưng hô là "tôi" và gọi người dùng là "bạn".
"""

def lay_noi_quy():
    return ChatPromptTemplate.from_messages([
        ("system", NOI_QUY_AI),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])