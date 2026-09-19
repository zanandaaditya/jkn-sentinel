import uuid
import random



MEDICINES=[

("Paracetamol","Analgesic"),
("Amlodipine","Cardiovascular"),
("Metformin","Diabetes"),
("Insulin","Diabetes"),
("Amoxicillin","Antibiotic"),
("Omeprazole","Digestive"),
("Atorvastatin","Cardiovascular"),
("Salbutamol","Respiratory"),
("Cefixime","Antibiotic"),
("Vitamin D","Supplement")

]



def generate_medicines(total=500):


    data=[]


    for i in range(total):


        if i < len(MEDICINES):

            name,category = MEDICINES[i]


        else:

            name = f"Synthetic Medicine {i}"

            category=random.choice(

                [
                    "Antibiotic",
                    "Cardiovascular",
                    "Supplement",
                    "Painkiller",
                    "Chronic Disease"
                ]

            )


        data.append({

            "id":
            str(uuid.uuid4()),


            "medicine_code":
            f"MED{i+1:04}",


            "name":
            name,


            "category":
            category,


            "standard_price":

            random.randint(
                5000,
                500000
            )


        })


    return data