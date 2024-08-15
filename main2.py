# main2.py
# This script is the primary entry point of the Portfolio APP
#
######################################################################################################

import streamlit as st
import base64
import os
from src.landing_page import display_home
#from src.chatbot_page import display_chatbot
from src.syllabus_page import display_syllabus
from src.course_structure_page import display_course_structure
from src.projects_page import display_projects
from utils.styles import get_styles_main, get_profile_image_style, get_styles_landing

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def main():
    # Get the path to the sidebar image
    sidebar_image_path = os.path.join(os.path.dirname(__file__), "images", "boy_and_dog.png")
    print(f"Sidebar image path: {sidebar_image_path}")  # Debug print

    # Encode the sidebar image
    sidebar_image_base64 = get_base64_of_bin_file(sidebar_image_path)
    print(f"Encoded image length: {len(sidebar_image_base64)}")  # Debug print

    st.set_page_config(
        page_title="Your App Title",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )


    # Main portfolio sidebar
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: white;'>Coder's University</h1>", unsafe_allow_html=True)

        # Profile picture
        profile_image_path = os.path.join(os.path.dirname(__file__), "images", "logo2.png")
        profile_image_base64 = get_base64_of_bin_file(profile_image_path)
        st.markdown(get_profile_image_style(profile_image_base64), unsafe_allow_html=True)

        sections = [
            'Home',
            'Syllabus',
            'Course Structure',
            'Student Projects',
            'Sign Up'
        ]

    selected_section = st.sidebar.radio('', sections)

    if selected_section == 'Home':
        #st.markdown(get_styles_main(sidebar_image_base64), unsafe_allow_html=True)
        display_home()
    elif selected_section == 'Syllabus':
        display_syllabus()
    elif selected_section == 'Course Structure':
        display_course_structure()
    elif selected_section == 'Student Projects':
        display_student_projects()
    elif selected_section == 'Sign Up':
        display_sign_up()

if __name__ == "__main__":
    main()
