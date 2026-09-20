const severityStyle = {

    LOW:
    "bg-green-100 text-green-700",

    MEDIUM:
    "bg-yellow-100 text-yellow-700",

    HIGH:
    "bg-red-100 text-red-700"

};


const factorStyle = {

    CLINICAL:
    "bg-purple-100 text-purple-700",

    COST:
    "bg-orange-100 text-orange-700",

    FACILITY:
    "bg-blue-100 text-blue-700",

    DOCTOR:
    "bg-cyan-100 text-cyan-700"

};



export default function FraudExplanation({
    data = []
}){


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
                    Why Was This Claim Flagged?
                </h2>


                <p className="
                    text-sm
                    text-gray-500
                    mt-1
                ">
                    Penjelasan faktor yang berkontribusi terhadap
                    fraud score klaim.
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
                        Tidak terdapat fraud explanation
                        pada klaim ini.
                    </div>

                )
                : (

                    <div className="
                        space-y-4
                    ">

                        {
                            data.map((item,index)=>(

                                <div
                                    key={
                                        item.id || index
                                    }
                                    className="
                                        border
                                        rounded-xl
                                        p-5
                                    "
                                >


                                    <div className="
                                        flex
                                        justify-between
                                        items-start
                                        gap-4
                                    ">


                                        <div>


                                            <div className="
                                                flex
                                                flex-wrap
                                                gap-2
                                                mb-3
                                            ">


                                                <span
                                                    className={`
                                                        text-xs
                                                        font-semibold
                                                        px-3
                                                        py-1
                                                        rounded-full

                                                        ${
                                                            factorStyle[
                                                                item.factor
                                                            ]
                                                            ||
                                                            "bg-gray-100 text-gray-700"
                                                        }
                                                    `}
                                                >

                                                    {item.factor}

                                                </span>



                                                <span
                                                    className={`
                                                        text-xs
                                                        font-semibold
                                                        px-3
                                                        py-1
                                                        rounded-full

                                                        ${
                                                            severityStyle[
                                                                item.severity
                                                            ]
                                                            ||
                                                            "bg-gray-100 text-gray-700"
                                                        }
                                                    `}
                                                >

                                                    {item.severity}

                                                </span>


                                            </div>



                                            <p className="
                                                text-gray-700
                                                leading-relaxed
                                            ">
                                                {item.description}
                                            </p>


                                        </div>



                                        <div className="
                                            shrink-0
                                            text-right
                                        ">

                                            <div className="
                                                text-xs
                                                text-gray-500
                                            ">
                                                Risk Contribution
                                            </div>


                                            <div className="
                                                text-2xl
                                                font-bold
                                                mt-1
                                            ">
                                                +{item.score}
                                            </div>

                                        </div>


                                    </div>


                                </div>

                            ))
                        }

                    </div>

                )
            }


        </div>

    );

}