import uuid
import random


MEDICINE_MASTER = [

{
"name":"Paracetamol 500 mg",
"category":"ANALGESIC",
"form":"TABLET",
"unit":"TABLET",
"price":500,
"chronic":False,
"severity":"RINGAN",
"match":False
},


{
"name":"Amoxicillin 500 mg",
"category":"ANTIBIOTIC",
"form":"CAPSULE",
"unit":"KAPSUL",
"price":1500,
"chronic":False,
"severity":"SEDANG",
"match":True
},


{
"name":"Metformin 500 mg",
"category":"ANTIDIABETIC",
"form":"TABLET",
"unit":"TABLET",
"price":1000,
"chronic":True,
"severity":"SEDANG",
"match":True
},


{
"name":"Amlodipine 10 mg",
"category":"ANTIHYPERTENSIVE",
"form":"TABLET",
"unit":"TABLET",
"price":2000,
"chronic":True,
"severity":"SEDANG",
"match":True
},


{
"name":"Salbutamol",
"category":"RESPIRATORY",
"form":"TABLET",
"unit":"TABLET",
"price":1000,
"chronic":False,
"severity":"SEDANG",
"match":True
},


{
"name":"Insulin",
"category":"ANTIDIABETIC",
"form":"INJECTION",
"unit":"VIAL",
"price":75000,
"chronic":True,
"severity":"BERAT",
"match":True
},


{
"name":"Epoetin Alfa",
"category":"RENAL",
"form":"INJECTION",
"unit":"VIAL",
"price":250000,
"chronic":True,
"severity":"BERAT",
"match":True
},


{
"name":"Obat Kemoterapi",
"category":"ONCOLOGY",
"form":"INJECTION",
"unit":"VIAL",
"price":500000,
"chronic":True,
"severity":"BERAT",
"match":True
},


{
"name":"Omeprazole",
"category":"GASTRO",
"form":"CAPSULE",
"unit":"KAPSUL",
"price":1500,
"chronic":False,
"severity":"RINGAN",
"match":False
}

]



def generate_medicines(total=500):

    data=[]


    for i in range(total):

        item=random.choice(
            MEDICINE_MASTER
        )


        data.append({

            "id":
            str(uuid.uuid4()),


            "medicine_code":
            f"MED-{i+1:06}",


            "name":
            item["name"],


            "category":
            item["category"],


            "form":
            item["form"],


            "unit":
            item["unit"],


            "standard_price":
            item["price"],


            "chronic_flag":
            item["chronic"],


            "severity_match":
            item["severity"],


            "requires_diagnosis_match":
            item["match"]

        })


    return data