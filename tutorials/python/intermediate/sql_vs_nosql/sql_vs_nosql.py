import sqlite3  # SQL DB
from tinydb import TinyDB, Query # NOSQL DB
import pandas as pd

# DATA ############################à
user_data = [
    {'userId':1, 'name': 'John', 'age': 20, 'countryId': 1},
    {'userId':2, 'name': 'Jack', 'age': 25, 'countryId': 1},
    {'userId':3, 'name': 'Jill', 'age': 20, 'countryId': 2},
    {'userId':4, 'name': 'Mario', 'age': 45, 'countryId': 3},
    {'userId':5, 'name': 'Luigi', 'age': 40, 'countryId': 3},
]
countries = [
    {'countryId': 1, 'name': 'USA'},
    {'countryId': 2, 'name': 'UK'},
    {'countryId': 3, 'name': 'ITALY'},
]

# SQL database ##########################
sql_db = sqlite3.connect('./data/sqlite_db.db')
user_df = pd.DataFrame(user_data)
countries_df = pd.DataFrame(countries)

user_df.to_sql('users', sql_db, if_exists='replace', index=False)
countries_df.to_sql('countries', sql_db, if_exists='replace', index=False)

# SELECTING
pd.read_sql("SELECT * FROM users", sql_db)
pd.read_sql("SELECT * FROM countries", sql_db)
# FILTERING
pd.read_sql("SELECT * FROM users WHERE age > 25", sql_db)
# SORTING
pd.read_sql("SELECT * FROM users ORDER BY age DESC", sql_db)
# GROUPING
pd.read_sql('SELECT countryId, AVG(age) "AvgAge" FROM users GROUP BY countryId', sql_db)
# JOINING
pd.read_sql('SELECT users.name, countries.name FROM users JOIN countries ON users.countryId = countries.countryId', sql_db)

# NOSQL database ######################
nosql_db = TinyDB('./data/tinydb_db.json')
# JOIN df
join_df = user_df.merge(countries_df, left_on='countryId', right_on='countryId')
join_df.rename(columns={'name_y': 'country', 'name_x':'name'}, inplace=True)
# CONVERT THE DF TO DICT
join_dict = join_df.to_dict('records')
nosql_db.insert_multiple(join_dict)

# SELECTING
nosql_db.all()
# FILTERING
nosql_db.search(Query().age > 25)
# ADVANCED FILTERING
first_letter_j = lambda x: x[0] == 'J'
nosql_db.search(Query().name.test(first_letter_j))


