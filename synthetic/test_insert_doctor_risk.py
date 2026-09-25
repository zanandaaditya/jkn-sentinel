from database import get_session

from models.doctor_risk_model import DoctorRiskProfile

from generator.doctor_risk_generator import generate_doctor_risk

from sqlalchemy import text



def insert_doctor_risk():


    session=get_session()


    doctors=session.execute(
        text(
            """
            SELECT
                id,
                speciality,
                doctor_type,
                experience_year

            FROM doctors
            """
        )
    ).mappings().all()



    print(
        len(doctors),
        "doctors loaded"
    )



    data=generate_doctor_risk(
        doctors
    )



    print(
        len(data),
        "doctor risk generated"
    )



    objects=[]


    for item in data:

        objects.append(
            DoctorRiskProfile(**item)
        )


    session.add_all(
        objects
    )


    session.commit()


    print(
        "DOCTOR RISK INSERT COMPLETE"
    )


    session.close()



if __name__=="__main__":

    insert_doctor_risk()