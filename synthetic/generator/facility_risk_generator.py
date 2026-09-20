import uuid
import random



def calculate_complexity(facility):


    if facility["facility_type"] == "FKTP":

        return (
            "BASIC",
            random.randint(
                10,
                20
            )
        )


    else:

        if facility["class"] == "Type A":

            return (
                "HIGH",
                random.randint(
                    5,
                    15
                )
            )


        elif facility["class"] == "Type B":

            return (
                "ADVANCED",
                random.randint(
                    10,
                    25
                )
            )


        else:

            return (
                "MEDIUM",
                random.randint(
                    15,
                    30
                )
            )




def generate_facility_risk(facilities):


    data=[]


    for facility in facilities:


        complexity, score = calculate_complexity(
            facility
        )


        data.append({

            "id":
            str(uuid.uuid4()),


            "facility_id":
            facility["id"],


            "facility_type":
            facility["facility_type"],


            "ownership":
            facility["ownership"],


            "facility_class":
            facility["class"],


            "accreditation":
            facility["accreditation"],


            "bed_capacity":
            facility["bed_capacity"],


            "complexity_level":
            complexity,


            "risk_score":
            score

        })


    return data