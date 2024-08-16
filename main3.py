import streamlit as st
import base64
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from src.middle_school_level.landing_page import display_home
from src.middle_school_level.syllabus_page import display_syllabus
from src.middle_school_level.course_structure_page import display_course_structure
from src.middle_school_level.projects_page import display_projects
from src.middle_school_level.courses_page import display_courses
from utils.styles import get_styles_main, get_profile_image_style, get_styles_landing

import pandas as pd
import sqlite3
import logging
import io
import openai
import time
import csv

# Load environment variables
load_dotenv()

# Initialize OpenAI API
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    st.error("OpenAI API key not found. Please check your .env file.")
    st.stop()

# Initialize the database
try:
    db = SQLDatabase.from_uri("sqlite:///kids_coding_university.db")
    st.success("Database connection successful")
except Exception as e:
    st.error(f"Failed to connect to the database: {str(e)}")
    st.stop()

# Initialize the language model
try:
    llm = ChatOpenAI(temperature=0, api_key=openai_api_key)
    st.success("Language model initialized successfully")
except Exception as e:
    st.error(f"Failed to initialize the language model: {str(e)}")
    st.stop()

# Initialize memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create a custom prompt template
template = """
You are an AI assistant for a coding university for kids. Your task is to answer questions about the courses,
teachers, and other aspects of the university. Use the provided SQL query results to inform your answers.
Here are some rules to follow:
1. Always base your answers on the SQL query results provided.
2. Refer to the previous questions and answers in the chat history when answering new questions.
3. If additional context from previous interactions is necessary, infer and use that context.
4. When the user asks to see a table, provide the table that is neatly sectioned into rows and columns using context.
5. Make sure to keep the responses as concise and informative as possible.
Here is the chat history, use this to understand the context of the conversation:
{chat_history}
Given the question: '{question}' and the SQL query result: {sql_result}, provide a concise and informative answer.
"""
PROMPT = PromptTemplate(
    input_variables=["chat_history", "question", "sql_result"],
    template=template
)

# Create the SQL query chain
sql_chain = create_sql_query_chain(llm, db)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def clear_memory():
    global memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    st.session_state.messages = []
    st.success("Chat history and memory cleared!")

def chatbot(input_text):
    global memory
    try:
        st.write("Generating SQL query...")
        # Generate SQL query
        sql_query = sql_chain.invoke({
            "question": input_text,
            "chat_history": memory.chat_memory.messages  # Pass chat history
        })
        st.write(f"Generated SQL query: {sql_query}")
        
        st.write("Executing query...")
        result = db.run(sql_query)
        st.write(f"Query result: {result}")
        
        st.write("Generating response...")
        response = llm.predict(PROMPT.format(
            chat_history=memory.chat_memory.messages,
            question=input_text,
            sql_result=result
        ))
        st.write(f"Generated response: {response}")
        
        memory.chat_memory.add_user_message(input_text)
        memory.chat_memory.add_ai_message(response)
        
        return response
    except Exception as e:
        st.error(f"An error occurred in chatbot function: {str(e)}")
        return f"An error occurred: {str(e)}"

def display_chatbot():
    st.header("AI Chatbot")
    st.write("Ask me anything about our courses!")

    # Add a button to clear memory
    if st.button("Clear Chat History"):
        clear_memory()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to know?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Thinking..."):
            response = chatbot(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    # Get the path to the sidebar image
    sidebar_image_path = os.path.join(os.path.dirname(__file__), "images", "boy_and_dog.png")
    print(f"Sidebar image path: {sidebar_image_path}")  # Debug print

    # Encode the sidebar image
    sidebar_image_base64 = get_base64_of_bin_file(sidebar_image_path)
    print(f"Encoded image length: {len(sidebar_image_base64)}")  # Debug print

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
            'Courses',
            'Student Projects',
            'AI Chatbot',
            'FAQ',
            'Sign Up',
        ]

    selected_section = st.sidebar.radio('', sections)

    if selected_section == 'Home':
        display_home()
    elif selected_section == 'Syllabus':
        display_syllabus()
    elif selected_section == 'Course Structure':
        display_course_structure()
    elif selected_section == 'Courses':
        display_courses()
    elif selected_section == 'Student Projects':
        display_projects()
    elif selected_section == 'AI Chatbot':
        display_chatbot()
    elif selected_section == 'FAQ':
        st.write("FAQ page is under construction.")
    elif selected_section == 'Sign Up':
        st.write("Sign Up page is under construction.")

if __name__ == "__main__":
    main()
