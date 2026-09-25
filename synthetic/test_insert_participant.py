from database import get_session

from generator.participant_generator import generate_participants

from models.participant_model import Participant



def insert_participants():


    session = get_session()


    print("Generating participants...")


    data = generate_participants(
        10000
    )


    print(
        len(data),
        "participants generated"
    )


    objects=[]


    for item in data:


        participant = Participant(
            **item
        )


        objects.append(
            participant
        )


    print("Inserting database...")


    session.add_all(
        objects
    )


    session.commit()


    print(
        "INSERT COMPLETE"
    )


    session.close()



if __name__ == "__main__":

    insert_participants()