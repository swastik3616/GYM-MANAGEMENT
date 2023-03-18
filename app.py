from flask import Flask,request,render_template,redirect,flash
from flask_sqlalchemy import SQLAlchemy
import mysql.connector as sql

app = Flask(__name__)
app.secret_key = "abc"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/gym"

db = SQLAlchemy(app)
class Joinus(db.Model):
    name = db.Column(db.String(30), primary_key=True)
    age = db.Column(db.Integer, unique=False)
    phone_number = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(30), unique=False, nullable=False)
    gender = db.Column(db.String(30), unique=False, nullable=False)
    membership = db.Column(db.String(30), unique=False, nullable=False)

class Sign(db.Model):
    username = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(30), unique=False)

@app.route('/join', methods =['GET','POST'])
def MemberInfo():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        phone_number = request.form.get('phone')
        email = request.form.get('email')
        gender = request.form.get('gender')
        membership = request.form.get('membership')
        entry = Joinus(name=name, age=age, phone_number=phone_number, email=email, gender=gender, membership=membership)
        db.session.add(entry)
        db.create_all()
        db.session.commit()
        return redirect('/success')
    return render_template("join.html")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods =['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('psw')
        con = sql.connect(host="localhost", user="root", password="root", database="gym")
        mypassword_queue = []
        sql_query = "SELECT *FROM sign WHERE username ='%s' AND password ='%s'" % (username, password)
        mycursor = con.cursor()
        try:
            mycursor.execute(sql_query)
            myresults = mycursor.fetchall()
            for row in myresults:
                for x in row:
                      mypassword_queue.append(x)
        except Exception as e:
            print(e)
            print('error occured')
        if (username and password) in mypassword_queue:
            flash("you are successfully logged in")
            return redirect('/profile')
        else:
            error = "invalid password"
    return render_template('login.html', error=error)
    con.close()
@app.route('/signup',methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('psw')
        rpassword = request.form.get('psw-repeat')
        if(password == rpassword):
            e = Sign(username=username, password=rpassword)
            db.session.add(e)
            db.create_all()
            db.session.commit()
            return redirect('/')
        else:
            error ="invalid password"
    return render_template("signup.html", error=error)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/index')
def ind():
    return render_template('index.html')


@app.route('/profile')
def prof():
    return render_template('profile.html')

@app.route('/profile1')
def profile2():
    con = sql.connect(host="localhost", user="root", password="root", database="gym")
    mycursor = con.cursor()
    mycursor.execute("SELECT *FROM joinus")
    myresults = mycursor.fetchall()
    print(myresults)
    con.close()
    return render_template('profile1.html',myresults=myresults[0])
if __name__ == "__main__":
    app.run(debug=True)


