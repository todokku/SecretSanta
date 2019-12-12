# added by Wiley for link gen
from flask import Flask, render_template, request, url_for
from flask_mail import Mail, Message  # added by Wiley for flaskmail
from itsdangerous import URLSafeSerializer  # added by Wiley for url generator
from threading import Thread  # added by Wiley for asynch emailing
# from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import select, column
import random
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# MAIL_PASSWORD = 'EMAIL_PASSWORD'
# SECRET_KEY = 'SPECIAL_KEY'

app.config.update(  # added by Wiley
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='OptimalSecretSanta@gmail.com',
    MAIL_PASSWORD=os.environ['EMAIL_PASSWORD'],
    SECRET_KEY=os.environ['SPECIAL_KEY'],
    MAIL_MAX_EMAILS=1000
)

mail = Mail(app)  # declares Mail instance
s = URLSafeSerializer(app.config['SECRET_KEY'])  # safe serializer instance used for unique link gen


def generate_token(email):  # Function to generate token for unique URL
    token = s.dumps(email, salt='email-confirm')
    return token


def send_thread_email(msg):  # emailing function using threading to send emails asynchronously
    with app.app_context():
        mail.send(msg)


ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:g4qtyx7v@localhost/test_db'
else:
    app.debug = False
    # if not debugging(aka normal circumstances assign this URI)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zyyzysejezblhz:17a351947912f2433f7d4ca45121650d224b002543e633d521e57d4c4bb6d874@ec2-174-129-253-63.compute-1.amazonaws.com:5432/ddui50dco58tad'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class SecretSanta(db.Model):  # a class to represent a person within the secret santa
    __tablename__ = 'secretsanta'
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.String(200))  # the person's name
    email = db.Column(db.String(200), unique=True)  # the person's email
    wishlist = db.Column(db.Text())
    partner = db.Column(db.String(200))  # target partner's email

    def __init__(self, member, email, partner):
        self.member = member
        self.email = email
        self.partner = partner


# take people in the group and randomize and assign them to the proper partners
def generate_pairings(emails):
    f = {}  # dict containing name:group
    for i, line in enumerate(emails):
        group = line.strip().split(" ")
        f.update({p: i for p in group})
    names = list(f.keys())

    while True:
        # continually shuffles until every person has been shuffled
        random.shuffle(names)
        assignments = {a: b for a, b in zip(names, names[1:] + [names[0]])}
        if all([f[a] != f[b] for a, b in assignments.items()]):
            break
    pairs = [None]*len(names)
    for a, b in assignments.items():
        pairs[f[a]] = b
    return pairs


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])  # run when user submits their info
def submit():
    if request.method == 'POST':
        member = request.form.getlist('member')
        email = request.form.getlist('email')
        pair = generate_pairings(email)
        print(member, email, pair)
        for ii in range(len(member)):
            if member[ii] == '' or email[ii] == '':
                return render_template('index.html', message='Please ensure all fields are entered')
            # elif: // Email validation goes here (Using email-validator pkg from pip)
            else:
                if db.session.query(SecretSanta).filter(SecretSanta.email == email[ii]).count() == 0:
                    data = SecretSanta(
                        member=member[ii], email=email[ii], partner=pair[ii])
                    db.session.add(data)
                    token = generate_token(email[ii])  # token generated for unique URL
                    link = url_for('wishlist', token=token, _external=True) #unique link created to route user to wishlist
                    msg = Message('Hello from Optimal Secret Santa!',  # email message
                                  sender='OptimalSecretSanta@gmail.com',
                                  recipients=[email[ii]])
                    msg.body = F"Hi {member[ii]},\n\nGreetings from the North Pole!\n\nYou have been added to a Secret Santa group created on optimal-secret-santa.herokuapp.com.\n\nPlease use the below link to fill out the wishlist/message you would like to send your Secret Santa.\n\nLink:{link}\n\nHappy Holidays!\n\nSincerely,\nOptimalSecretSanta"
                    thr = Thread(target=send_thread_email, args=[msg]) #create thread for asynchronous mail
                    thr.start()  
                else:
                    return render_template('index.html', message='A user with this email is already a part of Secret Santa')
        db.session.commit()
        return render_template('success.html')


@app.route('/wishlist/')
@app.route('/wishlist/<userid>')
def wishlist(userid=None):
    return render_template('wishlist.html', userid=userid)


@app.route('/return', methods=['POST'])
def wish_submit():
    if request.method == 'POST':
        partner = str(request.form.get('partner'))
        wlist = str(request.form.get('wishlist'))
        result = SecretSanta.query.filter_by(partner=partner).first()
        result.email
        partner_email = SecretSanta.query.filter_by(email=partner).first()
        partner_name = str(partner_email.member)
        member_name = str(result.member)
        # partner_list = str(result.wlist)
        # print(partner, wlist, result.email,
        # result.member, result.id, result.partner)
        msg = Message('Your Secret Santa Assignment is in!',  # generates email message for assignment email
                      sender='OptimalSecretSanta@gmail.com',
                      recipients=[result.email])
        msg.body = F"Hi {result.member},\n\nYou have been assigned as the Secret Santa for {partner_name}. Their wishlist is included below: \n\n{wlist}\n\nHappy Holidays!\n\nSincerely,\nOptimalSecretSanta"
        thr = Thread(target=send_thread_email, args=[msg])
        thr.start()  # send email asynchronously
        return render_template('success_wishlist.html')


if __name__ == '__main__':
    app.run(debug=True)
