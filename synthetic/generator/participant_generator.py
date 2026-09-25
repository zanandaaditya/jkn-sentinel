from faker import Faker
import random
import uuid
from datetime import datetime


fake = Faker("id_ID")



MEMBERSHIP = [
    "PBI",
    "PPU",
    "PBPU"
]



def generate_participants(total=10000):

    data=[]


    for i in range(total):

        participant = {

            "id":
            str(uuid.uuid4()),


            "participant_number":
            f"P{100000+i}",


            "name":
            fake.first_name() + " " + fake.last_name(),


            "gender":
            random.choice(
                [
                    "Laki-laki",
                    "Perempuan"
                ]
            ),


            "birth_date":
            fake.date_of_birth(
                minimum_age=18,
                maximum_age=70
            ),


            "membership_type":
            random.choice(
                MEMBERSHIP
            ),


            "status":
            "ACTIVE"

        }


        data.append(participant)


    return data