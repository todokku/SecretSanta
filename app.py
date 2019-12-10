# added by Wiley for link gen
from flask import Flask, render_template, request, url_for
from flask_mail import Mail, Message  # added by Wiley for flaskmail
from itsdangerous import URLSafeSerializer  # added by Wiley for url generator
from threading import Thread  # added by Wiley for asynch emailing
# from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
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

mail = Mail(app)  # added by Wiley
s = URLSafeSerializer(app.config['SECRET_KEY'])  # added by Wiley


def generate_token(email):  # added by Wiley
    token = s.dumps(email, salt='email-confirm')
    return token


def send_thread_email(msg):  # added by Wiley
    with app.app_context():
        mail.send(msg)


ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:[LOCAL_POSTGRES_PASSWORD]@localhost/test_db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zyyzysejezblhz:17a351947912f2433f7d4ca45121650d224b002543e633d521e57d4c4bb6d874@ec2-174-129-253-63.compute-1.amazonaws.com:5432/ddui50dco58tad'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class SecretSanta(db.Model):
    __tablename__ = 'secretsanta'
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    wishlist = db.Column(db.Text())
    partner = db.Column(db.String(200))

    def __init__(self, member, email, partner):
        self.member = member
        self.email = email
        # self.uuid = uuid
        # self.wishlist = wishlist
        self.partner = partner


def generate_pairings(emails):
    f = {}  # dict containing name:group
    for i, line in enumerate(emails):
        group = line.strip().split(" ")
        f.update({p: i for p in group})
    names = list(f.keys())

    while True:
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


@app.route('/submit', methods=['POST'])
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
                    token = generate_token(email[ii])  # wiley add start
                    link = url_for('wishlist', token=token, _external=True)
                    msg = Message('Hello from Optimal Secret Santa!',  # subject
                                  sender='OptimalSecretSanta@gmail.com',
                                  recipients=[email[ii]])
                    msg.body = F"Hi {member[ii]},\n\nGreetings from the North Pole!\n\nYou have been added to a Secret Santa group created on optimal-secret-santa.herokuapp.com.\n\nPlease use the below link to fill out the wishlist/message you would like to send your Secret Santa.\n\nLink:{link}\n\nHappy Holidays!\n\nSincerely,\nOptimalSecretSanta"
                    thr = Thread(target=send_thread_email, args=[msg])
                    thr.start()  # wiley add end
                else:
                    return render_template('index.html', message='A user with this email is already a part of Secret Santa')
        db.session.commit()
        return render_template('success.html')


@app.route('/wishlist/<userid>')
def wishlist(userid):
    return render_template('wishlist.html')


if __name__ == '__main__':
    app.run(debug=True)
