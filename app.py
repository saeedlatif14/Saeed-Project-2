#updated saeed
from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse
import logging
import subprocess

app = Flask(__name__)

# Environment Variables
DBHOST = os.environ.get("DB_HOST", "localhost")
DBUSER = os.environ.get("DB_USER", "root")
DBPWD = os.environ.get("DB_PASSWORD", "root")
DBPORT = int(os.environ.get("DBPORT", 3306))
DATABASE = os.environ.get("DATABASE", "employees")
COLOR_FROM_ENV = os.environ.get("APP_COLOR", "lime")
APP_NAME = os.environ.get("APP_NAME", "Slatif")

# Background image from S3
S3_IMAGE_URL = os.environ.get("S3_IMAGE_URL")
LOCAL_IMAGE_PATH = "static/background.jpg"

if S3_IMAGE_URL:
    print(f"🖼️ Downloading background image from: {S3_IMAGE_URL}")
    try:
        os.makedirs("static", exist_ok=True)
        subprocess.run(["curl", "-L", "-o", LOCAL_IMAGE_PATH, S3_IMAGE_URL], check=True)
        print("✅ Image downloaded to", LOCAL_IMAGE_PATH)
    except Exception as e:
        logging.error(f"❌ Failed to download image with curl: {e}")

# MySQL connection
db_conn = connections.Connection(
    host=DBHOST,
    port=DBPORT,
    user=DBUSER,
    password=DBPWD,
    db=DATABASE
)

output = {}
table = 'employee'

# Color styles
color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#89CFF0",
    "blue2": "#30336b",
    "pink": "#f4c2c2",
    "darkblue": "#130f40",
    "lime": "#C1FF9C",
}
SUPPORTED_COLORS = ",".join(color_codes.keys())
COLOR = random.choice(list(color_codes.keys()))

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', color=color_codes[COLOR], app_name=APP_NAME)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', color=color_codes[COLOR], app_name=APP_NAME)

@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"
    finally:
        cursor.close()

    return render_template('addempoutput.html', name=emp_name, color=color_codes[COLOR], app_name=APP_NAME)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", color=color_codes[COLOR], app_name=APP_NAME)

@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']
    

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()
        if result:
            output["emp_id"] = result[0]
            output["first_name"] = result[1]
            output["last_name"] = result[2]
            output["primary_skills"] = result[3]
            output["location"] = result[4]
    except Exception as e:
        print(e)
    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"],
                           location=output["location"], color=color_codes[COLOR], app_name=APP_NAME)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()

    if args.color:
        COLOR = args.color
        print("Color from command line:", COLOR)
    elif COLOR_FROM_ENV:
        COLOR = COLOR_FROM_ENV
        print("Color from environment:", COLOR)
    else:
        print("Random color selected:", COLOR)

    if COLOR not in color_codes:
        print(f"Color not supported: {COLOR}. Expected one of: {SUPPORTED_COLORS}")
        exit(1)

    app.run(host='0.0.0.0', port=8080, debug=True)
