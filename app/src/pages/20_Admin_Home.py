import streamlit as st
from modules.nav import SideBarLinks
import requests
import logging

logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

# Sidebar links
SideBarLinks()

st.title('System Admin Home Page')
st.write('')
st.write('')
st.write('### Menu:')

if st.button('System Analytics', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_System_Analytics.py')

if st.button('System Dashboard',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_System_Dashboard.py')