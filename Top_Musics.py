import os
import streamlit as st
import billboard
import requests

YOUTUBE_API_KEY = st.secrets.get("YOUTUBE_API_KEY") or os.getenv("YOUTUBE_API_KEY")


def get_youtube_track(title: str, artist: str):
    if not YOUTUBE_API_KEY:
        return None, None
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": f"{title} {artist}",
        "type": "video",
        "maxResults": 1,
        "key": YOUTUBE_API_KEY,
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        items = data.get("items", [])
        if not items:
            return None, None
        video_id = items[0]["id"].get("videoId")
        if not video_id:
            return None, None
        link = f"https://www.youtube.com/watch?v={video_id}"
        thumb = None
        snippet = items[0].get("snippet", {})
        thumbs = snippet.get("thumbnails", {})
        if thumbs.get("medium"):
            thumb = thumbs["medium"]["url"]
        elif thumbs.get("default"):
            thumb = thumbs["default"]["url"]
        return link, thumb
    except Exception:
        return None, None


st.title("Billboard Hot 100 - Top músicas por ano")

year = st.selectbox(
    "Ano",
    options=list(range(2025, 2006, -1)),
    index=0,
)
quantidade = st.slider(
    "Quantidade de músicas",
    min_value=5,
    max_value=100,
    value=10,
    step=5,
    help="O year-end Hot 100 tem até 100 músicas.",
)

if st.button("Buscar"):
    with st.spinner("Carregando..."):
        try:
            chart = billboard.ChartData("hot-100-songs", year=year)
            top_musicas = list(chart)[:quantidade]
        except Exception:
            st.error("Não foi possível carregar o ranking. Tente outro ano.")
            st.stop()

    for s in top_musicas:
        url_youtube, img_youtube = get_youtube_track(s.title, s.artist)
        img = getattr(s, "image", None) or img_youtube

        col1, col2 = st.columns([1, 4])
        with col1:
            if img:
                try:
                    st.image(img, width=80)
                except Exception:
                    st.caption("—")
            else:
                st.caption("—")
        with col2:
            st.write(f"**{s.rank}.** {s.title} — *{s.artist}* ({year})")
            if url_youtube:
                st.markdown(f"[Ouvir no YouTube]({url_youtube})")
            else:
                st.caption("Link YouTube não encontrado")