from flask import Flask, request , render_template,jsonify,redirect,url_for,session,flash,send_file
from ras.functions.functions import *
import os, re
from ras.functions.data_scrape import data_scrape
from ras.functions.data_analysis import statastics
from werkzeug.utils import secure_filename
from run import app

@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template(r"index.html")
    elif request.method == 'POST':
        email = request.form['uname']
        psd = request.form['psd']
        db,connection=connect_database(app.config['USER_DATABASE'])
        try:
            db.execute(f"SELECT password,institute_name FROM users WHERE email = '{email}' ")
            result = db.fetchall()
            if result[0][0] == psd:
                session["iname"]=str(result[0][1]).replace(" ","_")
                return redirect(url_for('getcsv'))
            else:
                flash('Invalid password. Try Again..', category='error')
                return render_template(r"index.html"),401
        except:
            flash('Invalid email/password. Try Again..', category='error')
            return render_template(r"index.html"),401
        


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
        db,connection=connect_database(app.config['USER_DATABASE'])
        sql_insert_query = "INSERT INTO users (email, password, phone_no, institute_name) VALUES (%s, %s, %s, %s)"
        user_data = (email, psd, phone, iname)
        db.execute(sql_insert_query,user_data)
        create_database_query = f"CREATE DATABASE IF NOT EXISTS {iname.replace(' ','_')}"
        db.execute(create_database_query)
        connection.commit()
        flash('User Registered Succesfully.', category='success')
        return render_template(r"signup.html")
    else:
        flash('Invalid Password or Mobile Number. Try Again..', category='error')
        return render_template(r"signup.html"),200



@app.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/health',methods=['GET','POST'])
def healthcheck():
    return jsonify(
        status="UP"
    )

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
        filename = f"{session['iname']}_{filename}"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        data_scrape(filename)
        # statastics(filename)
        zip_csv_files(app.config['CSV_DIRECTORY'],f"{session['iname']}_data")
        response = send_file(os.path.join("../",f"{session['iname']}_data"), as_attachment=True)
        try:
            return response
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "An error occurred while serving the file", 500
        finally:
            pass