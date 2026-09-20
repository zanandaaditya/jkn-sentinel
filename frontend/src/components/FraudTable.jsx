export default function FraudTable({
    data
}){


return (

<div className="
bg-white
rounded-xl
shadow-sm
border
p-6
mt-8
">


<h2 className="
text-lg
font-bold
mb-5
">

High Risk Claim Investigation

</h2>



<div className="
overflow-x-auto
">


<table className="
w-full
text-sm
">


<thead>

<tr className="
border-b
bg-slate-50
">


<th className="
p-3
text-left
">

Claim Code

</th>


<th className="
p-3
text-left
">

Score

</th>


<th className="
p-3
text-left
">

Risk

</th>


<th className="
p-3
text-left
">

Diagnosis

</th>


<th className="
p-3
text-left
">

Facility

</th>


<th className="
p-3
text-left
">

Reason

</th>


</tr>

</thead>




<tbody>


{
data.map(
(item,index)=>(


<tr

key={index}

className="
border-b
hover:bg-slate-50
"


>


<td className="
p-3
font-semibold
">

{item.claim_code}

</td>



<td className="
p-3
">

{item.fraud_score}

</td>




<td className="
p-3
">


<span className={

item.risk_level==="HIGH"

?

"px-3 py-1 rounded-full bg-red-100 text-red-700"

:

"px-3 py-1 rounded-full bg-yellow-100 text-yellow-700"

}

>

{item.risk_level}

</span>


</td>




<td className="
p-3
">

{item.diagnosis}

</td>




<td className="
p-3
">

{item.facility}

</td>




<td className="
p-3
max-w-md
">

{item.fraud_reason}

</td>



</tr>


)

)

}


</tbody>



</table>


</div>


</div>

)

}