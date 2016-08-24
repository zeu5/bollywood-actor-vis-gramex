import os
import sqlite3
import csv


config = {
	'DATABASE' : os.path.join(os.getcwd(), 'bollywood-actor.db')
}


def get_db():
	"""
	Opens a database connection if it doesnt exist otherwise returns from app context.
	"""
	return sqlite3.connect(config['DATABASE'])

def init_db():
	"""
	Reinitialises the database removing the previous data and populating it based on the csv
	"""
	db = get_db()
	with open(os.path.join(os.getcwd(), 'schema.sql')) as f:
		db.cursor().executescript(f.read())
	db.commit()
	populate_data(db)
	print "Initialised the database"


def populate_data(db):
	"""
	Fetch initial data from the csv in data/bollywood.celebrity.csv and insert into the database
	"""
	def get_csv_data():
		"""
		Retireves the csv as an array
		"""
		try:
			data = []
			with open(os.path.join(os.getcwd(), 'data/bollywood.celebrity.csv')) as csv_file:
				csv_reader = csv.reader(csv_file)
				header = csv_reader.next() #Header line Not needed
				for row in csv_reader:
					data.append(row)
			return data

		except Exception, e:
			print "Could not fetch data from the CSV"
			print e

	def insert_data(data_list, db):
		"""
		Inserts the data in the list into the database
		"""
		cursor = db.cursor()
		for data_row in data_list:
			try:
				cursor.execute('insert into celebrities values (?, ?, ?, ?, ?)',data_row)
			except Exception, e:
				# When it fails integrity error or null data is tried to be inserted
				continue
		db.commit()

	insert_data(get_csv_data(),db)

if __name__ == '__main__':
	init_db()

