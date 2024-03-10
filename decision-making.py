#   decision-making.py
#   Bruna Farina, 2024.03.07
#   Description: application for making decisions. It chooses from list of foods/movies/activities.
#   Ref: https://developer.themoviedb.org

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

API_KEY = "d3ebf605da6dc8d6ef411760eb67fa4c"
def movie_names(genre, pages):
    """
    :param genre: list of genre ID (values from tmdb_genres dict)
    :param pages: number of pages to be returned (each page returns 20 movies)
    :return: a list of dictionaries. Each one for a movie
    """
    movies = [] #empty list to store movie names
    merged_list = [] # empty list to store list of dictionaries
    for page in range(0, pages): #the api returns only 1 page (loop to get other pages)
        url = (f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&include_adult=false&include_video=false&language=en-US&page={page+1}&"
               f"sort_by=popularity.desc&vote_average.gte=5&vote_average.lte=10&with_genres={genre}&"
               f"without_genres={', '.join(str(x) for x in tmdb_genres.values())}") #convert dict values to a str
        response = requests.get(url)
        data = json.loads(response.text)
        merged_list = merged_list + data['results']
    return merged_list

def decide_for_me(user_request):
    """

    :param user_request: a sting indicating if the user wants a movie or a food.
    :return: food/movie chosen randomly. For movies, the user should filter by genre(s)
    """
    if user_request.lower() == "food": #if you want to return food
        rnd_food = random.choice(foods)
        print("I think you should have", rnd_food, "today")
    elif user_request.lower() == "movie": # if movie
        genres = input("Which kind(s) of movie do you like? ")
        if "," in genres: #in case you want more than 1 genre
            criteria = input("Do you mean multi genre movies (both genres at the same movie) or movies with only one genre? (answer: 'multi genre' or 'mono genre') ")
            if criteria == 'multi genre': #if you want, for example, genre 1 AND genre 2
                genres = list(genres.split(", "))
                genres = [genre.title() for genre in genres]
                desirable_genre = [tmdb_genres.pop(item) for item in genres]
                desirable_genre = ",".join(str(id) for id in desirable_genre)
            else: # if you want genre 1 OR genre 2
                genres = list(genres.split(", "))
                genres = [genre.title() for genre in genres]
                desirable_genre = [tmdb_genres.pop(item) for item in genres]
                desirable_genre = "|".join(str(id) for id in desirable_genre)
        else: #only one genre
            genres = genres.capitalize()
            desirable_genre = tmdb_genres.pop(genres)
        movie_list = movie_names(desirable_genre, 10) #each page returns 20 movies
        rnd_movie = random.choice(movie_list)
        print(f"I think you should watch '{rnd_movie['title']}', released on {rnd_movie['release_date']}")
    else:
        print("This is not 'food' or 'movie'")

user_request = input("What do you want me to choose for you: movie or food? ")

if __name__ == '__main__':
    decide_for_me(user_request)