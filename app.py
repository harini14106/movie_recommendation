import streamlit as st
import pandas as pd
import random

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("movies.csv")
    df = df.dropna(subset=['genres', 'title', 'vote_average', 'overview'])
    return df

df = load_data()

# UI Configuration
st.set_page_config(layout="wide")
st.title("🎬 MovieFlix - Genre-Based Recommendations")

# Genre Dropdown
all_genres = sorted(set(g.strip() for sublist in df['genres'].dropna().str.split() for g in sublist))
selected_genre = st.selectbox("Choose a Genre", all_genres)

# Filter movies by genre
filtered_df = df[df['genres'].str.contains(selected_genre, case=False, na=False)].reset_index(drop=True)

# Randomize and limit for display
filtered_df = filtered_df.sample(frac=1).head(20)

st.markdown(f"### Movies in **{selected_genre}** Genre")

# Show movies in horizontal rows (Netflix-style)
cols = st.columns(5)
for i, movie in filtered_df.iterrows():
    with cols[i % 5]:
        st.image(f"https://via.placeholder.com/300x450?text={movie['title']}", use_column_width=True)
        st.markdown(f"**{movie['title']}**")
        st.caption(f"⭐ {movie['vote_average']}")
        st.caption(movie['overview'][:100] + "...")

# Recommendations based on average rating in genre
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
    with rec_cols[i % 5]:
        st.image(f"https://via.placeholder.com/300x450?text={movie['title']}", use_column_width=True)
        st.markdown(f"**{movie['title']}**")
        st.caption(f"⭐ {movie['vote_average']}")
        st.caption(movie['overview'][:100] + "...")
