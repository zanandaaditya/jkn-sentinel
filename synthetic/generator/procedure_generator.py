import uuid
import random


PROCEDURE_MASTER = [


{
"name":
"Pemeriksaan Darah Lengkap",

"category":
"LABORATORY",

"level":
"DASAR",

"requires_specialist":
False,

"severity_match":
"RINGAN",

"facility_type":
"FKTP",

"standard_cost":
75000
},



{
"name":
"Pemeriksaan Elektrokardiogram",

"category":
"DIAGNOSTIC",

"level":
"MENENGAH",

"requires_specialist":
False,

"severity_match":
"SEDANG",

"facility_type":
"FKTP",

"standard_cost":
250000
},



{
"name":
"CT Scan Kepala",

"category":
"RADIOLOGY",

"level":
"LANJUT",

"requires_specialist":
True,

"severity_match":
"BERAT",

"facility_type":
"FKRTL",

"standard_cost":
1500000
},



{
"name":
"Hemodialisis",

"category":
"THERAPY",

"level":
"KHUSUS",

"requires_specialist":
True,

"severity_match":
"BERAT",

"facility_type":
"FKRTL",

"standard_cost":
1000000
},



{
"name":
"Operasi Apendiktomi",

"category":
"SURGERY",

"level":
"LANJUT",

"requires_specialist":
True,

"severity_match":
"BERAT",

"facility_type":
"FKRTL",

"standard_cost":
8000000
},



{
"name":
"Rawat Inap Kelas III",

"category":
"INPATIENT",

"level":
"MENENGAH",

"requires_specialist":
False,

"severity_match":
"SEDANG",

"facility_type":
"FKRTL",

"standard_cost":
500000
},



{
"name":
"Pelayanan Gawat Darurat",

"category":
"EMERGENCY",

"level":
"LANJUT",

"requires_specialist":
True,

"severity_match":
"BERAT",

"facility_type":
"FKRTL",

"standard_cost":
750000
},



{
"name":
"Fisioterapi",

"category":
"REHABILITATION",

"level":
"DASAR",

"requires_specialist":
False,

"severity_match":
"SEDANG",

"facility_type":
"FKTP",

"standard_cost":
150000
}


]



def generate_procedures(total=1000):

    data=[]


    for i in range(total):

        template=random.choice(
            PROCEDURE_MASTER
        )


        data.append({

            "id":
            str(uuid.uuid4()),


            "procedure_code":
            f"PROC-{i+1:06}",


            "name":
            template["name"],


            "category":
            template["category"],


            "level":
            template["level"],


            "requires_specialist":
            template["requires_specialist"],


            "severity_match":
            template["severity_match"],


            "facility_type":
            template["facility_type"],


            "standard_cost":
            template["standard_cost"]

        })


    return data