import uuid
import random

from datetime import date, timedelta



STATUS = [
    "SUBMITTED",
    "VERIFIED",
    "PAID"
]



def generate_claims(
        participants,
        facilities,
        doctors,
        diagnoses,
        total=1000
):

    claims=[]


    for i in range(total):

        participant = random.choice(
            participants
        )


        facility = random.choice(
            facilities
        )


        doctor = random.choice(
            doctors
        )


        diagnosis = random.choice(
            diagnoses
        )


        is_fraud = random.random() < 0.05


        if is_fraud:

            fraud_score = random.randint(
                60,
                100
            )

            risk_level = "HIGH"


        else:

            fraud_score = random.randint(
                0,
                20
            )

            risk_level = "LOW"



        claims.append({

            "id":
            str(uuid.uuid4()),


            "claim_code":
            f"CLM-{i+1:08}",


            "facility_id":
            facility["id"],


            "participant_id":
            participant["id"],


            "doctor_id":
            doctor["id"],


            "diagnosis_id":
            diagnosis["id"],


            "service_date":
            date.today()
            -
            timedelta(
                days=random.randint(
                    0,
                    365
                )
            ),


            "claim_amount":
            random.randint(
                50000,
                5000000
            ),


            "fraud_score":
            fraud_score,


            "risk_level":
            risk_level,


            "status":
            random.choice(
                STATUS
            )

        })


    return claims