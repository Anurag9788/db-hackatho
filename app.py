from flask import Flask,render_template,redirect,session,request,url_for,jsonify,session
from flaskext.mysql import MySQL
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import Helpers.face_taker as ft
import Helpers.face_recognizer as fr
import os
# from flask_migrate import Migrate
app = Flask(__name__,static_folder='templates/static')
CORS(app)
coordinates = []
app.config['UPLOAD_FOLDER'] = 'templates/static/uploads'


app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'trupti@1198'
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
    conn=db.connect()
    cur=conn.cursor()
    query_string = "SELECT * FROM patients"
    cur.execute(query_string)
    # cur.execute("INSERT INTO leaderboard(username) VALUES (%s)",(username))
    patients = cur.fetchall()

    query_string = "SELECT count(*) FROM patients"
    cur.execute(query_string)
    patients_count = cur.fetchall()
    for x in patients:
        print(x)
    conn.commit()
    cur.close()
    
    return render_template('caregiver.html',patients=patients,patients_count=patients_count)


@app.route('/patient')
def patientview():
    conn=db.connect()
    cur=conn.cursor()
    query_string = "SELECT * FROM patients"
    cur.execute(query_string)
    # cur.execute("INSERT INTO leaderboard(username) VALUES (%s)",(username))
    patients = cur.fetchall()

    query_string = "SELECT count(*) FROM patients"
    cur.execute(query_string)
    patients_count = cur.fetchall()
    for x in patients:
        print(x)
    conn.commit()
    cur.close()
    
    return render_template('patient.html',patients=patients,patients_count=patients_count)

@app.route('/registerpatient',methods=["GET","POST"])
def register():
    if request.method=='GET':
        return render_template("login.html")
    else:
        # fname=request.form['first_name']
        # lname=request.form['last_name']
        email=request.form['email']
        # password=request.form['password']
        # gender=request.form['gender']
        # dob=request.form['birthday']
        username=request.form['username']
        contact=request.form['phone']


        conn=db.connect()
        cur=conn.cursor()
        
        cur.execute("INSERT INTO patients VALUES (%s,%s,%s,%s,%s)",(email, username, gender, contact, dob))
        # cur.execute("INSERT INTO leaderboard(username) VALUES (%s)",(username))
    
        conn.commit()
        cur.close()
        # session['fname']=request.form['first_name']
        # session['email']=request.form['email']
        session['email']=email
        session['user_type']="caregiver"
        return redirect(url_for('login'))

@app.route('/getPatientDetails', methods=['GET'])
def getPatientDetails():
        conn=db.connect()
        cur=conn.cursor()
        uname="trupti"
        query_string = "SELECT * FROM patients WHERE  name= %s"
        cur.execute(query_string, (uname,))
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
        email=request.form['LoginId']
        password=request.form['Password']

        cur=db.connect().cursor()
        cur.execute(f"select * from patients where mail='{email}' ")
        user=cur.fetchone()
        
        cur.close()
        # print("hey")
        #if user > 0:
        if password:
            print(request.form)
            if "CaregiverLogin" in request.form and request.form['CaregiverLogin']=='caregiver':


                return render_template("caregiver.html")
            else:
                return  render_template("patient.html")

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

# @app.route('/patientupload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         first_name = request.form['full_name']
#         last_name = request.form['last_name']
#         date_of_birth = request.form['age']
#         image = request.files['image']

#         if image:
#             image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
#             image.save(image_path)

            
#             db.session.add(new_patient)
#             db.session.commit()

#             return redirect(url_for('index'))

#     return render_template('upload.html')


if __name__ =="__main__":
    with app.app_context():
        # db.create_all()
        pass
    app.run(debug=True,port=8080,use_reloader=False)