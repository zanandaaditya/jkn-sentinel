import uuid


DIAGNOSIS_MASTER = [

# ==================================================
# INFEKSI
# ==================================================

{
"icd_code":"A09",
"name":"Diare dan Gastroenteritis Infeksi",
"category":"INFEKSI",
"severity_level":"RINGAN",
"chronic_flag":False,
"requires_referral":False
},

{
"icd_code":"A41.9",
"name":"Sepsis Tidak Spesifik",
"category":"INFEKSI",
"severity_level":"BERAT",
"chronic_flag":False,
"requires_referral":True
},

{
"icd_code":"B20",
"name":"Penyakit HIV",
"category":"INFEKSI",
"severity_level":"BERAT",
"chronic_flag":True,
"requires_referral":True
},

{
"icd_code":"A90",
"name":"Demam Berdarah Dengue",
"category":"INFEKSI",
"severity_level":"BERAT",
"chronic_flag":False,
"requires_referral":True
},


# ==================================================
# RESPIRASI
# ==================================================

{
"icd_code":"J06.9",
"name":"Infeksi Saluran Pernapasan Akut",
"category":"RESPIRASI",
"severity_level":"RINGAN",
"chronic_flag":False,
"requires_referral":False
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
"icd_code":"J18.9",
"name":"Pneumonia Tidak Spesifik",
"category":"RESPIRASI",
"severity_level":"BERAT",
"chronic_flag":False,
"requires_referral":True
},

{
"icd_code":"J44.9",
"name":"Penyakit Paru Obstruktif Kronik",
"category":"RESPIRASI",
"severity_level":"BERAT",
"chronic_flag":True,
"requires_referral":True
},


# ==================================================
# KARDIOVASKULAR
# ==================================================

{
"icd_code":"I10",
"name":"Hipertensi Esensial",
"category":"KARDIOVASKULAR",
"severity_level":"SEDANG",
"chronic_flag":True,
"requires_referral":True
},

{
"icd_code":"I25.9",
"name":"Penyakit Jantung Iskemik",
"category":"KARDIOVASKULAR",
"severity_level":"BERAT",
"chronic_flag":True,
"requires_referral":True
},

{
"icd_code":"I21.9",
"name":"Infark Miokard Akut",
"category":"KARDIOVASKULAR",
"severity_level":"BERAT",
"chronic_flag":False,
"requires_referral":True
},

{
"icd_code":"I50.9",
"name":"Gagal Jantung",
"category":"KARDIOVASKULAR",
"severity_level":"BERAT",
"chronic_flag":True,
"requires_referral":True
},


# ==================================================
# METABOLIK
# ==================================================

{
"icd_code":"E11.9",
"name":"Diabetes Melitus Tipe 2",
"category":"METABOLIK",
"severity_level":"SEDANG",
"chronic_flag":True,
"requires_referral":True
},

{
"icd_code":"E10.9",
"name":"Diabetes Melitus Tipe 1",
"category":"METABOLIK",
"severity_level":"SEDANG",
"chronic_flag":True,
"requires_referral":True
},

{
"icd_code":"E78.5",
"name":"Gangguan Metabolisme Lipoprotein",
"category":"METABOLIK",
"severity_level":"SEDANG",
"chronic_flag":True,
"requires_referral":False
},


# ==================================================
# NEUROLOGI
# ==================================================

{
"icd_code":"I63.9",
"name":"Stroke",
"category":"NEUROLOGI",
"severity_level":"BERAT",
"chronic_flag":True,
"requires_referral":True
},

{
"icd_code":"G40.9",
"name":"Epilepsi",
"category":"NEUROLOGI",
"severity_level":"SEDANG",
"chronic_flag":True,
"requires_referral":True
},

{
"icd_code":"G43.9",
"name":"Migrain",
"category":"NEUROLOGI",
"severity_level":"RINGAN",
"chronic_flag":False,
"requires_referral":False
},


# ==================================================
# PENCERNAAN
# ==================================================

{
"icd_code":"K21.9",
"name":"Gastroesophageal Reflux Disease",
"category":"PENCERNAAN",
"severity_level":"SEDANG",
"chronic_flag":True,
"requires_referral":False
},

{
"icd_code":"K35.8",
"name":"Apendisitis Akut",
"category":"PENCERNAAN",
"severity_level":"BERAT",
"chronic_flag":False,
"requires_referral":True
},


# ==================================================
# GINJAL
# ==================================================

{
"icd_code":"N18.5",
"name":"Penyakit Ginjal Kronis Stadium 5",
"category":"GINJAL",
"severity_level":"BERAT",
"chronic_flag":True,
"requires_referral":True
},

{
"icd_code":"N20.0",
"name":"Batu Ginjal",
"category":"GINJAL",
"severity_level":"SEDANG",
"chronic_flag":False,
"requires_referral":True
},


# ==================================================
# MATA
# ==================================================

{
"icd_code":"H10.9",
"name":"Konjungtivitis",
"category":"MATA",
"severity_level":"RINGAN",
"chronic_flag":False,
"requires_referral":False
},

{
"icd_code":"H25.9",
"name":"Katarak Senilis",
"category":"MATA",
"severity_level":"SEDANG",
"chronic_flag":False,
"requires_referral":True
},


# ==================================================
# MUSKULOSKELETAL
# ==================================================

{
"icd_code":"M54.5",
"name":"Nyeri Pinggang",
"category":"MUSKULOSKELETAL",
"severity_level":"RINGAN",
"chronic_flag":False,
"requires_referral":False
},

{
"icd_code":"M17.9",
"name":"Osteoarthritis Lutut",
"category":"MUSKULOSKELETAL",
"severity_level":"SEDANG",
"chronic_flag":True,
"requires_referral":True
},


# ==================================================
# NEOPLASMA
# ==================================================

{
"icd_code":"C34.9",
"name":"Kanker Paru",
"category":"ONKOLOGI",
"severity_level":"BERAT",
"chronic_flag":True,
"requires_referral":True
},

{
"icd_code":"C50.9",
"name":"Kanker Payudara",
"category":"ONKOLOGI",
"severity_level":"BERAT",
"chronic_flag":True,
"requires_referral":True
}

]