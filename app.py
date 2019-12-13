from flask import Flask, render_template, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeSerializer
from threading import Thread
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config.update(
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

mail = Mail(app)  # Declares a Mail instance
s = URLSafeSerializer(app.config['SECRET_KEY'])  # Safe Serializer instance used for unique link gen, obfuscates email


def generate_token(email):  # Function to generate token for unique URL
    token = s.dumps(email, salt='email-confirm')
    return token


def send_thread_email(msg):  # Email function to send asynchronous emails (better performance)
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


class SecretSanta(db.Model):
    """An object representing a person in a Secret Santa group.

    Attributes:
      member: The person's name (gift giver)
      email: Their email
      wishlist: The gift recipient's wishlist
      partner: The gift recipient
    """
    __tablename__ = 'secretsanta'
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    wishlist = db.Column(db.Text())
    partner = db.Column(db.String(200))

    def __init__(self, member, email, partner):
        self.member = member
        self.email = email
        self.partner = partner


# Takes a list of unique emails and generates a list of pairs
def generate_pairings(emails):
    f = {}  # dict containing name:group
    for i, line in enumerate(emails):
        group = line.strip().split(" ")
        f.update({p: i for p in group})
    names = list(f.keys())

    while True:
        # Shuffle the list until valid
        random.shuffle(names)
        assignments = {a: b for a, b in zip(names, names[1:] + [names[0]])}
        # List is valid
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
            else:
                if db.session.query(SecretSanta).filter(SecretSanta.email == email[ii]).count() == 0:
                    data = SecretSanta(
                        member=member[ii], email=email[ii], partner=pair[ii])
                    db.session.add(data)
                    token = generate_token(email[ii])  # Token for unique URL
                    link = url_for('wishlist', token=token, _external=True)   # Unique URL that routes user to wishlist
                    msg = Message('Hello from Optimal Secret Santa!',
                                  sender='OptimalSecretSanta@gmail.com',
                                  recipients=[email[ii]])
                    msg.body = F"Hi {member[ii]},\n\nGreetings from the North Pole!\n\nYou have been added to a Secret Santa group created on optimal-secret-santa.herokuapp.com.\n\nPlease use the below link to fill out the wishlist/message you would like to send your Secret Santa.\n\nLink:{link}\n\nHappy Holidays!\n\nSincerely,\nOptimalSecretSanta"
                    thr = Thread(target=send_thread_email, args=[msg])   # Create a thread for asynchronous emailing, this prevents web hangs
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
        msg = Message('Your Secret Santa Assignment is in!',  # Generates email message for assignment email
                      sender='OptimalSecretSanta@gmail.com',
                      recipients=[result.email])
        msg.body = F"Hi {result.member},\n\nYou have been assigned as the Secret Santa for {partner_name}. Their wishlist is included below: \n\n{wlist}\n\nHappy Holidays!\n\nSincerely,\nOptimalSecretSanta"
        thr = Thread(target=send_thread_email, args=[msg])
        thr.start()  # Send email asynchronously in background
        return render_template('success_wishlist.html')


if __name__ == '__main__':
    app.run(debug=True)
