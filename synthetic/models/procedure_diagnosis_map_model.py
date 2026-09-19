from sqlalchemy import Column, String, Boolean, Integer
from models import Base


class ProcedureDiagnosisMap(Base):

    __tablename__ = "procedure_diagnosis_map"


    id = Column(
        String,
        primary_key=True
    )


    diagnosis_id = Column(
        String
    )


    procedure_id = Column(
        String
    )


    compatibility_level = Column(
        String(20)
    )


    is_recommended = Column(
        Boolean
    )


    risk_score = Column(
        Integer
    )