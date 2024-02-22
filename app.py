# Sam Zinn
# sjz20g
# due 02/21/24
# The program in this file is the individual work of Sam Zinn

from flask import Flask, render_template, request, redirect
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/enternew')
def new_review():
    return render_template('addReview.html')

# takes data received from addReview.html to add it to the DB
@app.route('/addreview', methods=['POST'])
def addreview():
    try:
        usr = request.form['Username']
        rev = request.form['Review']
        rate = request.form['Rating']
        tit = request.form['Title']
        dir = request.form['Director']    
        gen = request.form['Genre']     
        year = request.form['Year']
        movie_id = tit[:5].upper() + year  # assigning movie ID

        with sql.connect("movieData.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Reviews (Username, MovieID, ReviewTime, Rating, Review) VALUES (?, ?, datetime('now'), ?, ?)", (usr, movie_id, rate, rev))
            cur.execute("INSERT INTO Movies (MovieID, Title, Director, Genre, Year) VALUES (?, ?, ?, ?, ?)", (movie_id, tit, dir, gen, year))
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        print("An error occurred")
    finally:
        return redirect('/')
    
@app.route('/getreviews')
def get_reviews():
    return render_template('getReviews.html') 

@app.route('/getyear')
def get_year():
    return render_template('getYear.html') 

@app.route('/listbygenre', methods=['GET'])
def list_by_genre():
   try:
        genre = request.args.get('genre')
        with sql.connect("movieData.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            # fetching based on genre fed from user
            if genre:
                cur.execute("""SELECT Reviews.Rating, Reviews.Review, Movies.Title, Movies.Director FROM Reviews JOIN Movies ON Reviews.MovieID = Movies.MovieID WHERE Movies.Genre = ?""", (genre,))
            else:
                cur.execute("""SELECT Reviews.Rating, Reviews.Review, Movies.Title, Movies.Director FROM Reviews JOIN Movies ON Reviews.MovieID = Movies.MovieID""")
            rows = cur.fetchall()
        return render_template("listByGenre.html", rows=rows)
   except:
        print("An error occurred")

@app.route('/bestinyear', methods=['GET'])
def best_in_year():
    try:
        year = request.args.get('year')
        with sql.connect("movieData.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            # fetching based on year fed from user
            if year:
                cur.execute("""
                    SELECT Movies.Title, Movies.Genre, AVG(Reviews.Rating) AS AvgRating
                    FROM Reviews
                    JOIN Movies ON Reviews.MovieID = Movies.MovieID
                    WHERE Movies.Year = ?
                    GROUP BY Movies.MovieID
                    ORDER BY AvgRating DESC, Movies.Title ASC
                    LIMIT 5
                """, (year,))
            else:
                cur.execute("""
                    SELECT Movies.Title, Movies.Genre, AVG(Reviews.Rating) AS AvgRating
                    FROM Reviews
                    JOIN Movies ON Reviews.MovieID = Movies.MovieID
                    GROUP BY Movies.MovieID
                    ORDER BY AvgRating DESC, Movies.Title ASC
                    LIMIT 5
                """)
            rows = cur.fetchall()
        return render_template("bestInYear.html", rows=rows)
    except:
        print("An error occurred")

if __name__ == '__main__':
    app.run(debug=True)
