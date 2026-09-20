import {
    CheckCircle2,
    CircleDollarSign,
    Clock3,
    FilePlus2,
    RefreshCw,
    ShieldAlert,
    UserRound
} from "lucide-react";


import {
    translateCaseStatus,
    translatePriority,
    formatRupiah
} from "../utils/translations";

import {
    AlertTriangle,
    CircleCheck,
    ClockAlert,
    Siren
} from "lucide-react";

const eventLabel = {

    CASE_AUTO_ASSIGNED:
        "Ditugaskan Otomatis",

    CASE_CREATED:
        "Kasus Dibuat",

    CASE_UPDATED:
        "Kasus Diperbarui",

    INVESTIGATION_RESULT_UPDATED:
        "Hasil Investigasi Diperbarui",

    PRIORITY_NORMALIZED:
        "Prioritas Dinormalisasi",

    SLA_WARNING:
    "SLA Mendekati Batas",

    SLA_BREACHED:
        "SLA Terlewati",

    SLA_CRITICAL:
        "SLA Kritis",

    SLA_RETURNED_ON_TRACK:
        "SLA Kembali Normal",

    SLA_CLOSED_WITHIN_SLA:
        "Kasus Selesai Dalam SLA",

    SLA_CLOSED_BREACHED:
        "Kasus Selesai Setelah SLA",

    SLA_NO_POLICY:
        "Kebijakan SLA Tidak Ditemukan"
};



const resultLabel = {

    PENDING:
        "Belum Diputuskan",

    FRAUD_CONFIRMED:
        "Fraud Terkonfirmasi",

    NOT_FRAUD:
        "Tidak Terindikasi Fraud",

    INCONCLUSIVE:
        "Belum Dapat Disimpulkan"

};



const eventIcon = {

    CASE_CREATED:
        FilePlus2,

    CASE_UPDATED:
        RefreshCw,

    INVESTIGATION_RESULT_UPDATED:
        CircleDollarSign,

    PRIORITY_NORMALIZED:
        ShieldAlert

};



const parseNumber = (value)=>{

    if(
        value === null
        ||
        value === undefined
        ||
        value === ""
    ){

        return null;

    }


    const normalized =
        String(value)
        .replace(/\./g,"")
        .replace(",",".")
        .replace(/[^\d.-]/g,"");


    const parsed =
        Number(normalized);


    return Number.isNaN(parsed)
        ? null
        : parsed;

};



const parseAuditNote = (note)=>{

    if(!note){

        return {
            items: [],
            raw: ""
        };

    }


    const parts =
        note
        .split("|")
        .map(
            (item)=>item.trim()
        )
        .filter(Boolean);


    const items = [];


    parts.forEach((part)=>{


        const separatorIndex =
            part.indexOf(":");


        if(separatorIndex === -1){

            items.push({

                label:
                    "Catatan",

                value:
                    part,

                type:
                    "text"

            });


            return;

        }


        const key =
            part
            .slice(
                0,
                separatorIndex
            )
            .trim();


        const value =
            part
            .slice(
                separatorIndex + 1
            )
            .trim();



        if(
            key === "Hasil investigasi"
        ){

            items.push({

                label:
                    "Hasil Investigasi",

                value:
                    resultLabel[value]
                    || value,

                type:
                    "result"

            });


            return;

        }



        if(
            key === "Estimasi kerugian"
        ){

            const numeric =
                parseNumber(value);


            items.push({

                label:
                    "Estimasi Kerugian",

                value:
                    numeric === null
                    ? value
                    : formatRupiah(numeric),

                type:
                    "money"

            });


            return;

        }



        if(
            key === "Kerugian terkonfirmasi"
        ){

            const numeric =
                parseNumber(value);


            items.push({

                label:
                    "Kerugian Terkonfirmasi",

                value:
                    numeric === null
                    ? value
                    : formatRupiah(numeric),

                type:
                    "money"

            });


            return;

        }



        if(
            key === "Nilai pemulihan"
        ){

            const numeric =
                parseNumber(value);


            items.push({

                label:
                    "Nilai Pemulihan",

                value:
                    numeric === null
                    ? value
                    : formatRupiah(numeric),

                type:
                    "money"

            });


            return;

        }



        if(
            key === "Kesimpulan"
        ){

            items.push({

                label:
                    "Kesimpulan",

                value,

                type:
                    "text"

            });


            return;

        }



        if(
            key === "Catatan"
        ){

            items.push({

                label:
                    "Catatan",

                value,

                type:
                    "text"

            });


            return;

        }



        items.push({

            label:
                key,

            value,

            type:
                "text"

        });


    });


    return {

        items,

        raw:
            note

    };

};



const formatDateTime = (value)=>{

    if(!value){

        return "-";

    }


    return new Date(
        value
    ).toLocaleString(
        "id-ID",
        {
            dateStyle:
                "medium",

            timeStyle:
                "short"
        }
    );

};



export default function InvestigationTimeline({
    data = []
}){


    if(
        !Array.isArray(data)
        ||
        data.length === 0
    ){

        return (

            <div className="
                bg-white
                border
                rounded-xl
                shadow
                p-6
                mt-8
            ">


                <div className="
                    flex
                    items-center
                    gap-3
                ">

                    <Clock3
                        size={20}
                        className="
                            text-gray-400
                        "
                    />


                    <div>

                        <h2 className="
                            text-xl
                            font-bold
                        ">
                            Riwayat Investigasi
                        </h2>


                        <p className="
                            text-sm
                            text-gray-500
                            mt-1
                        ">
                            Belum ada aktivitas investigasi yang tercatat.
                        </p>

                    </div>


                </div>


            </div>

        );

    }


    const orderedData =
        [...data]
        .sort(
            (a,b)=>
                new Date(
                    b.created_at
                )
                -
                new Date(
                    a.created_at
                )
        );


    return (

        <div className="
            bg-white
            border
            rounded-xl
            shadow
            p-6
            mt-8
        ">


            {/* HEADER */}

            <div className="
                mb-6
            ">


                <h2 className="
                    text-xl
                    font-bold
                ">
                    Riwayat Investigasi
                </h2>


                <p className="
                    text-sm
                    text-gray-500
                    mt-1
                ">
                    Jejak audit perubahan status, prioritas, investigator, dan hasil pemeriksaan.
                </p>


            </div>



            {/* TIMELINE */}

            <div className="
                relative
            ">


                <div className="
                    absolute
                    left-5
                    top-0
                    bottom-0
                    w-px
                    bg-gray-200
                "/>


                <div className="
                    space-y-6
                ">


                    {
                        orderedData.map(
                            (item,index)=>{


                                const Icon =
                                    eventIcon[
                                        item.event_type
                                    ]
                                    ||
                                    RefreshCw;


                                const parsed =
                                    parseAuditNote(
                                        item.note
                                    );


                                const statusChanged =
                                    item.old_status
                                    &&
                                    item.new_status
                                    &&
                                    item.old_status
                                    !==
                                    item.new_status;


                                const priorityChanged =
                                    item.old_priority
                                    &&
                                    item.new_priority
                                    &&
                                    item.old_priority
                                    !==
                                    item.new_priority;


                                const investigatorChanged =
                                    (
                                        item.old_assigned_to
                                        ||
                                        item.new_assigned_to
                                    )
                                    &&
                                    item.old_assigned_to
                                    !==
                                    item.new_assigned_to;


                                return (

                                    <div
                                        key={
                                            item.id
                                            ||
                                            index
                                        }
                                        className="
                                            relative
                                            pl-14
                                        "
                                    >


                                        {/* ICON */}

                                        <div className="
                                            absolute
                                            left-0
                                            top-0
                                            z-10
                                            w-10
                                            h-10
                                            rounded-full
                                            border
                                            bg-white
                                            flex
                                            items-center
                                            justify-center
                                        ">

                                            <Icon
                                                size={18}
                                                className="
                                                    text-blue-600
                                                "
                                            />

                                        </div>



                                        {/* CARD */}

                                        <div className="
                                            border
                                            rounded-xl
                                            p-5
                                            bg-white
                                        ">


                                            <div className="
                                                flex
                                                flex-col
                                                md:flex-row
                                                md:items-start
                                                md:justify-between
                                                gap-3
                                            ">


                                                <div>


                                                    <div className="
                                                        font-bold
                                                    ">

                                                        {
                                                            eventLabel[
                                                                item.event_type
                                                            ]
                                                            ||
                                                            item.event_type
                                                            ||
                                                            "Aktivitas Investigasi"
                                                        }

                                                    </div>


                                                    <div className="
                                                        text-xs
                                                        text-gray-500
                                                        mt-1
                                                    ">

                                                        {
                                                            formatDateTime(
                                                                item.created_at
                                                            )
                                                        }

                                                    </div>


                                                </div>



                                                <div className="
                                                    flex
                                                    items-center
                                                    gap-2
                                                    text-sm
                                                    text-gray-500
                                                ">

                                                    <UserRound
                                                        size={15}
                                                    />

                                                    <span>

                                                        {
                                                            item.actor
                                                            ||
                                                            "SYSTEM"
                                                        }

                                                    </span>

                                                </div>


                                            </div>



                                            {/* CURRENT SNAPSHOT */}

                                            <div className="
                                                flex
                                                flex-wrap
                                                gap-2
                                                mt-4
                                            ">


                                                {
                                                    item.new_status && (

                                                        <span className="
                                                            inline-flex
                                                            px-3
                                                            py-1
                                                            rounded-full
                                                            text-xs
                                                            font-semibold
                                                            bg-blue-50
                                                            text-blue-700
                                                        ">

                                                            Status:{" "}

                                                            {
                                                                translateCaseStatus(
                                                                    item.new_status
                                                                )
                                                            }

                                                        </span>

                                                    )
                                                }


                                                {
                                                    item.new_priority && (

                                                        <span className="
                                                            inline-flex
                                                            px-3
                                                            py-1
                                                            rounded-full
                                                            text-xs
                                                            font-semibold
                                                            bg-gray-100
                                                            text-gray-700
                                                        ">

                                                            Prioritas:{" "}

                                                            {
                                                                translatePriority(
                                                                    item.new_priority
                                                                )
                                                            }

                                                        </span>

                                                    )
                                                }


                                            </div>



                                            {/* CHANGES */}

                                            {
                                                (
                                                    statusChanged
                                                    ||
                                                    priorityChanged
                                                    ||
                                                    investigatorChanged
                                                )
                                                && (

                                                    <div className="
                                                        grid
                                                        grid-cols-1
                                                        md:grid-cols-2
                                                        gap-3
                                                        mt-4
                                                    ">


                                                        {
                                                            statusChanged
                                                            && (

                                                                <div className="
                                                                    bg-gray-50
                                                                    rounded-lg
                                                                    p-3
                                                                ">

                                                                    <div className="
                                                                        text-xs
                                                                        text-gray-500
                                                                    ">
                                                                        Perubahan Status
                                                                    </div>


                                                                    <div className="
                                                                        text-sm
                                                                        font-semibold
                                                                        mt-1
                                                                    ">

                                                                        {
                                                                            translateCaseStatus(
                                                                                item.old_status
                                                                            )
                                                                        }

                                                                        {" → "}

                                                                        {
                                                                            translateCaseStatus(
                                                                                item.new_status
                                                                            )
                                                                        }

                                                                    </div>

                                                                </div>

                                                            )
                                                        }



                                                        {
                                                            priorityChanged
                                                            && (

                                                                <div className="
                                                                    bg-gray-50
                                                                    rounded-lg
                                                                    p-3
                                                                ">

                                                                    <div className="
                                                                        text-xs
                                                                        text-gray-500
                                                                    ">
                                                                        Perubahan Prioritas
                                                                    </div>


                                                                    <div className="
                                                                        text-sm
                                                                        font-semibold
                                                                        mt-1
                                                                    ">

                                                                        {
                                                                            translatePriority(
                                                                                item.old_priority
                                                                            )
                                                                        }

                                                                        {" → "}

                                                                        {
                                                                            translatePriority(
                                                                                item.new_priority
                                                                            )
                                                                        }

                                                                    </div>

                                                                </div>

                                                            )
                                                        }



                                                        {
                                                            investigatorChanged
                                                            && (

                                                                <div className="
                                                                    bg-gray-50
                                                                    rounded-lg
                                                                    p-3
                                                                    md:col-span-2
                                                                ">

                                                                    <div className="
                                                                        text-xs
                                                                        text-gray-500
                                                                    ">
                                                                        Perubahan Investigator
                                                                    </div>


                                                                    <div className="
                                                                        text-sm
                                                                        font-semibold
                                                                        mt-1
                                                                    ">

                                                                        {
                                                                            item.old_assigned_to
                                                                            ||
                                                                            "Belum ditugaskan"
                                                                        }

                                                                        {" → "}

                                                                        {
                                                                            item.new_assigned_to
                                                                            ||
                                                                            "Belum ditugaskan"
                                                                        }

                                                                    </div>

                                                                </div>

                                                            )
                                                        }


                                                    </div>

                                                )
                                            }



                                            {/* AUDIT NOTE DETAILS */}

                                            {
                                                parsed.items.length > 0
                                                && (

                                                    <div className="
                                                        mt-4
                                                        space-y-3
                                                    ">


                                                        {
                                                            parsed.items.map(
                                                                (detail,detailIndex)=>(

                                                                    <div
                                                                        key={
                                                                            detailIndex
                                                                        }
                                                                        className="
                                                                            bg-gray-50
                                                                            rounded-lg
                                                                            p-3
                                                                        "
                                                                    >

                                                                        <div className="
                                                                            text-xs
                                                                            text-gray-500
                                                                        ">

                                                                            {
                                                                                detail.label
                                                                            }

                                                                        </div>


                                                                        <div className="
                                                                            text-sm
                                                                            font-medium
                                                                            mt-1
                                                                            break-words
                                                                        ">

                                                                            {
                                                                                detail.value
                                                                            }

                                                                        </div>

                                                                    </div>

                                                                )
                                                            )
                                                        }


                                                    </div>

                                                )
                                            }



                                            {/* FALLBACK NOTE */}

                                            {
                                                parsed.items.length === 0
                                                &&
                                                item.note
                                                && (

                                                    <div className="
                                                        mt-4
                                                        text-sm
                                                        text-gray-600
                                                        bg-gray-50
                                                        rounded-lg
                                                        p-3
                                                    ">

                                                        {item.note}

                                                    </div>

                                                )
                                            }


                                        </div>


                                    </div>

                                );


                            }
                        )
                    }


                </div>


            </div>


        </div>

    );

}
