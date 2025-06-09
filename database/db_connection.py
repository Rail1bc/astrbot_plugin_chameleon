import sqlite3
import os
from contextlib import contextmanager

from astrbot.core.log import LogManager
logging = LogManager.GetLogger(log_name="[数据库连接]")

_instance = None

@contextmanager
def get_dbc(db_file=None):
    global _instance
    if _instance is None:
        _instance = DatabaseConnector(db_file)
    with _instance.get_database_connection() as conn:
        yield conn

class DatabaseConnector:
    """
    数据库连接。
    """

    def __init__(self, db_file=None):
        """
        初始化消息计数器，使用 SQLite 数据库存储。
        db_file 参数现在是可选的。如果为 None，则自动生成数据库文件路径。

        Args:
            db_file (str, optional): SQLite 数据库文件路径。
                                     如果为 None，则自动生成路径。
        """
        if db_file is None:
            # 获取当前文件所在目录
            current_file_dir = os.path.dirname(os.path.abspath(__file__))

            base_dir = current_file_dir
            for _ in range(3):
                base_dir = os.path.dirname(base_dir)
                # 避免一直向上到根目录之上，可以添加一个检查，如果已经是根目录，则停止
                if (
                        os.path.dirname(base_dir) == base_dir
                ):  # 检查是否已经到达根目录 (dirname(root) == root)
                    break  # 停止向上

            # 构建 chameleon_data 文件夹路径
            data_dir = os.path.join(base_dir, "chameleon_data")

            # 确保 chameleon_data 文件夹存在，如果不存在则创建
            os.makedirs(
                data_dir, exist_ok=True
            )  # exist_ok=True 表示如果目录已存在，不会抛出异常

            self.db_file = os.path.join(data_dir, "chameleon.db")
        else:
            self.db_file = db_file  # 如果用户显式提供了 db_file，则使用用户提供的路径

        self._initialize_db()

    def _initialize_db(self):
        """
        初始化 SQLite 数据库和表。
        如果表不存在，则创建表。
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # 会话数据表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS session_data (
                session_id TEXT NOT NULL,
                prompt_version INTEGER NOT NULL,
                history_index INTEGER NOT NULL,
                tool_num INTEGER NOT NULL,
                content_num INTEGER NOT NULL,
                PRIMARY KEY (session_id)
            )
            """)

            # 创建提示词历史表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS role_identity_history (
                session_id TEXT NOT NULL,
                prompt_version INTEGER NOT NULL,
                prompt_text TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (session_id, role_index)
            )
            """)

            # 创建对话上下文表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS history_context (
                session_id TEXT NOT NULL,
                history_index INTEGER NOT NULL,
                role_type TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
                content TEXT NOT NULL,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (session_id, history_index)
            )
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_history 
                ON history_context(session_id, history_index)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_identity_version 
                ON role_identity_history(session_id, prompt_version)
            """)

            conn.commit()
            logging.debug(f"SQLite 数据库初始化完成，文件路径: {self.db_file}")
        except sqlite3.Error as e:
            logging.error(f"初始化 SQLite 数据库失败: {e}")
            if conn:
                conn.rollback()  # 回滚事务
        finally:
            if conn:
                conn.close()


    def get_database_connection(self):
        """作为上下文管理器返回数据库连接"""
        conn = sqlite3.connect(self.db_file)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()