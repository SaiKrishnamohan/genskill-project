import datetime

from flask import Blueprint,Flask
from flask import render_template,request,redirect,url_for,jsonify
from flask import g, session

from . import db

app=Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    if request.method=='POST':
        username=request.form.get('username')
        conn=db.get_db()
        cursor=conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=%s",[username])
        userid=cursor.fetchone()
        if not userid:
            return redirect(url_for('signup'),302)
        else:
            return redirect(url_for('display',userid=userid),302)
    elif request.method=='GET':
        return render_template("index.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=='POST':
        name=request.form.get('Name')
        db.commit_db("INSERT INTO users (username) VALUES(%s)",[name])
        return redirect(url_for('index'))
    elif request.method=='GET':
        return render_template("sign_up.html")

@app.route("/<userid>/display")
def display(userid):
    info={}
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute("SELECT time,date,event FROM eventlist WHERE user_id=%s",userid)
    for time,date,event in cursor.fetchall():
        counter=1
        info[counter]=[time,date,event]
        counter+=1
    return render_template("display.html",info=info,userid=userid)
    
@app.route("/<userid>/add",methods=["GET","POST"])
def add(userid):
    if request.method=="POST":
        event=request.form.get('Event')
        date=request.form.get('Date')
        time=request.form.get('Time')
        db.commit_db("INSERT INTO eventlist (user_id,time,date,event) VALUES(%s,%s,%s,%s)",[userid,time,date,event])
        return redirect(url_for('display',userid=userid),302)
    elif request.method=="GET":
        return render_template("add.html",userid=userid)

