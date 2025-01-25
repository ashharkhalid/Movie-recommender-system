import streamlit as st
import pickle
import pandas as pd
import requests
import gdown

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=218c2646de95861531bf5136594c97b0&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        # Fetch poster and movie title
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Function to download files from Google Drive
@st.cache_resource
def download_file_from_gdrive(file_url, output_path):
    gdown.download(file_url, output_path, quiet=False)

# Download similarity.pkl from Google Drive
similarity_file_url = "https://drive.google.com/uc?id=1M47Qm8ttRTCGWH7PFCvGEc2R4Cu8MJWM"  # Update with file ID
similarity_file_path = "similarity.pkl"
download_file_from_gdrive(similarity_file_url, similarity_file_path)

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

# Movie selection dropdown
selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
