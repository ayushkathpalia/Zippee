from flask import Flask,request,jsonify,session,url_for
from flask_bcrypt import Bcrypt
from models import db,User,EmailAnalytics
from config import ApplicationConfig
from flask_session import Session
from flask_cors import CORS,cross_origin
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_apscheduler import APScheduler


app = Flask(__name__)
app.config.from_object(ApplicationConfig)
bcrypt = Bcrypt(app)
mail = Mail(app)
CORS(app,supports_credentials=True)
Session(app)
schedular = APScheduler()
serializer = URLSafeTimedSerializer(ApplicationConfig.SECRET_KEY,salt="email-comfirm")
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/@me",methods=["GET"])
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error":"Unauthorized"}), 401
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id" : user.id,
        "email" : user.email,
        "verified_user":user.verified_user,
        "name": user.name
    })

@app.route("/register",methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]
    name = request.json["name"]
    address = request.json["address"]
    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error" : "User already Exists"}), 409
    
    f = open('tokens.txt','w+')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email,password =hashed_password,name = name,address = address)
    db.session.add(new_user)
    db.session.commit()

    #send email
    serializer.dump(email,f=f,salt='email-confirm')
    msg = Message('Confirm Email',sender='fellasniperbot@gmail.com',recipients=[email])
    f = open('tokens.txt','r')
    token = f.readline()
    link = url_for('confirm_email',token=token,_external=True)
    msg.body = f'Please activate your account {link}'
    mail.send(msg)
    session["user_id"] = new_user.id
    return jsonify({
        "id" : new_user.id,
        "email" : new_user.email,
        "name" : new_user.name
    })

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token,salt='email-confirm',max_age=3600) #seconds
        user = User.query.filter_by(email=email).first()
        user.verified_user = True
        db.session.commit()
    except SignatureExpired:
        return 'TOKEN EXPIRED'
    return 'TOKEN VALID'

@app.route("/login",methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]
    user = User.query.filter_by(email=email).first()
    
    if user is None:
        return jsonify({"error":"Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password,password):
        return jsonify({"error":"Unauthorized"}), 401
    
    session["user_id"] = user.id
    
    return jsonify({
        "id" : user.id,
        "email" : user.email
    })

@app.route("/logout",methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"

@app.route("/emailanalysis")
def email_analysis():
    email_data = EmailAnalytics.query.all()
    all_data = [{'id':email.id,'email':email.email,'last_sent_on':email.last_sent_on,'email_delivered':email.email_delivered,'email_opened':email.email_opened} for email in email_data]
    return jsonify(all_data)

def schedule_mails():
    #send email
    emails = []
    print('in schedule mails')
    with app.app_context():
        user_data = User.query.filter_by(verified_user=True).all()
        for data in user_data:
            emails.append(data.email)
        emails.append('fellasniperbot@gmail.com')
        msg = Message('Daily Updates',sender='fellasniperbot@gmail.com',recipients=emails,extra_headers={'Disposition-Notification-To': 'fellasniperbot@gmail.com','Recipt-Notification-to':'fellasniperbot@gmail.com'})
        msg.body = f'Hi,Terms & Conditions Updated'
        print('mail sent')
        mail.send(msg)
    
        for email in emails:
            email_detail = EmailAnalytics(email=email)
            db.session.add(email_detail)
            db.session.commit()


# def checkifdelivered():
    # from imap_tools import MailBox,AND
    # print('in check delivered')
    # with MailBox('imap.mail.com').login('fellasniperbot@gmail.com','vjoritoicnkpfeec','INBOX') as mailbox:
    #     for msg in mailbox.fetch(AND(from_='mailer-daemon@googlemail.com',seen = True)):
    #         print(msg.subject)
    #         body = msg.text
    #         print(body)
    # import imaplib,email
    # imap_server = 'imap.gmail.com'
    # email_address = 'fellasniperbot@gmail.com'
    # password = 'vjoritoicnkpfeec'
    # imap = imaplib.IMAP4_SSL(imap_server)
    # imap.login(email_address,password)
    # imap.select('INBOX')
    # _,msgs = imap.search(None,'(FROM "Mail Delivery Subsystem")')

    # for msg in msgs[0].split():
    #     _,data = imap.fetch(msg,"(RFC822)")
    #     message = email.message_from_bytes(data[0][1])
    #     print(f"FROM:{message.get('FROM')}")
    #     print(f"DATE:{message.get('DATE')}")
    #     print(f"TO:{message.get('TO')}")
    #     #print(f"Final-Recipient:{message.get('Final-Recipient')}")
    #     # print("Content : ")
    #     for part in message.walk():
    #         if part.get_content_type() == 'text/plain':
    #             print(part.as_string())
    #     print('-------------------------------------')
    
    # imap.close()

# @app.route("/static/<path:path>")
# def static_file(path):
#     print(path)
#     return send_from_directory('static', path)



if __name__ == '__main__':
    schedular.add_job(id='mail_job',func=schedule_mails,trigger='cron',day_of_week='mon-sun',hour=16,minute=0)
    schedular.start()
    app.run(debug=True)
