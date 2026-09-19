from sqlalchemy import Column, String, Date
from models import Base


class Participant(Base):

    __tablename__ = "participants"


    id = Column(
        String,
        primary_key=True
    )


    participant_number = Column(
        String
    )


    name = Column(
        String
    )


    gender = Column(
        String
    )


    birth_date = Column(
        Date
    )


    membership_type = Column(
        String
    )


    status = Column(
        String
    )