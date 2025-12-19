import mysql.connector
from flask import Flask, render_template, request
import webbrowser

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="Form") 


mycur=mydb.cursor()

def display(id_exist):
    qdisplay='select * from emp where emp_ID = %s'
    id=(id_exist,)
    mycur.execute(qdisplay,id)
    res=mycur.fetchone()
    return res

def add(detail_list):
    qadd='insert into emp value(%s,%s,%s)'
    val=detail_list
    mycur.execute(qadd,detail_list)
    mydb.commit()
#    print('Row added')

def emp_exists(emp_id): 
    query = "SELECT emp_ID FROM emp WHERE emp_ID = %s"
    mycur.execute(query, (emp_id,))
    return mycur.fetchone() is not None


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/add')
def form():
    return render_template("form.html")

@app.route('/submit', methods=['POST'])
def submit():
    emp_id = request.form['empid']
    emp_name = request.form['empname']
    emp_role = request.form['emprole']
    if emp_exists(emp_id):
        return render_template("error.html", emp_id=emp_id)
    
    else:
        add((emp_id, emp_name, emp_role))
        return render_template("success.html")

@app.route('/view')
def view_page():
    return render_template("view.html")

@app.route('/view_result', methods=['POST'])
def view_result():
    emp_id = request.form['empid']
    data = display(emp_id)

    if data is None:
        return render_template("view.html",error="Employee ID not found")
    
    else:
        return render_template("view.html",emp=data)


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True,use_reloader=False)
