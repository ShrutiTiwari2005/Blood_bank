from dataclasses import dataclass

@dataclass
class Stock:
    """Real-time Clinical Stock Model v4.4"""
    city: str
    blood_group: str
    units_available: int
