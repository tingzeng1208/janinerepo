from flask import Flask, redirect, url_for, request, render_template, flash
import pandas as pd
import numpy as np

df1=pd.read_csv("resources/tmdb_5000_credits.csv")
df2=pd.read_csv("resources/tmdb_5000_movies.csv")


# Flask constructor
app = Flask(__name__)   


@app.route("/")
def home():
    return "test"

@app.route("/login", methods = ["POST", "GET"])
def login():
    if(request.method == "POST"):
        #can check if request.form["nm"] not blank, do more stuff with it
        user = request.form["nm"]
        return redirect(url_for("user", usr = user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    
    return f"<h1>{usr}</h1>"

if __name__=='__main__':
    app.run(debug = True)