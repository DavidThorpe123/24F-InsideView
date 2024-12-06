import pandas as pd
import altair as alt
import streamlit as st
from modules.nav import SideBarLinks
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

if st.button("Back", key="back_button"):
    st.switch_page('pages/02_recruiter_home.py')

st.title("View Student Feedback by Company.")

# Display all companies
companies = requests.get('http://web-api:4000/co/companies').json()
company_names = [company['name'] for company in companies]
st.markdown("### **Select a company to view feedback.**")
selected_company = st.selectbox("", company_names)

#option to filter by rating
rating_filter = st.slider("Filter by Rating", 1, 5, (1, 5), step=1)

#option to filter by date range
date_filter = st.checkbox("Filter by Date?")
if date_filter:
    start_date = st.date_input("Start Date", min_value=datetime(2000, 1, 1))
    end_date = st.date_input("End Date", max_value=datetime.today())
else:
    start_date, end_date = None, None

#get student feedback for selected company
if selected_company:
    for company in companies:
        if company['name'] == selected_company:
            company_id = company['id']
            break

    #get student feedback for selected company
    feedback_response = requests.get(f'http://web-api:4000/jp/jobPostings/reviews/{company_id}')

    if feedback_response.status_code == 200:
        feedback = feedback_response.json()
        st.markdown("### Student Feedback:")
        
        filtered_feedback = []
        
        for review in feedback:
            #format the date in a more readable way
            review_date = datetime.strptime(review['datePosted'], "%a, %d %b %Y %H:%M:%S %Z")
            
            #apply rating filter
            if rating_filter[0] <= review['rating'] <= rating_filter[1]:
                #apply date filter if selected
                if date_filter:
                    if start_date <= review_date.date() <= end_date:
                        filtered_feedback.append(review)
                else:
                    filtered_feedback.append(review)

        if filtered_feedback:
            for review in filtered_feedback:
                st.markdown(f"**{review['title']}**")
                st.markdown(f"Rating: {review['rating']}")
                st.markdown(f"Date Posted: {review_date.strftime('%B %d, %Y at %I:%M %p')}")
                st.markdown(f"Content: {review['content']}")
                st.markdown("---")
        else:
            st.info("No feedback available for this company with the selected filters.")
    else:
        st.error(f"Failed to load student feedback data. Status code: {feedback_response.status_code}")
