import streamlit as st
import pandas as pd
import requests

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("movies.csv")
    df = df.dropna(subset=['genres', 'title', 'vote_average', 'overview'])
    return df

df = load_data()

# --- TMDb API ---
API_KEY = "YOUR_TMDB_API_KEY"  # 🔐 Replace with your key
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_MOVIE_URL = "https://api.themoviedb.org/3/movie"

@st.cache_data(show_spinner=False)
def get_movie_data(title):
    clean_title = title.split("(")[0].strip()
    params = {"api_key": API_KEY, "query": clean_title}
    res = requests.get(TMDB_SEARCH_URL, params=params)
    results = res.json().get("results", [])
    
    if results:
        movie_id = results[0]["id"]
        poster_path = results[0].get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        video_res = requests.get(f"{TMDB_MOVIE_URL}/{movie_id}/videos", params={"api_key": API_KEY})
        videos = video_res.json().get("results", [])
        trailer_url = None
        for v in videos:
            if v["site"] == "YouTube" and v["type"] == "Trailer":
                trailer_url = f"https://www.youtube.com/watch?v={v['key']}"
                break

        return poster_url, trailer_url
    return None, None

# --- Page Setup ---
st.set_page_config(layout="wide", page_title="Netflix Style Movie App")
st.markdown("""
    <style>
    body { background-color: #111; color: #fff; }
    .movie-row { display: flex; overflow-x: auto; padding-bottom: 20px; }
    .movie-card {
        flex: 0 0 auto;
        width: 180px;
        margin-right: 15px;
        border-radius: 10px;
        overflow: hidden;
        background: #1c1c1c;
        transition: transform 0.3s;
    }
    .movie-card:hover { transform: scale(1.05); }
    .movie-card img { width: 100%; border-bottom: 1px solid #333; }
    .movie-card .details {
        padding: 10px;
        color: #fff;
        font-size: 14px;
    }
    .movie-card .title { font-weight: bold; }
    .movie-card .rating { font-size: 12px; color: gold; }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 MovieFlix - Netflix Style Movie Recommender")

# --- Genre Dropdown ---
all_genres = sorted(set(g.strip() for sublist in df['genres'].dropna().str.split() for g in sublist))
selected_genre = st.selectbox("Choose a Genre", all_genres)

# --- Filter by Genre ---
filtered_df = df[df['genres'].str.contains(selected_genre, case=False, na=False)].sample(frac=1).head(15)

# --- Display Section 1: Genre-based Movies ---
st.markdown(f"### 🎞️ {selected_genre} Picks")

st.markdown('<div class="movie-row">', unsafe_allow_html=True)
for _, movie in filtered_df.iterrows():
    poster_url, trailer_url = get_movie_data(movie["title"])
    if not poster_url or "None" in str(poster_url):
        poster_url = f"https://via.placeholder.com/300x450?text={movie['title']}"

    html = f"""
    <div class="movie-card">
        <img src="{poster_url}" alt="{movie['title']}">
        <div class="details">
            <div class="title">{movie['title']}</div>
            <div class="rating">⭐ {movie['vote_average']}</div>
            <div>{movie['overview'][:80]}...</div>
            {'<a href="' + trailer_url + '" target="_blank">🎬 Trailer</a>' if trailer_url else ''}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Display Section 2: Top Recommendations ---
st.markdown(f"### 🔥 Top Rated {selected_genre} Movies")

top_df = (
    df[df['genres'].str.contains(selected_genre, case=False, na=False)]
    .sort_values(by="vote_average", ascending=False)
    .drop_duplicates(subset='title')
    .head(15)
)

st.markdown('<div class="movie-row">', unsafe_allow_html=True)
for _, movie in top_df.iterrows():
    poster_url, trailer_url = get_movie_data(movie["title"])
    if not poster_url or "None" in str(poster_url):
        poster_url = f"https://via.placeholder.com/300x450?text={movie['title']}"

    html = f"""
    <div class="movie-card">
        <img src="{poster_url}" alt="{movie['title']}">
        <div class="details">
            <div class="title">{movie['title']}</div>
            <div class="rating">⭐ {movie['vote_average']}</div>
            <div>{movie['overview'][:80]}...</div>
            {'<a href="' + trailer_url + '" target="_blank">🎬 Trailer</a>' if trailer_url else ''}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
