export default function ChartCard({
    title,
    children
}){


return (

<div className="
bg-white
rounded-xl
shadow-sm
border
p-6
">


<h2 className="
text-lg
font-semibold
mb-4
">

{title}

</h2>


{children}


</div>

)

}