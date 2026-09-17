"""
app.py
------
Main Flask application file for the Song Recommendation System.

This file:
1. Starts the Flask web server.
2. Loads the song dataset and builds the recommendation model once at startup.
3. Defines the routes (URLs) that the browser/JavaScript can call:
      GET  /                -> loads the main HTML page
      GET  /api/songs       -> returns the full list of songs (for search/dropdown)
      GET  /api/recommend   -> returns recommendations for a chosen song
      GET  /api/filter      -> returns songs matching a genre/mood filter
"""

from flask import Flask, render_template, request, jsonify
import os

from recommender.recommendation import SongRecommender

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = Flask(__name__)

# Build an absolute path to the CSV file so the app works no matter
# which folder you run "python app.py" from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "songs.csv")

# Create the recommender engine and build the model ONE time when the
# server starts (not on every request) -- this keeps the app fast.
recommender = SongRecommender(DATA_PATH)
recommender.load_data()
recommender.build_model()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """Render the main page of the web app."""
    return render_template("index.html")


@app.route("/api/songs", methods=["GET"])
def get_songs():
    """
    Returns the full list of songs in JSON format.
    Used by the frontend to populate the search/select dropdown.
    """
    songs = recommender.get_all_songs()
    return jsonify({"songs": songs})


@app.route("/api/recommend", methods=["GET"])
def recommend():
    """
    Returns top-N recommended songs similar to the song given in the
    query string, e.g.  /api/recommend?song=Shape of You&top_n=5
    """
    song_title = request.args.get("song", "").strip()
    top_n = request.args.get("top_n", default=5, type=int)

    if not song_title:
        return jsonify({"error": "Please provide a song name using the 'song' parameter."}), 400

    results = recommender.recommend(song_title, top_n=top_n)

    if results is None:
        return jsonify({"error": f"Song '{song_title}' was not found in our dataset."}), 404

    return jsonify({
        "selected_song": song_title,
        "recommendations": results
    })


@app.route("/api/filter", methods=["GET"])
def filter_songs():
    """
    Returns songs matching a chosen genre and/or mood.
    Example: /api/filter?genre=Pop&mood=Happy
    """
    genre = request.args.get("genre", default="Any")
    mood = request.args.get("mood", default="Any")
    top_n = request.args.get("top_n", default=8, type=int)

    results = recommender.recommend_by_filters(genre=genre, mood=mood, top_n=top_n)
    return jsonify({"results": results})


# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # debug=True auto-reloads the server when code changes (useful during development)
    app.run(debug=True, host="0.0.0.0", port=5000)
