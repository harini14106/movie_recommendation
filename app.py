import streamlit as st
import pandas as pd
import requests
from imdb import IMDb

# OMDb API Key (Get your API key from https://www.omdbapi.com/)
OMDB_API_KEY = 'a7defab1'
OMDB_BASE_URL = "http://www.omdbapi.com/"

# Function to fetch IMDb rating
def get_imdb_rating(movie_name):
    ia = IMDb()
    movies = ia.search_movie(movie_name)
    if movies:
        movie_id = movies[0].movieID
        movie = ia.get_movie(movie_id)
        return movie.get('rating', 'N/A')
    return 'N/A'

# Fetch related movies using OMDb API
def get_related_movies(movie_name):
    url = f"{OMDB_BASE_URL}?s={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get('Search', []) if data.get('Response') == 'True' else []

# Read movie data from CSV
@st.cache
def load_movie_data():
    return pd.read_csv("movies.csv")

# Streamlit app UI setup
st.title("Netflix Styled Streamlit App with Movie Recommendations")

# Load movie data
movie_data = load_movie_data()

# Sidebar for movie selection (by title)
movie_name = st.sidebar.selectbox("Select a Movie", movie_data['Title'])

# Display selected movie details
selected_movie = movie_data[movie_data['Title'] == movie_name].iloc[0]

# Display movie poster and details
st.image(selected_movie['Poster'], use_column_width=True)
st.header(f"{selected_movie['Title']} ({selected_movie['Year']})")
st.write(f"**Genre**: {selected_movie['Genre']}")
st.write(f"**Director**: {selected_movie['Director']}")
st.write(f"**Plot**: {selected_movie['Plot']}")

# IMDb rating (using IMDbPY)
imdb_rating = get_imdb_rating(selected_movie['Title'])
st.write(f"**IMDb Rating**: {imdb_rating}/10")

# Movie Recommendation based on Genre from CSV
genre = selected_movie['Genre']
st.subheader(f"Movies similar to {selected_movie['Title']} in the '{genre}' genre:")

# Filter movies by the selected genre
recommended_movies = movie_data[movie_data['Genre'] == genre]

# Show top 3 recommended movies from CSV
for index, movie in recommended_movies.head(3).iterrows():
    st.image(movie['Poster'], width=120)
    st.write(f"**{movie['Title']}** ({movie['Year']})")
    st.write(f"Genre: {movie['Genre']}")
    st.write(f"IMDb Rating: {get_imdb_rating(movie['Title'])}/10")
    st.markdown("---")

# Fetch related movies from OMDb API based on the selected movie
st.subheader(f"Other movies you might like based on {selected_movie['Title']}:")

related_movies = get_related_movies(selected_movie['Title'])

# Show related movies from OMDb API
for movie in related_movies[:5]:  # Limit to top 5 results
    st.image(movie['Poster'], width=120)
    st.write(f"**{movie['Title']}** ({movie.get('Year', 'N/A')})")
    st.write(f"Genre: {movie.get('Type', 'N/A')}")
    st.write(f"IMDb Rating: {get_imdb_rating(movie['Title'])}/10")
    st.markdown("---")

# Add CSS transition effects for hover
st.markdown("""
    <style>
        .stImage {
            transition: transform 0.3s ease-in-out;
        }
        .stImage:hover {
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)
