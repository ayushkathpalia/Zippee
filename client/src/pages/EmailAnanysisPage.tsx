import React,{useState,useEffect} from 'react'
import httpClient from "../httpClient";
import { EmailInterface } from "../type";

const EmailAnanysisPage: React.FC = () => {
    const [data,setData] = useState<EmailInterface[]>([]);
    useEffect(() => {
        (async () =>{
            try{
                const resp = await httpClient.get("//127.0.0.1:5000/emailanalysis");
                setData(resp.data);
            }catch (error){
                console.log("Error");
            }
        })();
    }, []);
  return (
    <div>
        <h1>EmailAnanysisPage</h1>
        <table id="emailanalysistable">
            <tr>
                <th>Id</th>
                <th>Email</th>
                <th>Sent On</th>
                <th>Email Delivered</th>
                <th>Email Opened</th>
            </tr>
            
                {data != null ? 
                (data.map((value) => (
                        <tr>
                        <td>{value.id}</td>
                        <td>{value.email}</td>
                        <td>{value.last_sent_on}</td>
                        {value.email_delivered == true ? <td>True</td> : <td>False</td>}
                        {value.email_opened == true ? <td>True</td> : <td>False</td>}
                        </tr>
                ))):(
                    <tr>
                    <h2>No data found</h2>
                    </tr>
                )};
        </table>
    </div>
  )
}

export default EmailAnanysisPage