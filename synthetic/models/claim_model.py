from sqlalchemy import (
    Column,
    String,
    Numeric,
    Integer,
    Date
)

from sqlalchemy.dialects.postgresql import UUID

from models import Base


class Claim(Base):

    __tablename__ = "claims"


    id = Column(
        UUID,
        primary_key=True
    )


    claim_code = Column(
        String(50),
        nullable=False,
        unique=True
    )


    facility_id = Column(
        UUID
    )


    participant_id = Column(
        UUID
    )


    doctor_id = Column(
        UUID
    )


    diagnosis_id = Column(
        UUID
    )


    service_date = Column(
        Date
    )


    claim_amount = Column(
        Numeric
    )


    fraud_score = Column(
        Integer,
        default=0
    )


    risk_level = Column(
        String(20)
    )


    status = Column(
        String(50)
    )