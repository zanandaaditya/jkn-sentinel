from sqlalchemy import Column, String, ForeignKey
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


    name = Column(
        String
    )


    speciality = Column(
        String
    )


    provider_id = Column(
        String,
        ForeignKey(
            "providers.id"
        )
    )