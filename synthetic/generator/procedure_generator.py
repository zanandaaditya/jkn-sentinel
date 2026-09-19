import uuid
import random



PROCEDURE_LIST = [

("Laboratory Test","Laboratory"),
("CT Scan","Radiology"),
("MRI","Radiology"),
("Appendectomy","Surgery"),
("Heart Surgery","Surgery"),
("Hemodialysis","Renal"),
("Chemotherapy","Oncology"),
("Radiotherapy","Oncology"),
("Ultrasound","Radiology"),
("Medical Check Up","General"),
("Vaccination","Preventive")

]



def generate_procedures(total=100):

    data=[]


    for i in range(total):


        if i < len(PROCEDURE_LIST):

            name,category = PROCEDURE_LIST[i]


        else:

            name = f"Medical Procedure {i}"

            category = random.choice(
                [
                    "Surgery",
                    "Laboratory",
                    "Radiology",
                    "General"
                ]
            )


        data.append({

            "id":
            str(uuid.uuid4()),


            "procedure_code":
            f"PROC{i+1:04}",


            "name":
            name,


            "category":
            category,


            "standard_cost":
            random.randint(
                100000,
                15000000
            )

        })


    return data