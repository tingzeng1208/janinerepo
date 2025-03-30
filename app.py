from flask import Flask, redirect, url_for, request, render_template, flash
import pandas as pd
import numpy as np

#import python file
import movie_recommendation
import spotify_recommendation

#movie_recommendation.get_recommendations('Interstellar', movie_recommendation.cosine_sim2)


# Flask constructor
app = Flask(__name__)   


@app.route("/", methods = ["POST", "GET"])
def home():
    if(request.method == "POST"):
        #can check if request.form["nm"] not blank, do more stuff with it
        user = request.form["nm"]
        return redirect(url_for("user", usr = user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    MovieRecommendations = movie_recommendation.get_recommendations(usr, movie_recommendation.cosine_sim2)
    if MovieRecommendations:
        return render_template('recommendation.html', movies=MovieRecommendations, songs=spotify_recommendation.get_recommendation(usr))
    else:
        return render_template('recommendation.html', movies=[], message="NO MOTION DETECTED")

#@app.route("/<usr>/spot")
#def user(usr):
    

if __name__=='__main__':
    app.run(debug = True)