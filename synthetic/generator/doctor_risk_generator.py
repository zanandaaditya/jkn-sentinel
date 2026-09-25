import uuid
import random



def calculate_competency(doctor):


    if doctor["doctor_type"] == "DOKTER_UMUM":

        return (
            "BASIC",
            random.randint(
                10,
                25
            )
        )


    experience = doctor["experience_year"]


    if experience < 5:

        return (
            "INTERMEDIATE",
            random.randint(
                15,
                30
            )
        )


    elif experience < 15:

        return (
            "ADVANCED",
            random.randint(
                5,
                20
            )
        )


    else:

        return (
            "EXPERT",
            random.randint(
                3,
                15
            )
        )




def generate_doctor_risk(doctors):


    data=[]


    for doctor in doctors:


        competency, score = calculate_competency(
            doctor
        )


        data.append({

            "id":
            str(uuid.uuid4()),


            "doctor_id":
            doctor["id"],


            "speciality":
            doctor["speciality"],


            "doctor_type":
            doctor["doctor_type"],


            "experience_year":
            doctor["experience_year"],


            "competency_level":
            competency,


            "risk_score":
            score

        })


    return data