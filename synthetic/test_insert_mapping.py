from database import get_session

from models.procedure_diagnosis_map_model import ProcedureDiagnosisMap

from generator.procedure_mapping_generator import generate_mapping

from sqlalchemy import text



def load_data(session):


    diagnosis = session.execute(
        text(
            """
            SELECT
            id,
            icd_code,
            name

            FROM diagnosis
            """
        )
    ).mappings().all()



    procedures = session.execute(
        text(
            """
            SELECT
            id,
            procedure_code,
            name

            FROM procedures
            """
        )
    ).mappings().all()



    return diagnosis, procedures




def insert_mapping():


    session=get_session()


    diagnosis, procedures = load_data(
        session
    )


    print(
        len(diagnosis),
        "diagnosis loaded"
    )


    print(
        len(procedures),
        "procedures loaded"
    )



    data = generate_mapping(
        diagnosis,
        procedures,
        10000
    )


    print(
        len(data),
        "mapping generated"
    )


    objects=[]


    for item in data:


        objects.append(
            ProcedureDiagnosisMap(
                **item
            )
        )


    session.add_all(
        objects
    )


    session.commit()


    print(
        "MAPPING INSERT COMPLETE"
    )


    session.close()



if __name__=="__main__":

    insert_mapping()