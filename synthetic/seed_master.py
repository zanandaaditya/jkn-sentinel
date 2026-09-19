from database import get_session

from generator.participant_generator import generate_participants
from generator.provider_generator import generate_providers
from generator.doctor_generator import generate_doctors
from generator.diagnosis_generator import generate_diagnosis
from generator.procedure_generator import generate_procedures
from generator.medicine_generator import generate_medicines



def seed():


    print("="*50)
    print("JKN SENTINEL SYNTHETIC MASTER DATA")
    print("="*50)



    session = get_session()



    # ==========================
    # PARTICIPANTS
    # ==========================

    print("\nGenerating Participants...")


    participants = generate_participants(
        10000
    )


    print(
        f"{len(participants)} participants generated"
    )



    # ==========================
    # PROVIDERS
    # ==========================


    print("\nGenerating Providers...")


    providers = generate_providers(
        500
    )


    print(
        f"{len(providers)} providers generated"
    )



    # ==========================
    # DOCTORS
    # ==========================


    print("\nGenerating Doctors...")


    doctors = generate_doctors(
        providers
    )


    print(
        f"{len(doctors)} doctors generated"
    )



    # ==========================
    # DIAGNOSIS
    # ==========================


    print("\nGenerating Diagnosis...")


    diagnosis = generate_diagnosis()


    print(
        f"{len(diagnosis)} diagnosis generated"
    )



    # ==========================
    # PROCEDURES
    # ==========================


    print("\nGenerating Procedures...")


    procedures = generate_procedures()


    print(
        f"{len(procedures)} procedures generated"
    )



    # ==========================
    # MEDICINES
    # ==========================


    print("\nGenerating Medicines...")


    medicines = generate_medicines()


    print(
        f"{len(medicines)} medicines generated"
    )



    print("\nMASTER DATA GENERATION COMPLETE")



if __name__ == "__main__":

    seed()
