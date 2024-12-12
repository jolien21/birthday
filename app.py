import os
import sqlite3
#from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
#db = SQL("sqlite:///birthdays.db")
def get_db_connection():
    conn = sqlite3.connect('birthdays.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_table_data(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM birthdays")
    data = cursor.fetchall()
    conn.close()
    return data

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():

    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        #validate submission
        name = request.form.get("name")
        if not name:
            return redirect("/")
        
        month = request.form.get("month")
        if not month:
            return redirect("/")
        try:
            month = int(month)
        except ValueError:
            return redirect("/")
        if month < 1 or month > 12:
            return redirect("/")

        day = request.form.get("day")
        if not day:
            return redirect("/")
        try:
            day = int(day)
        except ValueError:
            return redirect("/")
        if day < 1 or day > 31:
            return redirect("/")

        conn.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", (name, month, day))
        conn.commit()
        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        #birthdays = cursor.execute("SELECT * FROM birthdays")
        #posts = cursor.fetchall()
        table_data = get_table_data('birthdays')
        return render_template("index.html", data=table_data)

@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")
    conn = get_db_connection()
    cursor = conn.cursor()

    if id:
      cursor.execute("DELETE FROM birthdays WHERE id = ?", (id))
      conn.commit()
      conn.close()
    return redirect("/")
