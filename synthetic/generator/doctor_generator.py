from faker import Faker
import uuid
import random


fake=Faker("id_ID")



SPECIALITY=[

"Umum",
"Bedah",
"Anak",
"Penyakit Dalam",
"Jantung",
"Mata",
"Orthopedi"

]



def generate_doctors(providers,total=5000):


    data=[]


    for i in range(total):


        doctor={


        "id":
        str(uuid.uuid4()),


        "doctor_code":
        f"DOC{i+1:05}",


        "name":
        fake.name(),


        "speciality":
        random.choice(
            SPECIALITY
        ),


        "provider_id":
        random.choice(
            providers
        )["id"]


        }


        data.append(doctor)


    return data