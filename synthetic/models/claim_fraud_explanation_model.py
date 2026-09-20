from sqlalchemy import (
    Column,
    String,
    Integer,
    Text
)

from sqlalchemy.dialects.postgresql import UUID

from models import Base



class ClaimFraudExplanation(Base):

    __tablename__ = "claim_fraud_explanation"


    id = Column(
        UUID,
        primary_key=True
    )


    claim_id = Column(
        UUID
    )


    factor = Column(
        String(50)
    )


    score = Column(
        Integer
    )


    severity = Column(
        String(20)
    )


    description = Column(
        Text
    )