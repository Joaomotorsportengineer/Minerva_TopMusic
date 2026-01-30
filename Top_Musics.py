import streamlit as st
import billboard

st.title("Billboard Hot 100 - Top 30 por ano")

# Seleção de ano
year = st.selectbox(
    "Ano",
    options=list(range(2025, 1957, -1)),  # 2025 até 1958
    index=0
)

# Botão para buscar o top 30
if st.button("Buscar top 30"):
    with st.spinner("Carregando..."):
        chart = billboard.ChartData('hot-100-songs', year=year)
        top_30 = list(chart)[:30]
    
    for s in top_30:
        st.write(f"**{s.rank}.** {s.title} — *{s.artist}*")