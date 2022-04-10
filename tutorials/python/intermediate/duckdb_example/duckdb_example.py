import duckdb
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
films = pd.read_html(url)[0]
print(films.head())

# We instantiate our DB in memory and try a select
con = duckdb.connect(database=':memory:')
con.execute("SELECT * FROM films").df()

# Let's clean the data
films_clean = con.execute("""
            SELECT 
                Rank
                , Peak
                , Title
                , Year
                , cast(replace("Worldwide gross"[instr("Worldwide gross",'$'):],',','') as bigint) as WorldwideGross
            FROM films
            """).df()
films_clean.dtypes

# Let's quickly calculate the average worldwide gross for each year and plot it
avg_year = con.execute("""
                        SELECT 
                            Year
                            , AVG(WorldwideGross) / 1000000 as "AVGGross(Mln)" 
                        FROM films_clean GROUP BY Year ORDER BY 1 DESC
                    """).df()
avg_year.plot(x='Year', y='AVGGross(Mln)', kind='bar')