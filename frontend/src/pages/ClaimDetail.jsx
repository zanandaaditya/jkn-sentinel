import {
    useParams
} from "react-router-dom";


import {
    useEffect,
    useState
} from "react";


import {
    getClaimDetail,
    getClaimDetails,
    getClaimRiskBreakdown,
    getClaimExplanation,
    getFraudCase,
    createFraudCase,
    updateFraudCase,
    getFraudCaseHistory
} from "../api/dashboard";



import ClinicalTable
from "../components/ClinicalTable";


import RiskBreakdown
from "../components/RiskBreakdown";


import FraudExplanation
from "../components/FraudExplanation";


import InvestigationCase
from "../components/InvestigationCase";

import InvestigationTimeline
from "../components/InvestigationTimeline";

import {
    translateRiskLevel,
    translateFraudReason,
    formatRupiah
} from "../utils/translations";

export default function ClaimDetail(){


    const {
        id
    } = useParams();



    // =====================================
    // CLAIM DATA
    // =====================================

    const [claim,setClaim] =
        useState(null);


    const [details,setDetails] =
        useState([]);


    const [riskBreakdown,setRiskBreakdown] =
        useState([]);


    const [explanations,setExplanations] =
        useState([]);



    // =====================================
    // FRAUD CASE
    // =====================================

    const [fraudCase,setFraudCase] =
        useState(null);

    const [caseHistory,setCaseHistory] =
        useState([]);

    const [caseSaving,setCaseSaving] =
        useState(false);


    const [caseMessage,setCaseMessage] =
        useState("");


    const [caseError,setCaseError] =
        useState("");



    // =====================================
    // PAGE STATE
    // =====================================

    const [loading,setLoading] =
        useState(true);


    const [error,setError] =
        useState(null);




    useEffect(()=>{


        console.log(
            "CLAIM ID:",
            id
        );


        setLoading(true);

        setError(null);



        // =====================================
        // CLAIM PROFILE
        // =====================================

        getClaimDetail(id)

        .then((result)=>{


            console.log(
                "CLAIM:",
                result
            );


            setClaim(result);


        })

        .catch((error)=>{


            console.error(
                "CLAIM ERROR:",
                error
            );


            setError(
                "Gagal mengambil claim profile."
            );


        })

        .finally(()=>{


            setLoading(false);


        });





        // =====================================
        // CLINICAL DETAILS
        // =====================================

        getClaimDetails(id)

        .then((result)=>{


            console.log(
                "DETAILS:",
                result
            );


            setDetails(
                result || []
            );


        })

        .catch((error)=>{


            console.error(
                "DETAIL ERROR:",
                error
            );


        });





        // =====================================
        // RISK BREAKDOWN
        // =====================================

        getClaimRiskBreakdown(id)

        .then((result)=>{


            console.log(
                "RISK BREAKDOWN:",
                result
            );


            setRiskBreakdown(
                result || []
            );


        })

        .catch((error)=>{


            console.error(
                "RISK BREAKDOWN ERROR:",
                error
            );


        });





        // =====================================
        // FRAUD EXPLANATION
        // =====================================

        getClaimExplanation(id)

        .then((result)=>{


            console.log(
                "FRAUD EXPLANATION:",
                result
            );


            setExplanations(
                result || []
            );


        })

        .catch((error)=>{


            console.error(
                "EXPLANATION ERROR:",
                error
            );


        });





        // =====================================
        // FRAUD INVESTIGATION CASE
        // =====================================

        getFraudCase(id)

        .then((result)=>{


            console.log(
                "FRAUD CASE:",
                result
            );


            setFraudCase(
                result || null
            );


        })

        .catch((error)=>{


            console.error(
                "FRAUD CASE ERROR:",
                error
            );


        });



        // =====================================
        // FRAUD CASE HISTORY
        // =====================================

        getFraudCaseHistory(id)

        .then((result)=>{


            console.log(
                "CASE HISTORY:",
                result
            );


            setCaseHistory(
                result || []
            );


        })

        .catch((error)=>{


            console.error(
                "CASE HISTORY ERROR:",
                error
            );


        });



    },[id]);

    // =====================================
    // CREATE FRAUD CASE
    // =====================================

    const handleCreateFraudCase = async()=>{


        try{


            setCaseSaving(true);

            setCaseError("");

            setCaseMessage("");



            const result =
                await createFraudCase(
                    id,
                    {
                        assigned_to: null,

                        investigation_note:
                            "Menunggu investigasi"
                    }
                );



            console.log(
                "CREATE FRAUD CASE:",
                result
            );


            setFraudCase(result);

            const history =
                await getFraudCaseHistory(id);


            setCaseHistory(
                history || []
            );

            setCaseMessage(
                "Fraud case berhasil dibuat."
            );


        }
        catch(error){


            console.error(
                "CREATE FRAUD CASE ERROR:",
                error
            );


            setCaseError(
                error?.response?.data?.detail
                ||
                "Gagal membuat fraud case."
            );


        }
        finally{


            setCaseSaving(false);


        }


    };





    // =====================================
    // UPDATE FRAUD CASE
    // =====================================

    const handleSaveInvestigation =
        async(form)=>{


        try{


            setCaseSaving(true);

            setCaseError("");

            setCaseMessage("");



            const result =
                await updateFraudCase(
                    id,
                    {
                        case_status:
                            form.case_status,

                        priority:
                            form.priority,

                        assigned_to:
                            form.assigned_to,

                        investigation_note:
                            form.investigation_note,

                        investigation_result:
                            form.investigation_result,

                        estimated_loss:
                            form.estimated_loss,

                        confirmed_loss:
                            form.confirmed_loss,

                        recovered_amount:
                            form.recovered_amount,

                        conclusion:
                            form.conclusion
                    }
                );



            console.log(
                "UPDATE FRAUD CASE:",
                result
            );


            setFraudCase(result);
            
            const history =
                await getFraudCaseHistory(id);


            setCaseHistory(
                history || []
            );

            setCaseMessage(
                "Investigation case berhasil diperbarui."
            );


        }
        catch(error){


            console.error(
                "UPDATE FRAUD CASE ERROR:",
                error
            );


            setCaseError(
                error?.response?.data?.detail
                ||
                "Gagal memperbarui investigation case."
            );


        }
        finally{


            setCaseSaving(false);


        }


    };






    // =====================================
    // LOADING
    // =====================================

    if(loading){

        return (

            <div className="
                p-6
                text-gray-500
            ">

                Loading Claim...

            </div>

        );

    }





    // =====================================
    // ERROR
    // =====================================

    if(error){

        return (

            <div className="
                bg-red-50
                border
                border-red-200
                text-red-700
                rounded-xl
                p-6
            ">

                {error}

            </div>

        );

    }





    // =====================================
    // CLAIM NOT FOUND
    // =====================================

    if(!claim){

        return (

            <div className="
                bg-yellow-50
                border
                border-yellow-200
                rounded-xl
                p-6
            ">

                Claim tidak ditemukan.

            </div>

        );

    }





    return (

        <div className="
            pb-12
        ">




            {/* =====================================
                PAGE HEADER
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

                    Claim Investigation Detail

                </h1>


                <p className="
                    text-gray-500
                    mt-2
                ">

                    Analisis detail klaim,
                    clinical validation,
                    fraud explanation,
                    dan proses investigasi.

                </p>


            </div>






            {/* =====================================
                CLAIM PROFILE
            ===================================== */}


            <div className="
                bg-white
                rounded-xl
                shadow
                border
                p-6
            ">


                <div className="
                    flex
                    justify-between
                    items-start
                    gap-4
                    mb-6
                ">


                    <div>

                        <h2 className="
                            text-xl
                            font-bold
                        ">

                            Claim Profile

                        </h2>


                        <p className="
                            text-sm
                            text-gray-500
                            mt-1
                        ">

                            Informasi utama klaim yang
                            sedang dianalisis.

                        </p>

                    </div>



                    <div className="
                        text-right
                    ">


                        <div className="
                            text-xs
                            text-gray-500
                        ">

                            Fraud Score

                        </div>


                        <div className="
                            text-3xl
                            font-bold
                        ">

                            {claim.fraud_score}

                        </div>


                    </div>


                </div>




                <div className="
                    grid
                    grid-cols-1
                    md:grid-cols-2
                    lg:grid-cols-3
                    gap-6
                ">



                    <div>

                        <div className="
                            text-sm
                            text-gray-500
                        ">
                            Claim Code
                        </div>

                        <div className="
                            font-semibold
                            mt-1
                        ">
                            {claim.claim_code}
                        </div>

                    </div>



                    <div>

                        <div className="
                            text-sm
                            text-gray-500
                        ">
                            Risk Level
                        </div>

                        <div className="
                            font-semibold
                            mt-1
                        ">
                            {
                                translateRiskLevel(
                                    claim.risk_level
                                )
                            }
                        </div>

                    </div>



                    <div>

                        <div className="
                            text-sm
                            text-gray-500
                        ">
                            Status
                        </div>

                        <div className="
                            font-semibold
                            mt-1
                        ">
                            {claim.status || "-"}
                        </div>

                    </div>



                    <div>

                        <div className="
                            text-sm
                            text-gray-500
                        ">
                            Diagnosis
                        </div>

                        <div className="
                            font-semibold
                            mt-1
                        ">
                            {claim.diagnosis || "-"}
                        </div>

                    </div>



                    <div>

                        <div className="
                            text-sm
                            text-gray-500
                        ">
                            Facility
                        </div>

                        <div className="
                            font-semibold
                            mt-1
                        ">
                            {claim.facility || "-"}
                        </div>

                    </div>



                    <div>

                        <div className="
                            text-sm
                            text-gray-500
                        ">
                            Claim Amount
                        </div>

                        <div className="
                            font-semibold
                            mt-1
                        ">

                            {
                                formatRupiah(
                                    claim.claim_amount
                                )
                            }

                        </div>

                    </div>


                </div>




                {
                    claim.fraud_reason && (

                        <div className="
                            mt-6
                            bg-red-50
                            border
                            border-red-100
                            rounded-lg
                            p-4
                        ">


                            <div className="
                                text-sm
                                font-semibold
                                text-red-700
                                mb-1
                            ">

                                Fraud Alert

                            </div>


                            <div className="
                                text-sm
                                text-red-700
                            ">

                                {
                                    translateFraudReason(
                                        claim.fraud_reason
                                    )
                                }

                            </div>


                        </div>

                    )
                }



            </div>






            {/* =====================================
                RISK BREAKDOWN
            ===================================== */}


            <RiskBreakdown

                data={
                    riskBreakdown
                }

            />






            {/* =====================================
                FRAUD EXPLANATION
            ===================================== */}


            <FraudExplanation

                data={
                    explanations
                }

            />






            {/* =====================================
                CLINICAL VALIDATION
            ===================================== */}


            <ClinicalTable

                data={
                    details
                }

            />






            {/* =====================================
                CASE MESSAGE
            ===================================== */}


            {
                caseMessage && (

                    <div className="
                        mt-8
                        bg-green-50
                        border
                        border-green-200
                        text-green-700
                        rounded-xl
                        p-4
                    ">

                        {caseMessage}

                    </div>

                )
            }



            {
                caseError && (

                    <div className="
                        mt-8
                        bg-red-50
                        border
                        border-red-200
                        text-red-700
                        rounded-xl
                        p-4
                    ">

                        {caseError}

                    </div>

                )
            }





            {/* =====================================
                INVESTIGATION CASE
            ===================================== */}


            <InvestigationCase

                fraudCase={
                    fraudCase
                }

                onCreate={
                    handleCreateFraudCase
                }

                onSave={
                    handleSaveInvestigation
                }

                saving={
                    caseSaving
                }

            />



            {/* =====================================
                INVESTIGATION TIMELINE
            ===================================== */}


            <InvestigationTimeline

                data={
                    caseHistory
                }

            />



        </div>

    );

}