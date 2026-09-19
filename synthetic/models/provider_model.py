from sqlalchemy import Column, String
from models import Base


class Provider(Base):

    __tablename__ = "providers"


    id = Column(
        String,
        primary_key=True
    )


    provider_code = Column(
        String
    )


    provider_name = Column(
        String
    )


    provider_type = Column(
        String
    )


    province = Column(
        String
    )


    class_name = Column(
        "class",
        String
    )


    status = Column(
        String
    )