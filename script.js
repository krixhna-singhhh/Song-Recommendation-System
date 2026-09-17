/* ---------------------------------------------------------
   script.js
   Frontend logic for the Song Recommendation System.
   Talks to the Flask backend using fetch() calls to the
   /api/songs, /api/recommend and /api/filter endpoints.
--------------------------------------------------------- */

// Keep the full song list in memory once loaded, so we don't
// have to re-fetch it every time.
let allSongs = [];

// DOM references
const songInput = document.getElementById("songInput");
const songList = document.getElementById("songList");
const topNSelect = document.getElementById("topN");
const recommendBtn = document.getElementById("recommendBtn");
const songError = document.getElementById("songError");

const genreFilter = document.getElementById("genreFilter");
const moodFilter = document.getElementById("moodFilter");
const filterBtn = document.getElementById("filterBtn");

const resultsSection = document.getElementById("resultsSection");
const resultsTitle = document.getElementById("resultsTitle");
const resultsGrid = document.getElementById("resultsGrid");


// -----------------------------------------------------------------
// Load all songs on page load: fill the datalist + genre/mood filters
// -----------------------------------------------------------------
async function loadSongs() {
  try {
    const response = await fetch("/api/songs");
    const data = await response.json();
    allSongs = data.songs;

    // Fill the <datalist> so users get autocomplete suggestions
    songList.innerHTML = "";
    allSongs.forEach(song => {
      const option = document.createElement("option");
      option.value = song.title;
      songList.appendChild(option);
    });

    // Build unique genre + mood lists for the filter dropdowns
    const genres = [...new Set(allSongs.map(s => s.genre))].sort();
    const moods = [...new Set(allSongs.map(s => s.mood))].sort();

    genres.forEach(g => {
      const opt = document.createElement("option");
      opt.value = g;
      opt.textContent = g;
      genreFilter.appendChild(opt);
    });

    moods.forEach(m => {
      const opt = document.createElement("option");
      opt.value = m;
      opt.textContent = m;
      moodFilter.appendChild(opt);
    });

  } catch (err) {
    console.error("Failed to load songs:", err);
  }
}


// -----------------------------------------------------------------
// Render a list of song objects into the results grid as cards
// -----------------------------------------------------------------
function renderSongs(songs, { showSimilarity = false } = {}) {
  resultsGrid.innerHTML = "";

  if (!songs || songs.length === 0) {
    resultsGrid.innerHTML = "<p>No songs found. Try a different search or filter.</p>";
    return;
  }

  songs.forEach(song => {
    const card = document.createElement("div");
    card.className = "song-card";

    card.innerHTML = `
      <h3>${song.title}</h3>
      <p><strong>Artist:</strong> ${song.artist}</p>
      <p><strong>Genre:</strong> ${song.genre}</p>
      <p><strong>Mood:</strong> ${song.mood}</p>
      ${song.tempo ? `<p><strong>Tempo:</strong> ${song.tempo}</p>` : ""}
      ${showSimilarity
        ? `<span class="tag similarity-tag">Similarity: ${(song.similarity * 100).toFixed(1)}%</span>`
        : ""}
    `;

    resultsGrid.appendChild(card);
  });

  resultsSection.style.display = "block";
}


// -----------------------------------------------------------------
// Handle "Get Recommendations" button click
// -----------------------------------------------------------------
async function handleRecommend() {
  const songTitle = songInput.value.trim();
  const topN = topNSelect.value;
  songError.textContent = "";

  if (!songTitle) {
    songError.textContent = "Please type or select a song first.";
    return;
  }

  try {
    const response = await fetch(`/api/recommend?song=${encodeURIComponent(songTitle)}&top_n=${topN}`);
    const data = await response.json();

    if (!response.ok) {
      songError.textContent = data.error || "Something went wrong.";
      resultsSection.style.display = "none";
      return;
    }

    resultsTitle.textContent = `Songs similar to "${data.selected_song}"`;
    renderSongs(data.recommendations, { showSimilarity: true });

  } catch (err) {
    console.error(err);
    songError.textContent = "Could not reach the server. Please try again.";
  }
}


// -----------------------------------------------------------------
// Handle "Browse Songs" (genre/mood filter) button click
// -----------------------------------------------------------------
async function handleFilter() {
  const genre = genreFilter.value;
  const mood = moodFilter.value;

  try {
    const response = await fetch(`/api/filter?genre=${encodeURIComponent(genre)}&mood=${encodeURIComponent(mood)}`);
    const data = await response.json();

    resultsTitle.textContent = `Songs matching Genre: ${genre}, Mood: ${mood}`;
    renderSongs(data.results, { showSimilarity: false });

  } catch (err) {
    console.error(err);
  }
}


// -----------------------------------------------------------------
// Event listeners
// -----------------------------------------------------------------
recommendBtn.addEventListener("click", handleRecommend);
filterBtn.addEventListener("click", handleFilter);

// Allow pressing "Enter" inside the song input to trigger recommendations
songInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    handleRecommend();
  }
});

// Kick things off
loadSongs();
