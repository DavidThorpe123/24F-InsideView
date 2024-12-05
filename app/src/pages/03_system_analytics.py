import streamlit as st
from modules.nav import SideBarLinks
import requests
import logging

logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

# Sidebar links
SideBarLinks()

if st.button("Back", key="back_button"):
    st.switch_page('pages/03_admin_home.py')

st.title("System Analytics:")

col1, col2, col3 = st.columns(3)
