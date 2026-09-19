import uuid
import random


DISEASES = [

("I10","Hypertension","Cardiovascular"),
("E11","Diabetes Mellitus","Endocrine"),
("J18","Pneumonia","Respiratory"),
("K35","Appendicitis","Digestive"),
("I21","Acute Myocardial Infarction","Cardiovascular"),
("N18","Chronic Kidney Disease","Renal"),
("K29","Gastritis","Digestive"),
("A09","Gastroenteritis","Digestive"),
("J45","Asthma","Respiratory"),
("C50","Breast Cancer","Oncology"),
("C34","Lung Cancer","Oncology"),
("M54","Back Pain","Musculoskeletal"),
("G43","Migraine","Neurology"),
("H25","Cataract","Eye"),
("F32","Depression","Mental Health")

]


def generate_diagnosis(total=200):

    data=[]


    for i in range(total):

        if i < len(DISEASES):

            code,name,category = DISEASES[i]

        else:

            code = f"X{i+100}"

            name = f"Synthetic Disease {i}"

            category = random.choice(
                [
                    "Cardiovascular",
                    "Respiratory",
                    "Digestive",
                    "Neurology",
                    "General"
                ]
            )


        data.append({

            "id":
            str(uuid.uuid4()),


            "icd_code":
            code,


            "name":
            name,


            "category":
            category

        })


    return data