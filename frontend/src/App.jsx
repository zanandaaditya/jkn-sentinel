import {
    BrowserRouter,
    Routes,
    Route
} from "react-router-dom";


import MainLayout from "./layouts/MainLayout";

import Dashboard from "./pages/Dashboard";

import ClaimDetail from "./pages/ClaimDetail";

import FraudCases from "./pages/FraudCases";

import FraudAnalytics from "./pages/FraudAnalytics";

import InvestigatorWorkbench from "./pages/InvestigatorWorkbench";

import InvestigatorRegistry from "./pages/InvestigatorRegistry";

function App(){


return (

<BrowserRouter>


<MainLayout>


<Routes>

    <Route
        path="/"
        element={<Dashboard/>}
    />

    <Route
        path="/fraud-cases"
        element={<FraudCases/>}
    />

    <Route
        path="/claims/:id"
        element={<ClaimDetail/>}
    />

    <Route
        path="/fraud-analytics"
        element={<FraudAnalytics/>}
    />

    <Route
        path="/investigator-workbench"
        element={<InvestigatorWorkbench/>}
    />

    <Route
        path="/investigators"
        element={
            <InvestigatorRegistry/>
        }
    />

</Routes>


</MainLayout>


</BrowserRouter>

)

}


export default App;