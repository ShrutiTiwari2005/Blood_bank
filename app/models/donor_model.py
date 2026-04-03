from dataclasses import dataclass
from typing import Optional

@dataclass
class Donor:
    """Medical Donor Registry Model v4.4"""
    id: Optional[int]
    name: str
    age: int
    blood_group: str
    city: str
    phone: str
    last_donation_date: str
    reliability_score: float = 8.0
