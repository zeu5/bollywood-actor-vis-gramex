import sqlite3
import os
from re import search, UNICODE


config = {
	'DATABASE' : os.path.join(os.getcwd(), 'data/bollywood-actor.db')
}

def get_db():
	"""
	Opens a database connection if it doesnt exist otherwise returns from app context.
	"""
	return sqlite3.connect(config['DATABASE'])


def get_movies(handler):
	"""
	Given an actor this API returns an array of movies the actor has acted in.
	The JSON format is an array of object where each object is a map of actor to an array of his movies
	[ { actor1 : [movie1, movie2] }, { actor2 : [movie2, movie3] } ]
	"""
	actors = handler.get_argument('actors')
	if search('([\w ]+,)*([\w ]+)', actors, UNICODE):
		# If actors are in comma seperated format
		actors = actors.split(',')
		result = {}
		db_cursor = get_db().cursor()
		for actor in actors:
			actor = actor.strip()
			db_cursor.execute('select distinct movie_name from celebrities where role=? and name=?',['Actor',actor])
			rows = db_cursor.fetchall()
			if len(rows):
				result[actor] = map(lambda x: x[0], rows)
		return result
	else:
		handler.send_error(204)

def get_actors(handler):
	"""
	Given an actor this API returns an array of actors who have acted in the movie.
	The JSON format is as follows
	[ { movie1 : [actor1, actor2] }, { movie2 : [actor2, actor3] } ]
	"""

	movies = handler.get_argument('movies')
	if search('([\w ]+,)*([\w ]+)', movies, UNICODE):
		# If movies are in comma seperated format
		movies = movies.split(',')
		result = {}
		db_cursor = get_db().cursor()
		for movie in movies:
			movie = movie.strip()
			db_cursor.execute('select distinct name from celebrities where role=? and movie_name=?',['Actor',movie])
			rows = db_cursor.fetchall()
			if len(rows):
				result[movie] = map(lambda x: x[0], rows)
		return result
	else:
		handler.send_error(204)