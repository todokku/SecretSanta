from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:g4qtyx7v@localhost/test_db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zyyzysejezblhz:17a351947912f2433f7d4ca45121650d224b002543e633d521e57d4c4bb6d874@ec2-174-129-253-63.compute-1.amazonaws.com:5432/ddui50dco58tad'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class SecretSanta(db.Model):
    __tablename__ = 'secretsanta'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(200), unique=True)
    member = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    wishlist = db.Column(db.Text())
    partner = db.Column(db.String(200))

    def __init__(self, member, email, wishlist=''):
        self.member = member
        self.email = email
        # self.uuid = uuid
        self.wishlist = wishlist
        # self.partner = partner

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
                    # Pass the email list to assignment function

                    data = SecretSanta(member=member[ii], email=email[ii], partner=pair[ii])
                    db.session.add(data)
                else:
                    return render_template('index.html', message='A user with this email is already a part of Secret Santa')
        db.session.commit()
        # send_mail(customer, dealer, rating, comments)
        # Send mail function - Working to get this updated with bulk emails
        return render_template('success.html')


@app.route('/wishlist/<user_id>', methods=['POST', 'GET'])
def wishlist(user_id):
    return render_template('wishlist.html')


if __name__ == '__main__':
    app.run(debug=True)
