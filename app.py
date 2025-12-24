import os
import requests
from flask import Flask, render_template, request
import json

app = Flask(__name__)

DATABASE_URL = "https://project-d670c-default-rtdb.firebaseio.com"


def display(emp_id):
    try:
        response = requests.get(f"{DATABASE_URL}/emp/{emp_id}.json")
        data = response.json()
        if data:
            return (emp_id, data.get("emp_name"), data.get("emp_role"))
        return None
    except Exception as e:
        print(f"Error reading data: {e}")
        return None


def add(detail_list):
    try:
        emp_id, emp_name, emp_role = detail_list
        data = {
            "emp_name": emp_name,
            "emp_role": emp_role
        }
        response = requests.put(f"{DATABASE_URL}/emp/{emp_id}.json", json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error adding data: {e}")
        return False


def emp_exists(emp_id):
    try:
        response = requests.get(f"{DATABASE_URL}/emp/{emp_id}.json")
        data = response.json()
        return data is not None
    except Exception as e:
        print(f"Error checking employee: {e}")
        return False


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/add')
def form():
    return render_template("form.html")


@app.route('/submit', methods=['POST'])
def submit():
    emp_id = request.form.get('empid', '').strip()
    emp_name = request.form.get('empname', '').strip()
    emp_role = request.form.get('emprole', '').strip()
    
    if not emp_id or not emp_name or not emp_role:
        return render_template("error.html", error="All fields are required")
    
    if emp_exists(emp_id):
        return render_template("error.html", emp_id=emp_id)
    
    if add((emp_id, emp_name, emp_role)):
        return render_template("success.html")
    else:
        return render_template("error.html", error="Failed to add employee")


@app.route('/view')
def view_page():
    return render_template("view.html")


@app.route('/view_result', methods=['POST'])
def view_result():
    emp_id = request.form.get('empid', '').strip()
    
    if not emp_id:
        return render_template("view.html", error="Employee ID is required")
    
    data = display(emp_id)

    if data is None:
        return render_template("view.html", error="Employee ID not found")
    else:
        return render_template("view.html", emp=data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    if os.environ.get("RENDER") is None:
        import webbrowser
        webbrowser.open(f"http://127.0.0.1:{port}")
    
    app.run(host="0.0.0.0", port=port, debug=False)