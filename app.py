import pickle
import streamlit as st
import requests


# Function to fetch movie posters from TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path


# Function to get movie recommendations based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


# Set up the Streamlit app
st.set_page_config(page_title="Movie Recommender System", page_icon="🎬", layout="wide")
st.title('🍿 Movie Recommender System')

# Load the movie data and similarity matrix
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# User input for movie selection
st.write("Select a movie to get recommendations:")
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values,
    help="You can start typing the movie name to search."
)

# Button to show recommendations
if st.button('Show Recommendations'):
    st.subheader(f"Movies similar to {selected_movie}:")
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display the recommended movies in a grid layout
    cols = st.columns(10)
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.image(poster, use_column_width=True)
            st.caption(name)
