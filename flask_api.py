from flask import Flask, request , render_template,jsonify,redirect,url_for,session,flash,send_file
from werkzeug.utils import secure_filename
from database_functions import *
import os, re
from data_scrape import data_scrape



app = Flask(__name__)
UPLOAD_FOLDER = 'PDF'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'raspibm'

@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template(r"index.html")
    elif request.method == 'POST':
        email = request.form['uname']
        psd = request.form['psd']
        db,connection=connect_database("RAS")
        try:
            db.execute(f"SELECT password,institute_name FROM users WHERE email = '{email}' ")
            result = db.fetchall()
            if result[0][0] == psd:
                session["iname"]=str(result[0][1]).replace(" ","_")
                return redirect(url_for('getcsv'))
            else:
                flash('Invalid password. Try Again..', category='error')
                return render_template(r"index.html")
        except:
            flash('Invalid email/password. Try Again..', category='error')
            return render_template(r"index.html")


def is_valid_password(psd,cpsd,phone):
    phone_pattern = r'^[789]\d{9}$'
    if psd != cpsd:
        return False
    if len(psd) < 8:
        return False
    if not re.match(phone_pattern,phone):
        return False
    if not (re.search(r'[A-Z]', psd) and
            re.search(r'[a-z]', psd) and
            re.search(r'\d', psd) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', psd)):
        return False
    
    return True


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template(r"signup.html")
    elif request.method == 'POST':
        email = request.form['uname']
        phone = request.form['phone']
        psd = request.form['psd']
        cpsd = request.form['cpsd']
        iname = request.form['iname']

    if is_valid_password(psd,cpsd,phone):
        db,connection=connect_database("RAS")
        sql_insert_query = "INSERT INTO users (email, password, phone_no, institute_name) VALUES (%s, %s, %s, %s)"
        user_data = (email, psd, phone, iname)
        db.execute(sql_insert_query,user_data)
        flash('User Registed Succesfully.', category='success')
        return render_template(r"signup.html")
    else:
        flash('Invalid Password or Mobile Number. Try Again..', category='error')
        return render_template(r"signup.html")


def is_pdf(filename):
    return filename.lower().endswith('.pdf')


@app.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/getcsv', methods=['GET','POST'])
def getcsv():
    if request.method == 'GET':
        try:
            return render_template(r'getcsv.html')
        except:
            return redirect(url_for('login'))
    if request.method == "POST":
        f = request.files['file']
        filename = secure_filename(f.filename)
        if not is_pdf(filename):
            return jsonify({"message": "File is not a PDF", "status_code": 400})
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        data_scrape(filename)
        response = send_file(f"TEMP/{filename[:-4]}.csv", as_attachment=True)
        try:
            return response
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "An error occurred while serving the file", 500
        

if __name__ == '__main__':
    app.run(debug=True)