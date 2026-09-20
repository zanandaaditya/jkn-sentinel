import axios from "axios";


const api = axios.create({

    baseURL:
        "http://localhost:8000"

});


export const getInvestigators = async(
    params = {}
)=>{

    const response = await api.get(
        "/investigators",
        {
            params
        }
    );

    return response.data;

};


export const getActiveInvestigators = async()=>{

    const response = await api.get(
        "/investigators/active"
    );

    return response.data;

};


export const createInvestigator = async(
    payload
)=>{

    const response = await api.post(
        "/investigators",
        payload
    );

    return response.data;

};


export const updateInvestigator = async(
    investigatorId,
    payload
)=>{

    const response = await api.patch(
        `/investigators/${investigatorId}`,
        payload
    );

    return response.data;

};

export const getInvestigatorCapacity = async()=>{

    const response = await api.get(
        "/investigators/capacity"
    );

    return response.data;

};