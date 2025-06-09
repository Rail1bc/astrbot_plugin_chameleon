from data.plugins.astrbot_plugin_chameleon.database.models import SessionData
from db_connection import get_dbc
from models import HistoryContent
from session_repository import SessionRepository
from datetime import datetime

class ContentRepository:
    @staticmethod
    def save_message(session_id: str, role_type: str, content: str):
        """保存对话消息并返回对象"""
        sd = SessionRepository.get_session_data(session_id)
        sd.history_index += 1
        match role_type:
            case "user", "assistant":
                sd.content_num += 1
            case  "Function":
                sd.tool_num += 1
        SessionRepository.update_session_data(sd)

        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conversation_context (session_id, history_index, role_type, content) "
                "VALUES (?, ?, ?, ?)",
                (session_id, sd.history_index, role_type, content)
            )


    @staticmethod
    def get_recent_conversation(session_id: str, limit: int = 10) -> list[dict]:
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
                   ][::-1]

    @staticmethod
    def clear_conversation(session_id: str):
        """清除用户的所有对话历史"""
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM conversation_context WHERE session_id = ?",
                (session_id)
            )