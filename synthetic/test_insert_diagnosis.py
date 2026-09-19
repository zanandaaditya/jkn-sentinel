from database import get_session

from generator.diagnosis_generator import generate_diagnosis

from models.diagnosis_model import Diagnosis



def insert_diagnosis():


    session = get_session()


    print(
        "Generating diagnosis..."
    )


    data = generate_diagnosis(
        200
    )


    print(
        len(data),
        "diagnosis generated"
    )


    objects=[]


    for item in data:


        diagnosis = Diagnosis(
            **item
        )


        objects.append(
            diagnosis
        )



    print(
        "Inserting diagnosis..."
    )


    session.add_all(
        objects
    )


    session.commit()


    print(
        "DIAGNOSIS INSERT COMPLETE"
    )


    session.close()



if __name__ == "__main__":

    insert_diagnosis()