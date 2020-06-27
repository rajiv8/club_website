from flask import Flask,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


with open("config.json","r") as c:
    params=json.load(c)["params"]

local_server=True

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.secret_key='super-secret-key'

if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"]=params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"]=params['prod_uri']


db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(13), nullable=False)
    mess = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(12), nullable=True)



@app.route("/")
def home():

    return render_template('index.html',params=params)
@app.route("/activity")
def activity():

    return render_template('activity.html',params=params)

@app.route("/contact",methods=['GET','POST'])
def contact():

    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name=name, phone_num=phone, mess=message, email=email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        flash("Thank you for contacting us, we will get back to you soon.","success")


    return render_template('contact.html',params=params)

@app.route("/team")
def team():

    return render_template('team.html')


if __name__ == '__main__':
    app.run(debug=True)

