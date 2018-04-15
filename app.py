from flask import Flask, session, render_template, redirect, request, url_for,flash,g
import sqlite3

app = Flask(__name__)


def get_db():
	db = getattr(g,'_database',None)
	if db is None:
		db = g._database = sqlite3.connect("database.db")
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g,'_database', None)
	if db is not None:
		db.close()

def query_db(query, args=(), one= False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

@app.route("/")
def home():
	if session['logged_In'] is True:
		return render_template("index1.html")
	else:
		return render_template("index.html")
	return render_template("index.html")

@app.route("/index",methods=['POST','GET'])
def index():
	if request.method == 'POST':
		roll = request.form['rollno']
		password = request.form['password']
		cur = get_db().cursor()
		donor= query_db('SELECT rollno FROM donor WHERE rollno=? AND password=?',[roll,password],one = True)
		if donor is None:
			flash("login failed")
			return redirect(url_for("login"))
		else:
			session['username']=donor
			session['logged_In']=True
			return render_template("index1.html")
	return redirect(url_for("home"))

@app.route("/Dlist")
def dlist():
	with sqlite3.connect("database.db") as con:
		con.row_factory=sqlite3.Row
		cur=con.cursor()
		cur.execute("SELECT * FROM donor")
		rows=cur.fetchall()
		return render_template("dlist.html",rows=rows)

@app.route("/dlist")
def dlist1():
	with sqlite3.connect("database.db") as con:
		con.row_factory=sqlite3.Row
		cur=con.cursor()
		cur.execute("SELECT * FROM donor")
		rows=cur.fetchall()
		return render_template("dlist1.html",rows=rows)

@app.route("/rlist")
def rlist1():
	with sqlite3.connect("database.db") as con:
		con.row_factory=sqlite3.Row
		cur=con.cursor()
		cur.execute("SELECT * FROM user")
		rows=cur.fetchall()
		return render_template("rlist1.html",rows=rows)

@app.route("/Rlist")
def rlist():
	with sqlite3.connect("database.db") as con:
		con.row_factory=sqlite3.Row
		cur=con.cursor()
		cur.execute("SELECT * FROM user")
		rows=cur.fetchall()
		return render_template("rlist.html",rows=rows)

@app.route("/request")
def req():
	return render_template("request.html")

@app.route("/confirm", methods=['POST','GET'])
def confirm():
	if request.method =='POST':

		try:
			username=request.form['u']
			bloodgroup=request.form['b']
			area=request.form['a']
			ldate=request.form['d']
			phno=request.form['ph']
			with sqlite3.connect("database.db") as con:
				cur=con.cursor()
				cur.execute("INSERT INTO user (username,bloodgroup,area,ldate,phno) VALUES (?,?,?,?,?)",(username,bloodgroup,area,ldate,phno))
				con.commit()
				flash("your request has been received")
				return redirect(url_for("rlist"))
		except:
			flash("technical issue try again")
			return render_template("request.html")

@app.route("/registration")
def signup():
	return render_template("registration.html")

@app.route("/account")
def account():
	rollno = session['username']
	with sqlite3.connect("database.db") as con:
		con.row_factory=sqlite3.Row
		cur = con.cursor()
		cur.execute("SELECT * FROM donor WHERE rollno=?",(rollno))
		rv=cur.fetchall()
		return render_template("account.html",users=rv)


@app.route("/signin",methods=['POST','GET'])
def signin():
	if request.method =='POST':
		try:
			r = request.form['r']
			p=request.form['p']
			u=request.form['u']
			b=request.form['b']
			a=request.form['a']
			ph=request.form['ph']
			e=request.form['e']
			av=request.form['av']
			with sqlite3.connect("database.db") as con:
				cur= con.cursor()
				cur.execute("INSERT INTO donor (rollno,password,username,bloodgroup,area,phno,email,availability) VALUES (?,?,?,?,?,?,?,?)",(r,p,u,b,a,ph,e,av))
				con.commit()
				session['username']=r
				session['logged_In']=True
				user2=session['username']
				return redirect(url_for("account",users=user2))
		except:
			flash("technical issue")
			return redirect(url_for("signup"))

@app.route("/login")
def login():
	return render_template("login.html")

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
	if session['logged_In'] is True:
		return render_template("vision1.html")
	else:
		return render_template("vision.html")

@app.route("/facts")
def facts():
	if session['logged_In'] is True:
		return render_template("facts1.html")
	else:
		return render_template("facts.html")

@app.route("/about")
def about():
	if session['logged_In'] is True:
		return render_template("about1.html")
	else:
		return render_template("about.html")

@app.route("/contact")
def contact():
	if session['logged_In'] is True:
		return render_template("contact1.html")
	else:
		return render_template("contact.html")

@app.route("/who")
def who():
	if session['logged_In'] is True:
		return render_template("whocan1.html")
	else:
		return render_template("whocan.html")

@app.route("/gallery")
def gallery():
	if session['logged_In'] is True:
		return render_template("gallery1.html")
	else:
		return render_template("gallery.html")

@app.route("/details")
def details():
	if session['logged_In'] is True:
		return render_template("details1.html")
	else:
		return render_template("details.html")

@app.route("/adminl")
def adminl():
	return render_template("adminl.html")

@app.route("/admin", methods=['POST','GET'])
def admin():
	if request.method == 'POST':
		user3 =request.form['username']
		passw =request.form['password']
		cur = get_db().cursor()
		admin= query_db('SELECT username FROM admin WHERE username=?  AND password=?',[user3,passw],one = True)
		if admin is None:
			flash("login failed")
			return render_template("adminl.html")
		else:
			flash("login success")
			session['username']=admin[0]
			session['logged_In']=True
			return render_template("admin.html")
		cur.close()

@app.route("/view")
def view():
	users=session['username']
	return render_template("view.html",users=users)
