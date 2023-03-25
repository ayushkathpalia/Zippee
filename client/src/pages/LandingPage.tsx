import React,{useState,useEffect} from "react";
import httpClient from "../httpClient";
import { User } from "../type";
import background from '../assets/bg-01.jpg'
import logo from '../assets/zippee-logo.jpeg'


const LandingPage: React.FC = () => {
    const [user,setUser] = useState<User | null>(null);
    
    const logoutUser = async () => {
        await httpClient.post("//127.0.0.1:5000/logout");
        window.location.href="/";
    }

    useEffect(() => {
        (async () =>{
            try{
                const resp = await httpClient.get("//127.0.0.1:5000/@me");
                setUser(resp.data);
            }catch (error){
                console.log("Not Authenticated");
            }
        })();
    }, []);
    return (
        <div className="limiter">
        <div className="container-login100" style={{backgroundImage:`url(${background})`}}>
            <div className="wrap-login100 p-l-55 p-r-55 p-t-65 p-b-54">
                <span className="login100-form-title p-b-49">
                        <img src={logo} alt="Image" width="100" height="70"></img><br></br>
                        <h3>Welcome to Zippee</h3>
                    </span>
                    {user != null ? (
                        <div>
                        <h2>Hi {user.name}</h2>
                        {user.verified_user == true ? <h3>Login Successful </h3>: <h3>Please activate your account by clicking the verification link sent</h3>}
                        <button className="buttonlandingpage" onClick={logoutUser}>Logout</button>
                    </div>
                    ):(
                    <div>
                        <h2>Hi User !</h2>
                        <div>
                            <a href="/login"><button className="buttonlandingpage">Login</button></a><br></br>
                            <a href="/register"><button className="buttonlandingpage">Register</button></a>
                        </div>
                    </div>
                    )}
            </div>
        </div>
        </div>
        )};
export default LandingPage;