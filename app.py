import index
import players
import streamlit as st
PAGES = {
    "Players": players,
    "Index": index
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()