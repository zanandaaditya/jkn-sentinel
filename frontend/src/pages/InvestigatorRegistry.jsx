import {
    useEffect,
    useState
} from "react";


import {
    ChevronLeft,
    ChevronRight,
    Pencil,
    Plus,
    RefreshCw,
    Search
} from "lucide-react";


import {
    createInvestigator,
    getInvestigators,
    updateInvestigator
} from "../api/investigators";



const emptyForm = {

    employee_code: "",

    full_name: "",

    email: "",

    phone: "",

    role: "INVESTIGATOR",

    unit: "",

    status: "ACTIVE",

    max_active_cases: 20

};



export default function InvestigatorRegistry(){


    const [result,setResult] =
        useState({

            items: [],

            pagination: {}

        });


    const [form,setForm] =
        useState(
            emptyForm
        );


    const [editingId,setEditingId] =
        useState(null);


    const [search,setSearch] =
        useState("");


    const [searchInput,setSearchInput] =
        useState("");


    const [role,setRole] =
        useState("");


    const [status,setStatus] =
        useState("");


    const [page,setPage] =
        useState(1);


    const [pageSize,setPageSize] =
        useState(10);


    const [loading,setLoading] =
        useState(true);


    const [saving,setSaving] =
        useState(false);


    const [message,setMessage] =
        useState("");


    const [error,setError] =
        useState("");



    const loadData = async()=>{


        try{


            setLoading(true);

            setError("");


            const data =
                await getInvestigators({

                    search:
                        search || undefined,

                    role:
                        role || undefined,

                    status:
                        status || undefined,

                    page,

                    page_size:
                        pageSize

                });


            setResult(

                data
                ||
                {

                    items: [],

                    pagination: {}

                }

            );


        }
        catch(error){


            console.error(
                "INVESTIGATOR REGISTRY ERROR:",
                error
            );


            setError(

                error?.response?.data?.detail

                ||

                "Gagal mengambil investigator registry."

            );


        }
        finally{


            setLoading(false);


        }


    };



    useEffect(()=>{


        loadData();


    },[
        search,
        role,
        status,
        page,
        pageSize
    ]);



    useEffect(()=>{


        const timer =
            setTimeout(()=>{


                setPage(1);


                setSearch(
                    searchInput.trim()
                );


            },350);


        return ()=>{


            clearTimeout(
                timer
            );


        };


    },[
        searchInput
    ]);



    const handleChange = (
        event
    )=>{


        const {
            name,
            value
        } = event.target;


        setForm(
            (previous)=>({

                ...previous,

                [name]:

                    name ===
                    "max_active_cases"

                    ?

                    Number(value)

                    :

                    value

            })
        );


    };



    const resetForm = ()=>{


        setEditingId(
            null
        );


        setForm(
            emptyForm
        );


    };



    const handleEdit = (
        item
    )=>{


        setEditingId(
            item.id
        );


        setForm({

            employee_code:
                item.employee_code
                ||
                "",

            full_name:
                item.full_name
                ||
                "",

            email:
                item.email
                ||
                "",

            phone:
                item.phone
                ||
                "",

            role:
                item.role
                ||
                "INVESTIGATOR",

            unit:
                item.unit
                ||
                "",

            status:
                item.status
                ||
                "ACTIVE",

            max_active_cases:
                Number(
                    item.max_active_cases
                    ||
                    0
                )

        });


        window.scrollTo({

            top: 0,

            behavior:
                "smooth"

        });


    };



    const handleSave = async(
        event
    )=>{


        event.preventDefault();


        if(
            !form.full_name.trim()
        ){


            setError(
                "Nama investigator wajib diisi."
            );


            return;

        }


        try{


            setSaving(true);

            setError("");

            setMessage("");


            const payload = {


                employee_code:
                    form.employee_code.trim()
                    ||
                    null,


                full_name:
                    form.full_name.trim(),


                email:
                    form.email.trim()
                    ||
                    null,


                phone:
                    form.phone.trim()
                    ||
                    null,


                role:
                    form.role,


                unit:
                    form.unit.trim()
                    ||
                    null,


                status:
                    form.status,


                max_active_cases:
                    Number(
                        form.max_active_cases
                        ||
                        0
                    )


            };


            if(
                editingId
            ){


                await updateInvestigator(

                    editingId,

                    payload

                );


                setMessage(
                    "Data investigator berhasil diperbarui."
                );


            }
            else{


                await createInvestigator(
                    payload
                );


                setMessage(
                    "Investigator berhasil ditambahkan."
                );


            }


            resetForm();


            await loadData();


        }
        catch(error){


            console.error(
                "SAVE INVESTIGATOR ERROR:",
                error
            );


            setError(

                error?.response?.data?.detail

                ||

                "Gagal menyimpan investigator."

            );


        }
        finally{


            setSaving(false);


        }


    };



    const pagination =
        result?.pagination
        ||
        {};



    return (

        <div className="
            pb-12
        ">


            {/* HEADER */}

            <div className="
                flex
                flex-col
                lg:flex-row
                lg:items-start
                lg:justify-between
                gap-4
                mb-8
            ">


                <div>


                    <div className="
                        text-sm
                        text-gray-500
                        mb-2
                    ">
                        Administration
                    </div>


                    <h1 className="
                        text-3xl
                        font-bold
                    ">
                        Investigator Registry
                    </h1>


                    <p className="
                        text-gray-500
                        mt-2
                    ">
                        Kelola investigator, supervisor, analis,
                        unit, status akun, dan kapasitas kasus aktif.
                    </p>


                </div>



                <button
                    onClick={
                        loadData
                    }
                    className="
                        inline-flex
                        items-center
                        gap-2
                        border
                        rounded-lg
                        px-4
                        py-2.5
                        font-semibold
                        hover:bg-gray-50
                    "
                >

                    <RefreshCw
                        size={17}
                    />

                    Muat Ulang

                </button>


            </div>



            {/* MESSAGE */}

            {
                message && (

                    <div className="
                        mb-6
                        bg-green-50
                        border
                        border-green-200
                        text-green-700
                        rounded-xl
                        p-4
                    ">
                        {message}
                    </div>

                )
            }



            {
                error && (

                    <div className="
                        mb-6
                        bg-red-50
                        border
                        border-red-200
                        text-red-700
                        rounded-xl
                        p-4
                    ">
                        {error}
                    </div>

                )
            }



            {/* FORM */}

            <form
                onSubmit={
                    handleSave
                }
                className="
                    bg-white
                    border
                    rounded-xl
                    p-6
                    mb-8
                "
            >


                <div className="
                    flex
                    items-center
                    justify-between
                    gap-4
                    mb-5
                ">


                    <div>


                        <h2 className="
                            text-lg
                            font-bold
                        ">

                            {
                                editingId

                                ?

                                "Edit Investigator"

                                :

                                "Tambah Investigator"
                            }

                        </h2>


                        <p className="
                            text-sm
                            text-gray-500
                            mt-1
                        ">
                            Investigator aktif dapat digunakan
                            dalam assignment Workbench.
                        </p>


                    </div>



                    {
                        editingId && (

                            <button
                                type="button"
                                onClick={
                                    resetForm
                                }
                                className="
                                    border
                                    rounded-lg
                                    px-4
                                    py-2
                                "
                            >
                                Batal Edit
                            </button>

                        )
                    }


                </div>



                <div className="
                    grid
                    grid-cols-1
                    md:grid-cols-2
                    xl:grid-cols-4
                    gap-4
                ">


                    <Field
                        label="Kode Pegawai"
                    >

                        <input
                            name="employee_code"
                            value={
                                form.employee_code
                            }
                            onChange={
                                handleChange
                            }
                            placeholder="INV-001"
                            className="
                                input-field
                            "
                        />

                    </Field>



                    <Field
                        label="Nama Lengkap *"
                    >

                        <input
                            name="full_name"
                            value={
                                form.full_name
                            }
                            onChange={
                                handleChange
                            }
                            placeholder="Nama investigator"
                            className="
                                input-field
                            "
                        />

                    </Field>



                    <Field
                        label="Email"
                    >

                        <input
                            type="email"
                            name="email"
                            value={
                                form.email
                            }
                            onChange={
                                handleChange
                            }
                            placeholder="nama@email.com"
                            className="
                                input-field
                            "
                        />

                    </Field>



                    <Field
                        label="Telepon"
                    >

                        <input
                            name="phone"
                            value={
                                form.phone
                            }
                            onChange={
                                handleChange
                            }
                            placeholder="08..."
                            className="
                                input-field
                            "
                        />

                    </Field>



                    <Field
                        label="Role"
                    >

                        <select
                            name="role"
                            value={
                                form.role
                            }
                            onChange={
                                handleChange
                            }
                            className="
                                input-field
                            "
                        >

                            <option value="INVESTIGATOR">
                                Investigator
                            </option>

                            <option value="SUPERVISOR">
                                Supervisor
                            </option>

                            <option value="ANALYST">
                                Analis
                            </option>

                        </select>

                    </Field>



                    <Field
                        label="Unit"
                    >

                        <input
                            name="unit"
                            value={
                                form.unit
                            }
                            onChange={
                                handleChange
                            }
                            placeholder="Fraud Investigation Unit"
                            className="
                                input-field
                            "
                        />

                    </Field>



                    <Field
                        label="Status"
                    >

                        <select
                            name="status"
                            value={
                                form.status
                            }
                            onChange={
                                handleChange
                            }
                            className="
                                input-field
                            "
                        >

                            <option value="ACTIVE">
                                Aktif
                            </option>

                            <option value="INACTIVE">
                                Nonaktif
                            </option>

                        </select>

                    </Field>



                    <Field
                        label="Maksimal Kasus Aktif"
                    >

                        <input
                            type="number"
                            min="0"
                            name="max_active_cases"
                            value={
                                form.max_active_cases
                            }
                            onChange={
                                handleChange
                            }
                            className="
                                input-field
                            "
                        />

                    </Field>


                </div>



                <div className="
                    flex
                    justify-end
                    mt-5
                ">


                    <button
                        type="submit"
                        disabled={
                            saving
                        }
                        className="
                            inline-flex
                            items-center
                            gap-2
                            bg-blue-600
                            text-white
                            rounded-lg
                            px-5
                            py-2.5
                            font-semibold
                            hover:bg-blue-700
                            disabled:opacity-50
                        "
                    >

                        <Plus
                            size={17}
                        />


                        {
                            saving

                            ?

                            "Menyimpan..."

                            :

                            editingId

                            ?

                            "Simpan Perubahan"

                            :

                            "Tambah Investigator"
                        }

                    </button>


                </div>


            </form>



            {/* FILTER */}

            <div className="
                bg-white
                border
                rounded-xl
                p-5
                mb-6
            ">


                <div className="
                    grid
                    grid-cols-1
                    md:grid-cols-2
                    xl:grid-cols-4
                    gap-4
                ">


                    <div className="
                        relative
                    ">


                        <Search
                            size={17}
                            className="
                                absolute
                                left-3
                                top-3
                                text-gray-400
                            "
                        />


                        <input
                            value={
                                searchInput
                            }
                            onChange={
                                (event)=>
                                    setSearchInput(
                                        event.target.value
                                    )
                            }
                            placeholder="Cari nama, kode, email, unit..."
                            className="
                                input-field
                                pl-10
                            "
                        />


                    </div>



                    <select
                        value={
                            role
                        }
                        onChange={
                            (event)=>{

                                setPage(1);

                                setRole(
                                    event.target.value
                                );

                            }
                        }
                        className="
                            input-field
                        "
                    >

                        <option value="">
                            Semua Role
                        </option>

                        <option value="INVESTIGATOR">
                            Investigator
                        </option>

                        <option value="SUPERVISOR">
                            Supervisor
                        </option>

                        <option value="ANALYST">
                            Analis
                        </option>

                    </select>



                    <select
                        value={
                            status
                        }
                        onChange={
                            (event)=>{

                                setPage(1);

                                setStatus(
                                    event.target.value
                                );

                            }
                        }
                        className="
                            input-field
                        "
                    >

                        <option value="">
                            Semua Status
                        </option>

                        <option value="ACTIVE">
                            Aktif
                        </option>

                        <option value="INACTIVE">
                            Nonaktif
                        </option>

                    </select>



                    <select
                        value={
                            pageSize
                        }
                        onChange={
                            (event)=>{

                                setPage(1);

                                setPageSize(
                                    Number(
                                        event.target.value
                                    )
                                );

                            }
                        }
                        className="
                            input-field
                        "
                    >

                        <option value={5}>
                            5 per halaman
                        </option>

                        <option value={10}>
                            10 per halaman
                        </option>

                        <option value={20}>
                            20 per halaman
                        </option>

                        <option value={50}>
                            50 per halaman
                        </option>

                    </select>


                </div>


            </div>



            {/* TABLE */}

            <div className="
                bg-white
                border
                rounded-xl
                overflow-hidden
            ">


                <div className="
                    overflow-x-auto
                ">


                    <table className="
                        w-full
                        text-sm
                    ">


                        <thead className="
                            bg-gray-50
                            text-gray-600
                        ">


                            <tr>

                                <th className="
                                    text-left
                                    px-5
                                    py-3
                                ">
                                    Investigator
                                </th>

                                <th className="
                                    text-left
                                    px-5
                                    py-3
                                ">
                                    Role
                                </th>

                                <th className="
                                    text-left
                                    px-5
                                    py-3
                                ">
                                    Unit
                                </th>

                                <th className="
                                    text-center
                                    px-5
                                    py-3
                                ">
                                    Aktif / Kapasitas
                                </th>

                                <th className="
                                    text-center
                                    px-5
                                    py-3
                                ">
                                    Selesai
                                </th>

                                <th className="
                                    text-center
                                    px-5
                                    py-3
                                ">
                                    Status
                                </th>

                                <th className="
                                    text-center
                                    px-5
                                    py-3
                                ">
                                    Aksi
                                </th>

                            </tr>


                        </thead>



                        <tbody>


                            {
                                loading

                                ?

                                (

                                    <tr>

                                        <td
                                            colSpan="7"
                                            className="
                                                px-5
                                                py-12
                                                text-center
                                                text-gray-500
                                            "
                                        >
                                            Memuat investigator...
                                        </td>

                                    </tr>

                                )

                                :

                                result.items.length === 0

                                ?

                                (

                                    <tr>

                                        <td
                                            colSpan="7"
                                            className="
                                                px-5
                                                py-12
                                                text-center
                                                text-gray-500
                                            "
                                        >
                                            Belum ada investigator.
                                        </td>

                                    </tr>

                                )

                                :

                                result.items.map(
                                    (item)=>(

                                        <tr
                                            key={
                                                item.id
                                            }
                                            className="
                                                border-t
                                            "
                                        >


                                            <td className="
                                                px-5
                                                py-4
                                            ">


                                                <div className="
                                                    font-semibold
                                                ">
                                                    {item.full_name}
                                                </div>


                                                <div className="
                                                    text-xs
                                                    text-gray-500
                                                    mt-1
                                                ">

                                                    {
                                                        item.employee_code
                                                        ||
                                                        "-"
                                                    }

                                                    {" · "}

                                                    {
                                                        item.email
                                                        ||
                                                        "-"
                                                    }

                                                </div>


                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                            ">
                                                {item.role}
                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                            ">
                                                {
                                                    item.unit
                                                    ||
                                                    "-"
                                                }
                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                                text-center
                                                font-semibold
                                            ">

                                                {
                                                    Number(
                                                        item.active_cases
                                                        ||
                                                        0
                                                    )
                                                }

                                                {" / "}

                                                {
                                                    Number(
                                                        item.max_active_cases
                                                        ||
                                                        0
                                                    )
                                                }

                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                                text-center
                                            ">

                                                {
                                                    Number(
                                                        item.closed_cases
                                                        ||
                                                        0
                                                    )
                                                }

                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                                text-center
                                            ">


                                                <span
                                                    className={
                                                        item.status
                                                        ===
                                                        "ACTIVE"

                                                        ?

                                                        "inline-flex px-3 py-1 rounded-full text-xs font-semibold bg-green-50 text-green-700"

                                                        :

                                                        "inline-flex px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-600"
                                                    }
                                                >

                                                    {
                                                        item.status
                                                        ===
                                                        "ACTIVE"

                                                        ?

                                                        "Aktif"

                                                        :

                                                        "Nonaktif"
                                                    }

                                                </span>


                                            </td>



                                            <td className="
                                                px-5
                                                py-4
                                                text-center
                                            ">


                                                <button
                                                    onClick={()=>
                                                        handleEdit(
                                                            item
                                                        )
                                                    }
                                                    className="
                                                        inline-flex
                                                        items-center
                                                        gap-2
                                                        border
                                                        rounded-lg
                                                        px-3
                                                        py-2
                                                        font-semibold
                                                        hover:bg-gray-50
                                                    "
                                                >

                                                    <Pencil
                                                        size={15}
                                                    />

                                                    Edit

                                                </button>


                                            </td>


                                        </tr>

                                    )
                                )
                            }


                        </tbody>


                    </table>


                </div>



                {/* PAGINATION */}

                <div className="
                    flex
                    flex-col
                    sm:flex-row
                    sm:items-center
                    sm:justify-between
                    gap-4
                    border-t
                    px-5
                    py-4
                ">


                    <div className="
                        text-sm
                        text-gray-500
                    ">

                        {
                            Number(
                                pagination.total
                                ||
                                0
                            )
                            .toLocaleString(
                                "id-ID"
                            )
                        }

                        {" pengguna · Halaman "}

                        {
                            pagination.page
                            ||
                            1
                        }

                        {" dari "}

                        {
                            pagination.total_pages
                            ||
                            1
                        }

                    </div>



                    <div className="
                        flex
                        gap-2
                    ">


                        <button
                            disabled={
                                !pagination.has_previous
                            }
                            onClick={()=>
                                setPage(
                                    (previous)=>
                                        Math.max(
                                            1,
                                            previous - 1
                                        )
                                )
                            }
                            className="
                                inline-flex
                                items-center
                                gap-2
                                border
                                rounded-lg
                                px-3
                                py-2
                                disabled:opacity-40
                            "
                        >

                            <ChevronLeft
                                size={16}
                            />

                            Sebelumnya

                        </button>



                        <button
                            disabled={
                                !pagination.has_next
                            }
                            onClick={()=>
                                setPage(
                                    (previous)=>
                                        previous + 1
                                )
                            }
                            className="
                                inline-flex
                                items-center
                                gap-2
                                border
                                rounded-lg
                                px-3
                                py-2
                                disabled:opacity-40
                            "
                        >

                            Berikutnya

                            <ChevronRight
                                size={16}
                            />

                        </button>


                    </div>


                </div>


            </div>



            <style>{`

                .input-field {

                    width: 100%;

                    border:
                        1px solid
                        rgb(209 213 219);

                    border-radius:
                        0.5rem;

                    padding:
                        0.625rem 1rem;

                    background:
                        white;

                }

            `}</style>


        </div>

    );

}



function Field({
    label,
    children
}){


    return (

        <label>


            <div className="
                text-sm
                font-semibold
                mb-2
            ">
                {label}
            </div>


            {children}


        </label>

    );

}