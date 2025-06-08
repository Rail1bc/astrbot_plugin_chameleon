from .db_connection import get_dbc
from .models import HistoryContent
from datetime import datetime

class ConversationRepository:
    @staticmethod
    def save_message(session_id: int, role_type: str, content: str) -> HistoryContent:
        """保存对话消息并返回对象"""
        with get_dbc() as conn:
            cursor = conn.cursor()

            # 获取最大下标
            cursor.execute(
                "SELECT MAX(history_index) FROM history_context WHERE session_id = ?",
                session_id
            )
            max_index = cursor.fetchone()[0] or 0

            new_index = max_index + 1
            cursor.execute(
                "INSERT INTO conversation_context (session_id, history_index, role_type, content) "
                "VALUES (?, ?, ?, ?)",
                (session_id, new_index, role_type, content)
            )

            return HistoryContent(
                session_id=session_id,
                history_index=new_index,
                role_type=role_type,
                content=content,
                create_time=datetime.now()
            )

    @staticmethod
    def get_recent_conversation(session_id: int, limit: int = 10) -> list[dict]:
        """获取用户最近的对话上下文（角色扮演格式）"""
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role, content FROM conversation_context "
                "WHERE session_id = ? "
                "ORDER BY timestamp DESC LIMIT ?",
                (session_id, limit)
            )
            return [
                       {"role": row["role"], "content": row["content"]}
                       for row in cursor.fetchall()
                   ][::-1]  # 反转顺序：从旧到新

    @staticmethod
    def clear_conversation(session_id: int):
        """清除用户的所有对话历史"""
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM conversation_context WHERE session_id = ?",
                (session_id)
            )