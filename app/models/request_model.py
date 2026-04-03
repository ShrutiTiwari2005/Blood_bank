from dataclasses import dataclass
from typing import Optional

@dataclass
class BloodRequest:
    """Institutional Procurement Request Model v4.4"""
    id: Optional[int]
    city: str
    blood_group: str
    units_required: int
    status: str # pending, approved, fulfilled, rejected
    user_id: Optional[int]
    created_at: Optional[str] = None
