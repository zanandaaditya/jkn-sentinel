from faker import Faker
import random
import uuid


fake = Faker("id_ID")


# Jenis fasilitas kesehatan
PROVIDER_TYPE = [
    "FKTP",
    "FKRTL"
]


# Kelas Rumah Sakit
CLASS = [
    "Type A",
    "Type B",
    "Type C",
    "Type D"
]


# 38 Provinsi Indonesia + Kota/Kabupaten utama
LOCATIONS = {

    "Aceh": [
        "Banda Aceh",
        "Lhokseumawe",
        "Langsa"
    ],

    "Sumatera Utara": [
        "Medan",
        "Binjai",
        "Pematangsiantar"
    ],

    "Sumatera Barat": [
        "Padang",
        "Bukittinggi",
        "Payakumbuh"
    ],

    "Riau": [
        "Pekanbaru",
        "Dumai",
        "Siak"
    ],

    "Kepulauan Riau": [
        "Batam",
        "Tanjung Pinang",
        "Bintan"
    ],

    "Jambi": [
        "Jambi",
        "Sungai Penuh",
        "Muara Bungo"
    ],

    "Sumatera Selatan": [
        "Palembang",
        "Prabumulih",
        "Lubuklinggau"
    ],

    "Kepulauan Bangka Belitung": [
        "Pangkal Pinang",
        "Sungailiat",
        "Tanjung Pandan"
    ],

    "Bengkulu": [
        "Bengkulu",
        "Curup",
        "Mukomuko"
    ],

    "Lampung": [
        "Bandar Lampung",
        "Metro",
        "Pringsewu"
    ],


    "DKI Jakarta": [
        "Jakarta Selatan",
        "Jakarta Timur",
        "Jakarta Barat"
    ],

    "Jawa Barat": [
        "Bandung",
        "Bogor",
        "Bekasi"
    ],

    "Jawa Tengah": [
        "Semarang",
        "Surakarta",
        "Magelang"
    ],

    "DI Yogyakarta": [
        "Yogyakarta",
        "Sleman",
        "Bantul"
    ],

    "Jawa Timur": [
        "Surabaya",
        "Malang",
        "Kediri"
    ],

    "Banten": [
        "Tangerang",
        "Serang",
        "Cilegon"
    ],


    "Bali": [
        "Denpasar",
        "Badung",
        "Gianyar"
    ],

    "Nusa Tenggara Barat": [
        "Mataram",
        "Bima",
        "Lombok"
    ],

    "Nusa Tenggara Timur": [
        "Kupang",
        "Ende",
        "Maumere"
    ],


    "Kalimantan Barat": [
        "Pontianak",
        "Singkawang"
    ],

    "Kalimantan Tengah": [
        "Palangka Raya",
        "Sampit"
    ],

    "Kalimantan Selatan": [
        "Banjarmasin",
        "Banjarbaru"
    ],

    "Kalimantan Timur": [
        "Samarinda",
        "Balikpapan"
    ],

    "Kalimantan Utara": [
        "Tarakan",
        "Tanjung Selor"
    ],


    "Sulawesi Utara": [
        "Manado",
        "Bitung"
    ],

    "Gorontalo": [
        "Gorontalo"
    ],

    "Sulawesi Tengah": [
        "Palu",
        "Poso"
    ],

    "Sulawesi Barat": [
        "Mamuju"
    ],

    "Sulawesi Selatan": [
        "Makassar",
        "Parepare",
        "Palopo"
    ],

    "Sulawesi Tenggara": [
        "Kendari",
        "Baubau"
    ],


    "Maluku": [
        "Ambon",
        "Tual"
    ],

    "Maluku Utara": [
        "Ternate",
        "Tidore"
    ],

    "Papua": [
        "Jayapura",
        "Biak"
    ],

    "Papua Barat": [
        "Manokwari",
        "Sorong"
    ],

    "Papua Selatan": [
        "Merauke"
    ],

    "Papua Tengah": [
        "Nabire",
        "Timika"
    ],

    "Papua Pegunungan": [
        "Wamena"
    ],

    "Papua Barat Daya": [
        "Sorong"
    ]

}



def generate_providers(total=500):

    data = []


    for i in range(total):


        # pilih provinsi dahulu
        province = random.choice(
            list(LOCATIONS.keys())
        )


        # pilih kota sesuai provinsi
        city = random.choice(
            LOCATIONS[province]
        )


        provider_type = random.choice(
            PROVIDER_TYPE
        )


        # Nama fasilitas sesuai jenis
        if provider_type == "FKRTL":

            provider_name = (
                "RS "
                + city
            )

        else:

            provider_name = random.choice(
                [
                    "Puskesmas ",
                    "Klinik "
                ]
            ) + city



        provider = {

            "id":
            str(uuid.uuid4()),


            "provider_code":
            f"FKES{i+1:05}",


            "provider_name":
            provider_name,


            "provider_type":
            provider_type,


            "province":
            province,


            "class_name":
            random.choice(
                CLASS
            ),


            "status":
            "ACTIVE"

        }


        data.append(provider)


    return data