import uuid


DIAGNOSIS_MASTER = [

    # ======================
    # RINGAN
    # ======================

    {
        "icd_code":"J06.9",
        "name":"Infeksi Saluran Pernapasan Akut",
        "category":"RESPIRASI",
        "severity_level":"RINGAN",
        "chronic_flag":False,
        "requires_referral":False
    },

    {
        "icd_code":"A09",
        "name":"Diare dan Gastroenteritis Infeksi",
        "category":"INFEKSI",
        "severity_level":"RINGAN",
        "chronic_flag":False,
        "requires_referral":False
    },


    {
        "icd_code":"H10.9",
        "name":"Konjungtivitis",
        "category":"MATA",
        "severity_level":"RINGAN",
        "chronic_flag":False,
        "requires_referral":False
    },


    # ======================
    # SEDANG
    # ======================

    {
        "icd_code":"E11.9",
        "name":"Diabetes Melitus Tipe 2",
        "category":"METABOLIK",
        "severity_level":"SEDANG",
        "chronic_flag":True,
        "requires_referral":True
    },


    {
        "icd_code":"I10",
        "name":"Hipertensi Esensial",
        "category":"KARDIOVASKULAR",
        "severity_level":"SEDANG",
        "chronic_flag":True,
        "requires_referral":True
    },


    {
        "icd_code":"J45.9",
        "name":"Asma",
        "category":"RESPIRASI",
        "severity_level":"SEDANG",
        "chronic_flag":True,
        "requires_referral":True
    },


    {
        "icd_code":"K21.9",
        "name":"Gastro Esophageal Reflux Disease",
        "category":"PENCERNAAN",
        "severity_level":"SEDANG",
        "chronic_flag":True,
        "requires_referral":False
    },


    # ======================
    # BERAT
    # ======================

    {
        "icd_code":"I63.9",
        "name":"Stroke",
        "category":"NEUROLOGI",
        "severity_level":"BERAT",
        "chronic_flag":True,
        "requires_referral":True
    },


    {
        "icd_code":"I21.9",
        "name":"Infark Miokard Akut",
        "category":"KARDIOVASKULAR",
        "severity_level":"BERAT",
        "chronic_flag":True,
        "requires_referral":True
    },


    {
        "icd_code":"N18.5",
        "name":"Penyakit Ginjal Kronis Stadium 5",
        "category":"GINJAL",
        "severity_level":"BERAT",
        "chronic_flag":True,
        "requires_referral":True
    },


    {
        "icd_code":"C34.9",
        "name":"Kanker Paru",
        "category":"ONKOLOGI",
        "severity_level":"BERAT",
        "chronic_flag":True,
        "requires_referral":True
    }

]



def generate_diagnosis(total=2000):


    data=[]


    for i in range(total):


        template = DIAGNOSIS_MASTER[
            i % len(DIAGNOSIS_MASTER)
        ]


        data.append({

            "id":
            str(uuid.uuid4()),


            "icd_code":
            template["icd_code"],


            "name":
            template["name"],


            "category":
            template["category"],


            "severity_level":
            template["severity_level"],


            "chronic_flag":
            template["chronic_flag"],


            "requires_referral":
            template["requires_referral"]

        })


    return data