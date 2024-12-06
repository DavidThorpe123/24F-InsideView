import streamlit as st
from modules.nav import SideBarLinks
import requests
import logging
logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')
SideBarLinks()

if st.button("Back", key="back_button"):
    st.switch_page('pages/00_student_home.py')

st.title("Here you can View Your Job Applications.")

applications = requests.get('http://api:4000/jp/jobPostings/applications').json()
application_ids = [application['id'] for application in applications]

st.write(
f"""
<div style="margin: 10px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; 
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); min-width: 200px;">
    <p><strong>Number of Applications Sent:</strong> {len(application_ids)}</p>
</div>
""",
unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    applications.reverse()
    for application in applications:
        st.write(f"{application['name']} @ {application['companyName']}")
        st.write(application['datePosted'])
        st.write(f"ID: {application['id']}")
        st.write('---')
    

