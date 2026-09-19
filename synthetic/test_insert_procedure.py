from database import get_session

from models.procedure_model import Procedure

from generator.procedure_generator import generate_procedures



def insert_procedure():

    session=get_session()


    data=generate_procedures(
        1000
    )


    print(
        len(data),
        "procedures generated"
    )


    objects=[]


    for item in data:

        objects.append(
            Procedure(**item)
        )


    session.add_all(objects)

    session.commit()


    print(
        "PROCEDURE INSERT COMPLETE"
    )


    session.close()



if __name__=="__main__":
    insert_procedure()