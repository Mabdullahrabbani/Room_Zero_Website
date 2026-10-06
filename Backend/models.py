from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    difficulty = Column(String, nullable=False)
    min_player = Column(Integer, default=1)
    max_player = Column(Integer, nullable=False)
    description = Column(Text)
    image = Column(String)
    price  = Column(Integer , nullable= True )

    bookings = relationship("Booking", back_populates="room")
class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        UniqueConstraint("room_id", "date", "time_slot", name="unique_slot"),
    )

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    date = Column(String, nullable=False)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    time_slot = Column(String, nullable=False)
    players = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    room = relationship("Room", back_populates="bookings")
class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))