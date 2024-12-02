from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class StaffBase(BaseModel):
    name: str
    role: str
    wage: float

class StaffCreate(StaffBase):
    pass

class StaffUpdate(StaffBase):
    pass

class VenueBase(BaseModel):
    name: str
    location: str
    cost: float
    max_capacity: int
    open_time: time
    close_time: time