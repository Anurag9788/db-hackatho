from flask import Flask,render_template,redirect,session,request,url_for,jsonify,session
from flaskext.mysql import MySQL
# from flask_sqlalchemy import SQLAlchemy
from pymysql import NULL
from flask_cors import CORS
import Helpers.face_taker as ft
import Helpers.face_recognizer as fr
# from flask_migrate import Migrate
app = Flask(__name__,static_folder='templates/static')
CORS(app)
coordinates = []
app.config['UPLOAD_FOLDER'] = 'templates/static/uploads'


app.config['MYSQL_DATABASE_HOST'] = 'dbhackathon'
app.config['MYSQL_DATABASE_USER'] = 'hackathon'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'dementia'

db=MySQL(app)
db.init_app(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres_password@dbhackathon:57432/hackathon'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# from models import * 
# migrate = Migrate(app, db)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/caregiver')
def caretakerview():
    return render_template('caregiver.html')

@app.route('/register',methods=["GET","POST"])
def register():
    if request.method=='GET':
        return render_template("login.html")
    else:
        # fname=request.form['first_name']
        # lname=request.form['last_name']
        email=request.form['email']
        # password=request.form['password']
        gender=request.form['gender']
        dob=request.form['birthday']
        username=request.form['username']
        contact=request.form['phone']


        conn=mysql.connect()
        cur=conn.cursor()
        
        cur.execute("INSERT INTO patients VALUES (%s,%s,%s,%s,%s)",(email, username, gender, contact, dob))
        # cur.execute("INSERT INTO leaderboard(username) VALUES (%s)",(username))
    
        conn.commit()
        cur.close()
        # session['fname']=request.form['first_name']
        # session['email']=request.form['email']
        session['email']=email
        session['user_type']=user_type
        return redirect(url_for('login'))

@app.route('/getPatientDetails', methods=['GET'])
def getPatientDetails():
        conn=mysql.connect()
        cur=conn.cursor()
        uname="trupti"
        cur.execute("Select * from patients WHERE name = {uname}")
        # cur.execute("INSERT INTO leaderboard(username) VALUES (%s)",(username))
        myresult = cur.fetchall()

        for x in myresult:
            print(x)
        conn.commit()
        cur.close()
    

    


@app.route('/caretakerlogin',methods=["GET","POST"])
def caretakerlogin():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        if email == "caretaker@admin.com" and password=="password":
            session['caretaker']=1
            return redirect(url_for('caretakerportal'))
        else:
            return "Error in password or email mismatch"
    else:
        return render_template('caretakerlogin.html')

@app.route('/caretakerportal',methods=["GET","POST"])
def caretakerportal():
    # total_Q=numQues()
    pass

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        cur=db.connect().cursor()
        cur.execute("select * from patients where email='"+email+"' ")
        user=cur.fetchone()
        
        cur.close()
        # print("hey")
        #if user > 0:
        if password == user[3]:
            print("hello")
            session['name']=user[0]
            session['lname']=user[1]
            session['email']=user[2]
            session['username']=user[6]
            session['user_marks']=0
            session['i']=1

            return render_template("home.html")

        else:
            return "Please enter Correct password again"

        # else:
        #     return "error User not found"
    else:
        return render_template('login.html')

@app.route('/send_coordinates', methods=['POST'])
def send_coordinates():
    data= request.get_json()
    if 'latitude' in data and 'longitude' in data:
        coordinates.append({'latitude': data['latitude'],'longitude': data['longitude']})
        return jsonify({'message': 'Coordinates received', 'data':data}),200
    else :
        return jsonify({'error':'Invalid data'}), 400

@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    return jsonify({'coordinates': coordinates}),200

@app.route('/take_photo/<name>',methods=['GET'])
def take_photos(name):
    # user = session['user_type']
    user = 'care_taker'
    ft.take_face(name,user)
    return render_template('home.html')

@app.route('/find_patient',methods=['GET','POST'])
def face_recognise():
    user = 'care_taker'
    fr.face_recognise(user)
    return render_template('home.html')

if __name__ =="__main__":
    with app.app_context():
        # db.create_all()
        pass
    app.run(debug=True,port=8080,use_reloader=False)