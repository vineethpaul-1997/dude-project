from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="mysql-service",
    user="root",
    password="root123",
    database="userdb"
)

cursor = db.cursor()

@app.route("/")
def home():
    return jsonify({
        "status":"Backend Running"
    })

@app.route("/register", methods=["POST"])
def register():

    data=request.get_json()

    username=data["username"]
    email=data["email"]
    password=data["password"]

    sql="""
    INSERT INTO users
    (username,email,password)
    VALUES(%s,%s,%s)
    """

    values=(username,email,password)

    cursor.execute(sql,values)

    db.commit()

    return jsonify({
        "message":"Registration Successful"
    })

@app.route("/login", methods=["POST"])
def login():

    data=request.get_json()

    username=data["username"]
    password=data["password"]

    sql="""
    SELECT *
    FROM users
    WHERE username=%s
    AND password=%s
    """

    values=(username,password)

    cursor.execute(sql,values)

    user=cursor.fetchone()

    if user:

        return jsonify({
            "message":"Login Successful"
        })

    return jsonify({
        "message":"Invalid Credentials"
    }),401

if __name__=="__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
