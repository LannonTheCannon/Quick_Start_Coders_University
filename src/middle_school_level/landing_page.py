import streamlit as st
import plotly.graph_objects as go

def display_home():
    # Header
    st.title("🚀 Kids Coding University")
    st.subheader("Where Young Minds Launch into the Digital Future!")

    # Introduction
    st.markdown("""
    Welcome to Kids Coding University - where coding is as fun as your favorite game! 
    Join us on an exciting 9-month adventure into the world of technology. 
    You'll learn to create cool apps, solve puzzles with code, and even talk to robots!
    """)

    st.divider()

    # Program Highlights
    st.header("🌟 What's Cool About Our Program?")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Time to Become a Tech Wizard", value="9 Months")
    with col2:
        st.metric(label="Awesome Projects", value="12+")
    with col3:
        st.metric(label="Cool Things to Learn", value="22+")
    with col4:
        st.metric(label="Official Certification", value="1")

    st.divider()

    # What You'll Learn
    st.header("🧠 What You'll Learn (and Why It's Awesome!)")

    skills = {
        "Python Power": {
            "icon": "🐍",
            "description": "Learn the language that powers YouTube and Instagram!",
            "projects": ["Make your own game", "Solve programming puzzles", "Create art with code"]
        },
        "Web Wizardry": {
            "icon": "🌐",
            "description": "Build your own websites and apps, just like the pros!",
            "projects": ["Design your personal website", "Create a family photo gallery", "Make an online quiz for friends"]
        },
        "Data Detective": {
            "icon": "🕵️",
            "description": "Discover hidden patterns in information, like a real scientist!",
            "projects": ["Analyze your favorite sports team's performance", "Track weather patterns", "Create cool charts and graphs"]
        },
        "AI Adventures": {
            "icon": "🤖",
            "description": "Teach computers to think and talk, it's like magic!",
            "projects": ["Build a chatbot friend", "Create a smart homework helper", "Design a game that learns as you play"]
        }
    }

    for skill, details in skills.items():
        with st.expander(f"{details['icon']} {skill}"):
            st.write(f"**{details['description']}**")
            st.write("Cool things you'll make:")
            for project in details['projects']:
                st.write(f"- {project}")
                
    st.divider()
    # Learning Journey
    st.header("🗺️ Your Coding Adventure Map")
    journey = {
        "Level 1: Code Cadet": "Learn the basics and start your first Python project",
        "Level 2: Web Explorer": "Create your own website and show it to the world",
        "Level 3: Data Dynamo": "Discover the secrets hidden in numbers and make amazing charts",
        "Level 4: AI Apprentice": "Bring your creations to life with artificial intelligence"
    }

    for level, description in journey.items():
        st.markdown(f"**{level}:** {description}")
    st.divider()
    # Why Parents Love Us
    st.header("👨‍👩‍👧‍👦 Why Parents Love Kids Coding University")
    st.markdown("""
    - 🧠 **Future-Ready Skills**: Your child will learn skills that are in high demand.
    - 🎨 **Creativity Boost**: Coding enhances problem-solving and creative thinking.
    - 🏆 **Confidence Builder**: Accomplishing coding projects builds self-esteem.
    - 👥 **New Friends**: Connect with other young coders in a fun, safe environment.
    - 📚 **Academic Edge**: Coding skills can help in math, science, and beyond!
    """)
    st.divider()
    # Testimonials
    st.header("💬 What Our Young Coders Say")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background-color: #E6F3FF; border-radius: 10px; padding: 10px;">
            <p style="color: #0066CC; margin-bottom: 5px;">
            "I made a game where my dog chases virtual squirrels. My family loves playing it!"
            </p>
            <p style="color: #0066CC; font-style: italic; margin-top: 0;">
            - Alex, Age 11
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background-color: #FFE6E6; border-radius: 10px; padding: 10px;">
            <p style="color: #CC0000; margin-bottom: 5px;">
            "I built a website about saving the ocean. Now my whole class is involved!"
            </p>
            <p style="color: #CC0000; font-style: italic; margin-top: 0;">
            - Mia, Age 13
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.divider()
    # Call to Action
    st.header("🚀 Ready to Start Your Coding Adventure?")
    st.write("Join Kids Coding University and blast off into the world of technology!")
##    if st.button("Sign Up for a Free Trial Class"):
##        st.balloons()
##        st.success("Woohoo! We'll contact you soon with details about your free trial class. Get ready for an awesome adventure!")

    # Footer
    st.markdown("---")
    st.markdown("© 2024 Kids Coding University | Made with ❤️ by young coders, for young coders!")

if __name__ == "__main__":
    display_home()
