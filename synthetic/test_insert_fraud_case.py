from database import get_session

from sqlalchemy import text

import uuid



def create_fraud_cases():


    session = get_session()


    claims = session.execute(
        text(
            """
            SELECT

                id,
                risk_level,
                fraud_score

            FROM claims

            WHERE risk_level IN (
                'HIGH',
                'MEDIUM'
            )

            """
        )
    ).mappings().all()



    print(
        len(claims),
        "risky claims loaded"
    )



    cases=[]



    for claim in claims:



        if claim["risk_level"] == "HIGH":

            priority = "URGENT"


        else:

            priority = "NORMAL"



        cases.append({

            "id":
            str(uuid.uuid4()),


            "claim_id":
            claim["id"],


            "case_status":
            "NEW",


            "priority":
            priority,


            "assigned_to":
            None,


            "investigation_note":
            "Menunggu investigasi"

        })



    for item in cases:

        session.execute(
            text(
                """
                INSERT INTO fraud_cases

                (
                    id,
                    claim_id,
                    case_status,
                    priority,
                    assigned_to,
                    investigation_note
                )

                VALUES

                (
                    :id,
                    :claim_id,
                    :case_status,
                    :priority,
                    :assigned_to,
                    :investigation_note
                )

                """
            ),
            item
        )



    session.commit()


    print(
        len(cases),
        "fraud cases created"
    )


    session.close()




if __name__=="__main__":

    create_fraud_cases()