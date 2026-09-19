from sqlalchemy import Column, String
from models import Base


class Diagnosis(Base):

    __tablename__ = "diagnosis"


    id = Column(
        String,
        primary_key=True
    )


    icd_code = Column(
        String
    )


    name = Column(
        String
    )


    category = Column(
        String
    )