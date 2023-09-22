from flask import Flask, request , render_template,jsonify,redirect,url_for,session,flash
from werkzeug.utils import secure_filename
from database_functions import *
import os



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
            db.execute(f"SELECT password FROM users WHERE email = '{email}' ")
            result = db.fetchall()
            if result[0][0] == psd:
                # session["email"]=email
                return redirect(url_for('dashboard'))
            else:
                flash('invalid password. Try Again..', category='error')
                return render_template(r"index.html")
        except:
            flash('invalid email/password. Try Again..', category='error')
            return render_template(r"index.html")

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if request.method == 'GET':
            return render_template(r'dashboard.html')
    if request.method == "POST":
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return redirect(url_for('dashboard'))
    # try:
    #     if session["email"]:
    #         # session.clear()
    #         return render_template(r'dashboard.html')
    # except KeyError:
    #     return redirect(url_for('login'))
        

if __name__ == '__main__':
    app.run(debug=True)