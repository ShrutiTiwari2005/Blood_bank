from dataclasses import dataclass
from typing import Optional

@dataclass
class DonorSchema:
    id: Optional[int]
    name: str
    age: int
    blood_group: str
    city: str
    phone: str
    last_donation_date: str

@dataclass
class StockSchema:
    city: str
    blood_group: str
    units_available: int

@dataclass
class UserSchema:
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    role: str # admin, staff, viewer
    created_at: Optional[str] = None
