import streamlit as st
import requests
from imdb import IMDb

# OMDb API URL and API Key (You'll need to get an API key from https://www.omdbapi.com/)
OMDB_API_KEY = 'a7defab1'
OMDB_BASE_URL = "http://www.omdbapi.com/"

# Function to fetch movie data from OMDb API
def get_movie_data(movie_name):
    url = f"{OMDB_BASE_URL}?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to fetch IMDb rating
def get_imdb_rating(movie_id):
    ia = IMDb()
    movie = ia.get_movie(movie_id)
    return movie.get('rating', 'N/A')

# Streamlit app UI setup
st.title("Netflix Styled Streamlit App")

# Sidebar for movie selection
movie_name = st.sidebar.text_input("Enter Movie Name", "Inception")
if movie_name:
    data = get_movie_data(movie_name)

    if data.get("Response") == "True":
        # Display movie poster and details
        st.image(data['Poster'], use_column_width=True)
        st.header(f"{data['Title']} ({data['Year']})")
        st.write(f"**Genre**: {data['Genre']}")
        st.write(f"**Director**: {data['Director']}")
        st.write(f"**Plot**: {data['Plot']}")

        # IMDb rating (using IMDbPY)
        ia = IMDb()
        movie_id = ia.search_movie(data['Title'])[0].movieID
        imdb_rating = get_imdb_rating(movie_id)
        st.write(f"**IMDb Rating**: {imdb_rating}/10")
    else:
        st.error("Movie not found, try a different title.")
st.markdown("""
    <style>
        .movie-container {
            transition: all 0.5s ease;
        }
        .movie-container:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)
