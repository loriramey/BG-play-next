import streamlit as st
from pages import Home
from pages import DataViz
from pages import About

pages = [
    st.Page(Home.home_page, title="Recommendations", icon="🎲", default=True),
    st.Page(DataViz.dataviz_page, title="Data Info", icon="📊"),
    st.Page(About.about_page, title="About the Project", icon="ℹ️"),
]

pg = st.navigation(pages)
pg.run()
