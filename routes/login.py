from flask import Flask, render_template, request, redirect, url_for,jsonify, session
from flask import Blueprint
import pymysql

bp = Blueprint('login', __name__, url_prefix='/')



# @bp.route('login', methods = ['GET','POST'])
# def login():

#     id = request.form['id']
#     pw = request.form['pw']

#     if (id == "admin") & (pw == "admin"):
#         return render_template('home_login.html', id=id)
#     else:
#         return render_template('home.html')

# @bp.route('login', methods=["GET","POST"])
# def login():
#     global ID, PW
#     loginId = request.args.get['loginId']
#     loginPw = request.args.get['loginPw']

#     if ID == loginId and PW == loginPw:
#         session["userID"] = loginId
#         return redirect(url_for("index"))
#     else:
#         return redirect(url_for("index"))
