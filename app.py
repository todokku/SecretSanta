from flask import Flask, render_template, request, url_for#added by Wiley for link gen
from flask_mail import Mail, Message#added by Wiley for flaskmail
from itsdangerous import URLSafeSerializer#added by Wiley for url generator
from threading import Thread#added by Wiley for asynch emailing
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
import info_2

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config.update(#added by Wiley
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'OptimalSecretSanta@gmail.com',
	MAIL_PASSWORD = 'AllIwantforChristmasisanA',
    SECRET_KEY = "PanatLovesDogs",
    MAIL_MAX_EMAILS = 1000
	)

mail=Mail(app) #added by Wiley
s = URLSafeSerializer(app.config['SECRET_KEY']) #added by Wiley

def generate_token(email): #added by Wiley
    token = s.dumps(email, salt= 'email-confirm')
    return token

def send_thread_email(msg):#added by Wiley
    with app.app_context():
        mail.send(msg)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:g4qtyx7v@localhost/test_db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zyyzysejezblhz:17a351947912f2433f7d4ca45121650d224b002543e633d521e57d4c4bb6d874@ec2-174-129-253-63.compute-1.amazonaws.com:5432/ddui50dco58tad'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# class Feedback(db.Model):
#     __tablename__ = 'feedback'
#     id = db.Column(db.Integer, primary_key=True)
#     #uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
#     member = db.Column(db.String(200))
#     email = db.Column(db.String(200), unique=True)
#     comments = db.Column(db.Text())

#     def __init__(self, member, email, comments=''):
#         self.member = member
#         self.email = email
#         self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        member = request.form.getlist('member')
        email = request.form.getlist('email')
        print(member, email)

        for ii in range(len(member)):
            if member[ii] == '' or email[ii] == '':
                return render_template('index.html', message='Please ensure all fields are entered')
            # elif: // Email validation goes here (Using email-validator pkg from pip)
            else:
                # if db.session.query(Feedback).filter(Feedback.email == email[ii]).count() == 0:
                #     data = Feedback(member[ii], email[ii])
                #     db.session.add(data)
                token = generate_token(ii['email'])#wiley add start
                link = url_for('wishlist', token = token, _external = True)
                try:
                    msg = Message('Hello from Optimal Secret Santa!',#subject
                    sender = 'OptimalSecretSanta@gmail.com',
                    recipients = [email[ii]])
                    msg.body = F"Hi {member[ii]},\n\nGreetings from the North Pole!\n\nYou have been added to a Secret Santa group created on optimal-secret-santa.herokuapp.com.\n\nPlease use the below link to fill out the wishlist/message you would like to send your Secret Santa.\n\nLink:{link}\n\nHappy Holidays!\n\nSincerely,\nOptimalSecretSanta."
                    thr = Thread(target=send_thread_email, args=[msg])
                    thr.start()#wiley add end
                    return
                except Exception as e:
                    return str(e)
            # else:
                return render_template('index.html', message='A user with this email is already a part of Secret Santa')
        #db.session.commit()
        # send_mail(customer, dealer, rating, comments)
        # Send mail function - Working to get this updated with bulk emails
        return render_template('success.html')


@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist(user_id):
    return render_template('wishlist.html')


if __name__ == '__main__':
    app.run(debug=True)
