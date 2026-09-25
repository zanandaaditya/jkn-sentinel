import {
    useEffect,
    useMemo,
    useState
} from "react";


import {
    AlertTriangle,
    CheckCircle2,
    CircleDollarSign,
    Clock3,
    RefreshCw,
    ShieldCheck,
    UserRound,
    WalletCards
} from "lucide-react";


import {
    BarChart,
    Bar,
    CartesianGrid,
    Legend,
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis
} from "recharts";


import {
    getFraudAnalytics,
    getInvestigatorAnalytics
} from "../api/fraudAnalytics";


import {
    formatRupiah,
    translateCaseStatus,
    translatePriority,
    translateRiskLevel
} from "../utils/translations";


const STATUS_COLORS = [
    "#2563eb",
    "#f59e0b",
    "#dc2626",
    "#16a34a",
    "#64748b"
];


const PRIORITY_COLORS = [
    "#dc2626",
    "#f97316",
    "#eab308",
    "#64748b",
    "#16a34a"
];


const RISK_COLORS = [
    "#dc2626",
    "#f59e0b",
    "#16a34a",
    "#64748b"
];


const AGING_COLORS = [
    "#16a34a",
    "#eab308",
    "#f97316",
    "#dc2626"
];


const agingLabel = {

    "0-3_DAYS":
        "0–3 hari",

    "4-7_DAYS":
        "4–7 hari",

    "8-14_DAYS":
        "8–14 hari",

    "OVER_14_DAYS":
        ">14 hari"

};


const formatPercent = (value)=>{

    return `${Number(value || 0).toFixed(1)}%`;

};


const formatDays = (value)=>{

    return `${Number(value || 0).toFixed(1)} hari`;

};


export default function FraudAnalytics(){


    const [data,setData] =
        useState(null);


    const [investigatorData,setInvestigatorData] =
        useState(null);


    const [slaDays,setSlaDays] =
        useState(7);


    const [loading,setLoading] =
        useState(true);


    const [error,setError] =
        useState("");


    const loadAnalytics = async()=>{


        try{


            setLoading(true);

            setError("");


            const [
                fraudResult,
                investigatorResult
            ] = await Promise.all([

                getFraudAnalytics(),

                getInvestigatorAnalytics(
                    slaDays
                )

            ]);


            setData(
                fraudResult || null
            );


            setInvestigatorData(
                investigatorResult || null
            );


        }
        catch(error){


            console.error(
                "FRAUD ANALYTICS ERROR:",
                error
            );


            setError(
                error?.response?.data?.detail
                ||
                "Gagal mengambil data analitik fraud."
            );


        }
        finally{


            setLoading(false);


        }


    };


    useEffect(()=>{


        loadAnalytics();


    },[slaDays]);


    const statusData =
        useMemo(()=>{

            return (
                data?.status_distribution
                ||
                []
            ).map(
                (item)=>({

                    ...item,

                    label:
                        translateCaseStatus(
                            item.case_status
                        ),

                    total:
                        Number(
                            item.total || 0
                        )

                })
            );

        },[data]);


    const priorityData =
        useMemo(()=>{

            return (
                data?.priority_distribution
                ||
                []
            ).map(
                (item)=>({

                    ...item,

                    label:
                        translatePriority(
                            item.priority
                        ),

                    total:
                        Number(
                            item.total || 0
                        )

                })
            );

        },[data]);


    const riskData =
        useMemo(()=>{

            return (
                data?.risk_distribution
                ||
                []
            ).map(
                (item)=>({

                    ...item,

                    label:
                        translateRiskLevel(
                            item.risk_level
                        ),

                    total:
                        Number(
                            item.total || 0
                        )

                })
            );

        },[data]);


    const agingData =
        useMemo(()=>{

            return (
                investigatorData?.aging_distribution
                ||
                []
            ).map(
                (item)=>({

                    ...item,

                    label:
                        agingLabel[
                            item.bucket
                        ]
                        ||
                        item.bucket,

                    total:
                        Number(
                            item.total || 0
                        )

                })
            );

        },[investigatorData]);


    const workloadData =
        useMemo(()=>{

            return (
                investigatorData?.investigator_performance
                ||
                []
            ).map(
                (item)=>({

                    ...item,

                    active_cases:
                        Number(
                            item.active_cases || 0
                        ),

                    closed_cases:
                        Number(
                            item.closed_cases || 0
                        ),

                    overdue_cases:
                        Number(
                            item.overdue_cases || 0
                        )

                })
            );

        },[investigatorData]);


    const financial =
        data?.financial_summary
        ||
        {};


    const summary =
        data?.summary
        ||
        {};


    const slaSummary =
        investigatorData?.summary
        ||
        {};


    if(loading){

        return (

            <div className="
                p-6
                text-gray-500
            ">
                Memuat analitik fraud...
            </div>

        );

    }


    return (

        <div className="
            pb-12
        ">


            <div className="
                flex
                flex-col
                md:flex-row
                md:items-start
                md:justify-between
                gap-4
                mb-8
            ">


                <div>


                    <div className="
                        text-sm
                        text-gray-500
                        mb-2
                    ">
                        Fraud Investigation Analytics
                    </div>


                    <h1 className="
                        text-3xl
                        font-bold
                    ">
                        Dashboard Analitik Fraud
                    </h1>


                    <p className="
                        text-gray-500
                        mt-2
                    ">
                        Ringkasan hasil investigasi, dampak finansial, kinerja investigator, case aging, dan pemantauan SLA.
                    </p>


                </div>


                <div className="
                    flex
                    flex-col
                    sm:flex-row
                    gap-3
                ">


                    <select
                        value={slaDays}
                        onChange={
                            (event)=>
                                setSlaDays(
                                    Number(
                                        event.target.value
                                    )
                                )
                        }
                        className="
                            border
                            rounded-lg
                            px-4
                            py-2.5
                            bg-white
                        "
                    >

                        <option value={3}>
                            SLA 3 Hari
                        </option>

                        <option value={7}>
                            SLA 7 Hari
                        </option>

                        <option value={14}>
                            SLA 14 Hari
                        </option>

                        <option value={30}>
                            SLA 30 Hari
                        </option>

                    </select>


                    <button
                        onClick={
                            loadAnalytics
                        }
                        className="
                            inline-flex
                            items-center
                            justify-center
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


            <div className="
                grid
                grid-cols-1
                sm:grid-cols-2
                xl:grid-cols-4
                gap-5
                mb-8
            ">


                <KpiCard
                    title="Total Kasus"
                    value={
                        Number(
                            summary.total_cases || 0
                        ).toLocaleString("id-ID")
                    }
                    subtitle={
                        `${Number(summary.confirmed_cases || 0).toLocaleString("id-ID")} terindikasi fraud`
                    }
                    icon={ShieldCheck}
                />


                <KpiCard
                    title="Kerugian Terkonfirmasi"
                    value={
                        formatRupiah(
                            financial.total_confirmed_loss || 0
                        )
                    }
                    subtitle="Nilai kerugian hasil investigasi"
                    icon={AlertTriangle}
                />


                <KpiCard
                    title="Nilai Pemulihan"
                    value={
                        formatRupiah(
                            financial.total_recovered_amount || 0
                        )
                    }
                    subtitle={
                        `Recovery rate ${formatPercent(financial.recovery_rate)}`
                    }
                    icon={CircleDollarSign}
                />


                <KpiCard
                    title="Sisa Kerugian"
                    value={
                        formatRupiah(
                            financial.outstanding_loss || 0
                        )
                    }
                    subtitle="Kerugian yang belum dipulihkan"
                    icon={WalletCards}
                />


            </div>


            <div className="
                grid
                grid-cols-1
                md:grid-cols-3
                gap-5
                mb-8
            ">


                <KpiCard
                    title="Rata-rata Umur Kasus Aktif"
                    value={
                        formatDays(
                            slaSummary.avg_active_case_age_days
                        )
                    }
                    subtitle={`Batas SLA saat ini ${slaDays} hari`}
                    icon={Clock3}
                />


                <KpiCard
                    title="Kasus Melewati SLA"
                    value={
                        Number(
                            slaSummary.overdue_active_cases || 0
                        ).toLocaleString("id-ID")
                    }
                    subtitle="Kasus aktif yang membutuhkan perhatian"
                    icon={AlertTriangle}
                />


                <KpiCard
                    title="SLA Compliance Rate"
                    value={
                        formatPercent(
                            slaSummary.sla_compliance_rate
                        )
                    }
                    subtitle="Persentase kasus selesai dalam SLA"
                    icon={CheckCircle2}
                />


            </div>


            <div className="
                grid
                grid-cols-1
                xl:grid-cols-2
                gap-6
                mb-6
            ">


                <ChartCard
                    title="Distribusi Status Kasus"
                    subtitle="Komposisi tahapan penanganan kasus fraud."
                >

                    <ResponsiveContainer
                        width="100%"
                        height={320}
                    >

                        <PieChart>

                            <Pie
                                data={statusData}
                                dataKey="total"
                                nameKey="label"
                                cx="50%"
                                cy="50%"
                                outerRadius={105}
                                label={
                                    ({label,total})=>
                                        `${label}: ${total}`
                                }
                            >

                                {
                                    statusData.map(
                                        (item,index)=>(

                                            <Cell
                                                key={
                                                    `${item.case_status}-${index}`
                                                }
                                                fill={
                                                    STATUS_COLORS[
                                                        index
                                                        %
                                                        STATUS_COLORS.length
                                                    ]
                                                }
                                            />

                                        )
                                    )
                                }

                            </Pie>

                            <Tooltip />

                        </PieChart>

                    </ResponsiveContainer>

                </ChartCard>


                <ChartCard
                    title="Distribusi Prioritas"
                    subtitle="Jumlah kasus berdasarkan tingkat prioritas investigasi."
                >

                    <ResponsiveContainer
                        width="100%"
                        height={320}
                    >

                        <BarChart
                            data={priorityData}
                            margin={{
                                top: 10,
                                right: 10,
                                left: 0,
                                bottom: 20
                            }}
                        >

                            <CartesianGrid
                                strokeDasharray="3 3"
                            />

                            <XAxis
                                dataKey="label"
                                interval={0}
                            />

                            <YAxis
                                allowDecimals={false}
                            />

                            <Tooltip />

                            <Bar
                                dataKey="total"
                                name="Jumlah Kasus"
                            >

                                {
                                    priorityData.map(
                                        (item,index)=>(

                                            <Cell
                                                key={
                                                    `${item.priority}-${index}`
                                                }
                                                fill={
                                                    PRIORITY_COLORS[
                                                        index
                                                        %
                                                        PRIORITY_COLORS.length
                                                    ]
                                                }
                                            />

                                        )
                                    )
                                }

                            </Bar>

                        </BarChart>

                    </ResponsiveContainer>

                </ChartCard>


            </div>


            <div className="
                grid
                grid-cols-1
                xl:grid-cols-2
                gap-6
                mb-6
            ">


                <ChartCard
                    title="Case Aging Aktif"
                    subtitle="Umur kasus aktif sejak kasus investigasi dibuat."
                >

                    <ResponsiveContainer
                        width="100%"
                        height={320}
                    >

                        <BarChart
                            data={agingData}
                        >

                            <CartesianGrid
                                strokeDasharray="3 3"
                            />

                            <XAxis
                                dataKey="label"
                            />

                            <YAxis
                                allowDecimals={false}
                            />

                            <Tooltip />

                            <Bar
                                dataKey="total"
                                name="Jumlah Kasus"
                            >

                                {
                                    agingData.map(
                                        (item,index)=>(

                                            <Cell
                                                key={
                                                    `${item.bucket}-${index}`
                                                }
                                                fill={
                                                    AGING_COLORS[
                                                        index
                                                        %
                                                        AGING_COLORS.length
                                                    ]
                                                }
                                            />

                                        )
                                    )
                                }

                            </Bar>

                        </BarChart>

                    </ResponsiveContainer>

                </ChartCard>


                <ChartCard
                    title="Beban Kerja Investigator"
                    subtitle="Perbandingan kasus aktif, selesai, dan melewati SLA."
                >

                    <ResponsiveContainer
                        width="100%"
                        height={320}
                    >

                        <BarChart
                            data={workloadData}
                            margin={{
                                top: 10,
                                right: 10,
                                left: 0,
                                bottom: 50
                            }}
                        >

                            <CartesianGrid
                                strokeDasharray="3 3"
                            />

                            <XAxis
                                dataKey="investigator"
                                angle={-20}
                                textAnchor="end"
                                interval={0}
                                height={80}
                            />

                            <YAxis
                                allowDecimals={false}
                            />

                            <Tooltip />

                            <Legend />

                            <Bar
                                dataKey="active_cases"
                                name="Aktif"
                                fill="#2563eb"
                            />

                            <Bar
                                dataKey="closed_cases"
                                name="Selesai"
                                fill="#16a34a"
                            />

                            <Bar
                                dataKey="overdue_cases"
                                name="Lewat SLA"
                                fill="#dc2626"
                            />

                        </BarChart>

                    </ResponsiveContainer>

                </ChartCard>


            </div>


            <div className="
                grid
                grid-cols-1
                xl:grid-cols-2
                gap-6
                mb-8
            ">


                <ChartCard
                    title="Distribusi Tingkat Risiko"
                    subtitle="Profil tingkat risiko klaim yang telah masuk investigasi."
                >

                    <ResponsiveContainer
                        width="100%"
                        height={320}
                    >

                        <PieChart>

                            <Pie
                                data={riskData}
                                dataKey="total"
                                nameKey="label"
                                cx="50%"
                                cy="50%"
                                outerRadius={105}
                                label={
                                    ({label,total})=>
                                        `${label}: ${total}`
                                }
                            >

                                {
                                    riskData.map(
                                        (item,index)=>(

                                            <Cell
                                                key={
                                                    `${item.risk_level}-${index}`
                                                }
                                                fill={
                                                    RISK_COLORS[
                                                        index
                                                        %
                                                        RISK_COLORS.length
                                                    ]
                                                }
                                            />

                                        )
                                    )
                                }

                            </Pie>

                            <Tooltip />

                        </PieChart>

                    </ResponsiveContainer>

                </ChartCard>


                <ChartCard
                    title="Dampak Finansial"
                    subtitle="Perbandingan estimasi, kerugian terkonfirmasi, nilai pemulihan, dan sisa kerugian."
                >

                    <ResponsiveContainer
                        width="100%"
                        height={320}
                    >

                        <BarChart
                            data={[
                                {
                                    name: "Estimasi",
                                    value: Number(
                                        financial.total_estimated_loss || 0
                                    )
                                },
                                {
                                    name: "Terkonfirmasi",
                                    value: Number(
                                        financial.total_confirmed_loss || 0
                                    )
                                },
                                {
                                    name: "Dipulihkan",
                                    value: Number(
                                        financial.total_recovered_amount || 0
                                    )
                                },
                                {
                                    name: "Sisa",
                                    value: Number(
                                        financial.outstanding_loss || 0
                                    )
                                }
                            ]}
                        >

                            <CartesianGrid
                                strokeDasharray="3 3"
                            />

                            <XAxis
                                dataKey="name"
                            />

                            <YAxis
                                tickFormatter={
                                    (value)=>
                                        `${Math.round(
                                            Number(value) / 1000000
                                        )} jt`
                                }
                            />

                            <Tooltip
                                formatter={
                                    (value)=>[
                                        formatRupiah(value),
                                        "Nilai"
                                    ]
                                }
                            />

                            <Legend />

                            <Bar
                                dataKey="value"
                                name="Nilai Finansial"
                                fill="#2563eb"
                            />

                        </BarChart>

                    </ResponsiveContainer>

                </ChartCard>


            </div>


            <div className="
                bg-white
                border
                rounded-xl
                shadow-sm
                overflow-hidden
                mb-8
            ">


                <div className="
                    p-5
                    border-b
                ">

                    <h2 className="
                        text-lg
                        font-bold
                    ">
                        Kinerja Investigator
                    </h2>

                    <p className="
                        text-sm
                        text-gray-500
                        mt-1
                    ">
                        Ringkasan beban kasus dan kepatuhan SLA per investigator.
                    </p>

                </div>


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

                                <th className="text-left px-5 py-3">
                                    Investigator
                                </th>

                                <th className="text-right px-5 py-3">
                                    Total
                                </th>

                                <th className="text-right px-5 py-3">
                                    Aktif
                                </th>

                                <th className="text-right px-5 py-3">
                                    Selesai
                                </th>

                                <th className="text-right px-5 py-3">
                                    Lewat SLA
                                </th>

                                <th className="text-right px-5 py-3">
                                    Rata-rata Umur
                                </th>

                                <th className="text-right px-5 py-3">
                                    Kerugian
                                </th>

                                <th className="text-right px-5 py-3">
                                    Pemulihan
                                </th>

                            </tr>

                        </thead>


                        <tbody>

                            {
                                (
                                    investigatorData?.investigator_performance
                                    ||
                                    []
                                ).map(
                                    (item)=>(

                                        <tr
                                            key={item.investigator}
                                            className="
                                                border-t
                                            "
                                        >

                                            <td className="
                                                px-5
                                                py-4
                                                font-semibold
                                            ">
                                                {item.investigator}
                                            </td>

                                            <td className="px-5 py-4 text-right">
                                                {Number(item.total_cases || 0).toLocaleString("id-ID")}
                                            </td>

                                            <td className="px-5 py-4 text-right">
                                                {Number(item.active_cases || 0).toLocaleString("id-ID")}
                                            </td>

                                            <td className="px-5 py-4 text-right">
                                                {Number(item.closed_cases || 0).toLocaleString("id-ID")}
                                            </td>

                                            <td className="px-5 py-4 text-right">
                                                {Number(item.overdue_cases || 0).toLocaleString("id-ID")}
                                            </td>

                                            <td className="px-5 py-4 text-right">
                                                {formatDays(item.avg_case_age_days)}
                                            </td>

                                            <td className="px-5 py-4 text-right">
                                                {formatRupiah(item.confirmed_loss || 0)}
                                            </td>

                                            <td className="px-5 py-4 text-right">
                                                {formatRupiah(item.recovered_amount || 0)}
                                            </td>

                                        </tr>

                                    )
                                )
                            }

                        </tbody>

                    </table>

                </div>


            </div>


            <div className="
                bg-white
                border
                rounded-xl
                shadow-sm
                overflow-hidden
            ">


                <div className="
                    p-5
                    border-b
                ">

                    <h2 className="
                        text-lg
                        font-bold
                    ">
                        Kasus Aktif Paling Lama
                    </h2>

                    <p className="
                        text-sm
                        text-gray-500
                        mt-1
                    ">
                        Sepuluh kasus aktif dengan umur investigasi paling lama.
                    </p>

                </div>


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

                                <th className="text-left px-5 py-3">
                                    Klaim
                                </th>

                                <th className="text-left px-5 py-3">
                                    Fasilitas
                                </th>

                                <th className="text-left px-5 py-3">
                                    Investigator
                                </th>

                                <th className="text-left px-5 py-3">
                                    Prioritas
                                </th>

                                <th className="text-right px-5 py-3">
                                    Fraud Score
                                </th>

                                <th className="text-right px-5 py-3">
                                    Umur Kasus
                                </th>

                                <th className="text-center px-5 py-3">
                                    SLA
                                </th>

                            </tr>

                        </thead>


                        <tbody>

                            {
                                (
                                    investigatorData?.oldest_active_cases
                                    ||
                                    []
                                ).map(
                                    (item)=>(

                                        <tr
                                            key={item.case_id}
                                            className="
                                                border-t
                                            "
                                        >

                                            <td className="
                                                px-5
                                                py-4
                                                font-semibold
                                            ">
                                                {item.claim_code}
                                            </td>

                                            <td className="px-5 py-4">
                                                {item.facility || "-"}
                                            </td>

                                            <td className="px-5 py-4">
                                                {item.assigned_to || "Belum Ditugaskan"}
                                            </td>

                                            <td className="px-5 py-4">
                                                {translatePriority(item.priority)}
                                            </td>

                                            <td className="
                                                px-5
                                                py-4
                                                text-right
                                                font-semibold
                                            ">
                                                {item.fraud_score ?? "-"}
                                            </td>

                                            <td className="px-5 py-4 text-right">
                                                {formatDays(item.age_days)}
                                            </td>

                                            <td className="px-5 py-4 text-center">

                                                <span className={
                                                    item.sla_breached
                                                    ? "inline-flex px-3 py-1 rounded-full text-xs font-semibold bg-red-50 text-red-700"
                                                    : "inline-flex px-3 py-1 rounded-full text-xs font-semibold bg-green-50 text-green-700"
                                                }>

                                                    {
                                                        item.sla_breached
                                                        ? "Terlambat"
                                                        : "Aman"
                                                    }

                                                </span>

                                            </td>

                                        </tr>

                                    )
                                )
                            }

                        </tbody>

                    </table>

                </div>


            </div>


        </div>

    );

}


function KpiCard({
    title,
    value,
    subtitle,
    icon: Icon
}){


    return (

        <div className="
            bg-white
            border
            rounded-xl
            p-5
            shadow-sm
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


                    <div className="
                        text-xs
                        text-gray-500
                        mt-2
                    ">
                        {subtitle}
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
                    shrink-0
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


function ChartCard({
    title,
    subtitle,
    children
}){


    return (

        <div className="
            bg-white
            border
            rounded-xl
            p-5
            shadow-sm
        ">


            <div className="
                mb-5
            ">


                <h2 className="
                    font-bold
                    text-lg
                ">
                    {title}
                </h2>


                <p className="
                    text-sm
                    text-gray-500
                    mt-1
                ">
                    {subtitle}
                </p>


            </div>


            {children}


        </div>

    );

}
