#!flask/bin/python3
import json
import sqlite3
from flask import Flask, jsonify, render_template, request

# подключение к бд

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

# Создание таблицы members
cursor.execute("""CREATE TABLE IF NOT EXISTS members
                  (id,  name, surname, contact, experience, description)
               """)
conn.commit()
cursor.close()
conn.close()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello'


@app.route('/members')
def get_members():
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor = conn.execute("SELECT * FROM members")
    data = [
        dict(id=row[0], name=row[1], surname=row[2], contact=row[3], experience=row[4], description=row[5]) for row
        in
        cursor.fetchall()
    ]
    return jsonify(data)


# add a new member


@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        x = request.get_json(force=True)

        sql = """INSERT INTO members (id, name, surname, contact, experience, description) VALUES(?,?,?,?,?,?)"""
        cursor = conn.execute(sql, (x["id"], x['name'], x["surname"], x["contact"], x["experience"], x["description"]))
        conn.commit()
    return 'welcome to club dude'


# delete member by id

@app.route('/members/delete/<int:id>', methods=['GET', 'DELETE'])
def delete_member(id):
    if request.method == 'DELETE':
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        sql = """ DELETE FROM members WHERE id=?"""
        conn.execute(sql, (id,))
        conn.commit()
        cursor = conn.execute("SELECT * FROM members")
    return 'bye dude'


# get member by id

@app.route('/members/get/<int:id>', methods=['GET'])
def get_member(id):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM members WHERE id=?", (id,))
    conn.commit()
    row = cursor.fetchone()
    data = {
        "id": row[0],
        "name": row[1],
        "surname": row[2],
        "contact": row[3],
        "experience": row[4],
        "description": row[5]

    }
    return jsonify(data)


# update member by id
#
@app.route('/members/update/<int:id>', methods=['PUT', 'GET'])
def update_member(id):
    if request.method == 'PUT':
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        x = request.get_json(force=True)
        cursor.execute(""" UPDATE members
        SET name=?, surname=?, contact=?, experience=?, description=?
        WHERE id=?""", (x['name'], x['surname'], x['contact'], x['experience'], x['description'], id))

        conn.commit()

        # return new one
        cursor.execute("SELECT * FROM members WHERE id=?", (id,))
        conn.commit()
        row = cursor.fetchone()
        data = {
            "id": row[0],
            "name": row[1],
            "surname": row[2],
            "contact": row[3],
            "experience": row[4],
            "description": row[5]

        }
        return jsonify(data)


# count of members
@app.route('/members/count')
def count():
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    #cursor = conn.execute('SELECT COUNT(*) FROM members')
    rows =cursor.fetchall()
    count =0
    for i in rows:
        count+=1

    count_members={
        "count": count
    }
    return jsonify(count_members)
if __name__ == "__main__":
    app.run()

# done:
# members: add delete get update count
