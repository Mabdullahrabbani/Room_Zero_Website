from database import SessionLocal
from models import Room


def seed_rooms():
    rooms = [
        Room(name="Victorian Detective Mystery", difficulty="Easy", price=30,
             min_player=1, max_player=2,
             description="Sherlock style investigation with hidden journals, coded phones, and secret compartments.",
             image="images/victorian.png"),
        Room(name="Haunted Mansion Escape", difficulty="Medium", price=35,
             min_player=1, max_player=4,
             description="Mysterious flickering lights, talking portraits, and séance table clues.",
             image="images/haunted.png"),
        Room(name="Spaceship Crash Landing", difficulty="Hard", price=40,
             min_player=1, max_player=6,
             description="Repair control panels, follow AI commands, and escape before the sun explodes.",
             image="images/spaceship.png"),
        Room(name="Time Traveler's Lab", difficulty="Extreme", price=45,
             min_player=1, max_player=8,
             description="Jump between timelines and solve puzzles in different eras.",
             image="images/lab.png"),
        Room(name="Floor Zero", difficulty="Customizable on spot", price=None,
             min_player=1, max_player=12,
             description="The experience resets. Define your own impossibility. Your unique challenge starts here, built from the ground up to test your limits.",
             image="images/floorzero.png"),
        Room(name="The Forgotten Facility", difficulty="Almost Impossible", price=55,
             min_player=8, max_player=12,
             description="A huge research facility with teamwork puzzles, power restoration, hidden passages, and optional Hunter Mode (1-4 hunters).",
             image="images/facility.png"),
    ]

    db = SessionLocal()
    try:
        if db.query(Room).count() == 0:
            db.add_all(rooms)
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    from database import engine, Base
    Base.metadata.create_all(bind=engine)
    seed_rooms()
