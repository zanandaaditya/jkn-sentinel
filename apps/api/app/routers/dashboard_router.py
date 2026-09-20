from fastapi import APIRouter

from sqlalchemy import text

from database import get_session


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/overview")
def overview():


    session = get_session()


    result = session.execute(
        text(
            """
            SELECT *
            FROM dashboard_overview
            """
        )
    ).mappings().first()


    session.close()


    return result





@router.get("/risk-distribution")
def risk_distribution():


    session=get_session()


    result=session.execute(
        text(
            """
            SELECT *
            FROM dashboard_risk_distribution
            """
        )
    ).mappings().all()


    session.close()


    return result





@router.get("/fraud-reasons")
def fraud_reason():


    session=get_session()


    result=session.execute(
        text(
            """
            SELECT *
            FROM dashboard_fraud_reason
            """
        )
    ).mappings().all()


    session.close()


    return result





@router.get("/high-risk")
def high_risk_claim():


    session=get_session()


    result = session.execute(
        text(
            """
            SELECT

                c.claim_code,

                c.fraud_score,

                c.risk_level,

                c.fraud_reason,


                d.name AS diagnosis,


                f.facility_name AS facility


            FROM claims c


            LEFT JOIN diagnosis d

            ON c.diagnosis_id = d.id


            LEFT JOIN facilities f

            ON c.facility_id = f.id



            WHERE c.risk_level IN (
                'HIGH',
                'MEDIUM'
            )


            ORDER BY

                c.fraud_score DESC


            LIMIT 20

            """
        )
    ).mappings().all()


    session.close()


    return result





@router.get("/facilities")
def facility_risk():


    session=get_session()


    result=session.execute(
        text(
            """
            SELECT *
            FROM dashboard_facility_risk
            LIMIT 20
            """
        )
    ).mappings().all()


    session.close()


    return result





@router.get("/doctors")
def doctor_risk():


    session=get_session()


    result=session.execute(
        text(
            """
            SELECT *
            FROM dashboard_doctor_risk
            LIMIT 20
            """
        )
    ).mappings().all()


    session.close()


    return result





@router.get("/cases")
def case_monitoring():


    session=get_session()


    result=session.execute(
        text(
            """
            SELECT *
            FROM dashboard_case_monitoring
            """
        )
    ).mappings().all()


    session.close()


    return result