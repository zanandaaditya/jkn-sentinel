from database import get_session

from models.claim_detail_model import ClaimDetail

from generator.claim_detail_generator import generate_claim_details

from sqlalchemy import text



def load_data(session):


    claims = session.execute(
        text(
            """
            SELECT
                id,
                diagnosis_id
            FROM claims
            """
        )
    ).mappings().all()



    procedures = session.execute(
        text(
            """
            SELECT
                id,
                standard_cost
            FROM procedures
            """
        )
    ).mappings().all()



    medicines = session.execute(
        text(
            """
            SELECT
                id,
                standard_price
            FROM medicines
            """
        )
    ).mappings().all()



    tariffs = session.execute(
        text(
            """
            SELECT
                id,
                standard_cost
            FROM tariff_master
            """
        )
    ).mappings().all()



    # ===============================
    # TAMBAHAN V2
    # PROCEDURE DIAGNOSIS MAPPING
    # ===============================

    procedure_maps = session.execute(
        text(
            """
            SELECT
                diagnosis_id,
                procedure_id,
                compatibility_level,
                risk_score
            FROM procedure_diagnosis_map
            """
        )
    ).mappings().all()



    # ===============================
    # TAMBAHAN V2
    # MEDICINE DIAGNOSIS MAPPING
    # ===============================

    medicine_maps = session.execute(
        text(
            """
            SELECT
                diagnosis_id,
                medicine_id,
                compatibility_level,
                risk_score
            FROM medicine_diagnosis_map
            """
        )
    ).mappings().all()



    return (
        claims,
        procedure_maps,
        medicine_maps,
        procedures,
        medicines,
        tariffs
    )




def insert_detail():


    session = get_session()



    (
        claims,
        procedure_maps,
        medicine_maps,
        procedures,
        medicines,
        tariffs

    ) = load_data(session)



    print(
        len(claims),
        "claims loaded"
    )


    print(
        len(procedure_maps),
        "procedure mappings loaded"
    )


    print(
        len(medicine_maps),
        "medicine mappings loaded"
    )



    data = generate_claim_details(
        claims,
        procedure_maps,
        medicine_maps,
        procedures,
        medicines,
        tariffs
    )



    print(
        len(data),
        "details generated"
    )



    objects = []



    for item in data:

        objects.append(
            ClaimDetail(**item)
        )



    session.add_all(
        objects
    )


    session.commit()



    print(
        "CLAIM DETAIL INSERT COMPLETE"
    )



    session.close()




if __name__ == "__main__":

    insert_detail()