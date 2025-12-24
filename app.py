import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, render_template, request
import webbrowser

app = Flask(__name__)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://project-d670c-default-rtdb.firebaseio.com"
})

ref = db.reference("emp")


def display(emp_id):
    data = ref.child(emp_id).get()
    if data:
        return (emp_id, data["emp_name"], data["emp_role"])
    return None

def add(detail_list):
    emp_id, emp_name, emp_role = detail_list
    ref.child(emp_id).set({
        "emp_name": emp_name,
        "emp_role": emp_role
    })

def emp_exists(emp_id): 
    return ref.child(emp_id).get() is not None


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
