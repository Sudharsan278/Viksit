import streamlit as st
from main_page import main_page
from repo_structure_page import repo_structure_page
from groq_assistant_page import groq_assistant_page
from resources_page import resources_page
import utils

# Set page configuration with a premium look
st.set_page_config(
    page_title="GitHub Repository Browser",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
css = utils.load_css('style.css')
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "main"

# Display the appropriate page
if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "repo_structure":
    repo_structure_page()
elif st.session_state.page == "groq_assistant":
    groq_assistant_page()
elif st.session_state.page == "resources":
    resources_page()