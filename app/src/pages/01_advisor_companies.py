import streamlit as st
from modules.nav import SideBarLinks

import logging
import requests
logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')


SideBarLinks()

if 'page_state' not in st.session_state:
    st.session_state.page_state = 'advisor_home'
if 'company_id' not in st.session_state:
    st.session_state.company_id = None
if 'company_name' not in st.session_state:
    st.session_state.company_name = None
if 'company_rating' not in st.session_state:
    st.session_state.company_rating = None




st.write('')
st.write('')


results = requests.get('http://api:4000/co/companiesSpecific').json()


if (st.session_state.page_state == 'advisor_home'):
    col1, col2 = st.columns([.5, 1])
    with col1:
      st.title(f"Welcome, {st.session_state['first_name']}!")
      st.write('### Employers (Companies):')
      for result in results:
        st.subheader(f"{result['CompanyName']}")
        st.write(f"Average Rating: {result['AverageRating']}")
        num_applicants = requests.get(f'http://api:4000/co/companies/{result["id"]}/count_applicants').json()
        st.write(f"Number of Applicants: {num_applicants[0]['AmountOfApplicants']}")
        if (st.button(f'View {result["CompanyName"]}', key=f'view_{result["id"]}')):
          st.session_state.page_state = 'company'
          st.session_state.company_id = result['id']
          st.session_state.company_name = result['CompanyName']
          st.session_state.company_rating = result['AverageRating']
          st.rerun()
      with col2:
        for i in range(9):
          st.write(' ')
        key_words = st.text_input('Enter in a company name, student interest, or job title here to find relevant positions:', key='search')
        if st.button('Search'):
         found_positions = requests.get(f'http://api:4000/co/companies/match_description/{key_words}').json()
         if len(found_positions) == 0:
          st.write('No positions found')
         else:
            st.write('### Positions:')
            for position in found_positions:
              st.write(f"Job Title: {position['JobName']}")
              st.write(f"Company: {position['CompanyName']}")
              st.write(f"Description: {position['Description']}")
              st.write('')


elif st.session_state.page_state == 'company':
      st.title(f"{st.session_state.company_name}")
      company_id = st.session_state.company_id
      col1, col2 = st.columns([.5, 1])
    
    
    
      reviews = requests.get(f'http://api:4000/co/companies/{company_id}').json()
      with col1:
      
        st.write('### Reviews:')
        for review in reviews:
            
            if st.button(f"Author: {review['FirstName']} {review['LastName']}", key=f'view_{review["StudentId"]}'):
              st.session_state.page_state = 'student'
              st.session_state.student_id = review['StudentId']
              st.rerun()
            st.write(f"Title: {review['ReviewTitle']}")
            st.write(f"Rating: {review['rating']}")
            st.write(f"Content: {review['ReviewContent']}")
            st.write('')
        
      with col2:
        avg_gpa = requests.get(f'http://api:4000/co/companies/avg_gpa_past_employee/{company_id}').json()
        st.write('### Company Information:')
        st.write(f"Average GPA of Past Employees: {avg_gpa[0]['AverageGPA']}")
        st.write(f"Company Contact Information: {avg_gpa[0]['firstName']}")
        st.write(f"Company Contact Information: {avg_gpa[0]['lastName']}")
        st.write(f"Company Contact Information: {avg_gpa[0]['phone']}")
        st.write(f"Company Contact Information: {avg_gpa[0]['email']}")

        
        for i in range(18):
          st.write(' ')
        
    
    
        if st.button("Back to Advisor Home"):
          st.session_state.page_state = 'advisor_home'
          st.rerun()
elif st.session_state.page_state == 'student':
      col1, col2 = st.columns([.5, 1])
      with col1:
        st.title(f"Student Profile")
        student_id = st.session_state.student_id
        student = requests.get(f'http://api:4000/st/students/{student_id}').json()
        st.write(f"Student ID: {student[0]['id']}")
        st.write(f"First Name: {student[0]['firstName']}")
        st.write(f"Last Name: {student[0]['lastName']}")
        st.write(f"GPA: {student[0]['gpa']}")
      with col2:
        for i in range(22):
          st.write(' ')

        if st.button("Back to Advisor Home"):
          st.session_state.page_state = 'advisor_home'
          st.rerun()
  
    
    
    




    

   

   
    
        
        
                 

    
