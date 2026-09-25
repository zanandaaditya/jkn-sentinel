from sqlalchemy import Column, String, Boolean
from models import Base


class Diagnosis(Base):

    __tablename__ = "diagnosis"


    id = Column(
        String,
        primary_key=True
    )


    icd_code = Column(
        String(20)
    )


    name = Column(
        String(150)
    )


    category = Column(
        String(100)
    )


    severity_level = Column(
        String(20)
    )


    chronic_flag = Column(
        Boolean
    )


    requires_referral = Column(
        Boolean
    )