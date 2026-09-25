import {
    translateClinicalMatch,
    formatRupiah
} from "../utils/translations";


export default function ClinicalTable({
    data = []
}){


    return (

        <div className="
            bg-white
            rounded-xl
            shadow
            border
            p-6
            mt-8
        ">


            <div className="
                mb-5
            ">

                <h2 className="
                    text-xl
                    font-bold
                ">
                    Validasi Klinis
                </h2>

                <p className="
                    text-sm
                    text-gray-500
                    mt-1
                ">
                    Pemeriksaan kesesuaian prosedur, obat, biaya, dan indikator risiko klaim.
                </p>

            </div>



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
                            bg-gray-50
                        ">


                            <th className="p-3 text-left">
                                Prosedur
                            </th>


                            <th className="p-3 text-left">
                                Obat
                            </th>


                            <th className="p-3 text-left">
                                Jumlah
                            </th>


                            <th className="p-3 text-left">
                                Biaya Ditagihkan
                            </th>


                            <th className="p-3 text-left">
                                Tarif Acuan
                            </th>


                            <th className="p-3 text-left">
                                Kesesuaian Prosedur
                            </th>


                            <th className="p-3 text-left">
                                Kesesuaian Obat
                            </th>


                            <th className="p-3 text-left">
                                Skor Risiko
                            </th>


                            <th className="p-3 text-left">
                                Anomali
                            </th>


                        </tr>


                    </thead>



                    <tbody>


                        {
                            data.length === 0
                            ? (

                                <tr>

                                    <td
                                        colSpan="9"
                                        className="
                                            p-6
                                            text-center
                                            text-gray-500
                                        "
                                    >
                                        Tidak terdapat data validasi klinis.
                                    </td>

                                </tr>

                            )
                            : (

                                data.map(
                                    (item,index)=>(


                                        <tr
                                            key={index}
                                            className="
                                                border-b
                                                last:border-b-0
                                                hover:bg-gray-50
                                            "
                                        >


                                            <td className="p-3">
                                                {item.procedure || "-"}
                                            </td>


                                            <td className="p-3">
                                                {item.medicine || "-"}
                                            </td>


                                            <td className="p-3">
                                                {item.quantity ?? "-"}
                                            </td>


                                            <td className="p-3">
                                                {
                                                    formatRupiah(
                                                        item.charged_amount
                                                    )
                                                }
                                            </td>


                                            <td className="p-3">
                                                {
                                                    formatRupiah(
                                                        item.tariff_amount
                                                    )
                                                }
                                            </td>


                                            <td className="p-3">

                                                {
                                                    translateClinicalMatch(
                                                        item.procedure_match
                                                    )
                                                }

                                            </td>


                                            <td className="p-3">

                                                {
                                                    translateClinicalMatch(
                                                        item.medicine_match
                                                    )
                                                }

                                            </td>


                                            <td className="p-3">

                                                <span className="
                                                    font-semibold
                                                ">
                                                    {item.detail_risk_score ?? 0}
                                                </span>

                                            </td>


                                            <td className="p-3">

                                                {
                                                    item.anomaly_flag
                                                    ? (

                                                        <span className="
                                                            inline-flex
                                                            px-3
                                                            py-1
                                                            rounded-full
                                                            text-xs
                                                            font-semibold
                                                            bg-red-100
                                                            text-red-700
                                                        ">
                                                            Terdeteksi
                                                        </span>

                                                    )
                                                    : (

                                                        <span className="
                                                            inline-flex
                                                            px-3
                                                            py-1
                                                            rounded-full
                                                            text-xs
                                                            font-semibold
                                                            bg-green-100
                                                            text-green-700
                                                        ">
                                                            Tidak
                                                        </span>

                                                    )
                                                }

                                            </td>



                                        </tr>


                                    )
                                )

                            )
                        }



                    </tbody>


                </table>


            </div>


        </div>

    );

}
