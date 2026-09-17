# 🎵 Song Recommendation System

A beginner-friendly, web-based Song Recommendation System built with **Python, Flask, Pandas, and Scikit-learn**. It recommends songs similar to a song the user selects, using **Content-Based Filtering** with **TF-IDF** and **Cosine Similarity**. Users can also browse songs directly by genre and mood.

---

## 1. Introduction

Music streaming platforms recommend songs to keep listeners engaged and help them discover new music that matches their taste. This project is a simplified, educational version of such a system, built as a college mini-project to demonstrate the practical application of **data preprocessing, feature engineering, and similarity-based machine learning** in a real, working web application.

---

## 2. Problem Statement

With thousands of songs available on any platform, manually finding songs similar to one's favorites is time-consuming. Users need a system that can automatically suggest songs based on shared characteristics such as genre, mood, artist style, and tempo — without needing large amounts of user listening history (which small projects and new platforms usually don't have).

---

## 3. Objectives

- Design and implement a content-based song recommendation engine.
- Use TF-IDF vectorization to numerically represent song characteristics.
- Use Cosine Similarity to measure how alike two songs are.
- Build a simple, functional web interface where users can search for a song and instantly view recommendations.
- Keep the technology stack simple and beginner-friendly so the project is easy to explain and demonstrate.

---

## 4. Features

- 🔍 **Search by Song** — type/select a song and get the top 5–10 most similar songs.
- 🎚 **Browse by Genre & Mood** — filter the dataset directly without picking a base song.
- 📊 **Similarity Score** — each recommendation shows how similar it is to the selected song (as a percentage).
- 🎤 **Artist & Genre Info** — every recommended song displays its artist, genre, mood, and tempo.
- 💻 **Clean, responsive UI** — simple HTML/CSS/JS frontend, no heavy frameworks.
- ⚡ **Fast** — the similarity model is built once at server startup, so recommendations are instant.

---

## 5. Technologies Used

| Layer            | Technology              |
|-------------------|--------------------------|
| Backend           | Python 3, Flask          |
| Data Handling     | Pandas                   |
| Machine Learning  | Scikit-learn (TF-IDF, Cosine Similarity) |
| Frontend          | HTML5, CSS3, JavaScript (Vanilla, no frameworks) |
| Data Storage      | CSV file (`data/songs.csv`) |

---

## 6. Methodology

1. **Data Collection** – A sample dataset of 40 songs was curated with the fields: `song_id, title, artist, genre, mood, tempo, tags`. (You can easily replace this with a larger public dataset, such as a Kaggle Spotify dataset, as long as it has similar columns.)
2. **Feature Engineering** – For every song, a combined text "feature soup" is created from its genre, mood, artist, tempo, and descriptive tags. Genre and mood are given extra weight since they are the strongest indicators of a song's style.
3. **Vectorization** – The `TfidfVectorizer` from Scikit-learn converts each song's feature soup into a numeric vector, where rare/descriptive words get higher weight than common words.
4. **Similarity Computation** – `cosine_similarity` computes a similarity score (0 to 1) between every pair of songs, based on the angle between their TF-IDF vectors.
5. **Recommendation** – When a user picks a song, the system looks up that song's similarity scores against all others, sorts them in descending order, and returns the top N (excluding the song itself).
6. **Web Integration** – Flask exposes this logic through simple JSON API endpoints, which the JavaScript frontend calls using `fetch()` to display results dynamically without reloading the page.

---

## 7. Algorithm Explanation

**Content-Based Filtering using TF-IDF + Cosine Similarity**

- **TF-IDF (Term Frequency–Inverse Document Frequency)**: A statistical measure that evaluates how important a word is in a document relative to a collection of documents. Common words (like "the song") get a low score, while distinctive words (like "synthwave" or "acoustic") get a higher score. Here, each "document" is one song's combined feature text.

- **Cosine Similarity**: Measures the cosine of the angle between two vectors. If two songs have very similar feature vectors, the angle between them is small, so the cosine similarity is close to **1** (highly similar). Unrelated songs have vectors pointing in very different directions, giving a similarity closer to **0**.

- **Why this approach for a college project?**
  - No user rating/history data is required (works from day one — the "cold start" problem of collaborative filtering doesn't apply).
  - Easy to explain and visualize: you can literally show the TF-IDF table and the similarity matrix.
  - Fully deterministic and reproducible, which is ideal for a project demo.

---

## 8. Project Structure

```
song-recommendation-system/
├── app.py                     # Flask application & API routes
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation (this file)
├── data/
│   └── songs.csv               # Sample song dataset
├── templates/
│   └── index.html              # Main web page
├── static/
│   ├── style.css                # Styling
│   └── script.js                 # Frontend logic (calls Flask APIs)
└── recommender/
    └── recommendation.py        # Core recommendation engine (TF-IDF + Cosine Similarity)
```

---

## 9. Installation & Setup

### Prerequisites
- Python 3.9 or higher installed on your system.

### Step-by-step Instructions

**1. Extract/clone the project and move into the folder:**
```bash
cd song-recommendation-system
```

**2. Create a virtual environment:**

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install the required dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the application:**
```bash
python app.py
```

**5. Open your browser and go to:**
```
http://127.0.0.1:5000/
```

### Testing it locally

- Try searching for a song already in the dataset, e.g. **"Shape of You"**, **"Perfect"**, or **"Bohemian Rhapsody"**, and click **Get Recommendations**.
- Try the **Browse by Genre & Mood** section — for example, select `Rock` + `Energetic` and click **Browse Songs**.
- You can also test the raw API directly in the browser:
  - `http://127.0.0.1:5000/api/songs`
  - `http://127.0.0.1:5000/api/recommend?song=Perfect&top_n=5`
  - `http://127.0.0.1:5000/api/filter?genre=Pop&mood=Happy`

---

## 10. How the Recommendation Works (Summary)

1. User selects/searches a song, e.g. **"Perfect" by Ed Sheeran**.
2. The Flask backend looks up this song's row in the pre-computed cosine similarity matrix.
3. It sorts all other songs by similarity score, highest first.
4. The top N songs (excluding "Perfect" itself) are returned as JSON, e.g. "Thinking Out Loud", "Perfect Duet", "All of Me" — songs that share the Pop genre, Romantic mood, and similar tags.
5. The frontend displays these as cards with artist, genre, mood, and similarity percentage.

---

## 11. Future Scope

- Replace the sample CSV with a larger real-world dataset (e.g., a public Spotify tracks dataset) with audio features like danceability, energy, and valence for richer recommendations.
- Add **Collaborative Filtering** (based on what similar users listened to) and combine it with content-based filtering into a **Hybrid Recommender**.
- Add user accounts and a "Liked Songs" history to personalize recommendations over time.
- Integrate a real music API (e.g., Spotify Web API) to fetch album art, previews, and playback.
- Deploy the app on a cloud platform (Render, Railway, PythonAnywhere) for public access.
- Add more advanced NLP embeddings (e.g., word2vec or sentence transformers) instead of TF-IDF for deeper semantic similarity.

---

## 12. Author Note

This project was built as an original academic mini-project to demonstrate practical use of Python, Flask, and Scikit-learn for building a real, functioning recommendation system suitable for classroom demonstration and viva/presentation.
