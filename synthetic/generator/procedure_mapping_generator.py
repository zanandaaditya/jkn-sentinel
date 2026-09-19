import uuid
import random


COMPATIBILITY_RULES = [

    {
        "level": "DIRECT",
        "recommended": True,
        "risk": 0
    },

    {
        "level": "SUPPORTING",
        "recommended": True,
        "risk": 10
    },

    {
        "level": "LIMITED",
        "recommended": False,
        "risk": 30
    },

    {
        "level": "UNMATCHED",
        "recommended": False,
        "risk": 80
    }

]



def generate_mapping(
        diagnoses,
        procedures,
        total=10000
):

    data=[]


    for i in range(total):


        diagnosis = random.choice(
            diagnoses
        )


        procedure = random.choice(
            procedures
        )


        # Buat distribusi realistis
        rand = random.random()


        if rand < 0.70:

            compatibility = COMPATIBILITY_RULES[0]


        elif rand < 0.90:

            compatibility = COMPATIBILITY_RULES[1]


        elif rand < 0.97:

            compatibility = COMPATIBILITY_RULES[2]


        else:

            compatibility = COMPATIBILITY_RULES[3]



        data.append({

            "id":
            str(uuid.uuid4()),


            "diagnosis_id":
            diagnosis["id"],


            "procedure_id":
            procedure["id"],


            "compatibility_level":
            compatibility["level"],


            "is_recommended":
            compatibility["recommended"],


            "risk_score":
            compatibility["risk"]

        })


    return data