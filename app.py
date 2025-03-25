import streamlit as st
import pickle
import pandas as pd

# Load preprocessed movie list and similarity matrix
movie_list = pickle.load(open("movie_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Function to recommend movies
def recommend(movie_title):
    # Convert to lowercase & remove spaces
    movie_title = movie_title.strip().lower()

    # Normalize titles
    movie_list['title'] = movie_list['title'].str.strip().str.lower()

    # Search for movie in DataFrame
    filtered_df = movie_list[movie_list['title'] == movie_title]

    if filtered_df.empty:
        return ["Movie not found in dataset! Please try another movie."]

    movie_index = filtered_df.index[0]

    # Get similarity scores & sort
    scores = list(enumerate(similarity[movie_index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]  # Top 5 similar movies

    # Get movie recommendations
    recommended_movies = [movie_list.iloc[i[0]]['title'] for i in scores]

    return recommended_movies

# Streamlit UI
st.title("🎬 Movie Recommender System")

# Movie selection
selected_movie = st.selectbox(
    "Search for a movie:", 
    options=sorted(movie_list['title'].unique())  # Sorted dropdown list
)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    st.subheader("🎥 Recommended Movies:")
    for idx, movie in enumerate(recommendations, 1):
        st.write(f"{idx}. {movie}")

# Footer
st.markdown("---")
st.markdown("👨‍💻 Developed by **Your Name** | 🚀 Powered by Streamlit")
