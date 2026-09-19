import uuid
import random



MATCH_SCORE = {

    "DIRECT":0,

    "SUPPORTING":10,

    "LIMITED":30,

    "UNMATCHED":50

}



def calculate_risk(
        procedure_match,
        medicine_match
):


    score = 0


    score += MATCH_SCORE.get(
        procedure_match,
        50
    )


    score += MATCH_SCORE.get(
        medicine_match,
        50
    )


    return min(
        score,
        100
    )





def generate_claim_details(
        claims,
        procedure_maps,
        medicine_maps,
        procedures,
        medicines,
        tariffs
):


    details=[]


    # index mapping agar cepat

    procedure_by_diag={}


    for item in procedure_maps:

        procedure_by_diag.setdefault(
            str(item["diagnosis_id"]),
            []
        ).append(item)



    medicine_by_diag={}


    for item in medicine_maps:

        medicine_by_diag.setdefault(
            str(item["diagnosis_id"]),
            []
        ).append(item)





    for claim in claims:


        diagnosis_id=str(
            claim["diagnosis_id"]
        )


        # =====================
        # PROCEDURE SELECTION
        # =====================


        available_procedure = (
            procedure_by_diag.get(
                diagnosis_id,
                []
            )
        )


        if available_procedure:


            mapping=random.choice(
                available_procedure
            )


            procedure_id=mapping["procedure_id"]


            procedure_match=(
                mapping["compatibility_level"]
            )


        else:


            procedure=random.choice(
                procedures
            )


            procedure_id=procedure["id"]


            procedure_match="UNMATCHED"




        # =====================
        # MEDICINE SELECTION
        # =====================


        available_medicine = (
            medicine_by_diag.get(
                diagnosis_id,
                []
            )
        )


        if available_medicine:


            mapping=random.choice(
                available_medicine
            )


            medicine_id=mapping["medicine_id"]


            medicine_match=(
                mapping["compatibility_level"]
            )


        else:


            medicine=random.choice(
                medicines
            )


            medicine_id=medicine["id"]


            medicine_match="UNMATCHED"





        tariff=random.choice(
            tariffs
        )


        tariff_amount=float(
            tariff["standard_cost"]
        )



        # sebagian kecil dibuat overbilling


        if random.random() < 0.05:


            charged_amount = (
                tariff_amount *
                random.randint(
                    3,
                    8
                )
            )


            anomaly=True


        else:


            charged_amount = (
                tariff_amount *
                random.uniform(
                    0.9,
                    1.2
                )
            )


            anomaly=False




        risk_score = calculate_risk(
            procedure_match,
            medicine_match
        )


        if anomaly:

            risk_score +=30


        risk_score=min(
            risk_score,
            100
        )




        details.append({

            "id":
            str(uuid.uuid4()),


            "claim_id":
            claim["id"],


            "procedure_id":
            procedure_id,


            "medicine_id":
            medicine_id,


            "quantity":
            random.randint(
                1,
                5
            ),


            "tariff_amount":
            tariff_amount,


            "charged_amount":
            charged_amount,


            "anomaly_flag":
            anomaly,


            "procedure_match":
            procedure_match,


            "medicine_match":
            medicine_match,


            "detail_risk_score":
            risk_score

        })


    return details