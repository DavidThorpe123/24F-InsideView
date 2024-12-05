import streamlit as st
from modules.nav import SideBarLinks

import logging
logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}! Let's get prepared.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Common Interview Questions', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/00_common_questions.py')

if st.button('View Company Reviews (Or add your own!)', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/00_company_reviews.py')

if st.button('View Postings and Apply', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/00_popular_companies.py')

if st.button('View Your Sent Applications', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/00_student_applications.py')