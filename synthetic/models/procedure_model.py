from sqlalchemy import Column, String, Boolean, Numeric
from models import Base


class Procedure(Base):

    __tablename__="procedures"


    id = Column(
        String,
        primary_key=True
    )


    procedure_code = Column(
        String(50)
    )


    name = Column(
        String(150)
    )


    category = Column(
        String(100)
    )


    level = Column(
        String(20)
    )


    requires_specialist = Column(
        Boolean
    )


    severity_match = Column(
        String(20)
    )


    facility_type = Column(
        String(20)
    )


    standard_cost = Column(
        Numeric(14,2)
    )