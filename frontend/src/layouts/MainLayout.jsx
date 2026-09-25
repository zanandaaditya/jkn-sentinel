import {
    LayoutDashboard,
    FileWarning,
    Building2,
    Stethoscope
} from "lucide-react";


export default function MainLayout({ children }) {

    return (

        <div className="flex min-h-screen bg-slate-100">


            <aside className="
                w-64
                bg-slate-900
                text-white
                p-5
            ">


                <h1 className="
                    text-xl
                    font-bold
                    mb-8
                ">
                    JKN SENTINEL
                </h1>


                <nav className="space-y-4">


                    <div className="flex items-center gap-3">
                        <LayoutDashboard size={20}/>
                        Dashboard
                    </div>


                    <div className="flex items-center gap-3">
                        <FileWarning size={20}/>
                        Fraud Cases
                    </div>


                    <div className="flex items-center gap-3">
                        <Building2 size={20}/>
                        Facilities
                    </div>


                    <div className="flex items-center gap-3">
                        <Stethoscope size={20}/>
                        Doctors
                    </div>


                </nav>


            </aside>


            <main className="
                flex-1
                p-8
            ">

                {children}

            </main>


        </div>

    );
}