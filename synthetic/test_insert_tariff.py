from database import get_session

from models.tariff_model import Tariff

from generator.tariff_generator import generate_tariffs

from sqlalchemy import text




def load_data(session):


    procedures=session.execute(
        text(
            """
            SELECT
            id,
            standard_cost

            FROM procedures
            """
        )
    ).mappings().all()



    medicines=session.execute(
        text(
            """
            SELECT
            id,
            standard_price

            FROM medicines
            """
        )
    ).mappings().all()



    return procedures, medicines





def insert_tariff():


    session=get_session()



    procedures, medicines = load_data(
        session
    )


    print(
        len(procedures),
        "procedures loaded"
    )


    print(
        len(medicines),
        "medicines loaded"
    )



    data=generate_tariffs(
        procedures,
        medicines,
        5000
    )



    print(
        len(data),
        "tariffs generated"
    )



    objects=[]


    for item in data:


        objects.append(
            Tariff(**item)
        )



    session.add_all(
        objects
    )


    session.commit()


    print(
        "TARIFF INSERT COMPLETE"
    )


    session.close()



if __name__=="__main__":

    insert_tariff()