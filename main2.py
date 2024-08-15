# main2.py
# This script is the primary entry point of the Portfolio APP
#
######################################################################################################

import streamlit as st
import base64
import os
from src.middle_school_level.landing_page import display_home
#from src.chatbot_page import display_chatbot
from src.middle_school_level.syllabus_page import display_syllabus
from src.middle_school_level.course_structure_page import display_course_structure
from src.middle_school_level.projects_page import display_projects
from utils.styles import get_styles_main, get_profile_image_style, get_styles_landing

import streamlit as st
import pandas as pd
import sqlite3
import os
import logging
import io

# Load environment variables
load_dontenv()

# Setup #####################################################################################

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error('OpenAI API key was not found. Please check your .env file.')
    st.stop()

client = openai.OpenAI(api_key=api_key)
logging.basicConfig(level=logging.INFO)
ASSISTANT_ID = 'asst_kGpo0qVcgHp4R5kItDuUNMZB'
THREAD_ID = 'thread_eNtAJYy1HFtZkZmKKosVWKXV'
conn = sqlite3.connect('real_estate.db')
cursor = conn.cursor()

##############################################################################################

# Create the properties table
cursor.execute('''
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY,
    address TEXT,
    price INTEGER,
    bedrooms INTEGER,
    bathrooms INTEGER,
    description TEXT
)
''')

data = """
address|price|bedrooms|bathrooms|description
123 Main St|300000|3|2|Beautiful house with garden, close to schools
456 Oak Ave|450000|4|3|Spacious family home, recently renovated kitchen
789 Pine Rd|275000|2|1|Cozy starter home, great for first-time buyers
321 Elm St|500000|5|4|Luxurious estate with pool and guest house
654 Maple Dr|325000|3|2|Charming bungalow, perfect for small families
987 Birch Ln|600000|4|3|Modern home with open floor plan and large yard
246 Cedar Ct|280000|2|1|Affordable townhouse, low maintenance
135 Willow St|350000|3|2|Classic colonial, well-maintained with upgrades
753 Aspen Blvd|410000|4|3|Contemporary design, near downtown amenities
159 Redwood Rd|475000|4|3|Elegant home in a desirable neighborhood
432 Birchwood Pl|320000|3|2|Renovated historic home, charming neighborhood
876 Cherry St|450000|4|3|Spacious suburban house, excellent school district
111 Pineapple Ln|330000|3|2|Eco-friendly home with solar panels
222 Orange Dr|420000|4|3|Lakefront property with stunning views
333 Lemon St|380000|3|2|Mountain cabin, secluded and private
444 Lime Blvd|360000|3|2|Urban loft, close to public transport
555 Mango Ct|440000|4|3|Beach house with private access
777 Apple Ave|460000|4|3|Luxury condo, high-end amenities
888 Banana Blvd|400000|3|2|Family home with large backyard
999 Coconut Ct|340000|3|2|Newly built, modern architecture
1010 Berry Ln|370000|3|2|Ranch-style house, one-story living
1111 Melon Dr|450000|4|3|Townhouse with community pool
1212 Peach St|380000|3|2|Single-family home in quiet cul-de-sac
1313 Pear Blvd|395000|3|2|Chic apartment in vibrant neighborhood
1414 Plum Pl|405000|3|2|Penthouse with skyline views
"""

df = pd.read_csv(io.StringIO(data), sep='|')
df.to_sql('properties', conn, if_exists='replace', index=False)
conn.commit()

# Verify data was loaded #############################################################
cursor.execute("SELECT COUNT(*) FROM properties")
count = cursor.fetchone()[0]
print(f"Number of properties in database: {count}")
# Verify data was loaded #############################################################


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def display_chatbot()

def main():
    # Get the path to the sidebar image
    sidebar_image_path = os.path.join(os.path.dirname(__file__), "images", "boy_and_dog.png")
    print(f"Sidebar image path: {sidebar_image_path}")  # Debug print

    # Encode the sidebar image
    sidebar_image_base64 = get_base64_of_bin_file(sidebar_image_path)
    print(f"Encoded image length: {len(sidebar_image_base64)}")  # Debug print

    st.set_page_config(page_title="Kids Coding University", page_icon="🚀", layout="wide")

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
            'AI Chatbot',
            'Sign Up',
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
    elif selected_section == 'AI Chatbot':
        display_chatbot()
    elif selected_section == 'Sign Up':
        display_sign_up()

if __name__ == "__main__":
    main()
