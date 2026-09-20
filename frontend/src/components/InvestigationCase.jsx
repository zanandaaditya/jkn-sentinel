import {
    useEffect,
    useMemo,
    useState
} from "react";

import {
    BadgeDollarSign,
    CheckCircle2,
    CircleDollarSign,
    FileSearch,
    ShieldCheck
} from "lucide-react";

import {
    formatRupiah
} from "../utils/translations";


export default function InvestigationCase({

    fraudCase,

    onCreate,

    onSave,

    saving = false

}){


    const [form,setForm] = useState({

        case_status: "NEW",

        priority: "MEDIUM",

        assigned_to: "",

        investigation_note: "",

        investigation_result: "PENDING",

        estimated_loss: "",

        confirmed_loss: "",

        recovered_amount: "",

        conclusion: ""

    });


    useEffect(()=>{


        if(fraudCase){

            setForm({

                case_status:
                    fraudCase.case_status || "NEW",

                priority:
                    fraudCase.priority || "MEDIUM",

                assigned_to:
                    fraudCase.assigned_to || "",

                investigation_note:
                    fraudCase.investigation_note || "",

                investigation_result:
                    fraudCase.investigation_result || "PENDING",

                estimated_loss:
                    fraudCase.estimated_loss ?? "",

                confirmed_loss:
                    fraudCase.confirmed_loss ?? "",

                recovered_amount:
                    fraudCase.recovered_amount ?? "",

                conclusion:
                    fraudCase.conclusion || ""

            });

        }


    },[fraudCase]);


    const handleChange = (event)=>{

        const {
            name,
            value
        } = event.target;


        if(
            name === "investigation_result"
        ){

            let nextStatus =
                form.case_status;


            if(
                value === "FRAUD_CONFIRMED"
            ){

                nextStatus = "CONFIRMED";

            }
            else if(
                value === "NOT_FRAUD"
            ){

                nextStatus = "CLEARED";

            }
            else if(
                value === "INCONCLUSIVE"
                ||
                value === "PENDING"
            ){

                nextStatus = "REVIEWING";

            }


            setForm((previous)=>({

                ...previous,

                investigation_result:
                    value,

                case_status:
                    nextStatus

            }));


            return;

        }


        setForm((previous)=>({

            ...previous,

            [name]: value

        }));

    };


    const normalizeNumber = (value)=>{

        if(
            value === ""
            ||
            value === null
            ||
            value === undefined
        ){

            return null;

        }


        const parsed =
            Number(value);


        return Number.isNaN(parsed)
            ? null
            : parsed;

    };


    const handleSave = ()=>{


        const payload = {

            case_status:
                form.case_status,

            priority:
                form.priority,

            assigned_to:
                form.assigned_to.trim()
                || null,

            investigation_note:
                form.investigation_note.trim()
                || null,

            investigation_result:
                form.investigation_result,

            estimated_loss:
                normalizeNumber(
                    form.estimated_loss
                ),

            confirmed_loss:
                normalizeNumber(
                    form.confirmed_loss
                ),

            recovered_amount:
                normalizeNumber(
                    form.recovered_amount
                ),

            conclusion:
                form.conclusion.trim()
                || null

        };


        onSave(payload);

    };


    const financialSummary =
        useMemo(()=>{


            const estimated =
                Number(
                    form.estimated_loss || 0
                );


            const confirmed =
                Number(
                    form.confirmed_loss || 0
                );


            const recovered =
                Number(
                    form.recovered_amount || 0
                );


            const outstanding =
                Math.max(
                    confirmed - recovered,
                    0
                );


            const recoveryRate =
                confirmed > 0
                ? (
                    recovered
                    /
                    confirmed
                ) * 100
                : 0;


            return {

                estimated,

                confirmed,

                recovered,

                outstanding,

                recoveryRate

            };


        },[
            form.estimated_loss,
            form.confirmed_loss,
            form.recovered_amount
        ]);


    if(!fraudCase){

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
                    items-start
                    gap-3
                ">

                    <div className="
                        w-10
                        h-10
                        rounded-lg
                        bg-blue-50
                        flex
                        items-center
                        justify-center
                    ">

                        <FileSearch
                            size={20}
                            className="
                                text-blue-600
                            "
                        />

                    </div>


                    <div>

                        <h2 className="
                            text-xl
                            font-bold
                        ">
                            Penanganan Kasus
                        </h2>


                        <p className="
                            text-sm
                            text-gray-500
                            mt-1
                            mb-6
                        ">
                            Klaim ini belum memiliki kasus investigasi.
                        </p>

                    </div>

                </div>


                <button
                    onClick={onCreate}
                    disabled={saving}
                    className="
                        bg-blue-600
                        text-white
                        px-5
                        py-2.5
                        rounded-lg
                        font-semibold
                        hover:bg-blue-700
                        disabled:opacity-50
                        disabled:cursor-not-allowed
                    "
                >

                    {
                        saving
                        ? "Membuat..."
                        : "Buat Kasus Investigasi"
                    }

                </button>


            </div>

        );

    }


    return (

        <div className="
            bg-white
            border
            rounded-xl
            shadow
            p-6
            mt-8
        ">


            {/* =====================================
                HEADER
            ===================================== */}


            <div className="
                flex
                flex-col
                md:flex-row
                md:items-start
                md:justify-between
                gap-4
                mb-7
            ">


                <div>


                    <div className="
                        flex
                        items-center
                        gap-3
                    ">

                        <div className="
                            w-10
                            h-10
                            rounded-lg
                            bg-blue-50
                            flex
                            items-center
                            justify-center
                        ">

                            <ShieldCheck
                                size={20}
                                className="
                                    text-blue-600
                                "
                            />

                        </div>


                        <div>

                            <h2 className="
                                text-xl
                                font-bold
                            ">
                                Penanganan Kasus
                            </h2>


                            <p className="
                                text-sm
                                text-gray-500
                                mt-1
                            ">
                                Kelola proses investigasi dan hasil pemeriksaan klaim.
                            </p>

                        </div>

                    </div>


                </div>



                <div className="
                    text-sm
                    text-gray-500
                ">

                    ID Kasus

                    <div className="
                        font-mono
                        text-gray-800
                        mt-1
                        break-all
                    ">
                        {fraudCase.id}
                    </div>

                </div>


            </div>



            {/* =====================================
                CASE MANAGEMENT
            ===================================== */}


            <div className="
                border
                rounded-xl
                p-5
            ">


                <h3 className="
                    font-bold
                    mb-4
                ">
                    Proses Investigasi
                </h3>


                <div className="
                    grid
                    grid-cols-1
                    md:grid-cols-2
                    gap-5
                ">


                    {/* STATUS */}

                    <div>


                        <label className="
                            block
                            text-sm
                            font-semibold
                            mb-2
                        ">
                            Status Kasus
                        </label>


                        <select
                            name="case_status"
                            value={form.case_status}
                            onChange={handleChange}
                            className="
                                w-full
                                border
                                rounded-lg
                                px-4
                                py-2.5
                                bg-white
                            "
                        >

                            <option value="NEW">
                                Baru
                            </option>

                            <option value="REVIEWING">
                                Dalam Pemeriksaan
                            </option>

                            <option value="CONFIRMED">
                                Terindikasi Fraud
                            </option>

                            <option value="CLEARED">
                                Tidak Terindikasi Fraud
                            </option>

                        </select>


                    </div>



                    {/* PRIORITY */}

                    <div>


                        <label className="
                            block
                            text-sm
                            font-semibold
                            mb-2
                        ">
                            Prioritas
                        </label>


                        <select
                            name="priority"
                            value={form.priority}
                            onChange={handleChange}
                            className="
                                w-full
                                border
                                rounded-lg
                                px-4
                                py-2.5
                                bg-white
                            "
                        >

                            <option value="LOW">
                                Rendah
                            </option>

                            <option value="NORMAL">
                                Normal
                            </option>

                            <option value="MEDIUM">
                                Sedang
                            </option>

                            <option value="HIGH">
                                Tinggi
                            </option>

                            <option value="URGENT">
                                Mendesak
                            </option>

                        </select>


                    </div>



                    {/* INVESTIGATOR */}

                    <div className="
                        md:col-span-2
                    ">


                        <label className="
                            block
                            text-sm
                            font-semibold
                            mb-2
                        ">
                            Investigator
                        </label>


                        <input
                            type="text"
                            name="assigned_to"
                            value={form.assigned_to}
                            onChange={handleChange}
                            placeholder="Masukkan nama investigator"
                            className="
                                w-full
                                border
                                rounded-lg
                                px-4
                                py-2.5
                            "
                        />


                    </div>



                    {/* NOTE */}

                    <div className="
                        md:col-span-2
                    ">


                        <label className="
                            block
                            text-sm
                            font-semibold
                            mb-2
                        ">
                            Catatan Investigasi
                        </label>


                        <textarea
                            name="investigation_note"
                            value={form.investigation_note}
                            onChange={handleChange}
                            rows="4"
                            placeholder="Masukkan catatan investigasi..."
                            className="
                                w-full
                                border
                                rounded-lg
                                px-4
                                py-3
                                resize-y
                            "
                        />


                    </div>


                </div>


            </div>



            {/* =====================================
                INVESTIGATION OUTCOME
            ===================================== */}


            <div className="
                border
                rounded-xl
                p-5
                mt-5
            ">


                <div className="
                    flex
                    items-center
                    gap-3
                    mb-5
                ">

                    <CheckCircle2
                        size={20}
                        className="
                            text-blue-600
                        "
                    />

                    <div>

                        <h3 className="
                            font-bold
                        ">
                            Hasil Investigasi
                        </h3>

                        <p className="
                            text-sm
                            text-gray-500
                            mt-1
                        ">
                            Tetapkan hasil akhir berdasarkan pemeriksaan klinis dan administratif.
                        </p>

                    </div>

                </div>


                <div className="
                    grid
                    grid-cols-1
                    gap-5
                ">


                    <div>


                        <label className="
                            block
                            text-sm
                            font-semibold
                            mb-2
                        ">
                            Keputusan Investigasi
                        </label>


                        <select
                            name="investigation_result"
                            value={
                                form.investigation_result
                            }
                            onChange={handleChange}
                            className="
                                w-full
                                border
                                rounded-lg
                                px-4
                                py-2.5
                                bg-white
                            "
                        >

                            <option value="PENDING">
                                Belum Diputuskan
                            </option>

                            <option value="FRAUD_CONFIRMED">
                                Fraud Terkonfirmasi
                            </option>

                            <option value="NOT_FRAUD">
                                Tidak Terindikasi Fraud
                            </option>

                            <option value="INCONCLUSIVE">
                                Belum Dapat Disimpulkan
                            </option>

                        </select>


                        <p className="
                            text-xs
                            text-gray-500
                            mt-2
                        ">

                            Hasil final akan menyesuaikan status kasus secara otomatis.

                        </p>


                    </div>



                    <div>


                        <label className="
                            block
                            text-sm
                            font-semibold
                            mb-2
                        ">
                            Kesimpulan
                        </label>


                        <textarea
                            name="conclusion"
                            value={form.conclusion}
                            onChange={handleChange}
                            rows="4"
                            placeholder="Tuliskan kesimpulan hasil investigasi..."
                            className="
                                w-full
                                border
                                rounded-lg
                                px-4
                                py-3
                                resize-y
                            "
                        />


                    </div>


                </div>


            </div>



            {/* =====================================
                FINANCIAL IMPACT
            ===================================== */}


            <div className="
                border
                rounded-xl
                p-5
                mt-5
            ">


                <div className="
                    flex
                    items-center
                    gap-3
                    mb-5
                ">

                    <BadgeDollarSign
                        size={20}
                        className="
                            text-blue-600
                        "
                    />

                    <div>

                        <h3 className="
                            font-bold
                        ">
                            Dampak Finansial
                        </h3>

                        <p className="
                            text-sm
                            text-gray-500
                            mt-1
                        ">
                            Catat estimasi, nilai terkonfirmasi, dan nilai pemulihan kasus.
                        </p>

                    </div>

                </div>


                <div className="
                    grid
                    grid-cols-1
                    md:grid-cols-3
                    gap-5
                ">


                    <div>


                        <label className="
                            block
                            text-sm
                            font-semibold
                            mb-2
                        ">
                            Estimasi Kerugian
                        </label>


                        <input
                            type="number"
                            min="0"
                            step="1"
                            name="estimated_loss"
                            value={form.estimated_loss}
                            onChange={handleChange}
                            placeholder="0"
                            className="
                                w-full
                                border
                                rounded-lg
                                px-4
                                py-2.5
                            "
                        />


                        <div className="
                            text-xs
                            text-gray-500
                            mt-2
                        ">
                            {
                                formatRupiah(
                                    financialSummary.estimated
                                )
                            }
                        </div>


                    </div>



                    <div>


                        <label className="
                            block
                            text-sm
                            font-semibold
                            mb-2
                        ">
                            Kerugian Terkonfirmasi
                        </label>


                        <input
                            type="number"
                            min="0"
                            step="1"
                            name="confirmed_loss"
                            value={form.confirmed_loss}
                            onChange={handleChange}
                            placeholder="0"
                            className="
                                w-full
                                border
                                rounded-lg
                                px-4
                                py-2.5
                            "
                        />


                        <div className="
                            text-xs
                            text-gray-500
                            mt-2
                        ">
                            {
                                formatRupiah(
                                    financialSummary.confirmed
                                )
                            }
                        </div>


                    </div>



                    <div>


                        <label className="
                            block
                            text-sm
                            font-semibold
                            mb-2
                        ">
                            Nilai Pemulihan
                        </label>


                        <input
                            type="number"
                            min="0"
                            step="1"
                            name="recovered_amount"
                            value={form.recovered_amount}
                            onChange={handleChange}
                            placeholder="0"
                            className="
                                w-full
                                border
                                rounded-lg
                                px-4
                                py-2.5
                            "
                        />


                        <div className="
                            text-xs
                            text-gray-500
                            mt-2
                        ">
                            {
                                formatRupiah(
                                    financialSummary.recovered
                                )
                            }
                        </div>


                    </div>


                </div>



                {/* FINANCIAL SUMMARY */}

                <div className="
                    grid
                    grid-cols-1
                    md:grid-cols-3
                    gap-4
                    mt-6
                ">


                    <div className="
                        bg-gray-50
                        rounded-xl
                        p-4
                    ">

                        <div className="
                            text-xs
                            text-gray-500
                        ">
                            Sisa Kerugian
                        </div>


                        <div className="
                            font-bold
                            mt-1
                        ">
                            {
                                formatRupiah(
                                    financialSummary.outstanding
                                )
                            }
                        </div>

                    </div>



                    <div className="
                        bg-gray-50
                        rounded-xl
                        p-4
                    ">

                        <div className="
                            text-xs
                            text-gray-500
                        ">
                            Tingkat Pemulihan
                        </div>


                        <div className="
                            font-bold
                            mt-1
                        ">
                            {
                                financialSummary
                                .recoveryRate
                                .toFixed(1)
                            }%
                        </div>

                    </div>



                    <div className="
                        bg-gray-50
                        rounded-xl
                        p-4
                    ">

                        <div className="
                            text-xs
                            text-gray-500
                        ">
                            Status Penutupan
                        </div>


                        <div className="
                            font-bold
                            mt-1
                        ">

                            {
                                fraudCase.closed_at
                                ? "Kasus Ditutup"
                                : "Kasus Aktif"
                            }

                        </div>

                    </div>


                </div>


            </div>



            {/* =====================================
                FOOTER
            ===================================== */}


            <div className="
                flex
                flex-col
                sm:flex-row
                sm:items-center
                sm:justify-between
                gap-4
                mt-6
                pt-6
                border-t
            ">


                <div className="
                    text-sm
                    text-gray-500
                ">


                    <div>

                        Dibuat:{" "}

                        {
                            fraudCase.created_at
                            ? new Date(
                                fraudCase.created_at
                            ).toLocaleString(
                                "id-ID",
                                {
                                    dateStyle: "medium",
                                    timeStyle: "short"
                                }
                            )
                            : "-"
                        }

                    </div>


                    {
                        fraudCase.closed_at && (

                            <div className="
                                mt-1
                            ">

                                Ditutup:{" "}

                                {
                                    new Date(
                                        fraudCase.closed_at
                                    ).toLocaleString(
                                        "id-ID",
                                        {
                                            dateStyle: "medium",
                                            timeStyle: "short"
                                        }
                                    )
                                }

                            </div>

                        )
                    }


                </div>



                <button
                    onClick={handleSave}
                    disabled={saving}
                    className="
                        inline-flex
                        items-center
                        justify-center
                        gap-2
                        bg-blue-600
                        text-white
                        px-6
                        py-2.5
                        rounded-lg
                        font-semibold
                        hover:bg-blue-700
                        disabled:opacity-50
                        disabled:cursor-not-allowed
                    "
                >

                    <CircleDollarSign
                        size={18}
                    />

                    {
                        saving
                        ? "Menyimpan..."
                        : "Simpan Investigasi"
                    }

                </button>


            </div>


        </div>

    );

}
