import streamlit as st
import firebase_admin
from firebase_admin import auth, credentials, initialize_app
import asyncio
from httpx_oauth.clients.google import GoogleOAuth2
from main_page import main_page
from repo_structure_page import repo_structure_page
from resources_page import resources_page
from code_editor_page import code_editor_page
from about_page import about_page
from community_page import community_page
import utils

# Page configuration
st.set_page_config(
    page_title="Codease Enigma",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
css = utils.load_css('style.css')
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Custom CSS to match the Codease Enigma design
st.markdown("""
<style>
    /* Global styles */
    body {
        background-color: #0e1117;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styles */
    .main-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 0;
    }
    
    .logo {
        font-size: 24px;
        font-weight: bold;
        color: white;
    }
    
    .nav-links {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    /* Hero section */
    .hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 60vh;
        text-align: center;
        padding: 20px;
    }
    
    .hero-title {
        font-size: 56px;
        font-weight: bold;
        margin-bottom: 20px;
        background: linear-gradient(90deg, #9c27b0, #7b1fa2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 24px;
        margin-bottom: 40px;
        max-width: 800px;
    }
    
    /* Form styles */
    .subscribe-form {
        display: flex;
        max-width: 600px;
        width: 100%;
        margin: 0 auto;
    }
    
    .email-input {
        flex-grow: 1;
        padding: 12px 20px;
        border-radius: 4px 0 0 4px;
        border: 1px solid #4b4b4b;
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    .subscribe-button {
        background-color: #6441a5;
        color: white;
        padding: 12px 24px;
        border-radius: 4px;
        border: none;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .subscribe-button:hover {
        background-color: #7e57c2;
    }
    
    /* Subscription plans */
    .subscription-container {
        display: flex;
        justify-content: center;
        gap: 24px;
        margin-top: 50px;
        flex-wrap: wrap;
    }
    
    .subscription-card {
        background: rgba(124, 77, 255, 0.1);
        border: 1px solid rgba(124, 77, 255, 0.2);
        border-radius: 12px;
        padding: 30px;
        max-width: 300px;
        width: 100%;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .subscription-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(124, 77, 255, 0.1);
    }
    
    .plan-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
        color: white;
    }
    
    .plan-price {
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #9c27b0;
    }
    
    .plan-description {
        margin-bottom: 30px;
        color: #b3b3b3;
    }
    
    .get-plan-button {
        background-color: #6441a5;
        color: white;
        padding: 12px 24px;
        border-radius: 4px;
        border: none;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s;
        width: 100%;
        display: block;
        text-align: center;
        text-decoration: none;
    }
    
    .get-plan-button:hover {
        background-color: #7e57c2;
    }
    
    /* Sign-in button with Google icon */
    .google-signin {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        text-decoration: none;
    }
    
    /* Dashboard styles */
    .dashboard-container {
        padding: 30px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .info-card {
        background-color: rgba(124, 77, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Utility classes */
    .text-center {
        text-align: center;
    }
    
    .mt-20 {
        margin-top: 20px;
    }
    
    .sign-up-button {
        background-color: #6441a5;
        color: white;
        padding: 8px 16px;
        border-radius: 4px;
        border: none;
        font-weight: bold;
        cursor: pointer;
        text-decoration: none;
    }
    
    .sign-up-button:hover {
        background-color: #7e57c2;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'email' not in st.session_state:
    st.session_state.email = ''
if 'show_subscription' not in st.session_state:
    st.session_state.show_subscription = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "repo_name" not in st.session_state:
    st.session_state.repo_name = ""

# Initialize Firebase app
try:
    cred = credentials.Certificate({
        "type": st.secrets["firebase"]["type"],
        "project_id": st.secrets["firebase"]["project_id"],
        "private_key_id": st.secrets["firebase"]["private_key_id"],
        "private_key": st.secrets["firebase"]["private_key"],
        "client_email": st.secrets["firebase"]["client_email"],
        "client_id": st.secrets["firebase"]["client_id"],
        "auth_uri": st.secrets["firebase"]["auth_uri"],
        "token_uri": st.secrets["firebase"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"],
        "universe_domain": st.secrets["firebase"]["universe_domain"]
    })
    try:
        firebase_admin.get_app()
    except ValueError:
        initialize_app(cred)
except Exception as e:
    st.error(f"Firebase initialization error: {e}")

    try:
        firebase_admin.get_app()
    except ValueError:
        initialize_app(cred)
except Exception as e:
    st.error(f"Firebase initialization error: {e}")

# Initialize Google OAuth2 client
try:
    # Update to use the correctly nested structure in st.secrets
    client_id = st.secrets["oauth"]["client_id"]
    client_secret = st.secrets["oauth"]["client_secret"]
    redirect_url = "https://viksit-ai.streamlit.app/"  
    client = GoogleOAuth2(client_id=client_id, client_secret=client_secret)
except Exception as e:
    st.error(f"OAuth client initialization error: {e}")
    client = None
def get_authorization_url():
    try:
        return asyncio.run(client.get_authorization_url(
            redirect_url,
            scope=["email", "profile", "openid"],
            extras_params={"access_type": "offline"},
        ))
    except Exception as e:
        st.error(f"Error generating authorization URL: {e}")
        return "#"

def check_authentication():
    """Check if we received a code from Google OAuth"""
    code = st.query_params.get('code')
    if code:
        # We have a code, so we've been redirected back from Google
        # Clear the code from URL
        st.query_params.clear()
        
        # Set authenticated to True - skipping actual token verification
        # since we just want to demonstrate redirection
        st.session_state.authenticated = True
        st.session_state.page = "main"  # Set to main page
        st.session_state.username = "user@example.com"  # Placeholder username
        st.session_state.email = "user@example.com"  # Placeholder email
        
        # Force a rerun to redirect to dashboard
        st.rerun()

def sign_out():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.repo_name = ""
    st.session_state.page = "landing"
    st.session_state.email = ""
    st.session_state.show_subscription = False
    st.rerun()

def show_subscription_plans():
    st.session_state.show_subscription = True
    st.rerun()

# UI Components
def landing_page():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown('<div class="logo">Talk To Code</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(
            '<div class="nav-links">'
            '<a href="#" style="color: white; text-decoration: none;"><img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="24" height="24" alt="LinkedIn"></a>'
            '<a href="#" style="color: white; text-decoration: none; margin-left: 20px;">Getting started &gt;</a>'
            '<a href="#" class="sign-up-button" style="margin-left: 20px;">Sign Up</a>'
            '</div>',
            unsafe_allow_html=True
        )
    
    # Hero Section
    st.markdown(
        '<div class="hero-section">'
        '<h1 class="hero-title">Codease Enigma</h1>'
        '<p class="hero-subtitle">Your AI coding guru that explains code and generates documentation for your codebase.</p>'
        '<div class="subscribe-form">'
        '<input type="email" placeholder="Enter your email" class="email-input">'
        '<button class="subscribe-button" id="subscribe-btn">Subscribe</button>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Button to show subscription plans (using Streamlit button instead of JavaScript)
    if st.button("Subscribe", key="subscribe_button", type="primary"):
        show_subscription_plans()
    
    # Show subscription plans if the button was clicked
    if st.session_state.show_subscription:
        st.markdown('<div class="subscription-container">', unsafe_allow_html=True)
        
        # Free Tier
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                '<div class="subscription-card">'
                '<h3 class="plan-title">Free Tier</h3>'
                '<p class="plan-price">$0/mo</p>'
                '<p class="plan-description">Get started with basic features. Perfect for beginners and casual users.</p>'
                '</div>',
                unsafe_allow_html=True
            )
            
            # Get authorization URL for Google sign-in
            auth_url = get_authorization_url()
            
            # Add the "Get Plan" button that triggers OAuth flow
            st.markdown(
                f'<a href="{auth_url}" class="get-plan-button google-signin">'
                '<svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" style="margin-right: 10px;">'
                '<path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12'
                's5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24s8.955,20,20,20'
                's20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"></path>'
                '<path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039'
                'l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"></path>'
                '<path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36'
                'c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"></path>'
                '<path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571'
                'c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"></path>'
                '</svg>'
                'Get Free Plan'
                '</a>',
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                '<div class="subscription-card">'
                '<h3 class="plan-title">Socially Backward</h3>'
                '<p class="plan-price">$9/mo</p>'
                '<p class="plan-description">Advanced features for small teams. Includes premium support and extended functionality.</p>'
                '<a href="#" class="get-plan-button">Coming Soon</a>'
                '</div>',
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                '<div class="subscription-card">'
                '<h3 class="plan-title">Pro</h3>'
                '<p class="plan-price">$29/mo</p>'
                '<p class="plan-description">Enterprise-grade features for professional developers. Unlimited access to all tools.</p>'
                '<a href="#" class="get-plan-button">Coming Soon</a>'
                '</div>',
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Check for authentication code in URL parameters
    check_authentication()

# Navigation bar
def render_navbar():
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
    
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
        if st.button("👥 Community", key="nav_community", use_container_width=True):
            st.session_state.page = "community"
            st.rerun()
    with col5:
        if st.button("ℹ️ About", key="nav_about", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()
    with col6:
        if st.button("🚪 Exit", key="nav_signout", use_container_width=True):
            sign_out()

# Main app logic - Routing between pages
def main():
    # Debug
    if st.sidebar.checkbox("Show state"):
        st.sidebar.write(st.session_state)
    
    # Routing
    if not st.session_state.authenticated:
        # Show landing page with subscription options
        landing_page()
    else:
        # User is authenticated, show navigation bar and appropriate page
        render_navbar()
        
        if st.session_state.page == "main":
            main_page()
        elif st.session_state.page == "repo_structure":
            repo_structure_page()
        elif st.session_state.page == "resources":
            resources_page()
        elif st.session_state.page == "code_editor":
            code_editor_page()
        elif st.session_state.page == "community":
            community_page()
        elif st.session_state.page == "about":
            about_page()

if __name__ == "__main__":
    main()