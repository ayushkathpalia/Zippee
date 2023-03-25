import { BrowserRouter,Routes,Route} from "react-router-dom"
import EmailAnanysisPage from "./pages/EmailAnanysisPage"
import LandingPage from "./pages/LandingPage"
import LoginPage from "./pages/LoginPage"
import NotFound from "./pages/NotFound"
import RegisterPage from "./pages/RegisterPage"

const Router = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" Component={LandingPage}/>
                <Route path="/login" Component={LoginPage}/>
                <Route path="/register" Component={RegisterPage}/>
                <Route path="/emailanalysis" Component={EmailAnanysisPage}/>
                <Route path="*" Component={NotFound}/>
            </Routes>
        </BrowserRouter>
    )
}
export default Router