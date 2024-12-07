import streamlit as st
from modules.nav import SideBarLinks
import requests
import logging
logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

if st.button("Back", key="back_button"):
    st.switch_page('pages/03_admin_home.py')

# Sidebar links
# SideBarLinks()


st.title("System Dashboard:")

# Display 4 columns
# Companies, Reviews, Students, Accounts
col1, col2, col3, col4 = st.columns(4)
student_buttons = []
student_emails = []



with col1:
    companies = requests.get('http://api:4000/co/companies').json()
    for company in companies:
        company_id = company['id']
        company_name = company['name']
        st.write(company_name)
        if st.button(f"Edit", key=f"edit_{company_id}"):
            st.session_state['editing_company'] = {
                'id': company_id,
                'name': company_name
            }

if 'editing_company' in st.session_state:
    with st.form("edit_form2"):
        editing_company = st.session_state['editing_company']
        st.write(f"Editing: {editing_company['name']}")

        updated_name = st.text_input("New Company Name", value=editing_company['name'])

        if st.form_submit_button("Save"):
            response = requests.put(
                f"http://api:4000/co/companies/{editing_company['id']}/{updated_name}"
            )

            if response.status_code == 200:
                st.success("Company name updated.")
                del st.session_state['editing_company']
            else:
                st.error("Failed to update company name.")

with col2:
    reviews_response = requests.get('http://api:4000/jp/jobPostings/reviews')
    if reviews_response.status_code == 200:
        reviews = reviews_response.json()
        st.header("Recent Reviews:")
        
        for review in reviews: 
            st.write(review['title'])
            st.write(review['content'])

            if st.button('Delete Review', key=review['id']):
                delete_response = requests.delete(f"http://api:4000/jp/jobPostings/reviews/{review['id']}")

                if delete_response.status_code == 200:
                    st.success("Review deleted.")
                else:
                    st.error('Couldnt delete review')

            st.write('---')
    else:
        st.error("Failed to fetch reviews.")




with col3:
    students_response = requests.get('http://api:4000/st/students')
    if students_response.status_code == 200:
        students = students_response.json()

        for student in students:
            stu_fn = student['firstName']
            stu_ln = student['lastName']
            stu_gpa = student['gpa']
            stu_gy = student['gradYear']
            stu_email = student['email']
            stu_id = student['id']
            stu_pn = student['phone']

            st.write(stu_fn + " " + stu_ln)
            st.write(f"GPA: {stu_gpa}")
            st.write(f"Grad Year: {stu_gy}")

            if st.button('Show Info', key=stu_email):
                st.write(stu_email)
                st.write(stu_pn)

            st.write('---')
    else:
        st.error("Failed to fetch students.")


with col4:
    accounts_response = requests.get('http://api:4000/ad/system_admins')
    if accounts_response.status_code == 200:
        accounts = accounts_response.json()
        for acc in accounts:
            acc_id = acc['id']
            acc_first = acc['firstName']
            acc_last = acc['lastName']
            acc_email = acc['email']
            st.write(acc_first, acc_last)
            if st.button(f"Edit", key=f"edit_{acc_email}"):
                st.session_state['editing_account'] = {
                    'id': acc_id,
                    'firstName': acc_first,
                    'lastName': acc_last
            }

if 'editing_account' in st.session_state:
    with st.form("edit_form"):
        editing_account = st.session_state['editing_account']
        st.write(f"Editing: {editing_account['id']}")

        updated_id = st.text_input("New Account ID", value=editing_account['id'])

        if st.form_submit_button("Save"):
            response = requests.put(
                f"http://api:4000/ad/system_admins/{editing_account['id']}",
                json={"id": updated_id}
            )

            if response.status_code == 200:
                st.success("Account ID updated.")
                del st.session_state['editing_account']
            else:
                st.error("Failed to update account ID.")