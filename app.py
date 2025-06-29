from flask import Flask, render_template
import duckdb
import pandas as pd

app = Flask(__name__)

# Country code override
def flag_code(team):
    override = {
        "CHN": "cn",  # CHN → China flag
        "UKR": "ua",
        "NED": "nl",
        "GBR": "gb",
        "USA": "us",
        "ZIM":"zw",
        "HUN": "hu"
        # Add more as needed
    }
    return override.get(team, team[:2].lower())

# Register Jinja filter
app.jinja_env.filters['flag_code'] = flag_code

@app.route("/")
def index():
    con = duckdb.connect("my_database.duckdb")

    query = """
    SELECT
        Athlete,
        Team,
        COUNT(*) AS total_races,
        CAST(SUM(
            CASE
                WHEN Rank = 1 THEN 10
                WHEN Rank = 2 THEN 5
                WHEN Rank = 3 THEN 3
                ELSE 0
            END
        ) AS INTEGER) AS total_score
    FROM olympic_results
    GROUP BY Athlete, Team
    ORDER BY total_score DESC
    LIMIT 15
    """
    df = con.execute(query).fetchdf()
    return render_template("scores.html", table=df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
