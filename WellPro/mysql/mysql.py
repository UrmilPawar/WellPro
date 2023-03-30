from flask import Flask, render_template, request,jsonify
import pymysql
from flask_cors import CORS

mysql = Flask(__name__)
CORS(mysql)

# Connecting to MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='feedback'
)

# Defining a function to insert data into the database
def insert_data(name, phone_number, email, message):
    with conn.cursor() as cursor:
        # Inserting data into the database
        sql = "INSERT INTO contacts (name, phone_number, email, message) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, phone_number, email, message))
    conn.commit()

# Routing for the contact form
@mysql.route('/contacts', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.json['name']
        phone_number = request.json['phone_number']
        email = request.json['email']
        message = request.json['message']

        # Inserting data into the database
        insert_data(name, phone_number, email, message)

        # Showing success message
        response = {'message': 'Form data received and stored successfully!'}
        return jsonify(response)

if __name__ == '__main__':
    mysql.run(port=5004)