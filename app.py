from flask import Flask, render_template, request
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:g4qtyx7v@localhost/test_db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zyyzysejezblhz:17a351947912f2433f7d4ca45121650d224b002543e633d521e57d4c4bb6d874@ec2-174-129-253-63.compute-1.amazonaws.com:5432/ddui50dco58tad'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    #uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    member = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    comments = db.Column(db.Text())

    def __init__(self, member, email, comments=''):
        self.member = member
        self.email = email
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        member = request.form.getlist('member')
        email = request.form.getlist('email')
        print(member, email)
        # return render_template('success.html')

        if member == '' or email == '':
            return render_template('index.html', message='Please enter required fields')

        # if db.session.query(Feedback).filter(Feedback.member == member).count() == 0:
        for ii in range(len(member)):
            data = Feedback(member[ii], email[ii])
            db.session.add(data)
        db.session.commit()
        # send_mail(customer, dealer, rating, comments)
        return render_template('success.html')
        # else:
        #     return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.run()
