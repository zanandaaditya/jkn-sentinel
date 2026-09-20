def calculate_clinical_score(details):


    score = 0


    for detail in details:


        if detail["procedure_match"] == "UNMATCHED":

            score += 25


        elif detail["procedure_match"] == "LIMITED":

            score += 15



        if detail["medicine_match"] == "UNMATCHED":

            score += 25


        elif detail["medicine_match"] == "LIMITED":

            score += 15



    return min(score,40)





def calculate_cost_score(details):


    score=0


    for detail in details:


        if detail["anomaly_flag"]:

            score += 25


    return min(score,25)





def calculate_facility_score(
        facility_risk
):


    if facility_risk is None:

        return 0



    return min(
        facility_risk["risk_score"],
        20
    )





def calculate_doctor_score(
        doctor_risk
):


    if doctor_risk is None:

        return 0



    return min(
        doctor_risk["risk_score"],
        10
    )





def determine_level(score):


    if score >= 80:

        return "HIGH"


    elif score >= 50:

        return "MEDIUM"


    else:

        return "LOW"





def generate_reason(
        clinical,
        cost,
        facility,
        doctor
):


    reasons=[]


    if clinical >= 25:

        reasons.append(
            "Clinical mismatch procedure/medicine"
        )


    if cost >=20:

        reasons.append(
            "Claim cost anomaly"
        )


    if facility >=15:

        reasons.append(
            "Facility capability risk"
        )


    if doctor >=8:

        reasons.append(
            "Doctor competency risk"
        )


    return reasons