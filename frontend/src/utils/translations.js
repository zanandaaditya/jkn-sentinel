// =====================================
// JKN SENTINEL UI TRANSLATION LAYER
// =====================================


export const caseStatusLabel = {

    NEW: "Baru",

    REVIEWING: "Dalam Pemeriksaan",

    CONFIRMED: "Terindikasi Fraud",

    CLEARED: "Tidak Terindikasi Fraud"

};



export const priorityLabel = {

    LOW: "Rendah",

    NORMAL: "Normal",

    MEDIUM: "Sedang",

    HIGH: "Tinggi",

    URGENT: "Mendesak"

};



export const riskLevelLabel = {

    LOW: "Rendah",

    MEDIUM: "Sedang",

    HIGH: "Tinggi"

};



export const factorLabel = {

    CLINICAL: "Klinis",

    COST: "Biaya",

    FACILITY: "Fasilitas",

    DOCTOR: "Dokter"

};



export const clinicalMatchLabel = {

    DIRECT: "Sesuai Langsung",

    SUPPORTING: "Pendukung",

    LIMITED: "Kesesuaian Terbatas",

    UNMATCHED: "Tidak Sesuai"

};



const fraudReasonDictionary = {

    "Clinical mismatch procedure/medicine":
        "Ketidaksesuaian klinis antara diagnosis, prosedur, atau obat",

    "Claim cost anomaly":
        "Terdapat anomali biaya klaim dibandingkan tarif acuan",

    "Facility capability risk":
        "Kapabilitas fasilitas tidak sesuai dengan kompleksitas layanan",

    "Doctor competency risk":
        "Profil kompetensi dokter menunjukkan faktor risiko"

};



export const translateFraudReason = (value)=>{

    if(!value){
        return "-";
    }


    return value

        .split(";")

        .map((reason)=>{

            const clean =
                reason.trim();


            return (
                fraudReasonDictionary[clean]
                ||
                clean
            );

        })

        .join("; ");

};



export const translateCaseStatus = (value)=>{

    return (
        caseStatusLabel[value]
        ||
        value
        ||
        "-"
    );

};



export const translatePriority = (value)=>{

    return (
        priorityLabel[value]
        ||
        value
        ||
        "-"
    );

};



export const translateRiskLevel = (value)=>{

    return (
        riskLevelLabel[value]
        ||
        value
        ||
        "-"
    );

};



export const translateFactor = (value)=>{

    return (
        factorLabel[value]
        ||
        value
        ||
        "-"
    );

};



export const translateClinicalMatch = (value)=>{

    return (
        clinicalMatchLabel[value]
        ||
        value
        ||
        "-"
    );

};



export const formatRupiah = (value)=>{

    if(
        value === null
        ||
        value === undefined
    ){
        return "-";
    }


    return new Intl.NumberFormat(
        "id-ID",
        {
            style: "currency",
            currency: "IDR",
            maximumFractionDigits: 0
        }
    ).format(value);

};



export const formatDateID = (value)=>{

    if(!value){
        return "-";
    }


    return new Date(value)
    .toLocaleDateString(
        "id-ID",
        {
            day: "2-digit",
            month: "short",
            year: "numeric"
        }
    );

};