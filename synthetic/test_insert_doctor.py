from database import get_session

from generator.doctor_generator import generate_doctors

from models.doctor_model import Doctor

from sqlalchemy import text



def insert_doctors():


    session=get_session()



    facilities=session.execute(
        text(
            """
            SELECT 
            id,
            facility_type

            FROM facilities
            """
        )
    ).fetchall()



    facility_list=[]


    for row in facilities:

        facility_list.append({

            "id":row[0],

            "facility_type":row[1]

        })



    print(
        len(facility_list),
        "facilities loaded"
    )



    doctors=generate_doctors(
        facility_list,
        50000
    )



    print(
        len(doctors),
        "doctors generated"
    )



    objects=[]


    for item in doctors:

        objects.append(
            Doctor(**item)
        )



    session.add_all(
        objects
    )


    session.commit()


    print(
        "DOCTOR INSERT COMPLETE"
    )


    session.close()



if __name__=="__main__":

    insert_doctors()