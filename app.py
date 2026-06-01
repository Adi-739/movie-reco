import requests
import streamlit as st
import time

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
API_BASE   = "https://movie-rec-466x.onrender.com"
TMDB_IMG   = "https://image.tmdb.org/t/p/w500"
TMDB_BIG   = "https://image.tmdb.org/t/p/original"

st.set_page_config(
    page_title="CINÉ — Movie Recommender",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL STYLES  — cinematic dark editorial
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e0d5;
}
.stApp { background: #0d0c0b; }
header[data-testid="stHeader"], footer { display: none !important; }

[data-testid="stSidebar"] {
    background: #131210 !important;
    border-right: 1px solid #2a2520;
}
[data-testid="stSidebar"] .block-container { padding-top: 2rem; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    color: #8a7f74 !important;
    font-size: 0.72rem !important;
    letter-spacing: .12em;
    text-transform: uppercase;
}

.block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1600px !important;
}

.cine-wordmark {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem; font-weight: 700;
    letter-spacing: .04em; color: #f0e8d8;
    line-height: 1; margin-bottom: .15rem;
}
.cine-sub {
    font-size: .78rem; letter-spacing: .22em;
    text-transform: uppercase; color: #6b5e4e; margin-bottom: 1.6rem;
}

.stTextInput > div > div > input {
    background: #1a1714 !important;
    border: 1px solid #2e2820 !important;
    border-radius: 4px !important;
    color: #e8e0d5 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: .6rem 1rem !important;
    caret-color: #c9a96e;
}
.stTextInput > div > div > input:focus {
    border-color: #c9a96e !important;
    box-shadow: 0 0 0 2px rgba(201,169,110,.12) !important;
}
.stTextInput > label {
    color: #8a7f74 !important;
    font-size: .72rem !important;
    letter-spacing: .14em;
    text-transform: uppercase;
}

.stSelectbox > div > div {
    background: #1a1714 !important;
    border: 1px solid #2e2820 !important;
    border-radius: 4px !important;
    color: #e8e0d5 !important;
}

hr {
    border: none !important;
    border-top: 1px solid #1e1c19 !important;
    margin: 1.6rem 0 !important;
}

.section-label {
    font-size: .7rem; letter-spacing: .2em;
    text-transform: uppercase; color: #6b5e4e;
    margin-bottom: 1rem; padding-bottom: .5rem;
    border-bottom: 1px solid #1e1c19;
}

.detail-meta-row { display: flex; gap: 1.4rem; flex-wrap: wrap; margin-bottom: .8rem; }
.detail-meta-item { font-size: .72rem; letter-spacing: .1em; text-transform: uppercase; color: #6b5e4e; }
.detail-meta-val { color: #c9a96e; }
.detail-overview {
    font-size: .97rem; line-height: 1.75;
    color: #b0a090; max-width: 64ch;
    font-style: italic;
    font-family: 'Playfair Display', serif;
}
.detail-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem; line-height: 1.1;
    color: #f0e8d8; margin-bottom: .6rem;
}

.stButton > button {
    background: transparent !important;
    border: 1px solid #2e2820 !important;
    color: #8a7f74 !important;
    font-size: .72rem !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
    padding: .38rem 1rem !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    border-color: #c9a96e !important;
    color: #c9a96e !important;
    background: rgba(201,169,110,.06) !important;
}

.backdrop-img {
    width: 100%; border-radius: 4px;
    mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 60%, transparent 100%);
    -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 60%, transparent 100%);
    margin-bottom: 1rem;
}

.rating-badge {
    display: inline-block;
    background: #c9a96e; color: #0d0c0b;
    font-size: .7rem; font-weight: 700;
    letter-spacing: .08em;
    padding: .22rem .6rem; border-radius: 2px;
    margin-left: .5rem; vertical-align: middle;
}

.stAlert { border-radius: 3px !important; }

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left !important;
    justify-content: flex-start !important;
}

.main .block-container { overflow-x: hidden; }

.genre-tag {
    display: inline-block;
    border: 1px solid #2e2820;
    padding: .18rem .55rem; border-radius: 2px;
    font-size: .65rem; letter-spacing: .08em;
    text-transform: uppercase; color: #6b5e4e;
    margin: .1rem .15rem .1rem 0;
}

/* ── Wake-up banner ── */
.wakeup-banner {
    background: linear-gradient(135deg, #1a1510, #221a10);
    border: 1px solid #c9a96e33;
    border-radius: 6px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
    display: flex; align-items: center; gap: 1rem;
}
.wakeup-text { color: #c9a96e; font-size: .85rem; letter-spacing: .04em; }
.wakeup-sub  { color: #6b5e4e; font-size: .75rem; margin-top: .2rem; }
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
# API HELPERS  — with retry + wake-up handling
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


def show_timeout_banner():
    st.markdown("""
    <div class='wakeup-banner'>
        <span style='font-size:1.8rem'>🎞️</span>
        <div>
            <div class='wakeup-text'>Server is waking up — this takes about 30–60 seconds on first load.</div>
            <div class='wakeup-sub'>Please refresh the page in a moment.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔄  Refresh Now"):
        st.cache_data.clear()
        st.rerun()


def handle_error(err: str | None, context: str = ""):
    if err == "__timeout__":
        show_timeout_banner()
    else:
        st.error(f"{context}: {err}" if context else err)


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
            })

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final   = matched if matched else raw_items

    suggestions = []
    for x in final[:10]:
        year  = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = final[:limit]
    return suggestions, cards


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
            })
    return cards


# ─────────────────────────────────────────────
# POSTER GRID
# ─────────────────────────────────────────────
def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("Nothing to display here.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx  = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]; idx += 1
            _tmdb_id = m.get("tmdb_id")
            _title   = m.get("title", "Untitled")
            _poster  = m.get("poster_url")
            _year    = (m.get("release_date") or "")[:4]

            with colset[c]:
                if _poster:
                    st.image(_poster, use_container_width=True)
                else:
                    st.markdown(
                        "<div style='aspect-ratio:2/3;background:#1a1714;"
                        "border-radius:3px;display:flex;align-items:center;"
                        "justify-content:center;font-size:2rem;color:#2a2520'>"
                        "🎞️</div>",
                        unsafe_allow_html=True,
                    )

                _yr_html = f"<span style='color:#c9a96e;font-size:.63rem'>{_year}</span>" if _year else ""
                st.markdown(
                    f"<div style='margin:.3rem 0 .4rem;font-size:.73rem;"
                    f"color:#c8bfb0;line-height:1.25;overflow:hidden;"
                    f"text-overflow:ellipsis;white-space:nowrap'>"
                    f"{_title}</div>{_yr_html}",
                    unsafe_allow_html=True,
                )

                if _tmdb_id:
                    if st.button("View", key=f"{key_prefix}_{r}_{c}_{idx}"):
                        goto_details(_tmdb_id)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
CATEGORIES = {
    "trending":    "🔥 Trending",
    "popular":     "📈 Popular",
    "top_rated":   "⭐ Top Rated",
    "now_playing": "🎭 Now Playing",
    "upcoming":    "🗓 Upcoming",
}

with st.sidebar:
    st.markdown("""
    <div style='font-family:"Playfair Display",serif;font-size:1.5rem;
    color:#f0e8d8;letter-spacing:.04em;margin-bottom:.2rem'>CINÉ</div>
    <div style='font-size:.65rem;letter-spacing:.22em;text-transform:uppercase;
    color:#4a4035;margin-bottom:2rem'>Movie Recommender</div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Navigate</div>", unsafe_allow_html=True)
    if st.button("🏠  Home"):
        goto_home()

    st.divider()

    st.markdown("<div class='section-label'>Browse</div>", unsafe_allow_html=True)
    for key, label in CATEGORIES.items():
        if st.button(label, key=f"cat_{key}"):
            st.session_state.category = key
            st.session_state.view = "home"
            st.rerun()

    st.divider()

    st.markdown("<div class='section-label'>Display</div>", unsafe_allow_html=True)
    grid_cols = st.slider("Columns", 3, 8, 6, label_visibility="visible")


# ─────────────────────────────────────────────
# WORDMARK
# ─────────────────────────────────────────────
st.markdown("""
<div class='cine-wordmark'>CINÉ</div>
<div class='cine-sub'>Discover · Explore · Recommend</div>
""", unsafe_allow_html=True)

st.divider()

# ═════════════════════════════════════════════
# VIEW: HOME
# ═════════════════════════════════════════════
if st.session_state.view == "home":

    typed = st.text_input(
        "Search",
        placeholder="Enter a title — Inception, Parasite, Dune…",
        label_visibility="collapsed",
    )

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
                    labels   = ["— select a title —"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0,
                                            label_visibility="collapsed")
                    if selected != "— select a title —":
                        lid = {s[0]: s[1] for s in suggestions}
                        goto_details(lid[selected])
                else:
                    st.info("No suggestions found.")

                if cards:
                    st.markdown(
                        f"<div class='section-label'>Results — {len(cards)} films</div>",
                        unsafe_allow_html=True,
                    )
                    poster_grid(cards, cols=grid_cols, key_prefix="search")

        st.stop()

    # ── HOME FEED ──
    cat_label = CATEGORIES.get(st.session_state.category, st.session_state.category)
    st.markdown(f"<div class='section-label'>{cat_label}</div>", unsafe_allow_html=True)

    home_cards, err = api_get(
        "/home",
        {"category": st.session_state.category, "limit": 24},
    )
    if err or not home_cards:
        handle_error(err, "Feed unavailable")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home")


# ═════════════════════════════════════════════
# VIEW: DETAILS
# ═════════════════════════════════════════════
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No film selected.")
        st.button("← Return", on_click=goto_home)
        st.stop()

    col_back, _ = st.columns([1, 8])
    with col_back:
        if st.button("← Back"):
            goto_home()

    data, err = api_get(f"/movie/id/{tmdb_id}")
    if err or not data:
        handle_error(err, "Could not load details")
        st.stop()

    if data.get("backdrop_url"):
        st.markdown(
            f"<img src='{data['backdrop_url']}' class='backdrop-img'>",
            unsafe_allow_html=True,
        )

    left, right = st.columns([1, 2.8], gap="large")

    with left:
        if data.get("poster_url"):
            st.image(data["poster_url"], use_container_width=True)
        else:
            st.markdown(
                "<div style='aspect-ratio:2/3;background:#1a1714;border-radius:4px;"
                "display:flex;align-items:center;justify-content:center;"
                "font-size:3rem;color:#2a2520'>🎞️</div>",
                unsafe_allow_html=True,
            )

    with right:
        title   = data.get("title", "Untitled")
        release = (data.get("release_date") or "")
        year    = release[:4]
        rating  = data.get("vote_average")
        genres  = data.get("genres", [])

        rating_html = (
            f"<span class='rating-badge'>★ {rating:.1f}</span>" if rating else ""
        )
        st.markdown(
            f"<div class='detail-title'>{title}{rating_html}</div>",
            unsafe_allow_html=True,
        )

        meta_parts = []
        if year:
            meta_parts.append(
                f"<span class='detail-meta-item'>Year "
                f"<span class='detail-meta-val'>{year}</span></span>"
            )
        if data.get("runtime"):
            meta_parts.append(
                f"<span class='detail-meta-item'>Runtime "
                f"<span class='detail-meta-val'>{data['runtime']} min</span></span>"
            )
        if data.get("original_language"):
            meta_parts.append(
                f"<span class='detail-meta-item'>Language "
                f"<span class='detail-meta-val'>{data['original_language'].upper()}</span></span>"
            )
        if meta_parts:
            st.markdown(
                f"<div class='detail-meta-row'>{''.join(meta_parts)}</div>",
                unsafe_allow_html=True,
            )

        if genres:
            tags = "".join(
                f"<span class='genre-tag'>{g['name']}</span>" for g in genres
            )
            st.markdown(f"<div style='margin-bottom:.8rem'>{tags}</div>", unsafe_allow_html=True)

        overview = data.get("overview") or "No overview available."
        st.markdown(f"<div class='detail-overview'>{overview}</div>", unsafe_allow_html=True)

    st.divider()

    title_str = (data.get("title") or "").strip()
    if title_str:
        bundle, err2 = api_get(
            "/movie/search",
            {"query": title_str, "tfidf_top_n": 12, "genre_limit": 12},
        )

        if not err2 and bundle:
            tfidf_cards = tfidf_to_cards(bundle.get("tfidf_recommendations"))
            genre_cards = bundle.get("genre_recommendations", [])

            if tfidf_cards:
                st.markdown(
                    "<div class='section-label'>Similar Films — By Content</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(tfidf_cards, cols=grid_cols, key_prefix="tfidf")

            if genre_cards:
                st.markdown(
                    "<div class='section-label'>Similar Films — By Genre</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(genre_cards, cols=grid_cols, key_prefix="genre")
        else:
            if err2 == "__timeout__":
                show_timeout_banner()
            else:
                genre_only, err3 = api_get(
                    "/recommend/genre", {"tmdb_id": tmdb_id, "limit": 18}
                )
                if not err3 and genre_only:
                    st.markdown(
                        "<div class='section-label'>Similar Films — By Genre</div>",
                        unsafe_allow_html=True,
                    )
                    poster_grid(genre_only, cols=grid_cols, key_prefix="genre_fallback")
                else:
                    handle_error(err3)
    else:
        st.info("No title available to compute recommendations.")