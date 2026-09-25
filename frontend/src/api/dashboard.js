import axios from "axios";


const api = axios.create({

    baseURL:
    "http://localhost:8000"

});



/*
|--------------------------------------------------------------------------
| DASHBOARD OVERVIEW
|--------------------------------------------------------------------------
*/

export const getOverview = async()=>{

    const response = await api.get(
        "/dashboard/overview"
    );

    return response.data;

};





/*
|--------------------------------------------------------------------------
| RISK DISTRIBUTION
|--------------------------------------------------------------------------
*/

export const getRiskDistribution = async()=>{

    const response = await api.get(
        "/dashboard/risk-distribution"
    );

    return response.data;

};





/*
|--------------------------------------------------------------------------
| FRAUD FACTOR ANALYSIS
|--------------------------------------------------------------------------
*/

export const getFraudReasons = async()=>{

    const response = await api.get(
        "/dashboard/fraud-reasons"
    );

    return response.data;

};





/*
|--------------------------------------------------------------------------
| HIGH RISK CLAIM INVESTIGATION
|--------------------------------------------------------------------------
*/

export const getHighRiskClaims = async()=>{

    const response = await api.get(
        "/dashboard/high-risk"
    );

    return response.data;

};





/*
|--------------------------------------------------------------------------
| FACILITY RISK
|--------------------------------------------------------------------------
*/

export const getFacilities = async()=>{

    const response = await api.get(
        "/dashboard/facilities"
    );

    return response.data;

};





/*
|--------------------------------------------------------------------------
| DOCTOR RISK
|--------------------------------------------------------------------------
*/

export const getDoctors = async()=>{

    const response = await api.get(
        "/dashboard/doctors"
    );

    return response.data;

};




/*
|--------------------------------------------------------------------------
| CLAIM DETAIL EXPLORER
|--------------------------------------------------------------------------
*/

export const getClaimDetail = async(claimId)=>{

    const response = await api.get(
        `/claims/${claimId}`
    );

    return response.data;

};





/*
|--------------------------------------------------------------------------
| CLAIM CLINICAL DETAILS
|--------------------------------------------------------------------------
*/
export const getClaimDetails = async(claimId)=>{

    const response = await api.get(
        `/claims/${claimId}/details`
    );

    return response.data;

};





/*
|--------------------------------------------------------------------------
| CLAIM RISK BREAKDOWN
|--------------------------------------------------------------------------
*/

export const getClaimRiskBreakdown = async(claimId)=>{

    const response = await api.get(
        `/claims/${claimId}/risk-breakdown`
    );

    return response.data;

};





/*
|--------------------------------------------------------------------------
| FRAUD EXPLANATION ENGINE
|--------------------------------------------------------------------------
*/

export const getClaimExplanation = async(claimId)=>{

    const response = await api.get(
        `/claims/${claimId}/explanation`
    );

    return response.data;

};

/*
|--------------------------------------------------------------------------
| FRAUD INVESTIGATION CASE
|--------------------------------------------------------------------------
*/

export const getFraudCase = async(claimId)=>{

    const response = await api.get(
        `/claims/${claimId}/case`
    );

    return response.data;

};



export const createFraudCase = async(
    claimId,
    payload
)=>{

    const response = await api.post(
        `/claims/${claimId}/case`,
        payload
    );

    return response.data;

};



export const updateFraudCase = async(
    claimId,
    payload
)=>{

    const response = await api.patch(
        `/claims/${claimId}/case`,
        payload
    );

    return response.data;

};

/*
|--------------------------------------------------------------------------
| FRAUD CASE HISTORY
|--------------------------------------------------------------------------
*/

export const getFraudCaseHistory = async(claimId)=>{

    const response = await api.get(
        `/claims/${claimId}/case/history`
    );

    return response.data;

};

/*
|--------------------------------------------------------------------------
| FRAUD CASE QUEUE
|--------------------------------------------------------------------------
*/

export const getFraudCaseQueue = async(params = {})=>{

    const response = await api.get(
        "/claims/cases/queue",
        {
            params
        }
    );

    return response.data;

};