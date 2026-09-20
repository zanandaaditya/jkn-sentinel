import {
    useEffect,
    useMemo,
    useState
} from "react";


import {
    AlertTriangle,
    BriefcaseBusiness,
    CheckSquare2,
    ChevronLeft,
    ChevronRight,
    ExternalLink,
    RefreshCw,
    Search,
    UserRound,
    UsersRound
} from "lucide-react";


import {
    useNavigate
} from "react-router-dom";


import {
    assignFraudCase,
    autoAssignFraudCases,
    bulkAssignFraudCases,
    getInvestigatorDirectory,
    getInvestigatorWorkbench
} from "../api/investigatorWorkbench";


import {
    getActiveInvestigators
} from "../api/investigators";


import {
    translateCaseStatus,
    translatePriority,
    translateRiskLevel
} from "../utils/translations";



const formatDays = (
    value
)=>{

    return `${Number(value || 0).toFixed(1)} hari`;

};

const getSlaLabel = (
    status
)=>{

    const labels = {

        ON_TRACK:
            "Dalam SLA",

        WARNING:
            "Mendekati Batas",

        BREACHED:
            "Melewati SLA",

        CRITICAL:
            "Kritis",

        CLOSED_WITHIN_SLA:
            "Selesai Dalam SLA",

        CLOSED_BREACHED:
            "Selesai Melewati SLA",

        NO_POLICY:
            "Tanpa Kebijakan"

    };


    return (
        labels[status]
        ||
        status
        ||
        "-"
    );

};



const getSlaBadgeClass = (
    status
)=>{

    switch(status){

        case "ON_TRACK":

            return (
                "bg-green-50 text-green-700 border-green-200"
            );


        case "WARNING":

            return (
                "bg-yellow-50 text-yellow-700 border-yellow-200"
            );


        case "BREACHED":

            return (
                "bg-orange-50 text-orange-700 border-orange-200"
            );


        case "CRITICAL":

            return (
                "bg-red-50 text-red-700 border-red-200"
            );


        case "CLOSED_WITHIN_SLA":

            return (
                "bg-blue-50 text-blue-700 border-blue-200"
            );


        case "CLOSED_BREACHED":

            return (
                "bg-red-50 text-red-700 border-red-200"
            );


        default:

            return (
                "bg-gray-50 text-gray-600 border-gray-200"
            );

    }

};



const formatDateTime = (
    value
)=>{

    if(!value){
        return "-";
    }


    return new Intl.DateTimeFormat(
        "id-ID",
        {
            dateStyle:
                "medium",

            timeStyle:
                "short"
        }
    ).format(
        new Date(value)
    );

};



const formatSlaRemaining = (
    hours,
    status
)=>{

    if(
        hours === null
        ||
        hours === undefined
    ){
        return "-";
    }


    const numericHours =
        Number(hours);


    const absoluteHours =
        Math.abs(
            numericHours
        );


    if(absoluteHours < 1){

        const minutes =
            Math.max(
                1,
                Math.round(
                    absoluteHours * 60
                )
            );


        if(
            status === "BREACHED"
            ||
            status === "CRITICAL"
        ){

            return `${minutes} menit terlambat`;

        }


        return `${minutes} menit tersisa`;

    }


    if(absoluteHours < 24){

        const rounded =
            absoluteHours.toFixed(1);


        if(
            status === "BREACHED"
            ||
            status === "CRITICAL"
        ){

            return `${rounded} jam terlambat`;

        }


        return `${rounded} jam tersisa`;

    }


    const days =
        (
            absoluteHours / 24
        ).toFixed(1);


    if(
        status === "BREACHED"
        ||
        status === "CRITICAL"
    ){

        return `${days} hari terlambat`;

    }


    return `${days} hari tersisa`;

};

export default function InvestigatorWorkbench(){


    const navigate =
        useNavigate();


    const [investigators,setInvestigators] =
        useState([]);


    const [
        registryInvestigators,
        setRegistryInvestigators
    ] = useState([]);


    const [result,setResult] =
        useState({

            items: [],

            pagination: {},

            summary: {}

        });


    const [
        selectedInvestigator,
        setSelectedInvestigator
    ] = useState("ALL");


    const [status,setStatus] =
        useState("");


    const [priority,setPriority] =
        useState("");


    const [search,setSearch] =
        useState("");


    const [searchInput,setSearchInput] =
        useState("");

    const [page,setPage] =
        useState(1);


    const [pageSize,setPageSize] =
        useState(10);


    const [loading,setLoading] =
        useState(true);


    const [
        savingCaseId,
        setSavingCaseId
    ] = useState(null);


    const [bulkSaving,setBulkSaving] =
        useState(false);


    const [
        selectedClaimIds,
        setSelectedClaimIds
    ] = useState([]);


    const [
        bulkInvestigatorId,
        setBulkInvestigatorId
    ] = useState("");


    const [error,setError] =
        useState("");


    const [message,setMessage] =
        useState("");


    const [
        assignmentDrafts,
        setAssignmentDrafts
    ] = useState({});



    /*
    =====================================
    OFFICIAL INVESTIGATOR OPTIONS
    =====================================
    */

    const investigatorOptions =
        useMemo(()=>{

            return (
                registryInvestigators
                ||
                []
            ).filter(
                (item)=>
                    item.status === "ACTIVE"
                    &&
                    item.role === "INVESTIGATOR"
            );

        },[
            registryInvestigators
        ]);



    const visibleClaimIds =
        useMemo(()=>{

            return (
                result?.items
                ||
                []
            ).map(
                (item)=>
                    item.claim_id
            );

        },[
            result
        ]);



    const allVisibleSelected =

        visibleClaimIds.length > 0

        &&

        visibleClaimIds.every(
            (claimId)=>
                selectedClaimIds.includes(
                    claimId
                )
        );



    /*
    =====================================
    LOAD INVESTIGATOR QUEUE
    =====================================
    */

    const loadInvestigators = async()=>{


        try{


            const data =
                await getInvestigatorDirectory();


            setInvestigators(
                data || []
            );


        }
        catch(error){


            console.error(
                "INVESTIGATOR DIRECTORY ERROR:",
                error
            );


        }


    };



    /*
    =====================================
    LOAD INVESTIGATOR REGISTRY
    =====================================
    */

    const loadRegistryInvestigators =
        async()=>{


            try{


                const data =
                    await getActiveInvestigators();


                setRegistryInvestigators(
                    data || []
                );


            }
            catch(error){


                console.error(
                    "ACTIVE INVESTIGATORS ERROR:",
                    error
                );


                setError(
                    error?.response?.data?.detail
                    ||
                    "Gagal mengambil daftar investigator."
                );


            }


        };



    /*
    =====================================
    LOAD WORKBENCH
    =====================================
    */

    const loadWorkbench = async()=>{


        try{


            setLoading(true);

            setError("");


            const params = {

                case_status:
                    status || undefined,

                priority:
                    priority || undefined,

                search:
                    search || undefined,

                page,

                page_size:
                    pageSize

            };


            if(
                selectedInvestigator
                ===
                "UNASSIGNED"
            ){


                params.unassigned =
                    true;


            }
            else if(
                selectedInvestigator
                !==
                "ALL"
            ){


                params.assigned_to =
                    selectedInvestigator;


            }


            const data =
                await getInvestigatorWorkbench(
                    params
                );


            setResult(

                data

                ||

                {

                    items: [],

                    pagination: {},

                    summary: {}

                }

            );


            /*
            =====================================
            ASSIGNMENT DRAFTS BY UUID
            =====================================
            */

            const nextDrafts = {};


            (
                data?.items
                ||
                []
            ).forEach(
                (item)=>{


                    nextDrafts[
                        item.case_id
                    ] =
                        item.assigned_investigator_id
                        ||
                        "";


                }
            );


            setAssignmentDrafts(
                nextDrafts
            );


        }
        catch(error){


            console.error(
                "INVESTIGATOR WORKBENCH ERROR:",
                error
            );


            setError(

                error?.response?.data?.detail

                ||

                "Gagal mengambil data workbench investigator."

            );


        }
        finally{


            setLoading(false);


        }


    };



    /*
    =====================================
    INITIAL / REFRESH LOAD
    =====================================
    */

    useEffect(()=>{

        loadInvestigators();

        loadRegistryInvestigators();

    },[]);



    useEffect(()=>{


        setSelectedClaimIds(
            []
        );


        loadWorkbench();


    },[
        selectedInvestigator,
        status,
        priority,
        search,
        page,
        pageSize
    ]);



    /*
    =====================================
    SEARCH DEBOUNCE
    =====================================
    */

    useEffect(()=>{


        const timer =
            setTimeout(()=>{


                setPage(1);


                setSearch(
                    searchInput.trim()
                );


            },350);


        return ()=>{


            clearTimeout(
                timer
            );


        };


    },[
        searchInput
    ]);



    const refreshAll = async()=>{


        await Promise.all([

            loadInvestigators(),

            loadRegistryInvestigators(),

            loadWorkbench()

        ]);


    };



    /*
    =====================================
    SINGLE ASSIGNMENT
    =====================================
    */

    const handleAssign = async(
        item
    )=>{


        try{


            setSavingCaseId(
                item.case_id
            );


            setError("");

            setMessage("");


            const investigatorId =

                assignmentDrafts[
                    item.case_id
                ]

                ||

                null;


            const selected =
                investigatorOptions.find(
                    (investigator)=>
                        investigator.id
                        ===
                        investigatorId
                );


            await assignFraudCase(

                item.claim_id,

                investigatorId

            );


            setMessage(

                selected

                ?

                `Kasus ${item.claim_code} berhasil ditugaskan kepada ${selected.full_name}.`

                :

                `Penugasan kasus ${item.claim_code} berhasil dilepas.`

            );


            await refreshAll();


        }
        catch(error){


            console.error(
                "ASSIGN CASE ERROR:",
                error
            );


            setError(

                error?.response?.data?.detail

                ||

                "Gagal mengubah penugasan kasus."

            );


        }
        finally{


            setSavingCaseId(
                null
            );


        }


    };



    /*
    =====================================
    CHECKBOX
    =====================================
    */

    const toggleClaim = (
        claimId
    )=>{


        setSelectedClaimIds(
            (previous)=>{


                if(
                    previous.includes(
                        claimId
                    )
                ){


                    return previous.filter(
                        (id)=>
                            id !== claimId
                    );


                }


                return [

                    ...previous,

                    claimId

                ];


            }
        );


    };



    const toggleVisible = ()=>{


        setSelectedClaimIds(
            (previous)=>{


                if(
                    allVisibleSelected
                ){


                    return previous.filter(
                        (claimId)=>
                            !visibleClaimIds.includes(
                                claimId
                            )
                    );


                }


                return Array.from(
                    new Set([

                        ...previous,

                        ...visibleClaimIds

                    ])
                );


            }
        );


    };



    /*
    =====================================
    BULK ASSIGNMENT
    =====================================
    */

        const handleAutoAssign = async()=>{


        if(
            selectedClaimIds.length === 0
        ){

            setError(
                "Pilih minimal satu kasus."
            );

            return;

        }


        try{


            setBulkSaving(true);

            setError("");

            setMessage("");


            const response =
                await autoAssignFraudCases(
                    selectedClaimIds
                );


            setMessage(
                `${response.assigned} kasus berhasil dialokasikan otomatis. `
                +
                `${response.skipped} kasus dilewati.`
            );


            setSelectedClaimIds(
                []
            );


            await refreshAll();


        }
        catch(error){


            console.error(
                "AUTO ASSIGN ERROR:",
                error
            );


            setError(
                error?.response?.data?.detail
                ||
                "Auto assignment gagal."
            );


        }
        finally{


            setBulkSaving(false);


        }


    };

    const pagination =
        result?.pagination
        ||
        {};


    const summary =
        result?.summary
        ||
        {};



    return (

        <div className="
            pb-12
        ">


            {/* HEADER */}

            <div className="
                flex
                flex-col
                lg:flex-row
                lg:items-start
                lg:justify-between
                gap-4
                mb-8
            ">


                <div>


                    <div className="
                        text-sm
                        text-gray-500
                        mb-2
                    ">
                        Fraud Operations
                    </div>


                        <h1 className="
                            text-3xl
                            font-bold
                        ">
                            Investigator Workbench
                        </h1>


                        <p className="
                            text-gray-500
                            mt-2
                        ">
                            Distribusi penugasan,
                            antrean investigator,
                            bulk assignment,
                            case aging,
                            dan pemantauan SLA investigasi.
                        </p>
                        <div className="
                            flex
                            flex-wrap
                            gap-2
                            mt-4
                        ">

                            <SlaPolicyChip
                                label="URGENT"
                                value="24 Jam"
                            />

                            <SlaPolicyChip
                                label="HIGH"
                                value="72 Jam"
                            />

                            <SlaPolicyChip
                                label="MEDIUM"
                                value="7 Hari"
                            />

                            <SlaPolicyChip
                                label="NORMAL"
                                value="14 Hari"
                            />

                            <SlaPolicyChip
                                label="LOW"
                                value="30 Hari"
                            />

                        </div>

                    </div>



                    <div className="
                        flex
                        gap-3
                    ">


                        <div className="
                            border
                            rounded-lg
                            px-4
                            py-2.5
                            bg-white
                            text-sm
                        ">
                            <span className="
                                text-gray-500
                            ">
                                SLA:
                            </span>

                            <span className="
                                font-semibold
                                ml-2
                            ">
                                Otomatis Berdasarkan Prioritas
                            </span>
                        </div>



                    <button
                        onClick={
                            refreshAll
                        }
                        className="
                            inline-flex
                            items-center
                            gap-2
                            border
                            rounded-lg
                            px-4
                            py-2.5
                            font-semibold
                            hover:bg-gray-50
                        "
                    >

                        <RefreshCw
                            size={17}
                        />

                        Muat Ulang

                    </button>


                </div>


            </div>



            {/* MESSAGES */}

            {
                message && (

                    <div className="
                        mb-6
                        bg-green-50
                        border
                        border-green-200
                        text-green-700
                        rounded-xl
                        p-4
                    ">
                        {message}
                    </div>

                )
            }



            {
                error && (

                    <div className="
                        mb-6
                        bg-red-50
                        border
                        border-red-200
                        text-red-700
                        rounded-xl
                        p-4
                    ">
                        {error}
                    </div>

                )
            }



            {/* KPI */}

            <div className="
                grid
                grid-cols-1
                sm:grid-cols-2
                xl:grid-cols-4
                gap-5
                mb-8
            ">

                <KpiCard
                    title="Kasus pada Tampilan"
                    value={
                        Number(
                            summary.total_cases
                            ||
                            0
                        )
                        .toLocaleString(
                            "id-ID"
                        )
                    }
                    icon={
                        BriefcaseBusiness
                    }
                />


                <KpiCard
                    title="Kasus Aktif"
                    value={
                        Number(
                            summary.active_cases
                            ||
                            0
                        )
                        .toLocaleString(
                            "id-ID"
                        )
                    }
                    icon={
                        UsersRound
                    }
                />


                <KpiCard
                    title="Belum Ditugaskan"
                    value={
                        Number(
                            summary.unassigned_cases
                            ||
                            0
                        )
                        .toLocaleString(
                            "id-ID"
                        )
                    }
                    icon={
                        UserRound
                    }
                />


                <KpiCard
                    title="Melewati SLA"
                    value={
                        Number(
                            summary.overdue_cases
                            ||
                            0
                        )
                        .toLocaleString(
                            "id-ID"
                        )
                    }
                    icon={
                        AlertTriangle
                    }
                />
                <KpiCard
                    title="Warning SLA"
                    value={
                        Number(
                            summary.warning_cases
                            ||
                            0
                        ).toLocaleString(
                            "id-ID"
                        )
                    }
                    icon={
                        AlertTriangle
                    }
                />


                <KpiCard
                    title="SLA Kritis"
                    value={
                        Number(
                            summary.critical_cases
                            ||
                            0
                        ).toLocaleString(
                            "id-ID"
                        )
                    }
                    icon={
                        AlertTriangle
                    }
                />


            </div>



            {/* BULK ASSIGNMENT */}

            <div className="
                bg-white
                border
                rounded-xl
                p-5
                mb-6
            ">


                <div className="
                    flex
                    flex-col
                    xl:flex-row
                    xl:items-end
                    xl:justify-between
                    gap-5
                ">


                    <div>


                        <div className="
                            flex
                            items-center
                            gap-2
                        ">


                            <CheckSquare2
                                size={19}
                                className="
                                    text-blue-600
                                "
                            />


                            <h2 className="
                                font-bold
                                text-lg
                            ">
                                Bulk Assignment
                            </h2>


                        </div>


                        <p className="
                            text-sm
                            text-gray-500
                            mt-2
                        ">

                            {
                                selectedClaimIds.length
                            }

                            {" kasus dipilih."}

                        </p>


                    </div>



                    <div className="
                        flex
                        flex-col
                        md:flex-row
                        gap-3
                        xl:min-w-[650px]
                    ">


                        <select
                            value={
                                bulkInvestigatorId
                            }
                            onChange={
                                (event)=>
                                    setBulkInvestigatorId(
                                        event.target.value
                                    )
                            }
                            className="
                                flex-1
                                border
                                rounded-lg
                                px-4
                                py-2.5
                                bg-white
                            "
                        >


                            <option value="">
                                Pilih Investigator
                            </option>


                            {
                                investigatorOptions.map(
                                    (investigator)=>{


                                        const active =
                                            Number(
                                                investigator.active_cases
                                                ||
                                                0
                                            );


                                        const capacity =
                                            Number(
                                                investigator.max_active_cases
                                                ||
                                                0
                                            );


                                        return (

                                            <option
                                                key={investigator.id}
                                                value={investigator.id}
                                                disabled={
                                                    Number(
                                                        investigator.active_cases || 0
                                                    )
                                                    >=
                                                    Number(
                                                        investigator.max_active_cases || 0
                                                    )
                                                }
                                            >

                                                {
                                                    investigator.full_name
                                                }

                                                {" · "}

                                                {
                                                    investigator.active_cases
                                                }

                                                {"/"}

                                                {
                                                    investigator.max_active_cases
                                                }

                                                {
                                                    Number(
                                                        investigator.active_cases || 0
                                                    )
                                                    >=
                                                    Number(
                                                        investigator.max_active_cases || 0
                                                    )
                                                    ? " · PENUH"
                                                    : " aktif"
                                                }

                                            </option>

                                        );


                                    }
                                )
                            }


                        </select>


                        <button
                            onClick={
                                handleAutoAssign
                            }
                            disabled={
                                bulkSaving
                                ||
                                selectedClaimIds.length === 0
                            }
                            className="
                                border
                                border-blue-600
                                text-blue-700
                                rounded-lg
                                px-5
                                py-2.5
                                font-semibold
                                hover:bg-blue-50
                                disabled:opacity-50
                            "
                        >
                            Auto Assign
                        </button>

                        <button
                            onClick={()=>
                                handleBulkAssign(
                                    bulkInvestigatorId
                                )
                            }
                            disabled={
                                bulkSaving
                                ||
                                selectedClaimIds.length
                                ===
                                0
                                ||
                                !bulkInvestigatorId
                            }
                            className="
                                bg-blue-600
                                text-white
                                rounded-lg
                                px-5
                                py-2.5
                                font-semibold
                                hover:bg-blue-700
                                disabled:opacity-50
                            "
                        >

                            {
                                bulkSaving

                                ?

                                "Menyimpan..."

                                :

                                "Tugaskan Terpilih"
                            }

                        </button>



                        <button
                            onClick={()=>
                                handleBulkAssign(
                                    null
                                )
                            }
                            disabled={
                                bulkSaving
                                ||
                                selectedClaimIds.length
                                ===
                                0
                            }
                            className="
                                border
                                rounded-lg
                                px-5
                                py-2.5
                                font-semibold
                                hover:bg-gray-50
                                disabled:opacity-50
                            "
                        >
                            Lepas Penugasan
                        </button>


                    </div>


                </div>


            </div>



            {/* INVESTIGATOR QUEUE */}

            <div className="
                bg-white
                border
                rounded-xl
                p-5
                mb-6
            ">


                <h2 className="
                    font-bold
                    text-lg
                ">
                    Antrean Investigator
                </h2>


                <p className="
                    text-sm
                    text-gray-500
                    mt-1
                    mb-4
                ">
                    Pilih investigator untuk melihat antrean kasusnya.
                </p>



                <div className="
                    flex
                    flex-wrap
                    gap-3
                ">


                    <QueueButton
                        active={
                            selectedInvestigator
                            ===
                            "ALL"
                        }
                        onClick={()=>{


                            setPage(1);


                            setSelectedInvestigator(
                                "ALL"
                            );


                        }}
                        title="Semua Kasus"
                    />


                    {
                        investigators.map(
                            (item)=>{


                                const isUnassigned =

                                    item.investigator

                                    ===

                                    "Belum Ditugaskan";


                                const value =

                                    isUnassigned

                                    ?

                                    "UNASSIGNED"

                                    :

                                    item.investigator;


                                return (

                                    <QueueButton
                                        key={
                                            item.investigator
                                        }
                                        active={
                                            selectedInvestigator
                                            ===
                                            value
                                        }
                                        onClick={()=>{


                                            setPage(1);


                                            setSelectedInvestigator(
                                                value
                                            );


                                        }}
                                        title={
                                            item.investigator
                                        }
                                        subtitle={
                                            `${item.active_cases} aktif · ${item.overdue_cases} lewat SLA`
                                        }
                                    />

                                );


                            }
                        )
                    }


                </div>


            </div>



            {/* FILTER */}

            <div className="
                bg-white
                border
                rounded-xl
                p-5
                mb-6
            ">


                <div className="
                    grid
                    grid-cols-1
                    md:grid-cols-2
                    xl:grid-cols-4
                    gap-4
                ">


                    <div className="
                        relative
                    ">


                        <Search
                            size={17}
                            className="
                                absolute
                                left-3
                                top-3
                                text-gray-400
                            "
                        />


                        <input
                            value={
                                searchInput
                            }
                            onChange={
                                (event)=>
                                    setSearchInput(
                                        event.target.value
                                    )
                            }
                            placeholder="Cari klaim, fasilitas, diagnosis..."
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
                        value={
                            status
                        }
                        onChange={
                            (event)=>{


                                setPage(1);


                                setStatus(
                                    event.target.value
                                );


                            }
                        }
                        className="
                            border
                            rounded-lg
                            px-4
                            py-2.5
                            bg-white
                        "
                    >

                        <option value="">
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
                        value={
                            priority
                        }
                        onChange={
                            (event)=>{


                                setPage(1);


                                setPriority(
                                    event.target.value
                                );


                            }
                        }
                        className="
                            border
                            rounded-lg
                            px-4
                            py-2.5
                            bg-white
                        "
                    >

                        <option value="">
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



                    <select
                        value={
                            pageSize
                        }
                        onChange={
                            (event)=>{


                                setPage(1);


                                setPageSize(
                                    Number(
                                        event.target.value
                                    )
                                );


                            }
                        }
                        className="
                            border
                            rounded-lg
                            px-4
                            py-2.5
                            bg-white
                        "
                    >

                        <option value={5}>
                            5 per halaman
                        </option>

                        <option value={10}>
                            10 per halaman
                        </option>

                        <option value={20}>
                            20 per halaman
                        </option>

                        <option value={50}>
                            50 per halaman
                        </option>

                    </select>


                </div>


            </div>



            {/* TABLE */}

            <div className="
                bg-white
                border
                rounded-xl
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
                            text-gray-600
                        ">


                            <tr>


                                <th className="
                                    px-5
                                    py-3
                                    text-center
                                ">

                                    <input
                                        type="checkbox"
                                        checked={
                                            allVisibleSelected
                                        }
                                        onChange={
                                            toggleVisible
                                        }
                                    />

                                </th>


                                <th className="text-left px-5 py-3">
                                    Klaim
                                </th>

                                <th className="text-left px-5 py-3">
                                    Fasilitas
                                </th>

                                <th className="text-left px-5 py-3">
                                    Risiko
                                </th>

                                <th className="text-left px-5 py-3">
                                    Status
                                </th>

                                <th className="text-left px-5 py-3">
                                    Prioritas
                                </th>

                                <th className="text-left px-5 py-3">
                                    SLA
                                </th>

                                <th className="text-left px-5 py-3">
                                    Investigator
                                </th>

                                <th className="text-center px-5 py-3">
                                    Aksi
                                </th>


                            </tr>


                        </thead>



                        <tbody>


                            {
                                loading

                                ?

                                (

                                    <tr>

                                        <td
                                            colSpan="9"
                                            className="
                                                px-5
                                                py-12
                                                text-center
                                                text-gray-500
                                            "
                                        >
                                            Memuat antrean kasus...
                                        </td>

                                    </tr>

                                )

                                :

                                result.items.length
                                ===
                                0

                                ?

                                (

                                    <tr>

                                        <td
                                            colSpan="9"
                                            className="
                                                px-5
                                                py-12
                                                text-center
                                                text-gray-500
                                            "
                                        >
                                            Tidak ada kasus yang sesuai filter.
                                        </td>

                                    </tr>

                                )

                                :

                                result.items.map(
                                    (item)=>(

                                        <tr
                                            key={
                                                item.case_id
                                            }
                                            className={`
                                                border-t
                                                align-top

                                                ${
                                                    item.sla_status === "CRITICAL"
                                                    ?
                                                    "bg-red-50/40"
                                                    :
                                                    ""
                                                }

                                                ${
                                                    item.sla_status === "BREACHED"
                                                    ?
                                                    "bg-orange-50/30"
                                                    :
                                                    ""
                                                }

                                                ${
                                                    item.sla_status === "WARNING"
                                                    ?
                                                    "bg-yellow-50/20"
                                                    :
                                                    ""
                                                }
                                            `}
                                        >


                                            <td className="
                                                px-5
                                                py-4
                                                text-center
                                            ">

                                                <input
                                                    type="checkbox"
                                                    checked={
                                                        selectedClaimIds.includes(
                                                            item.claim_id
                                                        )
                                                    }
                                                    onChange={()=>
                                                        toggleClaim(
                                                            item.claim_id
                                                        )
                                                    }
                                                />

                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                            ">


                                                <div className="
                                                    font-semibold
                                                ">
                                                    {item.claim_code}
                                                </div>


                                                <div className="
                                                    text-xs
                                                    text-gray-500
                                                    mt-1
                                                ">
                                                    Fraud Score {item.fraud_score}
                                                </div>


                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                            ">


                                                <div>
                                                    {item.facility || "-"}
                                                </div>


                                                <div className="
                                                    text-xs
                                                    text-gray-500
                                                    mt-1
                                                ">
                                                    {item.diagnosis || "-"}
                                                </div>


                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                            ">
                                                {
                                                    translateRiskLevel(
                                                        item.risk_level
                                                    )
                                                }
                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                            ">
                                                {
                                                    translateCaseStatus(
                                                        item.case_status
                                                    )
                                                }
                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                            ">
                                                {
                                                    translatePriority(
                                                        item.priority
                                                    )
                                                }
                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                                min-w-[220px]
                                            ">

                                                <div className="
                                                    flex
                                                    items-center
                                                    gap-2
                                                    mb-2
                                                ">

                                                    <span
                                                        className={`
                                                            inline-flex
                                                            items-center
                                                            px-2.5
                                                            py-1
                                                            rounded-full
                                                            border
                                                            text-xs
                                                            font-semibold

                                                            ${getSlaBadgeClass(
                                                                item.sla_status
                                                            )}
                                                        `}
                                                    >

                                                        {
                                                            getSlaLabel(
                                                                item.sla_status
                                                            )
                                                        }

                                                    </span>

                                                </div>


                                                <div className="
                                                    text-sm
                                                    font-semibold
                                                ">

                                                    {
                                                        formatSlaRemaining(
                                                            item.sla_remaining_hours,
                                                            item.sla_status
                                                        )
                                                    }

                                                </div>


                                                <div className="
                                                    text-xs
                                                    text-gray-500
                                                    mt-1
                                                ">

                                                    Deadline:

                                                    {" "}

                                                    {
                                                        formatDateTime(
                                                            item.sla_due_at
                                                        )
                                                    }

                                                </div>


                                                <div className="
                                                    text-xs
                                                    text-gray-400
                                                    mt-1
                                                ">

                                                    {
                                                        item.sla_hours
                                                        ?
                                                        `${item.sla_hours} jam · ${item.priority}`
                                                        :
                                                        "Policy SLA tidak tersedia"
                                                    }

                                                </div>

                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                                min-w-[280px]
                                            ">


                                                <select
                                                    value={
                                                        assignmentDrafts[
                                                            item.case_id
                                                        ]
                                                        ||
                                                        ""
                                                    }
                                                    onChange={
                                                        (event)=>
                                                            setAssignmentDrafts(
                                                                (previous)=>({

                                                                    ...previous,

                                                                    [item.case_id]:
                                                                        event.target.value

                                                                })
                                                            )
                                                    }
                                                    className="
                                                        w-full
                                                        border
                                                        rounded-lg
                                                        px-3
                                                        py-2
                                                        bg-white
                                                    "
                                                >


                                                    <option value="">
                                                        Belum Ditugaskan
                                                    </option>


                                                    {
                                                        investigatorOptions.map(
                                                            (investigator)=>{


                                                                const active =
                                                                    Number(
                                                                        investigator.active_cases
                                                                        ||
                                                                        0
                                                                    );


                                                                const capacity =
                                                                    Number(
                                                                        investigator.max_active_cases
                                                                        ||
                                                                        0
                                                                    );


                                                                return (

                                                                    <option
                                                                        key={investigator.id}
                                                                        value={investigator.id}
                                                                        disabled={
                                                                            Number(
                                                                                investigator.active_cases || 0
                                                                            )
                                                                            >=
                                                                            Number(
                                                                                investigator.max_active_cases || 0
                                                                            )
                                                                        }
                                                                    >

                                                                        {
                                                                            investigator.full_name
                                                                        }

                                                                        {" · "}

                                                                        {
                                                                            investigator.active_cases
                                                                        }

                                                                        {"/"}

                                                                        {
                                                                            investigator.max_active_cases
                                                                        }

                                                                        {
                                                                            Number(
                                                                                investigator.active_cases || 0
                                                                            )
                                                                            >=
                                                                            Number(
                                                                                investigator.max_active_cases || 0
                                                                            )
                                                                            ? " · PENUH"
                                                                            : " aktif"
                                                                        }

                                                                    </option>

                                                                );


                                                            }
                                                        )
                                                    }


                                                </select>


                                                {
                                                    item.assigned_to && (

                                                        <div className="
                                                            text-xs
                                                            text-gray-500
                                                            mt-2
                                                        ">
                                                            Saat ini: {item.assigned_to}
                                                        </div>

                                                    )
                                                }


                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                            ">


                                                <div className="
                                                    flex
                                                    items-center
                                                    justify-center
                                                    gap-2
                                                ">


                                                    <button
                                                        onClick={()=>
                                                            handleAssign(
                                                                item
                                                            )
                                                        }
                                                        disabled={
                                                            savingCaseId
                                                            ===
                                                            item.case_id
                                                        }
                                                        className="
                                                            border
                                                            rounded-lg
                                                            px-3
                                                            py-2
                                                            font-semibold
                                                            hover:bg-gray-50
                                                            disabled:opacity-50
                                                        "
                                                    >

                                                        {
                                                            savingCaseId
                                                            ===
                                                            item.case_id

                                                            ?

                                                            "Menyimpan..."

                                                            :

                                                            "Simpan"
                                                        }

                                                    </button>



                                                    <button
                                                        onClick={()=>
                                                            navigate(
                                                                `/claims/${item.claim_id}`
                                                            )
                                                        }
                                                        className="
                                                            inline-flex
                                                            items-center
                                                            justify-center
                                                            border
                                                            rounded-lg
                                                            p-2
                                                            hover:bg-gray-50
                                                        "
                                                        title="Buka detail klaim"
                                                    >

                                                        <ExternalLink
                                                            size={17}
                                                        />

                                                    </button>


                                                </div>


                                            </td>


                                        </tr>

                                    )
                                )
                            }


                        </tbody>


                    </table>


                </div>



                {/* PAGINATION */}

                <div className="
                    flex
                    flex-col
                    sm:flex-row
                    sm:items-center
                    sm:justify-between
                    gap-4
                    border-t
                    px-5
                    py-4
                ">


                    <div className="
                        text-sm
                        text-gray-500
                    ">

                        {
                            Number(
                                pagination.total
                                ||
                                0
                            )
                            .toLocaleString(
                                "id-ID"
                            )
                        }

                        {" kasus · Halaman "}

                        {
                            pagination.page
                            ||
                            1
                        }

                        {" dari "}

                        {
                            pagination.total_pages
                            ||
                            1
                        }

                    </div>



                    <div className="
                        flex
                        gap-2
                    ">


                        <button
                            disabled={
                                !pagination.has_previous
                            }
                            onClick={()=>
                                setPage(
                                    (previous)=>
                                        Math.max(
                                            1,
                                            previous - 1
                                        )
                                )
                            }
                            className="
                                inline-flex
                                items-center
                                gap-2
                                border
                                rounded-lg
                                px-3
                                py-2
                                disabled:opacity-40
                            "
                        >

                            <ChevronLeft
                                size={16}
                            />

                            Sebelumnya

                        </button>



                        <button
                            disabled={
                                !pagination.has_next
                            }
                            onClick={()=>
                                setPage(
                                    (previous)=>
                                        previous + 1
                                )
                            }
                            className="
                                inline-flex
                                items-center
                                gap-2
                                border
                                rounded-lg
                                px-3
                                py-2
                                disabled:opacity-40
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


        </div>

    );

}



function KpiCard({
    title,
    value,
    icon: Icon
}){


    return (

        <div className="
            bg-white
            border
            rounded-xl
            p-5
        ">


            <div className="
                flex
                items-start
                justify-between
                gap-4
            ">


                <div>


                    <div className="
                        text-sm
                        text-gray-500
                    ">
                        {title}
                    </div>


                    <div className="
                        text-2xl
                        font-bold
                        mt-2
                    ">
                        {value}
                    </div>


                </div>



                <div className="
                    w-10
                    h-10
                    rounded-lg
                    bg-gray-50
                    flex
                    items-center
                    justify-center
                ">

                    <Icon
                        size={20}
                        className="
                            text-blue-600
                        "
                    />

                </div>


            </div>


        </div>

    );

}



function QueueButton({
    active,
    onClick,
    title,
    subtitle
}){


    return (

        <button
            onClick={
                onClick
            }
            className={
                active

                ?

                "border border-blue-500 bg-blue-50 rounded-xl px-4 py-3 text-left"

                :

                "border rounded-xl px-4 py-3 text-left hover:bg-gray-50"
            }
        >


            <div className="
                font-semibold
            ">
                {title}
            </div>


            {
                subtitle && (

                    <div className="
                        text-xs
                        text-gray-500
                        mt-1
                    ">
                        {subtitle}
                    </div>

                )
            }


        </button>

    );

}

function SlaPolicyChip({
    label,
    value
}){

    return (

        <div className="
            inline-flex
            items-center
            gap-2
            border
            bg-white
            rounded-full
            px-3
            py-1.5
            text-xs
        ">

            <span className="
                text-gray-500
            ">
                {label}
            </span>


            <span className="
                font-semibold
            ">
                {value}
            </span>

        </div>

    );

}