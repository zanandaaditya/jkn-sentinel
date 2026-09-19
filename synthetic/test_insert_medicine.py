from database import get_session

from models.medicine_model import Medicine

from generator.medicine_generator import generate_medicines



def insert_medicine():

    session=get_session()


    data=generate_medicines(
        500
    )


    print(
        len(data),
        "medicines generated"
    )


    objects=[]


    for item in data:

        objects.append(
            Medicine(**item)
        )


    session.add_all(objects)

    session.commit()


    print(
        "MEDICINE INSERT COMPLETE"
    )


    session.close()



if __name__=="__main__":

    insert_medicine()