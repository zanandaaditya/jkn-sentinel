from database import get_session

from models.diagnosis_model import Diagnosis

from generator.diagnosis_generator import generate_diagnosis



def insert_diagnosis():

    session=get_session()


    data = generate_diagnosis(
        2000
    )


    print(
        len(data),
        "diagnosis generated"
    )


    objects=[]


    for item in data:

        objects.append(
            Diagnosis(**item)
        )


    session.add_all(objects)

    session.commit()


    print(
        "DIAGNOSIS INSERT COMPLETE"
    )


    session.close()



if __name__=="__main__":
    insert_diagnosis()