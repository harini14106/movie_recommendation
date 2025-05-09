import streamlit as st
import pandas as pd

# Sample movie data
data = {
    "title": [
        "Inception", "The Matrix", "Interstellar", "The Dark Knight", "Fight Club",
        "Forrest Gump", "The Shawshank Redemption", "The Godfather", "Pulp Fiction", "The Lord of the Rings"
    ],
    "poster_url": [
        "https://image.tmdb.org/t/p/w500/qmDpIHrmpJINaRKAfWQfftjCdyi.jpg",
        "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
        "https://image.tmdb.org/t/p/w500/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg",
        "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "https://image.tmdb.org/t/p/w500/bptfVGEQuv6vDTIMVCHjJ9Dz8PX.jpg",
        "https://image.tmdb.org/t/p/w500/saHP97rTPS5eLmrLQEcANmKrsFl.jpg",
        "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmt0fjIBkYqY1OYu.jpg",
        "https://image.tmdb.org/t/p/w500/eEslKSwcqmiNS6va24Pbxf2UKmJ.jpg",
        "https://image.tmdb.org/t/p/w500/dM2w364MScsjFf8pfMbaWUcWrR.jpg",
        "https://image.tmdb.org/t/p/w500/56zTpe2xvaA4alU51sRWPoKPYZy.jpg"
    ],
    "genre": [
        "Sci-Fi", "Action", "Sci-Fi", "Action", "Drama",
        "Drama", "Drama", "Crime", "Crime", "Fantasy"
    ],
    "trailer_url": [
        "https://www.youtube.com/watch?v=8hP9D6kZseM",
        "https://www.youtube.com/watch?v=vKQi3bBA1y8",
        "https://www.youtube.com/watch?v=zSWdZVtXT7E",
        "https://www.youtube.com/watch?v=EXeTwQWrcwY",
        "https://www.youtube.com/watch?v=SUXWAEX2jlg",
        "https://www.youtube.com/watch?v=bLvqoHBptjg",
        "https://www.youtube.com/watch?v=6hB3S9bIaco",
        "https://www.youtube.com/watch?v=sY1S34973zA",
        "https://www.youtube.com/watch?v=s7EdQ4FqbhY",
        "https://www.youtube.com/watch?v=V75dMMIW2B4"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Streamlit UI
st.set_page_config(layout="wide")
st.title("Netflix-Style Movie Recommender")

st.subheader("Popular Movies")

# Display movies in a grid
cols = st.columns(5)
for index, movie in df.iterrows():
    with cols[index % 5]:
        st.image(movie["poster_url"], use_column_width=True)
        st.markdown(f"**{movie['title']}**")
        st.caption(f"Genre: {movie['genre']}")
        st.markdown(f"[Watch Trailer]({movie['trailer_url']})")
