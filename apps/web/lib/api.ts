const API_URL =
process.env.NEXT_PUBLIC_API_URL;


export async function healthCheck(){


const response =
await fetch(

`${API_URL}/health`

);


return response.json();


}
