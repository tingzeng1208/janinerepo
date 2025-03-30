import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

df1=pd.read_csv("resources/tmdb_5000_credits.csv")
df2=pd.read_csv("resources/tmdb_5000_movies.csv")

df1.columns = ['id','tittle','cast','crew']
df2= df2.merge(df1,on='id')

#clean
tfidf = TfidfVectorizer(stop_words='english')
df2['overview'] = df2['overview'].fillna('')

#construct the  TF-IDF matrix
tfidf_matrix = tfidf.fit_transform(df2['overview'])
tfidf_matrix.shape

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()

#  return the recommendations in json formats
def get_recommendations_json(title, cosine_sim=cosine_sim, top_n=5):
    title = title.title()
    if title not in indices:
        return json.dumps({"error": "Movie title not found"})

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
    movie_indices = [i[0] for i in sim_scores]
    recommended_titles = df2['title'].iloc[movie_indices].tolist()

    # Build a JSON-friendly dict
    result = {
        "input": title,
        "recommendations": recommended_titles
    }
    return json.dumps(result, indent=2)

def get_recommendations(title, cosine_sim=cosine_sim):
    if title.title() not in indices:
        return []
    
    idx = indices[title.title()]
    sim_scores = list(enumerate(cosine_sim[idx])) #pairwise similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) #sort movies based on score
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    return df2['title'].iloc[movie_indices].tolist()


# Parse the stringified features into their corresponding python objects
from ast import literal_eval

features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(literal_eval)

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names

    return []

df2['director'] = df2['crew'].apply(get_director)

features = ['cast', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(get_list)

df2[['title', 'cast', 'director', 'keywords', 'genres']].head(3)

#convert all strings to lower case and get rid of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

#apply clean data
features = ['cast', 'keywords', 'director', 'genres']

for feature in features:
    df2[feature] = df2[feature].apply(clean_data)

def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
df2['soup'] = df2.apply(create_soup, axis=1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])

#gets the cosine similarity matrix based on the count_matrix
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

#reset index of our main dataframe and construct reverse mapping as before
df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])