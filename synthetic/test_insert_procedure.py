from database import get_session

from generator.procedure_generator import generate_procedures

from models.procedure_model import Procedure



def insert_procedures():


    session = get_session()


    print(
        "Generating procedures..."
    )


    data = generate_procedures(
        100
    )


    print(
        len(data),
        "procedures generated"
    )


    objects=[]


    for item in data:


        procedure = Procedure(
            **item
        )


        objects.append(
            procedure
        )



    print(
        "Inserting procedures..."
    )


    session.add_all(
        objects
    )


    session.commit()



    print(
        "PROCEDURE INSERT COMPLETE"
    )


    session.close()



if __name__ == "__main__":

    insert_procedures()