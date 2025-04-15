import streamlit as st
from main_page import main_page  # Import your existing main_page function
from repo_structure_page import repo_structure_page
from resources_page import resources_page
from code_editor_page import code_editor_page
from about_page import about_page
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
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "repo_name" not in st.session_state:
    st.session_state.repo_name = ""

# Simple authentication function (for demonstration)
def authenticate(username, password):
    # Replace with actual authentication logic
    if username and password:  # Simple validation for demo
        st.session_state.authenticated = True
        st.session_state.username = username
        return True
    return False

# Sign out function
def sign_out():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.repo_name = ""
    st.session_state.page = "main"
    st.rerun()

# Navigation bar
def render_navbar():
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    
    with col1:
        if st.button("📊 Repository", key="nav_repo", use_container_width=True):
            st.session_state.page = "repo_structure"
            st.rerun()
    with col2:
        if st.button("📚 Resources", key="nav_resources", use_container_width=True):
            st.session_state.page = "resources"
            st.rerun()
    with col3:
        if st.button("💻 Code Editor", key="nav_code_editor", use_container_width=True):
            st.session_state.page = "code_editor"
            st.rerun()
    with col4:
        if st.button("ℹ️ About", key="nav_about", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()
    with col5:
        if st.button("🚪 Sign Out", key="nav_signout", use_container_width=True):
            sign_out()

# Login screen
def login_page():
    st.markdown('<h1 style="text-align: center;">GitHub Repository Browser</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.subheader("Sign In")
        username = st.text_input("GitHub Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_button", use_container_width=True):
            if authenticate(username, password):
                st.success("Login successful!")
                st.session_state.page = "main"
                st.rerun()
            else:
                st.error("Invalid username or password")
                
        st.markdown("</div>", unsafe_allow_html=True)

# Display the appropriate page
if not st.session_state.authenticated and st.session_state.page != "about":
    login_page()
else:
    if st.session_state.authenticated:
        render_navbar()
        
    if st.session_state.page == "main":
        main_page()  # Using the imported main_page function
    elif st.session_state.page == "repo_structure":
        repo_structure_page()
    elif st.session_state.page == "resources":
        resources_page()
    elif st.session_state.page == "code_editor":
        code_editor_page()
    elif st.session_state.page == "about":
        about_page()