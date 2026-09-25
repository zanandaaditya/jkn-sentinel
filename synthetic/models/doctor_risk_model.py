from sqlalchemy import (
    Column,
    String,
    Integer
)

from sqlalchemy.dialects.postgresql import UUID

from models import Base



class DoctorRiskProfile(Base):

    __tablename__ = "doctor_risk_profile"


    id = Column(
        UUID,
        primary_key=True
    )


    doctor_id = Column(
        UUID
    )


    speciality = Column(
        String(100)
    )


    doctor_type = Column(
        String(50)
    )


    experience_year = Column(
        Integer
    )


    competency_level = Column(
        String(20)
    )


    risk_score = Column(
        Integer
    )