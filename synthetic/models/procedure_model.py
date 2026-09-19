from sqlalchemy import Column, String, Integer
from models import Base


class Procedure(Base):

    __tablename__ = "procedures"


    id = Column(
        String,
        primary_key=True
    )


    procedure_code = Column(
        String
    )


    name = Column(
        String
    )


    category = Column(
        String
    )


    standard_cost = Column(
        Integer
    )