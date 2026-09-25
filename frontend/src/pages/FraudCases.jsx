import {
    useEffect,
    useState
} from "react";


import {
    Link
} from "react-router-dom";


import {
    Search,
    ShieldAlert,
    Clock3,
    CircleCheckBig,
    FolderSearch,
    ChevronLeft,
    ChevronRight
} from "lucide-react";


import {
    getFraudCaseQueue
} from "../api/dashboard";


import {
    translateCaseStatus,
    translatePriority,
    translateRiskLevel,
    translateFraudReason,
    formatRupiah,
    formatDateID
} from "../utils/translations";



// =====================================
// BADGE STYLES
// =====================================

const statusStyle = {

    NEW:
        "bg-gray-100 text-gray-700",

    REVIEWING:
        "bg-blue-100 text-blue-700",

    CONFIRMED:
        "bg-red-100 text-red-700",

    CLEARED:
        "bg-green-100 text-green-700"

};



const priorityStyle = {

    LOW:
        "bg-green-100 text-green-700",

    NORMAL:
        "bg-gray-100 text-gray-700",

    MEDIUM:
        "bg-yellow-100 text-yellow-700",

    HIGH:
        "bg-orange-100 text-orange-700",

    URGENT:
        "bg-red-100 text-red-700"

};



export default function FraudCases(){


    // =====================================
    // DATA STATE
    // =====================================

    const [cases,setCases] =
        useState([]);


    const [pagination,setPagination] =
        useState({

            page: 1,

            page_size: 10,

            total: 0,

            total_pages: 0,

            has_previous: false,

            has_next: false

        });


    const [summary,setSummary] =
        useState({

            total_cases: 0,

            new_cases: 0,

            reviewing_cases: 0,

            confirmed_cases: 0,

            cleared_cases: 0,

            urgent_cases: 0,

            high_priority_cases: 0

        });


    const [loading,setLoading] =
        useState(true);


    const [error,setError] =
        useState("");



    // =====================================
    // FILTER STATE
    // =====================================

    const [search,setSearch] =
        useState("");


    const [statusFilter,setStatusFilter] =
        useState("ALL");


    const [priorityFilter,setPriorityFilter] =
        useState("ALL");


    const [page,setPage] =
        useState(1);


    const [pageSize,setPageSize] =
        useState(10);



    // =====================================
    // LOAD QUEUE
    // SERVER SIDE FILTER + PAGINATION
    // =====================================

    useEffect(()=>{


        let cancelled = false;


        const timer = setTimeout(
            async()=>{


                try{


                    setLoading(true);

                    setError("");


                    const params = {

                        page,

                        page_size:
                            pageSize

                    };


                    if(
                        statusFilter !== "ALL"
                    ){

                        params.case_status =
                            statusFilter;

                    }


                    if(
                        priorityFilter !== "ALL"
                    ){

                        params.priority =
                            priorityFilter;

                    }


                    if(
                        search.trim()
                    ){

                        params.search =
                            search.trim();

                    }



                    const result =
                        await getFraudCaseQueue(
                            params
                        );


                    if(cancelled){
                        return;
                    }


                    setCases(
                        result?.items || []
                    );


                    setPagination({

                        page:
                            result?.pagination?.page
                            ?? page,

                        page_size:
                            result?.pagination?.page_size
                            ?? pageSize,

                        total:
                            result?.pagination?.total
                            ?? 0,

                        total_pages:
                            result?.pagination?.total_pages
                            ?? 0,

                        has_previous:
                            result?.pagination?.has_previous
                            ?? false,

                        has_next:
                            result?.pagination?.has_next
                            ?? false

                    });


                    setSummary({

                        total_cases:
                            result?.summary?.total_cases
                            ?? 0,

                        new_cases:
                            result?.summary?.new_cases
                            ?? 0,

                        reviewing_cases:
                            result?.summary?.reviewing_cases
                            ?? 0,

                        confirmed_cases:
                            result?.summary?.confirmed_cases
                            ?? 0,

                        cleared_cases:
                            result?.summary?.cleared_cases
                            ?? 0,

                        urgent_cases:
                            result?.summary?.urgent_cases
                            ?? 0,

                        high_priority_cases:
                            result?.summary?.high_priority_cases
                            ?? 0

                    });


                }
                catch(error){


                    if(cancelled){
                        return;
                    }


                    console.error(
                        "FRAUD CASE QUEUE ERROR:",
                        error
                    );


                    setCases([]);


                    setError(
                        error?.response?.data?.detail
                        ||
                        "Gagal mengambil daftar kasus investigasi."
                    );


                }
                finally{


                    if(!cancelled){

                        setLoading(false);

                    }


                }


            },
            350
        );


        return ()=>{

            cancelled = true;

            clearTimeout(timer);

        };


    },[
        search,
        statusFilter,
        priorityFilter,
        page,
        pageSize
    ]);



    // =====================================
    // RESET PAGE WHEN FILTER CHANGES
    // =====================================

    const handleSearchChange = (event)=>{

        setSearch(
            event.target.value
        );

        setPage(1);

    };


    const handleStatusChange = (event)=>{

        setStatusFilter(
            event.target.value
        );

        setPage(1);

    };


    const handlePriorityChange = (event)=>{

        setPriorityFilter(
            event.target.value
        );

        setPage(1);

    };


    const handlePageSizeChange = (event)=>{

        setPageSize(
            Number(
                event.target.value
            )
        );

        setPage(1);

    };



    // =====================================
    // PAGINATION ACTIONS
    // =====================================

    const goPrevious = ()=>{

        if(
            pagination.has_previous
            &&
            page > 1
        ){

            setPage(
                page - 1
            );

        }

    };


    const goNext = ()=>{

        if(
            pagination.has_next
        ){

            setPage(
                page + 1
            );

        }

    };



    // =====================================
    // DISPLAY RANGE
    // =====================================

    const startItem =

        pagination.total === 0

        ? 0

        : (
            (
                pagination.page - 1
            )
            *
            pagination.page_size
        ) + 1;


    const endItem =

        pagination.total === 0

        ? 0

        : Math.min(

            pagination.page
            *
            pagination.page_size,

            pagination.total

        );



    return (

        <div className="
            pb-12
        ">


            {/* =====================================
                HEADER
            ===================================== */}


            <div className="
                mb-8
            ">


                <div className="
                    text-sm
                    text-gray-500
                    mb-2
                ">

                    Fraud Investigation Workspace

                </div>


                <h1 className="
                    text-3xl
                    font-bold
                ">

                    Antrean Kasus Fraud

                </h1>


                <p className="
                    text-gray-500
                    mt-2
                ">

                    Pantau dan kelola seluruh klaim
                    yang masuk ke proses investigasi.

                </p>


            </div>



            {
                error && (

                    <div className="
                        bg-red-50
                        border
                        border-red-200
                        text-red-700
                        rounded-xl
                        p-4
                        mb-6
                    ">

                        {error}

                    </div>

                )
            }



            {/* =====================================
                KPI SUMMARY
            ===================================== */}


            <div className="
                grid
                grid-cols-1
                sm:grid-cols-2
                xl:grid-cols-4
                gap-5
                mb-8
            ">


                <div className="
                    bg-white
                    border
                    rounded-xl
                    p-5
                    shadow-sm
                ">


                    <div className="
                        flex
                        justify-between
                        items-start
                    ">


                        <div>

                            <div className="
                                text-sm
                                text-gray-500
                            ">
                                Total Kasus
                            </div>


                            <div className="
                                text-3xl
                                font-bold
                                mt-2
                            ">
                                {summary.total_cases}
                            </div>

                        </div>


                        <FolderSearch
                            className="
                                text-gray-400
                            "
                        />


                    </div>

                </div>




                <div className="
                    bg-white
                    border
                    rounded-xl
                    p-5
                    shadow-sm
                ">


                    <div className="
                        flex
                        justify-between
                        items-start
                    ">


                        <div>

                            <div className="
                                text-sm
                                text-gray-500
                            ">
                                Mendesak
                            </div>


                            <div className="
                                text-3xl
                                font-bold
                                mt-2
                            ">
                                {summary.urgent_cases}
                            </div>

                        </div>


                        <ShieldAlert
                            className="
                                text-red-500
                            "
                        />


                    </div>

                </div>




                <div className="
                    bg-white
                    border
                    rounded-xl
                    p-5
                    shadow-sm
                ">


                    <div className="
                        flex
                        justify-between
                        items-start
                    ">


                        <div>

                            <div className="
                                text-sm
                                text-gray-500
                            ">
                                Dalam Pemeriksaan
                            </div>


                            <div className="
                                text-3xl
                                font-bold
                                mt-2
                            ">
                                {summary.reviewing_cases}
                            </div>

                        </div>


                        <Clock3
                            className="
                                text-blue-500
                            "
                        />


                    </div>

                </div>




                <div className="
                    bg-white
                    border
                    rounded-xl
                    p-5
                    shadow-sm
                ">


                    <div className="
                        flex
                        justify-between
                        items-start
                    ">


                        <div>

                            <div className="
                                text-sm
                                text-gray-500
                            ">
                                Terindikasi Fraud
                            </div>


                            <div className="
                                text-3xl
                                font-bold
                                mt-2
                            ">
                                {summary.confirmed_cases}
                            </div>

                        </div>


                        <CircleCheckBig
                            className="
                                text-red-500
                            "
                        />


                    </div>

                </div>


            </div>



            {/* =====================================
                SERVER FILTERS
            ===================================== */}


            <div className="
                bg-white
                border
                rounded-xl
                shadow-sm
                p-5
                mb-6
            ">


                <div className="
                    grid
                    grid-cols-1
                    md:grid-cols-4
                    gap-4
                ">


                    <div className="
                        relative
                        md:col-span-2
                    ">


                        <Search
                            size={18}
                            className="
                                absolute
                                left-3
                                top-1/2
                                -translate-y-1/2
                                text-gray-400
                            "
                        />


                        <input
                            type="text"
                            value={search}
                            onChange={
                                handleSearchChange
                            }
                            placeholder="Cari kode klaim, fasilitas, diagnosis, atau investigator..."
                            className="
                                w-full
                                border
                                rounded-lg
                                py-2.5
                                pl-10
                                pr-4
                            "
                        />


                    </div>



                    <select
                        value={statusFilter}
                        onChange={
                            handleStatusChange
                        }
                        className="
                            border
                            rounded-lg
                            px-4
                            py-2.5
                        "
                    >

                        <option value="ALL">
                            Semua Status
                        </option>

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



                    <select
                        value={priorityFilter}
                        onChange={
                            handlePriorityChange
                        }
                        className="
                            border
                            rounded-lg
                            px-4
                            py-2.5
                        "
                    >

                        <option value="ALL">
                            Semua Prioritas
                        </option>

                        <option value="URGENT">
                            Mendesak
                        </option>

                        <option value="HIGH">
                            Tinggi
                        </option>

                        <option value="MEDIUM">
                            Sedang
                        </option>

                        <option value="NORMAL">
                            Normal
                        </option>

                        <option value="LOW">
                            Rendah
                        </option>

                    </select>


                </div>



                <div className="
                    flex
                    flex-col
                    sm:flex-row
                    sm:items-center
                    sm:justify-between
                    gap-4
                    mt-4
                ">


                    <div className="
                        text-sm
                        text-gray-500
                    ">

                        {
                            loading
                            ? "Memuat data..."
                            : (
                                <>
                                    Menampilkan{" "}
                                    <b>{startItem}</b>
                                    {" - "}
                                    <b>{endItem}</b>
                                    {" dari "}
                                    <b>{pagination.total}</b>
                                    {" kasus sesuai filter."}
                                </>
                            )
                        }

                    </div>



                    <div className="
                        flex
                        items-center
                        gap-2
                    ">


                        <span className="
                            text-sm
                            text-gray-500
                        ">
                            Data per halaman
                        </span>


                        <select
                            value={pageSize}
                            onChange={
                                handlePageSizeChange
                            }
                            className="
                                border
                                rounded-lg
                                px-3
                                py-2
                                text-sm
                            "
                        >

                            <option value="5">
                                5
                            </option>

                            <option value="10">
                                10
                            </option>

                            <option value="20">
                                20
                            </option>

                            <option value="50">
                                50
                            </option>

                        </select>


                    </div>


                </div>


            </div>



            {/* =====================================
                CASE TABLE
            ===================================== */}


            <div className="
                bg-white
                border
                rounded-xl
                shadow-sm
                overflow-hidden
            ">


                <div className="
                    overflow-x-auto
                ">


                    <table className="
                        w-full
                        text-sm
                    ">


                        <thead className="
                            bg-gray-50
                            border-b
                        ">

                            <tr>

                                <th className="
                                    text-left
                                    p-4
                                ">
                                    Klaim
                                </th>

                                <th className="
                                    text-left
                                    p-4
                                ">
                                    Fasilitas / Diagnosis
                                </th>

                                <th className="
                                    text-left
                                    p-4
                                ">
                                    Fraud Score
                                </th>

                                <th className="
                                    text-left
                                    p-4
                                ">
                                    Status
                                </th>

                                <th className="
                                    text-left
                                    p-4
                                ">
                                    Prioritas
                                </th>

                                <th className="
                                    text-left
                                    p-4
                                ">
                                    Investigator
                                </th>

                                <th className="
                                    text-right
                                    p-4
                                ">
                                    Aksi
                                </th>

                            </tr>

                        </thead>



                        <tbody>


                            {
                                loading
                                ? (

                                    <tr>

                                        <td
                                            colSpan="7"
                                            className="
                                                text-center
                                                text-gray-500
                                                p-10
                                            "
                                        >
                                            Memuat antrean investigasi...
                                        </td>

                                    </tr>

                                )
                                : cases.length === 0
                                ? (

                                    <tr>

                                        <td
                                            colSpan="7"
                                            className="
                                                text-center
                                                text-gray-500
                                                p-10
                                            "
                                        >
                                            Tidak ada kasus yang sesuai filter.
                                        </td>

                                    </tr>

                                )
                                : (

                                    cases.map(
                                        (item)=>(

                                            <tr
                                                key={
                                                    item.case_id
                                                }
                                                className="
                                                    border-b
                                                    last:border-b-0
                                                    hover:bg-gray-50
                                                "
                                            >


                                                <td className="
                                                    p-4
                                                    align-top
                                                ">


                                                    <div className="
                                                        font-semibold
                                                        text-gray-900
                                                    ">
                                                        {item.claim_code}
                                                    </div>


                                                    <div className="
                                                        text-xs
                                                        text-gray-500
                                                        mt-1
                                                    ">
                                                        {
                                                            formatDateID(
                                                                item.service_date
                                                            )
                                                        }
                                                    </div>


                                                    <div className="
                                                        text-xs
                                                        text-gray-500
                                                        mt-1
                                                    ">
                                                        {
                                                            formatRupiah(
                                                                item.claim_amount
                                                            )
                                                        }
                                                    </div>


                                                </td>



                                                <td className="
                                                    p-4
                                                    align-top
                                                ">


                                                    <div className="
                                                        font-medium
                                                    ">
                                                        {
                                                            item.facility
                                                            || "-"
                                                        }
                                                    </div>


                                                    <div className="
                                                        text-xs
                                                        text-gray-500
                                                        mt-1
                                                    ">
                                                        {
                                                            item.diagnosis
                                                            || "-"
                                                        }
                                                    </div>


                                                </td>



                                                <td className="
                                                    p-4
                                                    align-top
                                                ">


                                                    <div className="
                                                        text-xl
                                                        font-bold
                                                    ">
                                                        {item.fraud_score}
                                                    </div>


                                                    <div className="
                                                        text-xs
                                                        text-gray-500
                                                        mt-1
                                                    ">
                                                        {
                                                            translateRiskLevel(
                                                                item.risk_level
                                                            )
                                                        }
                                                    </div>


                                                </td>



                                                <td className="
                                                    p-4
                                                    align-top
                                                ">


                                                    <span
                                                        className={`
                                                            inline-flex
                                                            px-3
                                                            py-1
                                                            rounded-full
                                                            text-xs
                                                            font-semibold

                                                            ${
                                                                statusStyle[
                                                                    item.case_status
                                                                ]
                                                                ||
                                                                "bg-gray-100 text-gray-700"
                                                            }
                                                        `}
                                                    >
                                                        {
                                                            translateCaseStatus(
                                                                item.case_status
                                                            )
                                                        }
                                                    </span>


                                                </td>



                                                <td className="
                                                    p-4
                                                    align-top
                                                ">


                                                    <span
                                                        className={`
                                                            inline-flex
                                                            px-3
                                                            py-1
                                                            rounded-full
                                                            text-xs
                                                            font-semibold

                                                            ${
                                                                priorityStyle[
                                                                    item.priority
                                                                ]
                                                                ||
                                                                "bg-gray-100 text-gray-700"
                                                            }
                                                        `}
                                                    >
                                                        {
                                                            translatePriority(
                                                                item.priority
                                                            )
                                                        }
                                                    </span>


                                                </td>



                                                <td className="
                                                    p-4
                                                    align-top
                                                ">

                                                    {
                                                        item.assigned_to
                                                        || "Belum ditugaskan"
                                                    }

                                                </td>



                                                <td className="
                                                    p-4
                                                    text-right
                                                    align-top
                                                ">


                                                    <Link
                                                        to={
                                                            `/claims/${item.claim_id}`
                                                        }
                                                        className="
                                                            inline-flex
                                                            bg-blue-600
                                                            text-white
                                                            px-4
                                                            py-2
                                                            rounded-lg
                                                            font-semibold
                                                            hover:bg-blue-700
                                                        "
                                                    >
                                                        Buka Investigasi
                                                    </Link>


                                                </td>


                                            </tr>

                                        )
                                    )

                                )
                            }


                        </tbody>


                    </table>


                </div>



                {/* =====================================
                    PAGINATION
                ===================================== */}


                <div className="
                    flex
                    flex-col
                    sm:flex-row
                    sm:items-center
                    sm:justify-between
                    gap-4
                    border-t
                    p-4
                ">


                    <div className="
                        text-sm
                        text-gray-500
                    ">

                        Halaman{" "}

                        <b>
                            {
                                pagination.total_pages === 0
                                ? 0
                                : pagination.page
                            }
                        </b>

                        {" dari "}

                        <b>
                            {pagination.total_pages}
                        </b>

                    </div>



                    <div className="
                        flex
                        items-center
                        gap-2
                    ">


                        <button
                            onClick={
                                goPrevious
                            }
                            disabled={
                                !pagination.has_previous
                                ||
                                loading
                            }
                            className="
                                inline-flex
                                items-center
                                gap-2
                                border
                                rounded-lg
                                px-4
                                py-2
                                text-sm
                                font-semibold
                                hover:bg-gray-50
                                disabled:opacity-40
                                disabled:cursor-not-allowed
                            "
                        >

                            <ChevronLeft
                                size={16}
                            />

                            Sebelumnya

                        </button>



                        <button
                            onClick={
                                goNext
                            }
                            disabled={
                                !pagination.has_next
                                ||
                                loading
                            }
                            className="
                                inline-flex
                                items-center
                                gap-2
                                border
                                rounded-lg
                                px-4
                                py-2
                                text-sm
                                font-semibold
                                hover:bg-gray-50
                                disabled:opacity-40
                                disabled:cursor-not-allowed
                            "
                        >

                            Berikutnya

                            <ChevronRight
                                size={16}
                            />

                        </button>


                    </div>


                </div>


            </div>



            {/* =====================================
                TRANSLATED FRAUD REASON PREVIEW
            ===================================== */}


            {
                cases.length > 0 && (

                    <div className="
                        mt-6
                        bg-white
                        border
                        rounded-xl
                        p-5
                    ">


                        <div className="
                            font-semibold
                            mb-2
                        ">
                            Contoh Interpretasi Fraud
                        </div>


                        <div className="
                            text-sm
                            text-gray-600
                            leading-relaxed
                        ">
                            {
                                translateFraudReason(
                                    cases[0]?.fraud_reason
                                )
                            }
                        </div>


                    </div>

                )
            }


        </div>

    );

}
