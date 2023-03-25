import React,{useState} from 'react'
import httpClient from '../httpClient';
import background from '../assets/bg-01.jpg'
import logo from '../assets/zippee-logo.jpeg'


const LoginPage:React.FC = () => {
    const [email,setEmail] = useState<string>("");
    const [password,setPassword] = useState<string>("");

    const loginUser = async () => {
            console.log(email,password)
        
    try{
        const resp = await httpClient.post("//127.0.0.1:5000/login",{
        email,
        password
    });
        window.location.href = "/"
    } catch (error : any){
        if (error.response.status === 401){
            alert('Invalid Credentials')
        }
    }
    };
  return (
    <div className="limiter">
        <div className="container-login100" style={{backgroundImage:`url(${background})`}}>
            <div className="wrap-login100 p-l-55 p-r-55 p-t-65 p-b-54">
                <form className="login100-form validate-form">
                    <span className="login100-form-title p-b-49">
                        <img src={logo} alt="Image" width="100" height="70"></img><br></br>
                        Login
                    </span>

                    <div className="wrap-input100  m-b-23">
                        <span className="label-input100">Email</span>
                        <input className="input100" type="text" value={email} onChange={(e) => setEmail(e.target.value)}></input>
                    </div>

                    <div className="wrap-input100">
                        <span className="label-input100">Password</span>
                        <input className="input100" type="password" value={password} onChange={(e) => setPassword(e.target.value)}></input>
                    </div>
                    <div className="container-login100-form-btn p-t-50">
                        <div className="wrap-login100-form-btn">
                            <div className="login100-form-bgbtn"></div>
                            <button className="login100-form-btn" type="button" onClick={() => loginUser()}>
                                Login
                            </button>
                        </div>
                    </div>
                    <div className="flex-col-c p-t-155">
                        <a href="/register" className="txt2">
                            Sign Up
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </div>
    // <div>
    //     <h1>Login</h1>
    //         <form>
    //             <div>
    //                 <label>Email: </label>
    //                 <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} id=""></input>
    //             </div>
    //             <div>
    //                 <label>Password: </label>
    //                 <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} id=""></input>
    //             </div>
    //         </form>
    //     <button type="button" onClick={() => loginUser()}>LogIn</button>
    // </div>
  )
}

export default LoginPage