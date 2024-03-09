#   decision-making.py
#   Bruna Farina, 2024.03.07
#   Description: application for making decisions. It chooses from list of foods/movies/activities.
#   Ref: https://developer.themoviedb.org


### NOTES:
# add more foods
# replace loops for list comprehension
# do I need the "genres" obj?
# replace "elif user_request.lower() is "movie":" for "else"? - DONE
# it's returning other movies other than the specified genre (ex: I want comedy; it also returns drama/comedy) - DONE
# rank by rate instead of popularity - DONE (but realized rate returns shit movies. Back to popularity, but add a rate filter) - DONE
#problem: some movies have similar/same name, it's better to return also the year (or director name) to have some more info - DONE

import requests
import random
import json

# dict of foods
foods = ["pasta", "pizza", "hamburger", "sushi", "indian_food", "mexican food"]

# dict of movie genres (from TMDB)
tmdb_genres = {
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
    movies = [] #empty list to store movie names
    merged_list = [] # empty list to store list of dictionaries

    # remove the desirable movie genre from "genres" dict and store its key
    if "," in genre:
        desirable_genre = [tmdb_genres.pop(item) for item in genre]
        desirable_genre = ",".join(str(id) for id in desirable_genre)
    else:
        desirable_genre = tmdb_genres.pop(genre)
    for page in range(0, pages): #the api returns only 1 page (loop to get other pages)
        url = (f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page+1}&"
               f"sort_by=popularity.desc&vote_average.gte=5&vote_average.lte=10&with_genres={desirable_genre}&"
               f"without_genres={', '.join(str(x) for x in tmdb_genres.values())}") #convert dict values to a str
        headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkM2ViZjYwNWRhNmRjOGQ2ZWY0MTE3NjBlYjY3ZmE0YyIsInN1YiI6IjY1ZTljMjQ1NmEyMjI3MDE4Njk2NmM5MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dozyRSZ-_MPi-sWqQSuYQloqtotrDLMZM3Wq4lgdM-4"
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        merged_list = merged_list + data['results']
    return merged_list

def decide_for_me(user_request):
    if user_request.lower() == "food":
        rnd_food = random.choice(foods)
        print("I think you should have", rnd_food, "today")

    elif user_request.lower() == "movie":
        genres = input("Which kind of movie do you like? ")

        if "," in genres:
            genres = list(genres.split(", "))
            genres = [genre.title() for genre in genres]
        else:
            genres = genres.capitalize()

        movie_list = movie_names(genres, 5) #each page returns 20 movies
        rnd_movie = random.choice(movie_list)
        print(f"I think you should watch '{rnd_movie['title']}', released on {rnd_movie['release_date']}")

    else:
        print("This is not 'food' or 'movie'")

user_request = input("What do you want me to choose for you: movie or food? ")

if __name__ == '__main__':
    decide_for_me(user_request)