from db_connection import get_dbc
from models import RoleIdentity
from datetime import datetime

class RoleRepository:
    @staticmethod
    def save_prompt_version(session_id: int, prompt_text: str) -> RoleIdentity:
        """保存新的提示词版本并返回对象"""
        with get_dbc() as conn:
            cursor = conn.cursor()

            # 获取最大下标
            cursor.execute(
                "SELECT MAX(prompt_version) FROM role_identity_history WHERE session_id = ?",
                session_id
            )
            max_prompt_version = cursor.fetchone()[0] or 0

            # 插入最新提示词
            new_prompt_version = max_prompt_version + 1
            cursor.execute(
                "INSERT INTO role_identity_history (session_id, prompt_version, prompt_text)"
                "VALUES (?, ?, ?)",
                (session_id, new_prompt_version, prompt_text)
            )

            # 返回新创建的提示词对象
            return RoleIdentity(
                session_id=session_id,
                prompt_version=new_prompt_version,
                prompt_text=prompt_text,
                updated_at=datetime.now()
            )

    @staticmethod
    def get_current_prompt(session_id: int) -> str:
        """获取用户当前最新的提示词文本"""
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT prompt_text FROM role_identity_history "
                "WHERE session_id = ? "
                "ORDER BY prompt_version DESC LIMIT 1",
                (session_id,)
            )
            result = cursor.fetchone()
            return result["prompt_text"] if result else None

    @staticmethod
    def get_prompt_history(session_id: int, limit: int = 5) -> list[RoleIdentity]:
        """获取用户的提示词变更历史"""
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT session_id, prompt_version, prompt_text, updated_at "
                "FROM role_identity_history "
                "WHERE session_id = ? "
                "ORDER BY prompt_version DESC LIMIT ?",
                (session_id, limit)
            )
            return [
                RoleIdentity(
                    session_id=session_id,
                    prompt_version=row["prompt_version"],
                    prompt_text=row["prompt_text"],
                    updated_at=datetime.fromisoformat(row["updated_at"])
                )
                for row in cursor.fetchall()
            ]