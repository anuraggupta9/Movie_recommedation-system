import streamlit as st
import pickle
import pandas as pd
import requests

# 🔹 Fetch poster using TMDB movie ID
def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=aa1a07fe07105050ecbe47349703953a"
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_df.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# 🔹 Load files
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_df = pickle.load(open('movies.pkl', 'rb'))

# 🔹 UI
st.title('🎬 Movie Recommender System')

movies_titles = movies_df['title'].values
selected_movie_name = st.selectbox("Select a movie", movies_titles)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    st.subheader("Recommended Movies")
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
