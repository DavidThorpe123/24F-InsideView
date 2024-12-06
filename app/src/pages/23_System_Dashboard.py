import streamlit as st
from modules.nav import SideBarLinks
import requests
import logging
logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

# Sidebar links
SideBarLinks()

if st.button("Back", key="back_button"):
    st.switch_page('pages/20_Admin_Home')

st.title("System Dashboard:")

# Display 4 columns
# Companies, Reviews, Students, Accounts
col1, col2, col3 = st.columns(3)
student_buttons = []
student_emails = []

with col1:
    companies = requests.get('http://api:4000/co/companies').json()
    company_names = [company['name'] for company in companies]
    for company in companies:
        company_id = company['id']
        company_name = company['name']
        st.write(company_name)
        if st.button(f"Edit", key=f"edit_{company_id}"):
            st.session_state['editing_company'] = {
                'id': company_id,
                'name': company_name
            }
            st.experimental_rerun

if 'editing_company' in st.session_state:
    with st.form("edit_form"):
        editing_company = st.session_state['editing_company']
        st.write(f"Editing: {editing_company['name']}")

        updated_name = st.text_input("New Company Name", value=editing_company['name'])

        if st.form_submit_button("Save"):
            response = requests.put(
                f"http://api:4000/co/companies/{editing_company['id']}",
                json={"name": updated_name}
            )

            if response.status_code == 200:
                st.success("Company name updated.")
                del st.session_state['editing_company']
                st.experimental_rerun()
            else:
                st.error("Failed to update company name.")

with col2:
    reviews_response = requests.get('http://api:4000/jp/jobPostings/reviews').json()
    if reviews_response.status_code == 200:
        reviews = reviews_response.json()
        st.header("Recent Reviews:")
        st.json(reviews)
    else:
        st.error("Failed to fetch reviews.")




with col3:
    students_response = requests.get('http://api:4000/students/')
    if students_response.status_code == 200:
        students = students_response.json()
        for _ in range(len(students)):
            student_buttons.append(st.empty())
            student_emails.append(st.empty())
        st.json(students)

        def show_student_email(idx):
            if student_emails[idx].container():
                student_emails[idx].empty()
            else:
                student_emails[idx].write(students[idx]['email'])
        
        for i, button in enumerate(student_buttons):
            with button.container():
                st.button("Show Email", key = f"show_email_{i}", on_click=lambda: show_student_email(i))
    else:
        st.error("Failed to fetch students.")





# with col4:
#     accounts = requests.get()