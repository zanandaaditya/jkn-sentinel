from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Boolean,
    String
)

from sqlalchemy.dialects.postgresql import UUID

from models import Base



class ClaimDetail(Base):

    __tablename__ = "claim_details"


    id = Column(
        UUID,
        primary_key=True
    )


    claim_id = Column(
        UUID
    )


    procedure_id = Column(
        UUID
    )


    medicine_id = Column(
        UUID
    )


    quantity = Column(
        Integer
    )


    tariff_amount = Column(
        Numeric(14,2)
    )


    charged_amount = Column(
        Numeric(14,2)
    )


    anomaly_flag = Column(
        Boolean,
        default=False
    )


    procedure_match = Column(
        String(20)
    )


    medicine_match = Column(
        String(20)
    )


    detail_risk_score = Column(
        Integer,
        default=0
    )