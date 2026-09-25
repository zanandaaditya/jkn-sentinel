from database import get_session

from models.claim_model import Claim

from generator.claim_generator import generate_claims

from sqlalchemy import text



def load_data(session):

    participants = session.execute(
        text(
            """
            SELECT id
            FROM participants
            """
        )
    ).mappings().all()


    facilities = session.execute(
        text(
            """
            SELECT id
            FROM facilities
            """
        )
    ).mappings().all()


    doctors = session.execute(
        text(
            """
            SELECT id
            FROM doctors
            """
        )
    ).mappings().all()


    diagnoses = session.execute(
        text(
            """
            SELECT id
            FROM diagnosis
            """
        )
    ).mappings().all()


    return (
        participants,
        facilities,
        doctors,
        diagnoses
    )



def insert_claim():


    session = get_session()


    participants, facilities, doctors, diagnoses = load_data(
        session
    )


    print(
        len(participants),
        "participants loaded"
    )

    print(
        len(facilities),
        "facilities loaded"
    )

    print(
        len(doctors),
        "doctors loaded"
    )

    print(
        len(diagnoses),
        "diagnosis loaded"
    )


    data = generate_claims(
        participants,
        facilities,
        doctors,
        diagnoses,
        1000
    )


    print(
        len(data),
        "claims generated"
    )


    objects=[]


    for item in data:

        objects.append(
            Claim(**item)
        )


    session.add_all(
        objects
    )


    session.commit()


    print(
        "CLAIM INSERT COMPLETE"
    )


    session.close()



if __name__=="__main__":

    insert_claim()