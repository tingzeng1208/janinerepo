import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import random

import movie_recommendation
import app

df1=pd.read_csv("resources/tmdb_5000_credits.csv")
df2=pd.read_csv("resources/tmdb_5000_movies.csv")

df1.columns = ['id','tittle','cast','crew']
df2= df2.merge(df1,on='id')


##creating song recommendations
client_id = '8cd0b7c42d3d49b88fcaf0bcfeb560e2' #Annie's unique Spotify API id
client_secret = 'ccbb044a4f10451aaee7189cb3d197bf'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

def get_keywords_movie(movie_title):
  movie_data = df2[df2['title'] == movie_title]
  if not movie_data.empty:
    keywords = movie_data.iloc[0]['keywords']
    return keywords[:2]
  return []


def get_genres_movie(movie_title):
  movie_data = df2[df2['title'] == movie_title]
  if not movie_data.empty:
    genres = movie_data.iloc[0]['genres']
    return genres[:2]
  return []


#returns a spotify link to a playlist correlated with the keyword
def search_playlists(keyword, limit=1):
    keyword = keyword.lower()
    access_token = get_access_token()
    search_url = f"https://api.spotify.com/v1/search?q=genre%3A{keyword}&type=playlist"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(search_url, headers=headers)
    data = response.json()
    playList = data["playlists"]
    items = playList["items"]
    itemList = [x for x in items if x is not None]
    if len(itemList) == 0:
      return ""
    itemList = itemList[0]
    externalLink = itemList["external_urls"]["spotify"]
    return externalLink

def findTracks(playlistID, num=1):
    access_token = get_access_token()
    search_url = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(search_url, headers=headers)
    data = response.json()
    items = data["items"]

    random_tracks = random.sample(items, min(num, len(items)))

    names = []
    for item in random_tracks:
      track = item["track"]
      name = track["name"]
      singer = ', '.join([artist["name"] for artist in track["artists"]])
      names.append(f"{name} by {singer}")
    return names

def get_playlist_id(url):
    return url.split("playlist/")[-1].split("?")[0]

def reformat(songName):
    newNames = []
    for arr in songName:
      for name in arr:
        newNames.append(name)
    return newNames

#after user inputs their title
def get_recommendation(title):
    songNames = []
    #title = title
    genres = get_genres_movie(title)
    keywords = get_keywords_movie(title)

    for i in range(3):
        if search_playlists(title) == "":
            continue
        songNames.append(findTracks(get_playlist_id(search_playlists(title))))

    for genre in genres:
        if search_playlists(genre) == "":
            continue
        songNames.append(findTracks(get_playlist_id(search_playlists(genre))))

    for keyword in keywords:
        if search_playlists(keyword) == "":
            continue
        songNames.append(findTracks(get_playlist_id(search_playlists(keyword))))

    while len(songNames) < 5:
        if search_playlists(title) == "":
            break
        songNames.append(findTracks(get_playlist_id(search_playlists(title))))

    songNames = reformat(songNames)
    songNames.sort()
    songNames = songNames[:5]
    if len(songNames) == 0:
        #print("no motion detected")
        return []
    else:
        #print(songNames)
        return songNames

#print(get_recommendation("Frozen"))