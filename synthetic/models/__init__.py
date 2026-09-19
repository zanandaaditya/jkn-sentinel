from sqlalchemy.orm import declarative_base


Base = declarative_base()


from models.provider_model import Provider
from models.doctor_model import Doctor
from models.participant_model import Participant
from models.diagnosis_model import Diagnosis
from models.procedure_model import Procedure