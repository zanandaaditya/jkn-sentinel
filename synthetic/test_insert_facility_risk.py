from database import get_session

from models.facility_risk_model import FacilityRiskProfile

from generator.facility_risk_generator import generate_facility_risk

from sqlalchemy import text



def insert_facility_risk():


    session=get_session()


    facilities=session.execute(
        text(
            """
            SELECT
                id,
                facility_type,
                ownership,
                class,
                accreditation,
                bed_capacity

            FROM facilities
            """
        )
    ).mappings().all()



    print(
        len(facilities),
        "facilities loaded"
    )



    data=generate_facility_risk(
        facilities
    )


    print(
        len(data),
        "risk profiles generated"
    )



    objects=[]


    for item in data:

        objects.append(
            FacilityRiskProfile(**item)
        )



    session.add_all(
        objects
    )


    session.commit()


    print(
        "FACILITY RISK INSERT COMPLETE"
    )


    session.close()



if __name__=="__main__":

    insert_facility_risk()