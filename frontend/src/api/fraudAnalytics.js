import axios from "axios";


const api = axios.create({

    baseURL:
        "http://localhost:8000"

});


export const getFraudAnalytics = async()=>{

    const response = await api.get(
        "/claims/cases/analytics"
    );

    return response.data;

};


export const getInvestigatorAnalytics = async(
    slaDays = 7
)=>{

    const response = await api.get(
        "/claims/cases/investigator-analytics",
        {
            params: {
                sla_days: slaDays
            }
        }
    );

    return response.data;

};
