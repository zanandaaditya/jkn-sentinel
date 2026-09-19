from database import get_session

from generator.doctor_generator import generate_doctors

from models.doctor_model import Doctor


from sqlalchemy import text



def insert_doctors():


    session = get_session()


    print(
        "Loading providers..."
    )


    providers = session.execute(
        text(
            "SELECT id FROM providers"
        )
    ).fetchall()



    provider_list = [

        {
            "id": row[0]
        }

        for row in providers

    ]



    print(
        len(provider_list),
        "providers loaded"
    )



    print(
        "Generating doctors..."
    )



    data = generate_doctors(
        provider_list,
        5000
    )



    print(
        len(data),
        "doctors generated"
    )



    objects=[]



    for item in data:


        doctor = Doctor(
            **item
        )


        objects.append(
            doctor
        )



    print(
        "Inserting doctors..."
    )



    session.add_all(
        objects
    )


    session.commit()



    print(
        "DOCTOR INSERT COMPLETE"
    )


    session.close()



if __name__ == "__main__":

    insert_doctors()