from database import get_session

from models.medicine_diagnosis_map_model import MedicineDiagnosisMap

from generator.medicine_mapping_generator import generate_medicine_mapping

from sqlalchemy import text



def load_data(session):


    diagnoses = session.execute(
        text(
            """
            SELECT
            id,
            icd_code,
            name

            FROM diagnosis
            """
        )
    ).mappings().all()



    medicines = session.execute(
        text(
            """
            SELECT
            id,
            medicine_code,
            name

            FROM medicines
            """
        )
    ).mappings().all()


    return diagnoses, medicines




def insert_mapping():


    session=get_session()


    diagnoses, medicines = load_data(
        session
    )


    print(
        len(diagnoses),
        "diagnosis loaded"
    )


    print(
        len(medicines),
        "medicines loaded"
    )



    data = generate_medicine_mapping(
        diagnoses,
        medicines,
        10000
    )


    print(
        len(data),
        "medicine mapping generated"
    )



    objects=[]


    for item in data:

        objects.append(
            MedicineDiagnosisMap(
                **item
            )
        )


    session.add_all(
        objects
    )


    session.commit()


    print(
        "MEDICINE MAPPING INSERT COMPLETE"
    )


    session.close()



if __name__=="__main__":

    insert_mapping()