import streamlit as st
import json
import os
from datetime import datetime

def save_signup(data):
    if not os.path.exists('signups.json'):
        with open('signups.json', 'w') as f:
            json.dump([], f)
    
    with open('signups.json', 'r+') as f:
        signups = json.load(f)
        signups.append(data)
        f.seek(0)
        json.dump(signups, f, indent=2)

def display_sign_up():
    st.header("Sign Up for Kids Coding University")
    st.write("Please fill out the form below to sign up your child for our coding courses.")

    with st.form("signup_form"):
        parent_name = st.text_input("Parent/Guardian Name")
        child_name = st.text_input("Child's Name")
        child_age = st.number_input("Child's Age", min_value=5, max_value=18, value=10)
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        course_interest = st.selectbox(
            "Which course are you interested in?",
            ["Beginner Python", "Intermediate Python", "Advanced Web Development", "AI and Machine Learning for Kids"]
        )
        additional_info = st.text_area("Any additional information or questions?")

        if st.form_submit_button("Submit Sign Up"):
            if parent_name and child_name and email and phone:
                signup_data = {
                    "parent_name": parent_name,
                    "child_name": child_name,
                    "child_age": child_age,
                    "email": email,
                    "phone": phone,
                    "course_interest": course_interest,
                    "additional_info": additional_info,
                    "signup_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_signup(signup_data)
                st.success("Thank you for signing up! We'll contact you soon with more information.")
            else:
                st.error("Please fill out all required fields.")
