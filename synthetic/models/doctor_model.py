from sqlalchemy import Column, String, Integer, ForeignKey
from models import Base


class Doctor(Base):

    __tablename__ = "doctors"


    id = Column(
        String,
        primary_key=True
    )


    doctor_code = Column(
        String
    )


    sip_number = Column(
        String
    )


    name = Column(
        String
    )


    speciality = Column(
        String
    )


    doctor_type = Column(
        String
    )


    facility_id = Column(
        String,
        ForeignKey(
            "facilities.id"
        )
    )


    experience_year = Column(
        Integer
    )


    status = Column(
        String
    )