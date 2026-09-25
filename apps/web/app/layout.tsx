import "./globals.css";


export const metadata = {

title:"JKN SENTINEL",

description:
"Explainable Risk Intelligence Platform"

};


export default function RootLayout({

children,

}: Readonly<{

children: React.ReactNode;

}>) {


return (

<html lang="en">

<body>

{children}

</body>

</html>

)

}
