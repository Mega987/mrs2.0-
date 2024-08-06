import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=bc4eb15169a481ca444b8342939febee&language=en-US')
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/original" + poster_path
        else:
            st.error("Poster path not found.")
            # return None
    except requests.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        # return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
   
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies_posters.append(poster_url)
        else:
            # Fallback to a default image if poster is not available
            recommended_movies_posters.append("https://via.placeholder.com/500x750?text=No+Poster+Available")
    
    return recommended_movies, recommended_movies_posters

# Load movie data
movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)  # Assuming movies_dict is a dictionary with a 'title' key

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Choose your movie', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    for idx, (name, poster) in enumerate(zip(names, posters)):
        if idx == 0:
            with col1:
                st.text(name)
                st.image(poster)
        elif idx == 1:
            with col2:
                st.text(name)
                st.image(poster)
        elif idx == 2:
            with col3:
                st.text(name)
                st.image(poster)
        elif idx == 3:
            with col4:
                st.text(name)
                st.image(poster)
        elif idx == 4:
            with col5:
                st.text(name)
                st.image(poster)
