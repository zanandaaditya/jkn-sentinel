const factorLabels = {
    CLINICAL: "Clinical Risk",
    COST: "Cost Anomaly",
    FACILITY: "Facility Risk",
    DOCTOR: "Doctor Risk"
};


const factorDescriptions = {
    CLINICAL: "Kesesuaian diagnosis, prosedur, dan obat",
    COST: "Analisis biaya klaim dan tarif standar",
    FACILITY: "Kesesuaian kemampuan fasilitas kesehatan",
    DOCTOR: "Profil kompetensi dan risiko dokter"
};


export default function RiskBreakdown({ data = [] }){


    const totalScore = data.reduce(
        (total,item)=> total + Number(item.score || 0),
        0
    );


    return (

        <div className="
            bg-white
            rounded-xl
            shadow
            border
            p-6
            mt-8
        ">


            <div className="mb-6">

                <h2 className="
                    text-xl
                    font-bold
                ">
                    Risk Breakdown
                </h2>


                <p className="
                    text-sm
                    text-gray-500
                    mt-1
                ">
                    Kontribusi faktor risiko terhadap indikasi fraud klaim.
                </p>

            </div>



            {
                data.length === 0
                ? (
                    <div className="
                        text-gray-500
                        text-sm
                        py-6
                    ">
                        Tidak terdapat risk breakdown pada klaim ini.
                    </div>
                )
                : (

                    <div className="space-y-6">

                        {
                            data.map((item,index)=>{


                                const score =
                                    Number(item.score || 0);


                                const percentage =
                                    totalScore > 0
                                    ? Math.round(
                                        (score / totalScore) * 100
                                    )
                                    : 0;


                                return (

                                    <div
                                        key={index}
                                        className="
                                            border-b
                                            pb-5
                                            last:border-b-0
                                            last:pb-0
                                        "
                                    >


                                        <div className="
                                            flex
                                            items-center
                                            justify-between
                                            gap-4
                                            mb-2
                                        ">


                                            <div>

                                                <div className="
                                                    font-semibold
                                                    text-gray-900
                                                ">
                                                    {
                                                        factorLabels[item.factor]
                                                        || item.factor
                                                    }
                                                </div>


                                                <div className="
                                                    text-xs
                                                    text-gray-500
                                                    mt-1
                                                ">
                                                    {
                                                        factorDescriptions[item.factor]
                                                        || "Fraud risk factor"
                                                    }
                                                </div>

                                            </div>



                                            <div className="text-right">

                                                <div className="
                                                    font-bold
                                                    text-lg
                                                ">
                                                    +{score}
                                                </div>


                                                <div className="
                                                    text-xs
                                                    text-gray-500
                                                ">
                                                    {percentage}% contribution
                                                </div>

                                            </div>


                                        </div>



                                        <div className="
                                            w-full
                                            bg-gray-100
                                            rounded-full
                                            h-2.5
                                            overflow-hidden
                                        ">

                                            <div
                                                className="
                                                    bg-blue-600
                                                    h-2.5
                                                    rounded-full
                                                    transition-all
                                                "
                                                style={{
                                                    width:
                                                    `${Math.min(percentage,100)}%`
                                                }}
                                            />

                                        </div>



                                        {
                                            item.findings !== undefined && (

                                                <div className="
                                                    text-xs
                                                    text-gray-400
                                                    mt-2
                                                ">
                                                    {
                                                        item.findings
                                                    } finding(s)
                                                </div>

                                            )
                                        }


                                    </div>

                                );

                            })
                        }


                        <div className="
                            bg-gray-50
                            rounded-lg
                            p-4
                            flex
                            justify-between
                            items-center
                        ">

                            <span className="
                                font-semibold
                                text-gray-700
                            ">
                                Total Explanation Score
                            </span>


                            <span className="
                                text-2xl
                                font-bold
                            ">
                                {totalScore}
                            </span>

                        </div>


                    </div>

                )
            }


        </div>

    );

}