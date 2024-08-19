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
from src.middle_school_level.courses_page import display_courses
from src.middle_school_level.sign_up_page import display_sign_up
from utils.styles import get_styles_main, get_profile_image_style, get_styles_landing
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import sqlite3
import os
import logging
import io
import openai
import time
import sqlite3
import csv

# Load environment variables
load_dotenv()

# Setup #####################################################################################

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error('OpenAI API key was not found. Please check your .env file.')
    st.stop()

client = openai.OpenAI(api_key=api_key)

logging.basicConfig(level=logging.INFO)
ASSISTANT_ID = 'asst_mgnLV1tlOpmytiq1eUCixZ0N'
THREAD_ID = 'thread_gpesqxGVn0zvniW08rTWhitW'

# Relational Database on SQLite ############################################################

# Relational Database Schema
conn = sqlite3.connect('kids_coding_university.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
Create TABLE IF NOT EXISTS Courses (
    CourseID INTEGER PRIMARY KEY,
    ProgramName TEXT,
    AgeRange TEXT,
    Duration TEXT,
    LanguagesTaught TEXT,
    Cost REAL,
    Prerequisites TEXT,
    LearningOutcomes TEXT,
    ClassFormat TEXT,
    ClassSize INTEGER,
    CertificationOffered TEXT,
    WeeklyTimeCommitment TEXT,
    AdditionalCosts TEXT,
    ProgressTracking TEXT,
    HomeworkProjects TEXT,
    StudentSupport TEXT,
    AdvancedOpportunities TEXT,
    OnlineSafetyMeasures TEXT,
    RefundPolicy TEXT,
    ParentInvolvement TEXT,
    CareerPreparation TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Teachers (
    TeacherID INTEGER PRIMARY KEY,
    Name TEXT,
    Qualifications TEXT,
    Biography TEXT,
    SpecialtyAreas TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS CourseTeachers(
    CourseID INTEGER,
    TeacherID INTEGER,
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
    FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS FAQ (
    FAQID INTEGER PRIMARY KEY,
    Question TEXT,
    Answer TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS CourseTopics (
    TopicID INTEGER PRIMARY KEY,
    CourseID INTEGER,
    TopicName TEXT,
    TopicDescription TEXT,
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
)
''')

conn.commit()
conn.close() 

# CSV to SQLite function ######################################################################################


import csv
import sqlite3
import streamlit as st
import os

def import_csv_to_sqlite(csv_file, table_name, db_file='kids_coding_university.db'):
    try:
        # Check if file exists
        if not os.path.exists(csv_file):
            st.error(f"Error: The file {csv_file} does not exist.")
            return

        # Check if file is readable
        if not os.access(csv_file, os.R_OK):
            st.error(f"Error: The file {csv_file} is not readable. Check file permissions.")
            return

        # Check if file is empty
        if os.stat(csv_file).st_size == 0:
            st.error(f"Error: The file {csv_file} is empty.")
            return

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get the column names from the SQLite table
        cursor.execute(f"PRAGMA table_info({table_name})")
        table_columns = [row[1] for row in cursor.fetchall()]

        with open(csv_file, 'r', encoding='utf-8-sig') as file:
            # Read the first few lines of the file for debugging
            first_lines = [next(file) for _ in range(2)]
            #st.write(f"First few lines of {csv_file}:")
            #st.code("\n".join(first_lines))
            
            # Reset file pointer to the beginning
            file.seek(0)
            
            csv_reader = csv.DictReader(file)
            csv_columns = [col for col in csv_reader.fieldnames if col and col.strip()]

            if not csv_columns:
                st.error(f"Error: No valid columns found in {csv_file}")
                return

            # Check if CSV columns match table columns
            if set(csv_columns) != set(table_columns):
                st.error(f"Column mismatch in {csv_file}. CSV columns: {csv_columns}, Table columns: {table_columns}")
                return

            for row in csv_reader:
                # Only use columns that exist in the table and remove empty values
                filtered_row = {k: v for k, v in row.items() if k in table_columns and k.strip() and v and v.strip()}
                if filtered_row:  # Only insert if we have data
                    columns = ', '.join(filtered_row.keys())
                    placeholders = ', '.join(['?' for _ in filtered_row])
                    sql = f'INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})'
                    cursor.execute(sql, list(filtered_row.values()))

        conn.commit()
        #st.success(f"Successfully imported data into {table_name}")
    except sqlite3.Error as e:
        st.error(f"An error occurred while importing data into {table_name}: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred while processing {csv_file}: {str(e)}")
    finally:
        if conn:
            conn.close()

# Usage
try: 
    import_csv_to_sqlite('./data/courses.csv', 'Courses')
    import_csv_to_sqlite('./data/teachers.csv', 'Teachers')
    import_csv_to_sqlite('./data/course_teachers.csv', 'CourseTeachers')
    import_csv_to_sqlite('./data/faq.csv', 'FAQ')
    import_csv_to_sqlite('./data/course_topics.csv', 'CourseTopics')
except Exception as e:
    st.error(f'An error occurred during the data import: {str(e)}')



###############################################################################################################

# Verify data was loaded correctly
conn = sqlite3.connect('kids_coding_university.db')
cursor = conn.cursor()

# Check Courses table
cursor.execute("SELECT COUNT(*) FROM Courses")
courses_count = cursor.fetchone()[0]
print(f"Number of courses in database: {courses_count}")

# Check Teachers table
cursor.execute("SELECT COUNT(*) FROM Teachers")
teachers_count = cursor.fetchone()[0]
print(f"Number of teachers in database: {teachers_count}")

# Check CourseTopics table
cursor.execute("SELECT COUNT(*) FROM CourseTopics")
topics_count = cursor.fetchone()[0]
print(f"Number of course topics in database: {topics_count}")

# Check FAQ table
cursor.execute("SELECT COUNT(*) FROM FAQ")
faq_count = cursor.fetchone()[0]
print(f"Number of FAQ entries in database: {faq_count}")

conn.close()

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def display_chatbot():
    st.markdown('<p class="big-font">AI Chatbot Assistant</p>', unsafe_allow_html=True)
    st.write("Ask me anything about our coding courses!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about our courses"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in fetch_response(prompt):
                full_response += response
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
def execute_sql_query(query):
    try:
        conn = sqlite3.connect('kids_coding_university.db')
        result = pd.read_sql_query(query, conn)
        conn.close()
        return result
    except Exception as e:
        logging.error(f"Error executing SQL query: {e}")
        return None

def wait_for_run_complete(thread_id, run_id):
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime('%H:%M:%S', time.gmtime(elapsed))
                logging.info(f'Run completed in {formatted_elapsed_time}')
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                return last_message.content[0].text.value
        except Exception as e:
            logging.error(f'An error occurred while retrieving the run: {e}')
            return 'Sorry, I encountered an error. Please try again.'
        time.sleep(1)

def check_active_runs(thread_id):
    runs = client.beta.threads.runs.list(thread_id=thread_id)
    for run in runs.data:
        if run.status == "in_progress":
            return run.id
    return None

def fetch_response(user_input):
    try:
        active_run_id = check_active_runs(THREAD_ID)
        if active_run_id:
            wait_for_run_complete(THREAD_ID, active_run_id)

        sql_generation_prompt = f"""Given the following SQL table schema:
    
    CREATE TABLE Courses (
        CourseID INTEGER PRIMARY KEY,
        ProgramName TEXT,
        AgeRange TEXT,
        Duration TEXT,
        LanguagesTaught TEXT,
        Cost REAL,
        Prerequisites TEXT,
        LearningOutcomes TEXT,
        ClassFormat TEXT,
        ClassSize INTEGER,
        CertificationOffered TEXT,
        WeeklyTimeCommitment TEXT,
        AdditionalCosts TEXT,
        ProgressTracking TEXT,
        HomeworkProjects TEXT,
        StudentSupport TEXT,
        AdvancedOpportunities TEXT,
        OnlineSafetyMeasures TEXT,
        RefundPolicy TEXT,
        ParentInvolvement TEXT,
        CareerPreparation TEXT
    )

    CREATE TABLE CourseTopics (
        TopicID INTEGER PRIMARY KEY,
        CourseID INTEGER,
        TopicName TEXT,
        TopicDescription TEXT,
        FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
    )

    CREATE TABLE FAQ (
        FAQID INTEGER PRIMARY KEY,
        Question TEXT,
        Answer TEXT
    )

    Generate a SQL query to answer the following question:
    {user_input}

    Return only the SQL query, without any additional text or markdown formatting."""


        client.beta.threads.messages.create(
            thread_id=THREAD_ID,
            role='user',
            content=sql_generation_prompt
        )

        run = client.beta.threads.runs.create(
            thread_id=THREAD_ID,
            assistant_id=ASSISTANT_ID
        )
        
        sql_query = wait_for_run_complete(THREAD_ID, run.id)
        
        sql_query = sql_query.strip('`').replace('sql\n', '')

        # !IMPORTANT! ################################# Execute the generated SQL query 
        query_result = execute_sql_query(sql_query)

        if query_result is not None and not query_result.empty:
            query_result_str = query_result.to_string(index=False)
        else:
            query_result_str = "No results found for the given query."

        # !IMPORTANT! ################################# Now, ask the Assistant to interpret the results
        interpretation_prompt = f"""SQL Query: {sql_query}
        
Query Result:
{query_result_str}

User Question: {user_input}

You are an AI assistant for Kids Coding University. Provide an accurate and helpful response based on the SQL query, its results, and the user's original question.
If the query didn't return any results, suggest the user ask about available courses or provide general information about the coding programs.
For questions not related to the coding courses or the university, politely redirect the conversation to course-related topics.

Remember previous questions and context from this conversation when formulating your response."""


        client.beta.threads.messages.create(
            thread_id=THREAD_ID,
            role='user',
            content=interpretation_prompt
        )

        run = client.beta.threads.runs.create(
            thread_id=THREAD_ID,
            assistant_id=ASSISTANT_ID
        )
        
        response = wait_for_run_complete(THREAD_ID, run.id)
        
        return response

    except openai.APIError as e:
        if "Can't add messages to thread" in str(e):
            logging.warning("Caught active run error, retrying...")
            time.sleep(2)
            return fetch_response(user_input)
        else:
            logging.error(f"OpenAI API error: {str(e)}")
            return "Sorry, I encountered an API error. Please try again later."
    except Exception as e:
        logging.error(f'Error in fetch_response: {str(e)}', exc_info=True)
        return "I apologize, but I'm having trouble processing that request. Is there anything specific about our courses you'd like to know?"


def main():
    # Get the path to the sidebar image
    sidebar_image_path = os.path.join(os.path.dirname(__file__), "images", "boy_and_dog.png")
    print(f"Sidebar image path: {sidebar_image_path}")  # Debug print

    # Encode the sidebar image
    sidebar_image_base64 = get_base64_of_bin_file(sidebar_image_path)
    print(f"Encoded image length: {len(sidebar_image_base64)}")  # Debug print

    #st.set_page_config(page_title="Kids Coding University", page_icon="🚀", layout="wide")

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
    elif selected_section == 'AI Chatbot':
        display_chatbot()
    elif selected_section == 'Sign Up':
        display_sign_up()

if __name__ == "__main__":
    main()
