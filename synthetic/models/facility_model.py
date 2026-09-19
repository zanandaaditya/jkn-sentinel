from sqlalchemy import Column, String, Integer
from models import Base


class Facility(Base):

    __tablename__ = "facilities"


    id = Column(
        String,
        primary_key=True
    )


    facility_code = Column(
        String
    )


    facility_name = Column(
        String
    )


    facility_type = Column(
        String
    )


    ownership = Column(
        String
    )


    province = Column(
        String
    )


    city = Column(
        String
    )


    class_name = Column(
        "class",
        String
    )


    accreditation = Column(
        String
    )


    bed_capacity = Column(
        Integer
    )


    status = Column(
        String
    )