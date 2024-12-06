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
st.write('')

st.write('### Jobs Posted Over the Last 7 Days:')
jobs = requests.get('http://api:4000/jp/jobPostings')
job_num = 0
for job in jobs:
    job_num = job_num + 1
st.write(job_num)
st.write('')
st.write('')

st.write('### Number of Companies:')
comps = requests.get('http://api:4000/co/companies')
comp_num = 0
for comp in comps:
    comp_num = comp_num + 1
st.write(comp_num)
st.write('')
st.write('')

st.write('### Number of Students:')
studs = requests.get('http://api:4000/st/students')
stud_num = 0
for stud in studs:
    stud_num = stud_num + 1
st.write(stud_num)
st.write('')
st.write('')

st.write('### Reviews Posted Over the Last 7 Days:')
revs = requests.get('http://api:4000/rv/reviews')
rev_num = 0
for rev in revs:
    rev_num = rev_num + 1
st.write(rev_num)