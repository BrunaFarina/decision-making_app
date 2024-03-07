#   decision-making.py
#   Bruna Farina, 2024.03.07
#   Description: application for making decisions. It chooses from list of foods/movies/activities.
#   Ref: https://developer.themoviedb.org


### NOTAS:
# add more foods
# replace loops for list comprehension
# do I need the "genres" obj?
# replace "elif user_request.lower() is "movie":" for "else"?

import requests
import random
import json

#dict of foods
foods = ["pasta", "pizza", "hamburger", "sushi", "indian_food", "mexican food"]

genres = {
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

def movie_names(genre, pages):
    movies = []
    for page in range(0, 200): #the api returns only 1 page (loop to get other pages)
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_genres={genres[genre]}"
        headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkM2ViZjYwNWRhNmRjOGQ2ZWY0MTE3NjBlYjY3ZmE0YyIsInN1YiI6IjY1ZTljMjQ1NmEyMjI3MDE4Njk2NmM5MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dozyRSZ-_MPi-sWqQSuYQloqtotrDLMZM3Wq4lgdM-4"
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        for dictionary in data['results']:
            movies.append(dictionary['title'])
    return movies

def decide_movie(user_request):
    user_request = input("What do you want me to choose for you? Movie or Food?")

    if user_request.lower() is "food":
        rnd_food = random.choice(foods)
        print("I think you should eat", rnd_food, "today")

    elif user_request.lower() is "movie":
        genre = input("Which kind of movie do you like?").capitalize()
        movies = movie_names(genre, 200)
        rnd_movie = random.choice(movies)
        print("You should watch", rnd_movie)







