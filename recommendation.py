"""
recommendation.py
------------------
This module contains the core logic of our Song Recommendation System.

ALGORITHM USED: Content-Based Filtering using TF-IDF + Cosine Similarity

Why this approach?
- It does not need any data about other users (no "user ratings" needed),
  so it works well even with a small dataset.
- It recommends songs that are textually/thematically similar to a song
  the user already likes, based on features like genre, mood, artist, tempo
  and descriptive tags.

HOW IT WORKS (step by step):
1. For every song, we combine its important features (genre, mood, artist,
   tempo, tags) into a single string called a "combined feature soup".
2. We convert every song's "feature soup" into a numeric vector using
   TF-IDF (Term Frequency - Inverse Document Frequency). This gives more
   importance to words that are descriptive/rare and less importance to
   very common words.
3. We compute Cosine Similarity between every pair of songs. Cosine
   similarity measures the angle between two vectors -- the smaller the
   angle, the more similar the songs are (score close to 1 = very similar,
   score close to 0 = not similar).
4. When a user selects a song, we look up its similarity scores with every
   other song, sort them in descending order, and return the top N most
   similar songs (excluding the song itself).
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SongRecommender:
    """
    A content-based song recommendation engine.

    Usage:
        recommender = SongRecommender("data/songs.csv")
        recommender.build_model()
        results = recommender.recommend("Shape of You", top_n=5)
    """

    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None                # Will hold the songs dataframe
        self.tfidf_matrix = None       # Will hold the TF-IDF vectors
        self.cosine_sim = None         # Will hold the similarity matrix
        self.indices = None            # Maps song title -> row index

    def load_data(self):
        """Load the CSV dataset into a pandas DataFrame."""
        self.df = pd.read_csv(self.data_path)

        # Fill any missing values with empty strings so TF-IDF doesn't break
        for col in ["genre", "mood", "artist", "tempo", "tags"]:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna("")

        return self.df

    def _create_feature_soup(self, row):
        """
        Combine multiple descriptive columns of a song into a single string.
        Repeating the genre and mood gives them slightly more weight in the
        TF-IDF calculation since they are strong indicators of song style.
        """
        return " ".join([
            row["genre"], row["genre"],   # genre counted twice -> more weight
            row["mood"], row["mood"],     # mood counted twice -> more weight
            row["artist"],
            row["tempo"],
            row["tags"]
        ]).lower()

    def build_model(self):
        """
        Build the TF-IDF matrix and Cosine Similarity matrix.
        This should be called once when the Flask app starts.
        """
        if self.df is None:
            self.load_data()

        # Step 1: Create the combined feature text for every song
        self.df["feature_soup"] = self.df.apply(self._create_feature_soup, axis=1)

        # Step 2: Convert text into TF-IDF vectors
        # stop_words='english' removes common words like "the", "is", "and"
        tfidf = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = tfidf.fit_transform(self.df["feature_soup"])

        # Step 3: Compute cosine similarity between every pair of songs
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

        # Step 4: Build a quick lookup: song title (lowercase) -> row index
        self.indices = pd.Series(
            self.df.index, index=self.df["title"].str.lower()
        ).drop_duplicates()

        return self.cosine_sim

    def get_all_songs(self):
        """Return the list of songs (id, title, artist, genre) for the dropdown/search UI."""
        return self.df[["song_id", "title", "artist", "genre", "mood"]].to_dict(orient="records")

    def recommend(self, song_title, top_n=5):
        """
        Return the top_n songs most similar to the given song_title.

        Steps:
        1. Find the row index of the selected song.
        2. Get its similarity scores with all other songs.
        3. Sort by similarity score (highest first).
        4. Skip the song itself and return the next top_n songs.
        """
        song_title_lower = song_title.lower().strip()

        if song_title_lower not in self.indices:
            return None  # Song not found in dataset

        idx = self.indices[song_title_lower]

        # In case of duplicate titles, `idx` could be a Series; take the first
        if isinstance(idx, pd.Series):
            idx = idx.iloc[0]

        # List of (index, similarity_score) tuples for the selected song
        sim_scores = list(enumerate(self.cosine_sim[idx]))

        # Sort songs based on similarity score, highest first
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Exclude the song itself (it will always have similarity = 1.0 with itself)
        sim_scores = [s for s in sim_scores if s[0] != idx]

        # Take only the top N recommendations
        top_scores = sim_scores[:top_n]

        recommendations = []
        for i, score in top_scores:
            song = self.df.iloc[i]
            recommendations.append({
                "song_id": int(song["song_id"]),
                "title": song["title"],
                "artist": song["artist"],
                "genre": song["genre"],
                "mood": song["mood"],
                "tempo": song["tempo"],
                "similarity": round(float(score), 3)
            })

        return recommendations

    def recommend_by_filters(self, genre=None, mood=None, top_n=8):
        """
        Bonus feature: recommend songs directly by genre and/or mood,
        without needing to pick a specific base song first.
        Useful for users who just want "Happy Pop songs" for example.
        """
        filtered = self.df.copy()

        if genre and genre != "Any":
            filtered = filtered[filtered["genre"].str.lower() == genre.lower()]

        if mood and mood != "Any":
            filtered = filtered[filtered["mood"].str.lower() == mood.lower()]

        filtered = filtered.head(top_n)

        return filtered[["song_id", "title", "artist", "genre", "mood", "tempo"]].to_dict(orient="records")
