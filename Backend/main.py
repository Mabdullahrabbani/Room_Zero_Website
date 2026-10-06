from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, get_db
from SendEmail import send_booking_email
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import smtplib
import models
import schemas
app = FastAPI()
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_headers=["*"],
    allow_methods=["*"],
)
# ---------- Rooms ----------
@app.get("/rooms", response_model=list[schemas.RoomOut])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(models.Room).all()


@app.get("/rooms/{room_id}", response_model=schemas.RoomOut)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room Not Found")
    return room


@app.get("/rooms/{room_id}/slots")
def get_slots(room_id: int, date: str, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room Not Found")

    booked = db.query(models.Booking.time_slot).filter(
        models.Booking.room_id == room_id,
        models.Booking.date == date,
    ).all()
    booked = {b[0] for b in booked}

    return {
        "date": date,
        "available": [s for s in schemas.ALLOWED_SLOTS if s not in booked],
    }


# ---------- Bookings ----------
@app.post("/bookings", response_model=schemas.BookingOut)
def create_booking(data: schemas.BookingCreate, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == data.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if data.players < room.min_player or data.players > room.max_player:
        raise HTTPException(
            status_code=400,
            detail=f"This room needs {room.min_player} to {room.max_player} players",
        )

    taken = db.query(models.Booking).filter(
        models.Booking.room_id == data.room_id,
        models.Booking.date == data.date,
        models.Booking.time_slot == data.time_slot,
    ).first()
    if taken:
        raise HTTPException(status_code=409, detail="This slot is already booked")

    booking = models.Booking(**data.model_dump())
    db.add(booking)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="This slot is already booked")
    try:
        send_booking_email(
            to_email=data.email,
            name=data.name,
            room_name=room.name,
            date=data.date,
            time_slot=data.time_slot,
            players=data.players,
            booking_id=booking.id,
        )
    except smtplib.SMTPRecipientsRefused:
        db.rollback()
        raise HTTPException(status_code=400, detail="This email address does not exist")
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=502,
            detail="Could not send the confirmation email, so the booking was not made",
        )
    db.commit()
    db.refresh(booking)
    return booking


@app.get("/bookings/{booking_id}", response_model=schemas.BookingOut)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@app.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"message": "Booking cancelled"}

# ---------- Reviews ----------
@app.post("/reviews", response_model=schemas.ReviewOut)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    data = models.Review(**review.model_dump())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data
@app.get("/reviews", response_model=list[schemas.ReviewOut])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(models.Review).order_by(models.Review.id.desc()).all() 