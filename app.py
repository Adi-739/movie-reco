import requests
import streamlit as st
import time

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
API_BASE = "https://movie-rec-466x.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
TMDB_BIG = "https://image.tmdb.org/t/p/original"

st.set_page_config(
    page_title="FLICKR — Stream & Discover",
    page_icon="▶",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CATEGORIES
# ─────────────────────────────────────────────
CATEGORIES = {
    "trending":    "Trending Now",
    "popular":     "Popular",
    "top_rated":   "Top Rated",
    "now_playing": "Now Playing",
    "upcoming":    "Coming Soon",
}

# ─────────────────────────────────────────────
# NETFLIX-STYLE CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #e5e5e5;
    background: #141414;
}

.stApp { background: #141414 !important; }

/* Hide all streamlit chrome */
header[data-testid="stHeader"],
footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu { display: none !important; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

section[data-testid="stSidebar"] { display: none !important; }

/* ── TOP NAVBAR ── */
.nf-nav {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 9999;
    height: 68px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 4%;
    background: linear-gradient(to bottom, rgba(20,20,20,1) 0%, rgba(20,20,20,0) 100%);
    transition: background .3s;
}
.nf-nav.scrolled { background: rgba(20,20,20,.97) !important; }
.nf-logo {
    font-size: 1.9rem;
    font-weight: 700;
    color: #e50914;
    letter-spacing: -.02em;
    text-transform: uppercase;
    font-family: 'Inter', sans-serif;
}
.nf-nav-links {
    display: flex; gap: 1.4rem; align-items: center;
}
.nf-nav-link {
    font-size: .82rem;
    color: #e5e5e5;
    cursor: pointer;
    transition: color .15s;
    letter-spacing: .01em;
}
.nf-nav-link:hover { color: #fff; }
.nf-nav-link.active { color: #fff; font-weight: 600; }
.nf-search-wrap {
    display: flex; align-items: center; gap: 1rem;
}

/* ── HERO BANNER ── */
.nf-hero {
    position: relative;
    width: 100%;
    height: 85vh;
    min-height: 500px;
    overflow: hidden;
    margin-bottom: 0;
}
.nf-hero-bg {
    position: absolute; inset: 0;
    background-size: cover;
    background-position: center top;
    transform: scale(1.04);
    transition: transform 8s ease;
}
.nf-hero-bg:hover { transform: scale(1); }
.nf-hero-vignette {
    position: absolute; inset: 0;
    background: linear-gradient(
        to right,
        rgba(20,20,20,.95) 0%,
        rgba(20,20,20,.6) 40%,
        rgba(20,20,20,.1) 70%,
        rgba(20,20,20,0) 100%
    ),
    linear-gradient(
        to top,
        rgba(20,20,20,1) 0%,
        rgba(20,20,20,.4) 25%,
        rgba(20,20,20,0) 60%
    );
}
.nf-hero-content {
    position: absolute;
    bottom: 20%;
    left: 4%;
    max-width: 480px;
}
.nf-hero-badge {
    display: inline-flex; align-items: center; gap: .4rem;
    font-size: .72rem; font-weight: 700;
    letter-spacing: .18em; text-transform: uppercase;
    color: #e50914; margin-bottom: .8rem;
}
.nf-hero-badge::before {
    content: '';
    display: inline-block;
    width: 2px; height: 14px;
    background: #e50914;
}
.nf-hero-title {
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 700;
    line-height: 1.05;
    color: #fff;
    text-shadow: 2px 2px 8px rgba(0,0,0,.6);
    margin-bottom: .8rem;
    letter-spacing: -.02em;
}
.nf-hero-meta {
    display: flex; align-items: center; gap: .8rem;
    margin-bottom: 1rem; flex-wrap: wrap;
}
.nf-hero-rating {
    color: #46d369; font-size: .82rem; font-weight: 700;
}
.nf-hero-year { color: #aaa; font-size: .82rem; }
.nf-hero-desc {
    font-size: .9rem; line-height: 1.6;
    color: #ccc; margin-bottom: 1.4rem;
    display: -webkit-box; -webkit-line-clamp: 3;
    -webkit-box-orient: vertical; overflow: hidden;
}
.nf-hero-btns { display: flex; gap: .75rem; }
.nf-btn-play {
    display: inline-flex; align-items: center; gap: .5rem;
    background: #fff; color: #000;
    padding: .55rem 1.6rem;
    border-radius: 4px;
    font-size: .95rem; font-weight: 700;
    cursor: pointer; border: none;
    transition: background .15s;
    text-decoration: none;
}
.nf-btn-play:hover { background: rgba(255,255,255,.85); }
.nf-btn-info {
    display: inline-flex; align-items: center; gap: .5rem;
    background: rgba(109,109,110,.7); color: #fff;
    padding: .55rem 1.6rem;
    border-radius: 4px;
    font-size: .95rem; font-weight: 600;
    cursor: pointer; border: none;
    transition: background .15s;
}
.nf-btn-info:hover { background: rgba(109,109,110,.5); }

/* ═══════════════════════════════════════
   TAB BAR — single unified implementation
   Functional st.buttons styled as tabs.
   The HTML .nf-tabs div is removed entirely.
═══════════════════════════════════════ */

/* Wrapper: make the st.columns row look like a sticky tab bar */
div[data-testid="stHorizontalBlock"].tab-row {
    background: #141414 !important;
    border-bottom: 1px solid #222 !important;
    padding: 0 4% !important;
    position: sticky !important;
    top: 68px !important;
    z-index: 100 !important;
    margin: 0 !important;
    gap: 0 !important;
    overflow-x: auto !important;
    scrollbar-width: none !important;
}
div[data-testid="stHorizontalBlock"].tab-row::-webkit-scrollbar { display: none !important; }

/* Individual tab buttons */
div[data-testid="stHorizontalBlock"].tab-row .stButton > button {
    background: transparent !important;
    border: none !important;
    border-bottom: 2.5px solid transparent !important;
    border-radius: 0 !important;
    color: #aaa !important;
    font-size: .82rem !important;
    font-weight: 500 !important;
    padding: .7rem .6rem !important;
    line-height: 1 !important;
    transition: color .2s, border-color .2s !important;
    font-family: 'Inter', sans-serif !important;
    white-space: nowrap !important;
    width: 100% !important;
    box-shadow: none !important;
    letter-spacing: .01em !important;
}
div[data-testid="stHorizontalBlock"].tab-row .stButton > button:hover {
    color: #fff !important;
    background: transparent !important;
    border-bottom-color: #666 !important;
    box-shadow: none !important;
}
div[data-testid="stHorizontalBlock"].tab-row .stButton > button:focus {
    box-shadow: none !important;
    outline: none !important;
}

/* ── SEARCH BAR ── */
.nf-search-container {
    padding: 1.5rem 4% .5rem;
    background: #141414;
}
.stTextInput > div > div > input {
    background: #2a2a2a !important;
    border: 1px solid #333 !important;
    border-radius: 4px !important;
    color: #fff !important;
    font-size: .95rem !important;
    padding: .7rem 1.2rem .7rem 2.8rem !important;
    font-family: 'Inter', sans-serif !important;
    caret-color: #e50914;
    width: 100% !important;
}
.stTextInput > div > div > input:focus {
    border-color: #e50914 !important;
    box-shadow: 0 0 0 1px #e5091433 !important;
    background: #1a1a1a !important;
}
.stTextInput > div > div::before {
    content: '🔍';
    position: absolute;
    left: .9rem; top: 50%;
    transform: translateY(-50%);
    font-size: .85rem;
    z-index: 1;
    pointer-events: none;
}
.stTextInput > div { position: relative; }
.stTextInput > label { display: none !important; }

/* ── SECTION HEADER ── */
.nf-section-header {
    display: flex; align-items: baseline;
    gap: .8rem; padding: 2rem 4% .8rem;
}
.nf-section-title {
    font-size: 1.1rem; font-weight: 600;
    color: #e5e5e5; letter-spacing: .01em;
}
.nf-section-explore {
    font-size: .78rem; color: #54b9c5;
    font-weight: 500; cursor: pointer;
    opacity: 0; transition: opacity .3s;
    display: flex; align-items: center; gap: .3rem;
}
.nf-section-header:hover .nf-section-explore { opacity: 1; }

/* ── MOVIE CARD ── */
.nf-card {
    position: relative;
    border-radius: 4px;
    overflow: hidden;
    cursor: pointer;
    background: #1a1a1a;
    transition: transform .3s cubic-bezier(.25,.46,.45,.94);
    aspect-ratio: 2/3;
}
.nf-card:hover {
    transform: scale(1.08);
    z-index: 10;
    box-shadow: 0 14px 50px rgba(0,0,0,.8);
}
.nf-card img {
    width: 100%; height: 100%;
    object-fit: cover; display: block;
}

/* ── DETAIL PAGE ── */
.nf-detail-hero {
    position: relative;
    width: 100%;
    height: 70vh;
    min-height: 400px;
    overflow: hidden;
}
.nf-detail-hero-bg {
    position: absolute; inset: 0;
    background-size: cover;
    background-position: center 20%;
    filter: brightness(.55);
}
.nf-detail-hero-vignette {
    position: absolute; inset: 0;
    background: linear-gradient(
        to top,
        #141414 0%,
        rgba(20,20,20,.5) 40%,
        rgba(20,20,20,.1) 100%
    );
}
.nf-detail-poster {
    flex-shrink: 0;
    width: 220px;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,.7);
    border: 1px solid rgba(255,255,255,.08);
}
.nf-detail-poster img { width: 100%; display: block; }
.nf-detail-title {
    font-size: clamp(1.8rem, 3vw, 2.8rem);
    font-weight: 700; color: #fff;
    line-height: 1.1; margin-bottom: .7rem;
    letter-spacing: -.02em;
}
.nf-detail-stats {
    display: flex; gap: 1rem;
    align-items: center; flex-wrap: wrap;
    margin-bottom: 1rem;
}
.nf-match { color: #46d369; font-weight: 700; font-size: .9rem; }
.nf-detail-year { color: #aaa; font-size: .85rem; }
.nf-detail-runtime { color: #aaa; font-size: .85rem; }
.nf-detail-lang {
    border: 1px solid #aaa; color: #aaa;
    font-size: .7rem; padding: .1rem .35rem;
    border-radius: 2px; font-weight: 600;
}
.nf-detail-genres {
    display: flex; gap: .4rem; flex-wrap: wrap; margin-bottom: 1rem;
}
.nf-genre-pill {
    background: rgba(255,255,255,.1);
    color: #ccc; font-size: .72rem;
    padding: .25rem .7rem; border-radius: 20px;
    border: 1px solid rgba(255,255,255,.15);
}
.nf-detail-overview {
    font-size: .9rem; line-height: 1.7;
    color: #ccc; max-width: 600px;
    margin-bottom: 1.5rem;
}

/* ── GENERAL BUTTONS (non-tab) ── */
.stButton > button {
    background: rgba(109,109,110,.5) !important;
    border: none !important;
    color: #fff !important;
    font-size: .82rem !important;
    font-weight: 600 !important;
    border-radius: 4px !important;
    padding: .5rem 1.2rem !important;
    transition: background .2s !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    background: rgba(109,109,110,.8) !important;
}

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    background: #2a2a2a !important;
    border: 1px solid #333 !important;
    border-radius: 4px !important;
    color: #fff !important;
}
.stSelectbox > label { display: none !important; }

/* ── MISC ── */
hr {
    border: none !important;
    border-top: 1px solid #222 !important;
    margin: 1rem 0 !important;
}
.nf-wakeup {
    margin: 1rem 4%;
    background: linear-gradient(135deg, #1a0a0a, #2a1010);
    border: 1px solid #e5091433;
    border-radius: 6px;
    padding: 1.2rem 1.5rem;
    display: flex; align-items: center; gap: 1rem;
}
.nf-wakeup-text { color: #ff6b6b; font-size: .88rem; font-weight: 500; }
.nf-wakeup-sub  { color: #666; font-size: .75rem; margin-top: .2rem; }
.main .block-container { overflow-x: hidden; }
section.main > div { padding-top: 68px; }
.nf-results-label {
    padding: .5rem 4% 0;
    font-size: .78rem; color: #666;
    letter-spacing: .08em; text-transform: uppercase;
}

/* ══════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════ */
@media (max-width: 900px) {
    .block-container { padding: 0 !important; }
    .nf-nav { padding: 0 3%; height: 56px; }
    .nf-nav-links { display: none; }
    .nf-logo { font-size: 1.4rem; }
    .nf-hero { height: 55vh; min-height: 320px; }
    .nf-hero-content { bottom: 12%; max-width: 90%; }
    .nf-hero-title { font-size: 1.6rem; }
    .nf-hero-desc { display: none; }
    div[data-testid="stHorizontalBlock"].tab-row { top: 56px !important; padding: 0 3% !important; }
    .nf-section-header { padding: 1.5rem 3% .6rem; }
    .nf-section-title { font-size: .95rem; }
    section.main > div { padding-top: 56px; }
    .nf-detail-poster { width: 140px; }
    .nf-detail-title { font-size: 1.5rem; }
    .nf-detail-hero { height: 45vh; }
    .nf-search-container { padding: 1rem 3% .5rem; }
}

@media (max-width: 600px) {
    .nf-nav { padding: 0 4%; height: 52px; }
    .nf-logo { font-size: 1.25rem; }
    .nf-hero { height: 50vh; min-height: 280px; }
    .nf-hero-content { bottom: 10%; left: 4%; max-width: 95%; }
    .nf-hero-title { font-size: 1.3rem; }
    .nf-hero-badge { font-size: .65rem; }
    .nf-hero-btns { gap: .5rem; }
    .nf-btn-play, .nf-btn-info { padding: .45rem 1rem; font-size: .82rem; }
    div[data-testid="stHorizontalBlock"].tab-row { top: 52px !important; }
    div[data-testid="stHorizontalBlock"].tab-row .stButton > button {
        font-size: .7rem !important;
        padding: .6rem .3rem !important;
    }
    section.main > div { padding-top: 52px; }
    .nf-detail-hero { height: 38vh; min-height: 220px; }
    .nf-detail-poster { width: 110px; }
    .nf-detail-title { font-size: 1.2rem; }
    .nf-detail-overview { font-size: .82rem; }
    .stButton > button {
        padding: .6rem .8rem !important;
        font-size: .75rem !important;
        min-height: 40px !important;
    }
    .nf-search-container { padding: .8rem 4% .4rem; }
    .stTextInput > div > div > input { font-size: .9rem !important; }
}

@media (max-width: 380px) {
    .nf-hero-title { font-size: 1.1rem; }
    .nf-logo { font-size: 1.1rem; }
    .nf-detail-title { font-size: 1rem; }
    .nf-hero { height: 45vh; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE + ROUTING
# ─────────────────────────────────────────────
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None
if "category" not in st.session_state:
    st.session_state.category = "trending"
if "hero_idx" not in st.session_state:
    st.session_state.hero_idx = 0

qp_view = st.query_params.get("view")
qp_id   = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except Exception:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    st.query_params.pop("id", None)
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# ─────────────────────────────────────────────
# API HELPERS
# ─────────────────────────────────────────────
@st.cache_data(ttl=60)
def api_get(path: str, params: dict | None = None):
    for attempt in range(3):
        try:
            r = requests.get(f"{API_BASE}{path}", params=params, timeout=60)
            if r.status_code >= 400:
                return None, f"HTTP {r.status_code}"
            return r.json(), None
        except requests.exceptions.Timeout:
            if attempt == 2:
                return None, "__timeout__"
            time.sleep(5)
        except Exception as e:
            return None, str(e)
    return None, "__timeout__"


def valid_url(url):
    return isinstance(url, str) and url.startswith("http") and len(url) > 10


def show_timeout_banner():
    st.markdown("""
    <div class='nf-wakeup'>
        <span style='font-size:1.6rem'>⏳</span>
        <div>
            <div class='nf-wakeup-text'>Server is waking up — please wait 30–60 seconds.</div>
            <div class='nf-wakeup-sub'>Render free tier spins down after inactivity.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns([1, 8])
    with col1:
        if st.button("↺  Retry"):
            st.cache_data.clear()
            st.rerun()


def handle_error(err, context=""):
    if err == "__timeout__":
        show_timeout_banner()
    elif err:
        st.error(f"{context}: {err}" if context else str(err))


def parse_search(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()
    raw_items = []
    if isinstance(data, dict) and "results" in data:
        for m in data.get("results") or []:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
                "vote_average": m.get("vote_average"),
            })
    elif isinstance(data, list):
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title   = (m.get("title") or "").strip()
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": m.get("poster_url"),
                "release_date": m.get("release_date", ""),
                "vote_average": m.get("vote_average"),
            })
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final   = matched if matched else raw_items
    suggestions = []
    for x in final[:10]:
        year  = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))
    return suggestions, final[:limit]


def tfidf_to_cards(items):
    cards = []
    for x in items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({
                "tmdb_id":      tmdb["tmdb_id"],
                "title":        tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url":   tmdb.get("poster_url"),
                "release_date": tmdb.get("release_date", ""),
                "vote_average": tmdb.get("vote_average"),
            })
    return cards


# ─────────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────────
st.markdown("""
<div class='nf-nav' id='nf-nav'>
    <div style='display:flex;align-items:center;gap:2.5rem'>
        <div class='nf-logo'>FLICKR</div>
        <div class='nf-nav-links'>
            <span class='nf-nav-link active'>Home</span>
            <span class='nf-nav-link'>Movies</span>
            <span class='nf-nav-link'>My List</span>
        </div>
    </div>
    <div class='nf-search-wrap'>
        <span style='color:#aaa;font-size:.8rem;cursor:pointer'>🔍 Search</span>
        <span style='color:#aaa;font-size:.8rem'>👤</span>
    </div>
</div>
<script>
window.addEventListener('scroll', function() {
    var nav = document.getElementById('nf-nav');
    if (nav) nav.className = window.scrollY > 50 ? 'nf-nav scrolled' : 'nf-nav';
});
</script>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# POSTER CARD GRID
# ─────────────────────────────────────────────
def poster_grid(cards, cols=6, key_prefix="g", section_title=None):
    if not cards:
        return

    if section_title:
        st.markdown(
            f"<div class='nf-section-header'>"
            f"<span class='nf-section-title'>{section_title}</span>"
            f"<span class='nf-section-explore'>Explore All ›</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    rows = (len(cards) + cols - 1) // cols
    idx  = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]; idx += 1
            _id     = m.get("tmdb_id")
            _title  = m.get("title", "Unknown")
            _poster = m.get("poster_url")
            _year   = (m.get("release_date") or "")[:4]
            _rating = m.get("vote_average")

            with colset[c]:
                if valid_url(_poster):
                    st.markdown(
                        f"<div class='nf-card'>"
                        f"<img src='{_poster}' loading='lazy' "
                        f"style='width:100%;display:block;aspect-ratio:2/3;object-fit:cover;border-radius:4px'>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<div style='aspect-ratio:2/3;background:#1a1a1a;border-radius:4px;"
                        "display:flex;align-items:center;justify-content:center;"
                        "font-size:2rem;color:#333'>🎬</div>",
                        unsafe_allow_html=True,
                    )

                rating_str = f"★{_rating:.1f}  " if _rating else ""
                st.markdown(
                    f"<div style='font-size:.72rem;font-weight:600;color:#e5e5e5;"
                    f"overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"
                    f"margin:.35rem 0 .1rem;font-family:Inter,sans-serif'>{_title}</div>"
                    f"<div style='font-size:.63rem;color:#46d369;font-family:Inter,sans-serif'>"
                    f"{rating_str}<span style='color:#888'>{_year}</span></div>",
                    unsafe_allow_html=True,
                )

                if _id:
                    if st.button("▶ Open", key=f"{key_prefix}_{r}_{c}_{idx}",
                                  use_container_width=True):
                        goto_details(_id)


# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────
def render_hero(cards):
    if not cards:
        return
    hero    = cards[min(st.session_state.hero_idx, len(cards)-1)]
    title   = hero.get("title", "")
    poster  = hero.get("poster_url", "")
    year    = (hero.get("release_date") or "")[:4]
    rating  = hero.get("vote_average")
    tmdb_id = hero.get("tmdb_id")
    bg_url  = poster if valid_url(poster) else ""

    rating_html = f'<span class="nf-hero-rating">● {rating:.0f}% Match</span>' if rating else ""
    year_html   = f'<span class="nf-hero-year">{year}</span>' if year else ""

    st.markdown(f"""
    <div class='nf-hero'>
        <div class='nf-hero-bg' style='background-image:url("{bg_url}");'></div>
        <div class='nf-hero-vignette'></div>
        <div class='nf-hero-content'>
            <div class='nf-hero-badge'>Featured Film</div>
            <div class='nf-hero-title'>{title}</div>
            <div class='nf-hero-meta'>
                {rating_html}
                {year_html}
            </div>
            <div class='nf-hero-btns'>
                <span class='nf-btn-play'>▶ &nbsp;Play</span>
                <span class='nf-btn-info'>ℹ More Info</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if tmdb_id:
        col1, col2, *_ = st.columns([1, 1, 8])
        with col2:
            if st.button("ℹ  More Info", key="hero_btn"):
                goto_details(tmdb_id)


# ═════════════════════════════════════════════
# RENDER ACTIVE TAB HIGHLIGHT
# Injects a small <style> block that colours
# whichever button matches the active category.
# ═════════════════════════════════════════════
def render_tab_active_style():
    cat_keys = list(CATEGORIES.keys())
    active   = st.session_state.category
    try:
        # nth-of-type is 1-indexed; buttons inside .tab-row columns
        idx = cat_keys.index(active) + 1
    except ValueError:
        idx = 1
    st.markdown(f"""
    <style>
    div[data-testid="stHorizontalBlock"].tab-row
        > div:nth-child({idx})
        .stButton > button {{
        color: #fff !important;
        border-bottom-color: #e50914 !important;
        font-weight: 600 !important;
    }}
    </style>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
# VIEW: HOME
# ═════════════════════════════════════════════
if st.session_state.view == "home":

    # ── Inject wrapper class onto the next st.columns block ──
    # Streamlit doesn't let us add classes to stHorizontalBlock directly,
    # so we use a JS snippet that runs immediately and tags the NEXT sibling.
    st.markdown("""
    <script>
    (function() {
        function tagTabRow() {
            var blocks = document.querySelectorAll('[data-testid="stHorizontalBlock"]');
            blocks.forEach(function(b) {
                var btns = b.querySelectorAll('button');
                if (btns.length === 5) {
                    b.classList.add('tab-row');
                }
            });
        }
        tagTabRow();
        setTimeout(tagTabRow, 300);
        setTimeout(tagTabRow, 800);
    })();
    </script>
    """, unsafe_allow_html=True)

    # ── Active tab highlight ──
    render_tab_active_style()

    # ── Tab buttons (single source of truth) ──
    tab_cols = st.columns(len(CATEGORIES))
    for i, (key, label) in enumerate(CATEGORIES.items()):
        with tab_cols[i]:
            if st.button(label, key=f"tab_{key}", use_container_width=True):
                st.session_state.category = key
                st.rerun()

    # ── Search ──
    st.markdown("<div class='nf-search-container'>", unsafe_allow_html=True)
    typed = st.text_input("Search", placeholder="🔍  Search movies — Inception, Dune, Parasite…",
                           label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            data, err = api_get("/tmdb/search", {"query": typed.strip()})
            if err or data is None:
                handle_error(err, "Search error")
            else:
                suggestions, cards = parse_search(data, typed.strip(), limit=24)

                if suggestions:
                    labels   = ["— Select a title —"] + [s[0] for s in suggestions]
                    selected = st.selectbox("", labels, index=0)
                    if selected != "— Select a title —":
                        lid = {s[0]: s[1] for s in suggestions}
                        goto_details(lid[selected])

                if cards:
                    poster_grid(cards, cols=6, key_prefix="search",
                                section_title=f"Search Results — {len(cards)} films")
        st.stop()

    # ── Load home feed ──
    home_cards, err = api_get("/home", {"category": st.session_state.category, "limit": 24})
    if err or not home_cards:
        handle_error(err, "Feed unavailable")
        st.stop()

    # ── Hero ──
    render_hero(home_cards)

    # ── Grid ──
    cat_label = CATEGORIES.get(st.session_state.category, "Movies")
    poster_grid(home_cards, cols=6, key_prefix="home", section_title=cat_label)


# ═════════════════════════════════════════════
# VIEW: DETAILS
# ═════════════════════════════════════════════
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No film selected.")
        if st.button("← Home"):
            goto_home()
        st.stop()

    data, err = api_get(f"/movie/id/{tmdb_id}")
    if err or not data:
        handle_error(err, "Could not load film")
        st.stop()

    title    = data.get("title", "Untitled")
    overview = data.get("overview") or "No overview available."
    release  = data.get("release_date") or ""
    year     = release[:4]
    rating   = data.get("vote_average")
    runtime  = data.get("runtime")
    lang     = (data.get("original_language") or "").upper()
    genres   = data.get("genres", [])
    backdrop = data.get("backdrop_url")
    poster   = data.get("poster_url")

    bg_url = backdrop if valid_url(backdrop) else (poster if valid_url(poster) else "")

    st.markdown(f"""
    <div class='nf-detail-hero'>
        <div class='nf-detail-hero-bg' style='background-image:url("{bg_url}")'></div>
        <div class='nf-detail-hero-vignette'></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Back to Home", key="back_btn"):
        goto_home()

    left, right = st.columns([1, 3], gap="large")

    with left:
        if valid_url(poster):
            st.markdown(f"""
            <div class='nf-detail-poster'>
                <img src='{poster}' alt='{title}'>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='nf-detail-poster' style='aspect-ratio:2/3;background:#1a1a1a;
            display:flex;align-items:center;justify-content:center;font-size:3rem'>🎬</div>
            """, unsafe_allow_html=True)

    with right:
        match_html   = f'<span class="nf-match">{rating*10:.0f}% Match</span>' if rating else ""
        year_html    = f'<span class="nf-detail-year">{year}</span>' if year else ""
        runtime_html = f'<span class="nf-detail-runtime">{runtime}m</span>' if runtime else ""
        lang_html    = f'<span class="nf-detail-lang">{lang}</span>' if lang else ""

        genre_pills = "".join(
            f"<span class='nf-genre-pill'>{g['name']}</span>" for g in genres
        )

        st.markdown(f"""
        <div style='padding-top:1rem'>
            <div class='nf-detail-title'>{title}</div>
            <div class='nf-detail-stats'>
                {match_html}{year_html}{runtime_html}{lang_html}
            </div>
            <div class='nf-detail-genres'>{genre_pills}</div>
            <div class='nf-detail-overview'>{overview}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Recommendations ──
    title_str = title.strip()
    if title_str:
        bundle, err2 = api_get("/movie/search",
                               {"query": title_str, "tfidf_top_n": 12, "genre_limit": 12})

        if not err2 and bundle:
            tfidf_cards = tfidf_to_cards(bundle.get("tfidf_recommendations"))
            genre_cards = bundle.get("genre_recommendations", [])

            if tfidf_cards:
                poster_grid(tfidf_cards, cols=6, key_prefix="tfidf",
                            section_title="Because You Watched · Similar Films")
            if genre_cards:
                poster_grid(genre_cards, cols=6, key_prefix="genre",
                            section_title="More Like This · By Genre")
        else:
            if err2 == "__timeout__":
                show_timeout_banner()
            else:
                genre_only, err3 = api_get("/recommend/genre",
                                           {"tmdb_id": tmdb_id, "limit": 18})
                if not err3 and genre_only:
                    poster_grid(genre_only, cols=6, key_prefix="gf",
                                section_title="More Like This")
                else:
                    handle_error(err3)


# ═══════════════════════════════════════
# ABOUT SECTION
# ═══════════════════════════════════════
st.markdown("---")
st.markdown(
    "<div style='text-align:center;padding:2rem 0 .5rem;font-size:2rem'>🎬</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div style='text-align:center;font-size:1.3rem;font-weight:700;color:#fff;font-family:Inter,sans-serif'>About This Project</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div style='text-align:center;margin:.5rem auto 1.2rem;width:40px;height:2px;background:#e50914;border-radius:2px'></div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div style='text-align:center;max-width:650px;margin:0 auto 1.5rem;font-size:.9rem;line-height:1.8;color:#aaa;font-family:Inter,sans-serif'>"
    "This movie recommendation system was entirely built by me — from the backend API to this frontend UI. "
    "It uses <b style='color:#e5e5e5'>Cosine Similarity</b> on TF-IDF vectors to find films with similar content, "
    "combined with <b style='color:#e5e5e5'>genre-based discovery</b> via the TMDB API. "
    "The backend runs on FastAPI deployed on Render, and the frontend is built with Streamlit."
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div style='text-align:center;margin-bottom:1rem'>"
    "<span style='background:rgba(229,9,20,.1);border:1px solid rgba(229,9,20,.25);"
    "border-radius:6px;padding:.45rem 1rem;font-size:.8rem;color:#ccc;font-family:Inter,sans-serif'>"
    "🎓 Final Year B.Tech Student"
    "</span></div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div style='text-align:center;font-size:1rem;font-weight:700;color:#fff;font-family:Inter,sans-serif;margin-bottom:.3rem'>Aditya Halder</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div style='text-align:center;margin-bottom:.6rem'>"
    "<a href='mailto:halderaditya519@gmail.com' "
    "style='color:#e50914;font-size:.85rem;font-family:Inter,sans-serif;text-decoration:none'>"
    "✉ halderaditya519@gmail.com</a></div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div style='text-align:center;font-size:.72rem;color:#444;font-family:Inter,sans-serif;padding-bottom:2rem'>"
    "Have a question or feedback? Feel free to reach out via email."
    "</div>",
    unsafe_allow_html=True,
)
