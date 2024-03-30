import pickle
import streamlit as st
import requests

def fetch_poster(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key=6f54375151750bfd1984f4eb6801eab5&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = f"http://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
    return None

# Load the pickled data
with open('artifacts/series_list.pickle', 'rb') as series_file:
    series = pickle.load(series_file)

with open('artifacts/similarity.pickle', 'rb') as simulation_file:
    simulation = pickle.load(simulation_file)

def recommend(movie):
    index = series[series['title'] == movie].index[0]
    distance = sorted(list(enumerate(simulation[index])), reverse=True, key=lambda x: x[1])
    recommend_series = []
    recommend_poster = []
    for i in distance[1:11]:
        series_id = series.iloc[i[0]]['id']
        poster_url = fetch_poster(series_id)
        if poster_url:
            recommend_poster.append(poster_url)
        recommend_series.append(series.iloc[i[0]]['title'])
    return recommend_series, recommend_poster

st.title('Movies Recommender System')

series_list = series['title'].values
selected_series = st.selectbox('Select your movie', series_list)

if st.button('Show Recommendation'):
    try:
        recommend_series, recommend_poster = recommend(selected_series)

        # Create five columns for layout
        col1, col2, col3, col4, col5 = st.columns(5)

        # Use st.container to create individual containers for each movie
        for i in range(0, min(10, len(recommend_series)), 5):
            # Create a container for current movie with styling
            with col1:
                container = st.container()
                if i < len(recommend_series):
                    container.markdown(f"""
                        <style>
                            .movie-container {{
                                text-align: center;
                                margin: 10px;
                                border-radius: 10px;
                                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                            }}
                            .movie-title {{
                                margin-top: 5px;
                                font-weight: bold;
                                font-size: 1em;
                            }}
                        </style>
                        <div class="movie-container">
                            <p class="movie-title">{recommend_series[i][:50]}</p>
                            <img src="{recommend_poster[i]}" alt="{recommend_series[i]}" style="width:100%">
                        </div>
                    """, unsafe_allow_html=True)
            with col2:
                container = st.container()
                if i + 1 < len(recommend_series):
                    container.markdown(f"""
                        <style>
                            .movie-container {{
                                text-align: center;
                                margin: 10px;
                                border-radius: 10px;
                                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                            }}
                            .movie-title {{
                                margin-top: 5px;
                                font-weight: bold;
                                font-size: 1em;
                            }}
                        </style>
                        <div class="movie-container">
                            <p class="movie-title">{recommend_series[i+1][:50]}</p>
                            <img src="{recommend_poster[i+1]}" alt="{recommend_series[i+1]}" style="width:100%">
                        </div>
                    """, unsafe_allow_html=True)
            with col3:
                container = st.container()
                if i + 2 < len(recommend_series):
                    container.markdown(f"""
                        <style>
                            .movie-container {{
                                text-align: center;
                                margin: 10px;
                                border-radius: 10px;
                                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                            }}
                            .movie-title {{
                                margin-top: 5px;
                                font-weight: bold;
                                font-size: 1em;
                            }}
                        </style>
                        <div class="movie-container">
                            <p class="movie-title">{recommend_series[i+2][:50]}</p>
                            <img src="{recommend_poster[i+2]}" alt="{recommend_series[i+2]}" style="width:100%">
                        </div>
                    """, unsafe_allow_html=True)
            with col4:
                container = st.container()
                if i + 3 < len(recommend_series):
                    container.markdown(f"""
                        <style>
                            .movie-container {{
                                text-align: center;
                                margin: 10px;
                                border-radius: 10px;
                                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                            }}
                            .movie-title {{
                                margin-top: 5px;
                                font-weight: bold;
                                font-size: 1em;
                            }}
                        </style>
                        <div class="movie-container">
                            <p class="movie-title">{recommend_series[i+3][:50]}</p>
                            <img src="{recommend_poster[i+3]}" alt="{recommend_series[i+3]}" style="width:100%">
                        </div>
                    """, unsafe_allow_html=True)
            with col5:
                container = st.container()
                if i + 4 < len(recommend_series):
                    container.markdown(f"""
                        <style>
                            .movie-container {{
                                text-align: center;
                                margin: 10px;
                                border-radius: 10px;
                                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                            }}
                            .movie-title {{
                                margin-top: 5px;
                                font-size: 1em;
                            }}
                        </style>
                        <div class="movie-container">
                            <p class="movie-title">{recommend_series[i+4][:50]}</p>
                            <img src="{recommend_poster[i+4]}" alt="{recommend_series[i+4]}" style="width:100%">
                        </div>
                    """, unsafe_allow_html=True)

    except KeyError:
        st.error("Selected movie not found. Please try again.")
    except IndexError:
        st.warning("IndexError: The loop went out of range. Please check your data.")
