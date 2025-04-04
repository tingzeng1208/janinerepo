from flask import Flask, redirect, url_for, request, render_template, flash, request, jsonify
import pandas as pd
import numpy as np
import json

#import python file
import movie_recommendation
import spotify_recommendation
from flask_cors import CORS



#movie_recommendation.get_recommendations('Interstellar', movie_recommendation.cosine_sim2)


# Flask constructor
app = Flask(__name__)   

# must allow CORS for the app to work with front end
CORS(app)

# new routes to return jason data

@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    title = data.get("title", "")
    
    if not title:
        return jsonify({"error": "No title provided"}), 400

    # Get movie recommendations as dict
    movie_result = movie_recommendation.get_recommendations_json(title)
    if isinstance(movie_result, str):  # convert back from json string
        movie_result = json.loads(movie_result)

    # Get song recommendations
    songs_result = spotify_recommendation.get_recommendation_json(title)
    if isinstance(songs_result, str):  # convert back from json string
        songs_result = json.loads(songs_result)

    # Combine both into one response
    full_result = {
        "input": title,
        "recommendations": movie_result.get("recommendations", []),
        "songs": songs_result.get("songs", []),
        "message": "SUCCESS"
    }

    return jsonify(full_result)

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "API is running"})

# end of new routes

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