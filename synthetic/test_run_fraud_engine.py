from database import get_session

from sqlalchemy import text
from engine.explanation_engine import generate_explanations

from models.claim_fraud_explanation_model import ClaimFraudExplanation

from engine.fraud_scoring_engine import (
    calculate_clinical_score,
    calculate_cost_score,
    calculate_facility_score,
    calculate_doctor_score,
    determine_level,
    generate_reason
)



def run_engine():


    session = get_session()


    claims = session.execute(
        text(
            """
            SELECT
                id,
                facility_id,
                doctor_id

            FROM claims
            """
        )
    ).mappings().all()



    print(
        len(claims),
        "claims loaded"
    )



    processed = 0



    for claim in claims:



        # ==========================
        # CLAIM DETAILS
        # ==========================


        details = session.execute(
            text(
                """
                SELECT

                    procedure_match,
                    medicine_match,
                    anomaly_flag

                FROM claim_details

                WHERE claim_id=:claim_id

                """
            ),
            {
                "claim_id":
                claim["id"]
            }
        ).mappings().all()



        clinical_score = calculate_clinical_score(
            details
        )


        cost_score = calculate_cost_score(
            details
        )



        # ==========================
        # FACILITY RISK
        # ==========================


        facility_risk = session.execute(
            text(
                """
                SELECT
                    risk_score

                FROM facility_risk_profile

                WHERE facility_id=:facility_id

                """
            ),
            {
                "facility_id":
                claim["facility_id"]
            }
        ).mappings().first()



        facility_score = calculate_facility_score(
            facility_risk
        )



        # ==========================
        # DOCTOR RISK
        # ==========================


        doctor_risk = session.execute(
            text(
                """
                SELECT
                    risk_score

                FROM doctor_risk_profile

                WHERE doctor_id=:doctor_id

                """
            ),
            {
                "doctor_id":
                claim["doctor_id"]
            }
        ).mappings().first()



        doctor_score = calculate_doctor_score(
            doctor_risk
        )



        # ==========================
        # FINAL SCORE
        # ==========================


        total_score = (

            clinical_score
            +
            cost_score
            +
            facility_score
            +
            doctor_score

        )


        total_score = min(
            total_score,
            100
        )



        level = determine_level(
            total_score
        )



        reasons = generate_reason(
            clinical_score,
            cost_score,
            facility_score,
            doctor_score
        )



        reason_text = "; ".join(
            reasons
        )



        session.execute(
            text(
                """
                UPDATE claims

                SET

                    fraud_score=:score,

                    risk_level=:level,

                    fraud_reason=:reason


                WHERE id=:id

                """
            ),
            {

                "score":
                total_score,


                "level":
                level,


                "reason":
                reason_text,


                "id":
                claim["id"]

            }
        )


        # =====================================
        # INSERT FRAUD EXPLANATION
        # =====================================

        explanations = generate_explanations(
            claim["id"],
            clinical_score,
            cost_score,
            facility_score,
            doctor_score
        )


        for exp in explanations:

            session.add(
                ClaimFraudExplanation(**exp)
            )



        processed += 1



    session.commit()


    print(
        processed,
        "claims scored"
    )


    session.close()




if __name__=="__main__":

    run_engine()