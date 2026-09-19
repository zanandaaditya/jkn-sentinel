from sqlalchemy.orm import declarative_base


Base = declarative_base()


from models.facility_model import Facility
from models.doctor_model import Doctor
from models.diagnosis_model import Diagnosis
from models.procedure_model import Procedure
from models.medicine_model import Medicine
from models.tariff_model import Tariff

from models.claim_model import Claim
from models.claim_detail_model import ClaimDetail