# 🎬 FLICKR — Movie Recommendation System

> A Netflix-inspired movie discovery and recommendation web app built entirely from scratch by a Final Year B.Tech student.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![Render](https://img.shields.io/badge/Backend-Render-46E3B7?style=flat-square)
![Streamlit Cloud](https://img.shields.io/badge/Frontend-Streamlit%20Cloud-FF4B4B?style=flat-square)

---

## 🖼️ Preview

| Home Feed | Movie Details |
|-----------|---------------|
| Hero banner + trending grid | Backdrop, genres, recommendations |

---

## ✨ Features

- 🔥 **Home Feed** — Browse Trending, Popular, Top Rated, Now Playing, and Upcoming movies
- 🔎 **Smart Search** — Keyword search with live dropdown suggestions powered by TMDB
- 🎯 **Content-Based Recommendations** — Uses **Cosine Similarity** on TF-IDF vectors to find similar films
- 🎭 **Genre Recommendations** — Discover more films in the same genre via TMDB Discover API
- 🎞️ **Movie Details Page** — Full backdrop, poster, overview, runtime, language, genres, and rating
- 📱 **Responsive Design** — Works on desktop, tablet, and mobile
- ⚡ **Fast & Cached** — API responses cached to reduce load time

---

## 🧠 How Recommendations Work

```
User selects a movie
        ↓
TF-IDF vectorizer transforms movie metadata (title, overview, genres)
        ↓
Cosine Similarity computed against all movies in the dataset
        ↓
Top-N most similar movies returned
        ↓
TMDB API fetches posters and details for each result
```

The **TF-IDF + Cosine Similarity** approach works by:
1. Converting each movie's text data into a numerical vector
2. Measuring the angle between vectors — smaller angle = more similar
3. Ranking all movies by similarity score and returning the top matches

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit (Python) |
| Backend API | FastAPI (Python) |
| Recommendation Engine | Scikit-learn (TF-IDF + Cosine Similarity) |
| Movie Data | TMDB API |
| Dataset | movies_metadata.csv |
| Backend Hosting | Render (Free Tier) |
| Frontend Hosting | Streamlit Cloud |

---

## 📁 Project Structure

```
movie-reco/
│
├── app.py               # Streamlit frontend (Netflix-style UI)
├── main.py              # FastAPI backend (all API routes)
├── df.pkl               # Preprocessed movie DataFrame
├── indices.pkl          # Title → index mapping for TF-IDF lookup
├── tfidf.pkl            # Fitted TF-IDF vectorizer
├── tfidf_matrix.pkl     # Precomputed TF-IDF sparse matrix
├── requirements.txt     # Python dependencies
└── README.md            # You are here
```

---

## 🚀 Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/Adi-739/movie-reco.git
cd movie-reco
```

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root:

```
TMDB_API_KEY=your_tmdb_api_key_here
```

Get a free API key at [themoviedb.org](https://www.themoviedb.org/settings/api)

### 5. Start the backend

```bash
uvicorn main:app --reload --port 8000
```

### 6. Start the frontend

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/home` | Home feed (trending, popular, etc.) |
| GET | `/tmdb/search` | Search movies by keyword |
| GET | `/movie/id/{tmdb_id}` | Full movie details |
| GET | `/movie/search` | TF-IDF + genre recommendations bundle |
| GET | `/recommend/genre` | Genre-based recommendations |
| GET | `/health` | Health check |

---

## 📦 requirements.txt

```
fastapi
uvicorn
httpx
pandas
numpy
scikit-learn
python-dotenv
pydantic
streamlit
requests
```

---

## 👤 Author

**Aditya Halder**
Final Year B.Tech Student

📧 [halderaditya519@gmail.com](mailto:halderaditya519@gmail.com)
🐙 [github.com/Adi-739](https://github.com/Adi-739)

> Built this entire project — dataset preprocessing, recommendation engine, REST API, and frontend UI — independently as a personal project.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
  Made with ❤️ by Aditya Halder
</div>
