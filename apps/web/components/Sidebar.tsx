const menu = [

{
name:"Dashboard",
path:"/dashboard"
},

{
name:"Risk Queue",
path:"/risk"
},

{
name:"Claims",
path:"/claims"
},

{
name:"Case Management",
path:"/cases"
},

{
name:"Audit Trail",
path:"/audit"
}

]


export default function Sidebar(){


return (

<aside>


<h2>
JKN SENTINEL
</h2>


<nav>

{

menu.map((item)=>(


<a 
key={item.path}
href={item.path}
>

{item.name}

</a>


))

}


</nav>


</aside>

)

}
