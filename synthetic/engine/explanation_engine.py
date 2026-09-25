import uuid



def severity(score):


    if score >= 25:

        return "HIGH"


    elif score >= 10:

        return "MEDIUM"


    else:

        return "LOW"





def generate_explanations(
        claim_id,
        clinical_score,
        cost_score,
        facility_score,
        doctor_score
):


    results=[]



    if clinical_score > 0:

        results.append({

            "id":
            str(uuid.uuid4()),


            "claim_id":
            claim_id,


            "factor":
            "CLINICAL",


            "score":
            clinical_score,


            "severity":
            severity(
                clinical_score
            ),


            "description":
            "Procedure atau medicine tidak sesuai dengan diagnosis"

        })




    if cost_score > 0:

        results.append({

            "id":
            str(uuid.uuid4()),


            "claim_id":
            claim_id,


            "factor":
            "COST",


            "score":
            cost_score,


            "severity":
            severity(
                cost_score
            ),


            "description":
            "Nilai klaim memiliki indikasi anomali biaya dibanding tarif"

        })




    if facility_score >= 15:

        results.append({

            "id":
            str(uuid.uuid4()),


            "claim_id":
            claim_id,


            "factor":
            "FACILITY",


            "score":
            facility_score,


            "severity":
            severity(
                facility_score
            ),


            "description":
            "Kemampuan fasilitas tidak sesuai kompleksitas layanan"

        })




    if doctor_score > 8:

        results.append({

            "id":
            str(uuid.uuid4()),


            "claim_id":
            claim_id,


            "factor":
            "DOCTOR",


            "score":
            doctor_score,


            "severity":
            severity(
                doctor_score
            ),


            "description":
            "Profil kompetensi dokter memiliki risiko terhadap layanan"

        })



    return results