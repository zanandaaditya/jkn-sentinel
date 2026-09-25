import axios from "axios";


const api = axios.create({

    baseURL:
        "http://localhost:8000"

});


export const getInvestigatorDirectory = async(
    slaDays = 7
)=>{

    const response = await api.get(
        "/claims/cases/investigators",
        {
            params: {

                sla_days:
                    slaDays

            }
        }
    );

    return response.data;

};


export const getInvestigatorWorkbench = async(
    params = {}
)=>{

    const response = await api.get(
        "/claims/cases/workbench",
        {
            params
        }
    );

    return response.data;

};


export const assignFraudCase = async(
    claimId,
    investigatorId
)=>{

    const response = await api.patch(
        `/claims/${claimId}/case/assign`,
        {
            investigator_id:
                investigatorId || null
        }
    );

    return response.data;

};


export const bulkAssignFraudCases = async(
    claimIds,
    investigatorId
)=>{

    const response = await api.patch(
        "/claims/cases/bulk-assign",
        {
            claim_ids:
                claimIds,

            investigator_id:
                investigatorId || null
        }
    );

    return response.data;

};

export const autoAssignFraudCases = async(
    claimIds
)=>{

    const response = await api.post(
        "/claims/cases/auto-assign",
        {
            claim_ids:
                claimIds
        }
    );

    return response.data;

};