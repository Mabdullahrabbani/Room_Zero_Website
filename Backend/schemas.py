from pydantic import BaseModel , EmailStr , Field , field_validator
from datetime import date as date_type
from email_validator import validate_email , EmailNotValidError
ALLOWED_SLOTS = ['10:00' , '12:00' , '14:00' , '16:00' , '18:00']
class RoomOut(BaseModel):
    id : int 
    name : str 
    difficulty :str 
    price : int   | None = None 
    min_player : int 
    max_player : int 
    description : str | None = None 
    image:str | None = None 
    class Config:
        from_attributes = True
class BookingCreate(BaseModel):
    room_id : int 
    name : str
    email : str 
    date : str
    time_slot : str 
    players : int 
    @field_validator('time_slot')
    @classmethod
    def check_time(cls , v):
        if v not in ALLOWED_SLOTS:
            raise ValueError(f"Invalid time slot '{v}'. Allowed: {ALLOWED_SLOTS}")
        return v 
    @field_validator("date")
    @classmethod
    def check_date(cls , v):
        try:
         d= date_type.fromisoformat(v)
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        if d < date_type.today():
                        raise ValueError("Date cannot be in the past")
        return v 
    @field_validator('email')
    @classmethod
    def check_email(cls , v):
        try:
              return validate_email(v, check_deliverability = True ).normalized
        except EmailNotValidError as e:
             raise ValueError(str(e))
class BookingOut(BaseModel):
    id: int
    room_id: int
    name: str
    date: str
    time_slot: str
    players: int
    class Config:
        from_attributes = True
class ReviewCreate(BaseModel):
    name : str 
    rating : int 
    comment : str 
class ReviewOut(BaseModel):
    id: int
    name: str
    rating: int
    comment: str

    class Config:
        from_attributes = True




