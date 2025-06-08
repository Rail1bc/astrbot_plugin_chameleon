from dataclasses import dataclass
from datetime import datetime

@dataclass
class RoleIdentity:
    session_id: int
    prompt_version: int
    prompt_text: str
    updated_at: datetime

@dataclass
class HistoryContent:
    session_id: int
    history_index: int
    role_type: str  # 'user', 'assistant', 'system'
    content: str
    create_time: datetime