from database import get_session

from generator.provider_generator import generate_providers

from models.provider_model import Provider
from models.doctor_model import Doctor


def insert_providers():


    session = get_session()


    print("Generating providers...")


    data = generate_providers(
        500
    )


    print(
        len(data),
        "providers generated"
    )


    objects=[]


    for item in data:


        provider = Provider(
            **item
        )


        objects.append(
            provider
        )


    print(
        "Inserting providers..."
    )


    session.add_all(
        objects
    )


    session.commit()


    print(
        "PROVIDER INSERT COMPLETE"
    )


    session.close()



if __name__ == "__main__":

    insert_providers()