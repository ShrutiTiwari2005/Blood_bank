from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """Institutional User Profile Model v4.4"""
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    role: str # admin, staff, viewer
    created_at: Optional[str] = None
    last_login: Optional[str] = None
