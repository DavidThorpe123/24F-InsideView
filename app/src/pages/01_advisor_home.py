import streamlit as st
from modules.nav import SideBarLinks

import logging
logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}!. Let's get prepared.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Hiring Companies', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_advisor_companies.py')
