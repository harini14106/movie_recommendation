import streamlit as st
import pandas as pd
import requests
import random

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("movies.csv")
    df = df.dropna(subset=['genres', 'title', 'vote_average', 'overview'])
    return df

df = load_data()

# TMDb API Setup
API_KEY = "YOUR_TMDB_API_KEY"  # Replace with your API key
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_MOVIE_URL = "https://api.themoviedb.org/3/movie"

def get_movie_data(title):
    """Fetch poster and trailer URL from TMDb"""
    params = {"api_key": API_KEY, "query": title}
    response = requests.get(TMDB_SEARCH_URL, params=params)
    results = response.json().get("results", [])
    if results:
        movie_id = results[0]["id"]
        poster_path = results[0].get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        trailer_response = requests.get(f"{TMDB_MOVIE_URL}/{movie_id}/videos", params={"api_key": API_KEY})
        videos = trailer_response.json().get("results", [])
        trailer_url = None
        for video in videos:
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
                break

        return poster_url, trailer_url
    return None, None

# UI Setup
st.set_page_config(layout="wide")
st.title("🎬 MovieFlix - Genre-Based Recommendations with Posters & Trailers")

# Genre Filter
all_genres = sorted(set(g.strip() for sublist in df['genres'].dropna().str.split() for g in sublist))
selected_genre = st.selectbox("Choose a Genre", all_genres)

# Filter Movies
filtered_df = df[df['genres'].str.contains(selected_genre, case=False, na=False)].reset_index(drop=True)
filtered_df = filtered_df.sample(frac=1).head(10)

st.markdown(f"### Movies in **{selected_genre}** Genre")

cols = st.columns(5)
for i, movie in filtered_df.iterrows():
    poster_url, trailer_url = get_movie_data(movie["title"])
    with cols[i % 5]:
        st.image(poster_url or f"https://via.placeholder.com/300x450?text={movie['title']}", use_column_width=True)
        st.markdown(f"**{movie['title']}**")
        st.caption(f"⭐ {movie['vote_average']}")
        st.caption(movie['overview'][:100] + "...")
        if trailer_url:
            st.markdown(f"[🎬 Watch Trailer]({trailer_url})", unsafe_allow_html=True)

# Recommendations
st.markdown("---")
st.markdown(f"### 🔥 Top Recommended {selected_genre} Movies")

top_recommendations = (
    df[df['genres'].str.contains(selected_genre, case=False, na=False)]
    .sort_values(by="vote_average", ascending=False)
    .drop_duplicates(subset='title')
    .head(10)
)

rec_cols = st.columns(5)
for i, movie in top_recommendations.iterrows():
    poster_url, trailer_url = get_movie_data(movie["title"])
    with rec_cols[i % 5]:
        st.image(poster_url or f"https://via.placeholder.com/300x450?text={movie['title']}", use_column_width=True)
        st.markdown(f"**{movie['title']}**")
        st.caption(f"⭐ {movie['vote_average']}")
        st.caption(movie['overview'][:100] + "...")
        if trailer_url:
            st.markdown(f"[🎬 Watch Trailer]({trailer_url})", unsafe_allow_html=True)

