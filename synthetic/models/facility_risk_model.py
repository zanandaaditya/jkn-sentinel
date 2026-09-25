from sqlalchemy import (
    Column,
    String,
    Integer
)

from sqlalchemy.dialects.postgresql import UUID

from models import Base



class FacilityRiskProfile(Base):

    __tablename__ = "facility_risk_profile"


    id = Column(
        UUID,
        primary_key=True
    )


    facility_id = Column(
        UUID
    )


    facility_type = Column(
        String(20)
    )


    ownership = Column(
        String(50)
    )


    facility_class = Column(
        "class",
        String(20)
    )


    accreditation = Column(
        String(50)
    )


    bed_capacity = Column(
        Integer
    )


    complexity_level = Column(
        String(20)
    )


    risk_score = Column(
        Integer
    )