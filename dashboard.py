import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard",  page_icon="🎵", layout="wide")
st.markdown("""
<style>
h1, h2, h3 {
    color: #1DB954 !important;
}
.stMetric {
    background: rgba(29, 185, 84, 0.1);
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #1DB954;
}
.stSlider > div > div > div {
    background-color: #1DB954 !important;
}
.stSlider [role="slider"] {
    background-color: #1DB954 !important;
    border: 2px solid white !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #1DB954 !important;
}
section[data-testid="stSidebar"] .stRadio label {
    color: #1DB954 !important;
}
section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background-color: #1DB954 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

st.title("🎵 Music Analytics 2024")

# ── Încărcare date ────────────────────────────────────────────────
fisier = st.file_uploader("Încarcă fișierul CSV", type=["csv"])

if fisier is None:
    st.info("Încarcă un fișier CSV pentru a continua.")
    st.stop()

df = pd.read_csv(fisier)

# ── Statistici generale ───────────────────────────────────────────
top_spotify = df.loc[df["Spotify Streams"].idxmax()]
top_youtube = df.loc[df["YouTube Views"].idxmax()]
top_tiktok = df.loc[df["TikTok Views"].idxmax()]

st.subheader("🏆 Cele mai ascultate melodii:")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🎧 Top Spotify",
        f"{top_spotify['Spotify Streams']:,.0f}",
    )
    st.caption(f"{top_spotify['Track']} - {top_spotify['Artist']}")

with col2:
    st.metric(
        "📺 Top YouTube",
        f"{top_youtube['YouTube Views']:,.0f}",
    )
    st.caption(f"{top_youtube['Track']} - {top_youtube['Artist']}")

with col3:
    st.metric(
        "🎵 Top TikTok",
        f"{top_tiktok['TikTok Views']:,.0f}",
    )
    st.caption(f"{top_tiktok['Track']} - {top_tiktok['Artist']}")

st.divider()

st.subheader("Caută o melodie dupa nume:")

track_list = sorted(df["Track"].unique())
selected_track = st.selectbox("Selectează melodia:", track_list)

song = df[df["Track"] == selected_track].iloc[0]

st.markdown("Detalii:")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Spotify Streams", f"{song['Spotify Streams']:,.0f}")

with col2:
    st.metric("YouTube Views", f"{song['YouTube Views']:,.0f}")

with col3:
    st.metric("TikTok Views", f"{song['TikTok Views']:,.0f}")

st.write(f"🎤 **Artist:** {song['Artist']}")

st.divider()

st.subheader("Vizualizare date")

numar_randuri = st.slider(
    "Câte rânduri să afișăm?",
    min_value=5,
    max_value=len(df),
    value=10,
    step=5,
    key=1
)

st.dataframe(
    df.head(numar_randuri),
    use_container_width=True
)

# ── Filtre în sidebar ─────────────────────────────────────────────
st.sidebar.header("Filtre")
optiuni = df["Artist"].unique().tolist()
selectie = st.sidebar.multiselect("Filtru", optiuni, default=["Billie Eilish"])
df_filtrat = df[df["Artist"].isin(selectie)]
st.write("Pentru a filtra datasetul folositi-va de filtrele din partea stanga")
st.subheader("Dataset Filtrat")
numar_randuri = st.slider(
    "Câte rânduri să afișăm?",
    min_value=5,
    max_value=len(df),
    value=10,
    step=5,
    key=2
)

st.dataframe(
    df_filtrat.head(numar_randuri),
    use_container_width=True
)

st.write("Pentru a alege platforma folositi-va de radioboxul din stanga")
st.subheader("Numarul de ascultari ale melodiilor artistilor selectati")

platforma = st.sidebar.radio(
    "Alege platforma:",
    ["Spotify Streams", "YouTube Views", "TikTok Views"]
)

graf_df = df_filtrat.sort_values(platforma, ascending=False).set_index("Track")[platforma]

st.bar_chart(
    graf_df,
color="#1DB954"
)

# ── Grafic 1 — Plotly ─────────────────────────────────────────────
st.subheader("Media ascultărilor per artist")

platforma = st.selectbox(
    "Selectează platforma pentru care vrei să afișezi mediile:",
    ["Spotify Streams", "YouTube Views", "TikTok Views"],
    key=67
)

fig = px.bar(
    df_filtrat.groupby("Artist")[platforma]
    .mean()
    .reset_index(),
    x="Artist",
    y=platforma,
    title=f"Media ascultărilor pe {platforma} per artist",
    color_discrete_sequence=["#1DB954"]
)
st.plotly_chart(fig, use_container_width=True)
# ── Grafic 2 — Matplotlib ─────────────────────────────────────────
st.subheader("Distribuția ascultărilor pe melodii")
platforma = st.selectbox(
    "Selectează platforma pentru care vrei să afișezi mediile:",
    ["Spotify Streams", "YouTube Views", "TikTok Views"],
    key=89
)

distributie = (
    df_filtrat.groupby(["Track", "Artist"])[platforma]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

labels = [f"{track} - {artist}" for track, artist in distributie.index]

fig, ax = plt.subplots(figsize=(3,3))

wedges, texts, autotexts = ax.pie(
    distributie.values,
    labels=labels,
    autopct="%1.1f%%",
    startangle=140,
    pctdistance=0.75,
    wedgeprops=dict(width=0.5, edgecolor="#0f0f0f", linewidth=1)
)

ax.set_title(f"Top 5 melodii după {platforma}", fontsize=10)

col1, col2, col3 = st.columns([1,10,1])
with col2:
    st.pyplot(fig)

plt.close(fig)