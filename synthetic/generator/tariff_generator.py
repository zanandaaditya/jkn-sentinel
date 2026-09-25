import uuid
import random



SERVICE_TYPES = [

    "PROCEDURE",
    "MEDICINE",
    "LABORATORY",
    "RADIOLOGY",
    "INPATIENT"

]


FACILITY_TYPES = [

    "FKTP",
    "FKRTL"

]


CLASSES = [

    "CLASS_I",
    "CLASS_II",
    "CLASS_III",
    "VIP"

]



def generate_tariffs(
        procedures,
        medicines,
        total=5000
):


    data=[]


    for i in range(total):


        service_type=random.choice(
            SERVICE_TYPES
        )


        procedure_id=None
        medicine_id=None



        if service_type=="MEDICINE":

            medicine=random.choice(
                medicines
            )

            medicine_id=medicine["id"]


            standard_cost=float(
                medicine["standard_price"]
            )



        else:

            procedure=random.choice(
                procedures
            )

            procedure_id=procedure["id"]


            standard_cost=float(
                procedure["standard_cost"]
            )



        # batas kewajaran biaya

        minimum_cost = (
            standard_cost * 0.8
        )


        maximum_cost = (
            standard_cost * 1.5
        )



        data.append({

            "id":
            str(uuid.uuid4()),


            "tariff_code":
            f"TAR-{i+1:06}",


            "service_type":
            service_type,


            "facility_type":
            random.choice(
                FACILITY_TYPES
            ),


            "tariff_class":
            random.choice(
                CLASSES
            ),

            "procedure_id":
            procedure_id,


            "medicine_id":
            medicine_id,


            "standard_cost":
            standard_cost,


            "minimum_cost":
            minimum_cost,


            "maximum_cost":
            maximum_cost,


            "year":
            2023

        })


    return data