import {
    useEffect,
    useState
} from "react";


import {
    getOverview,
    getRiskDistribution,
    getFraudReasons,
    getHighRiskClaims
} from "../api/dashboard";


import StatCard from "../components/StatCard";

import ChartCard from "../components/ChartCard";

import FraudTable from "../components/FraudTable";


import {
    PieChart,
    Pie,
    Cell,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend
} from "recharts";



export default function Dashboard(){


    const [data,setData] = useState(null);

    const [riskData,setRiskData] = useState([]);

    const [fraudData,setFraudData] = useState([]);

    const [highRisk,setHighRisk] = useState([]);




    useEffect(()=>{


        console.log(
            "Dashboard component loaded"
        );



        // ==========================
        // LOAD OVERVIEW KPI
        // ==========================


        getOverview()

        .then((result)=>{


            console.log(
                "OVERVIEW:",
                result
            );


            setData(result);


        })


        .catch((error)=>{


            console.error(
                "OVERVIEW ERROR:",
                error
            );


        });







        // ==========================
        // LOAD RISK DISTRIBUTION
        // ==========================


        getRiskDistribution()

        .then((result)=>{


            console.log(
                "RISK DATA:",
                result
            );


            setRiskData(result);


        })


        .catch((error)=>{


            console.error(
                "RISK ERROR:",
                error
            );


        });







        // ==========================
        // LOAD FRAUD FACTOR
        // ==========================


        getFraudReasons()

        .then((result)=>{


            console.log(
                "FRAUD FACTOR:",
                result
            );


            setFraudData(result);


        })


        .catch((error)=>{


            console.error(
                "FRAUD ERROR:",
                error
            );


        });







        // ==========================
        // LOAD HIGH RISK CLAIM
        // ==========================


        getHighRiskClaims()

        .then((result)=>{


            console.log(
                "HIGH RISK CLAIM:",
                result
            );


            setHighRisk(result);


        })


        .catch((error)=>{


            console.error(
                "HIGH RISK ERROR:",
                error
            );


        });




    },[]);







    if(!data)

    return (

        <div className="
            flex
            items-center
            justify-center
            h-64
            text-xl
        ">

            Loading Dashboard...

        </div>

    );






    return (

        <div>





            <h1 className="
                text-3xl
                font-bold
                mb-8
            ">

                JKN SENTINEL Dashboard

            </h1>






            {/* ==========================
                KPI SECTION
            ========================== */}



            <div className="
                grid
                grid-cols-1
                md:grid-cols-4
                gap-5
            ">


                <StatCard

                    title="Total Claims"

                    value={
                        data.total_claim
                    }

                />



                <StatCard

                    title="Average Fraud Score"

                    value={
                        data.average_fraud_score
                    }

                />



                <StatCard

                    title="High Risk"

                    value={
                        data.high_risk_claim
                    }

                />



                <StatCard

                    title="Medium Risk"

                    value={
                        data.medium_risk_claim
                    }

                />


            </div>









            {/* ==========================
                CHART SECTION
            ========================== */}



            <div className="
                grid
                grid-cols-1
                md:grid-cols-2
                gap-6
                mt-8
            ">





                <ChartCard

                    title="Risk Distribution"

                >


                    <PieChart

                        width={400}

                        height={300}

                    >


                        <Pie

                            data={riskData}

                            dataKey="total"

                            nameKey="risk_level"

                            cx="50%"

                            cy="50%"

                            outerRadius={100}

                            label


                        >


                            {
                                riskData.map(
                                    (item,index)=>(

                                        <Cell

                                            key={index}

                                        />

                                    )
                                )
                            }


                        </Pie>


                        <Tooltip />

                        <Legend />


                    </PieChart>


                </ChartCard>







                <ChartCard

                    title="Fraud Factor Analysis"

                >



                    <BarChart

                        width={450}

                        height={300}

                        data={fraudData}

                    >


                        <CartesianGrid />


                        <XAxis

                            dataKey="factor"

                        />


                        <YAxis />


                        <Tooltip />

                        <Legend />


                        <Bar

                            dataKey="total"

                        />


                    </BarChart>


                </ChartCard>





            </div>







            {/* ==========================
                HIGH RISK INVESTIGATION
            ========================== */}



            <FraudTable

                data={highRisk}

            />






        </div>

    )

}