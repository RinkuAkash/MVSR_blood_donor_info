from flask import Flask, session, render_template, redirect, request, url_for,flash
import models as dbHandler

app = Flask(__name__)

app.secret_key='secret key'

@app.route("/")
def home():
	if session('logged_In') == False:
		return render_template("index.html")
	else:
		return render_template("index1.html")


@app.route("/logout")
def logout():
	session.pop('username', None)
	session['logged_In']=False
	return render_template('login.html')

@app.route("/home")
def home1():
   
 return redirect(url_for("home"))

@app.route("/vision")
def vision():
	return render_template("vision.html")
@app.route("/facts")
def facts():
	return render_template("facts.html")

@app.route("/adminl")
def adminl():
	return render_template("adminl.html")

@app.route("/admin", methods=['POST'])
def admin():
	if request.method == 'POST':
		username =request.form['username']
		password =request.form['password']
		users = dbHandler.retrieveAdmin()
		session['username']= request.form['username']
		session['logged_In']=True
		flash("Welcome ADMIN"+users)
		return render_template("admin.html")
	else:
				flash("It seems entered username or password wrong")
				return redirect(url_for('adminl'))

@app.route("/view")
def view():
	return render_template("view.html",users=session['username'])
if __name__=="__main__":
   app.run(debug=True)
