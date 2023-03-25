export interface User{
    id:string;
    email:string;
    name:string;
    verified_user:boolean;
}

export interface EmailInterface{
    id:BigInteger;
    email:string;
    last_sent_on : string;
    email_delivered: boolean;
    email_opened : boolean;
}
