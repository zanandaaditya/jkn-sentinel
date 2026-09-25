from sqlalchemy import Column, String, Numeric, Integer
from models import Base


class Tariff(Base):

    __tablename__="tariff_master"


    id = Column(
        String,
        primary_key=True
    )


    tariff_code = Column(
        String(50)
    )


    service_type = Column(
        String(50)
    )


    facility_type = Column(
        String(20)
    )


    tariff_class = Column(
        "class",
        String(20)
    )


    procedure_id = Column(
        String
    )


    medicine_id = Column(
        String
    )


    standard_cost = Column(
        Numeric(14,2)
    )


    minimum_cost = Column(
        Numeric(14,2)
    )


    maximum_cost = Column(
        Numeric(14,2)
    )


    year = Column(
        Integer
    )