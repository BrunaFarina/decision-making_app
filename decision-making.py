#   decision-making.py
#   Bruna Farina, 2024.03.07
#   Description: application for making decisions. It chooses from list of foods/movies/activities.
#   Ref: https://developer.themoviedb.org

import requests
import random
import json

# dict of movie genres (from TMDB)
TMDB_GENRES = {
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Family": 10751,
    "Fantasy": 14,
    "History": 36,
    "Horror": 27,
    "Music": 10402,
    "Mystery": 9648,
    "Romance": 10749,
    "Science Fiction": 878,
    "TV Movie": 10770,
    "Thriller": 53,
    "War": 10752,
    "Western": 37
}

API_KEY = "d3ebf605da6dc8d6ef411760eb67fa4c"
def get_movie_names(genre_ids, pages):
    """
    :param genre_ids: List of genre IDs
    :param pages: Number of pages to fetch
    :return: List of dictionaries, each containing movie information
    """
    movies = [] #empty list to store movie names
    merged_list = [] # empty list to store list of dictionaries
    for page in range(pages): #the api returns only 1 page (loop to get other pages)
        url = f"https://api.themoviedb.org/3/discover/movie"
        params_api = {
            "api_key": API_KEY,
            "include_adult": "false",
            "include_video": "false",
            "language": "en-US",
            "page": page + 1,
            "sort_by": "popularity.desc",
            "vote_average.gte": 5,
            "vote_average.lte": 10,
            "with_genres": genre_ids,
            "without_genres": ','.join(map(str, TMDB_GENRES.values()))
        }
        response = requests.get(url, params=params_api)
        if response.status_code == 200:
            data = response.json()
            movies.extend(data.get('results', []))
        else:
            print("Error fetching movies:", response.text)
    return movies

def decide_for_me(user_request):
    """
    :param user_request: a string indicating the genre(s) of  movie.
    :return: randomly chosen movie based on genre(s)
    """
    if "," in user_request: #in case you want more than 1 genre
        criteria = input("Do you want multi genre movies (both genres at the same movie) or movies with only one genre? (answer: 'multi genre' or 'mono genre') ")
        if criteria == 'multi genre': #if you want, for example, genre 1 AND genre 2
            genres = list(user_request.split(", "))
            genres = [genre.title() for genre in genres]
            desirable_genre = [TMDB_GENRES.pop(item) for item in genres]
            desirable_genre = ",".join(str(id) for id in desirable_genre)
        else: # if you want genre 1 OR genre 2
            genres = list(user_request.split(", "))
            genres = [genre.title() for genre in genres]
            desirable_genre = [TMDB_GENRES.pop(item) for item in genres]
            desirable_genre = "|".join(str(id) for id in desirable_genre)
    else: #only one genre
        genres = user_request.capitalize()
        desirable_genre = TMDB_GENRES.pop(genres)
    movie_list = get_movie_names(desirable_genre, 10) #each page returns 20 movies
    rnd_movie = random.choice(movie_list)
    print(f"I think you should watch '{rnd_movie['title']}', released on {rnd_movie['release_date']}")

#user_request = "Comedy, drama"
if __name__ == '__main__':
    decide_for_me(input("Which genre(s) of movie do you like? (Separate by commas): "))