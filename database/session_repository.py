from db_connection import get_dbc
from models import SessionData

class SessionRepository:

    # 持久化新会话
    @staticmethod
    def save_new_session_data(session_id: str, prompt_version: int,history_index: int, tool_num: int, content_num: int) -> SessionData:
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO session_data (session_id, prompt_version, history_index, tool_num, content_num)
                VALUES (?, ?, ?, ?, ?)
            """, (session_id, prompt_version, history_index, tool_num, content_num))

    # 更新会话数据
    @staticmethod
    def update_session_data(sd: SessionData):
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE session_data
                SET prompt_version = ?, history_index = ?, tool_num = ?, content_num = ?
                WHERE session_id = ?
            """, (sd.prompt_version, sd.history_index, sd.tool_num, sd.content_num, sd.session_id))

    # 更新会话数据，仅更新角色演进版本
    @staticmethod
    def update_session_prompt_version(session_id: str, prompt_version: int):
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE session_data
                SET prompt_version = ?
                WHERE session_id = ?
            """, (prompt_version, session_id))

    # 更新会话数据，仅更新历史下标
    @staticmethod
    def update_session_history_index(session_id: str, history_index: int):
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE session_data
                SET history_index = ?
                WHERE session_id = ?
            """, (history_index, session_id))

    # 更新会话数据，仅更新工具调用数
    @staticmethod
    def update_session_tool_num(session_id: str, tool_num: int):
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE session_data
                SET tool_num = ?
                WHERE session_id = ?
            """, (tool_num, session_id))

    # 更新会话数据，仅更新真实上下文数
    @staticmethod
    def update_session_content_num(session_id: str, content_num: int):
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE session_data
                SET content_num = ?
                WHERE session_id = ?
            """, (content_num, session_id))


    # 查询会话数据
    @staticmethod
    def get_session_data(session_id: str) -> SessionData:
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT prompt_version, history_index, tool_num, content_num
                FROM session_data
                WHERE session_id = ?
            """, (session_id,))
            row = cursor.fetchone()
            if row:
                return SessionData(session_id, row[0], row[1], row[2], row[3])

    # 查询某会话的角色演进版本
    @staticmethod
    def get_session_prompt_version(session_id: str) -> int:
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT prompt_version
                FROM session_data
                WHERE session_id = ?
            """, (session_id,))
            row = cursor.fetchone()
            return row if row[0] else 0

    # 查询某会话的当前历史下标
    @staticmethod
    def get_session_history_index(session_id: str) -> int:
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT history_index
                FROM session_data
                WHERE session_id = ?
            """, (session_id,))
            row = cursor.fetchone()
            return row if row[0] else 0

    # 查询某会话的工具调用数
    @staticmethod
    def get_session_tool_num(session_id: str) -> int:
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tool_num
                FROM session_data
                WHERE session_id = ?
            """, (session_id,))
            row = cursor.fetchone()
            return row if row[0] else 0

    # 查询某会话的真实上下文数
    @staticmethod
    def get_session_content_num(session_id: str) -> int:
        with get_dbc() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT content_num
                FROM session_data
                WHERE session_id = ?
            """, (session_id,))
            row = cursor.fetchone()
            return row if row[0] else 0