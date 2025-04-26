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

st.set_page_config(
    page_title="VIKSIT.AI",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

css = utils.load_css('style.css')
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.markdown("""
<style>
    /* Global styles */
    body {
        color: white;
        font-family: 'Inter', sans-serif;
        background-color: #0e1117;
    }
    
    
/* Floating code background */
body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    background-color: rgba(14, 17, 23, 0.95);
    background-image: 
        repeating-linear-gradient(rgba(124, 77, 255, 0.05) 0px, transparent 2px, transparent 4px),
        radial-gradient(rgba(124, 77, 255, 0.05) 1px, transparent 2px);
    background-size: 100% 4px, 30px 30px;
    pointer-events: none;
}

/* Add floating code snippets */
.floating-code {
    position: fixed;
    color: rgba(124, 77, 255, 0.15);
    font-family: monospace;
    font-size: 14px;
    white-space: nowrap;
    pointer-events: none;
    z-index: -1;
    text-shadow: 0 0 5px rgba(124, 77, 255, 0.2);
    animation: float-up 60s linear infinite;
}

.floating-code:nth-child(1) { top: 15%; left: 10%; animation-duration: 80s; }
.floating-code:nth-child(2) { top: 35%; left: 5%; animation-duration: 120s; animation-delay: -20s; }
.floating-code:nth-child(3) { top: 60%; left: 15%; animation-duration: 90s; animation-delay: -15s; }
.floating-code:nth-child(4) { top: 25%; right: 10%; animation-duration: 110s; animation-delay: -30s; }
.floating-code:nth-child(5) { top: 70%; right: 15%; animation-duration: 100s; animation-delay: -10s; }
.floating-code:nth-child(6) { top: 45%; right: 5%; animation-duration: 85s; animation-delay: -25s; }

@keyframes float-up {
    0% {
        transform: translateY(100vh) rotate(5deg);
        opacity: 0;
    }
    10% {
        opacity: 1;
    }
    90% {
        opacity: 1;
    }
    100% {
        transform: translateY(-100vh) rotate(-5deg);
        opacity: 0;
    }
}
    
    /* App background */
    .stApp {
        background-color: #0e1117;
    }
    
    .main-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 30px;
        background: rgba(30, 30, 40, 0.7);
        border-radius: 12px;
        border: 1px solid rgba(124, 77, 255, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 30px;
    }

    .logo {
        font-size: 28px;
        font-weight: bold;
        color: white;
        text-shadow: 0 0 10px rgba(124, 77, 255, 0.7);
        letter-spacing: 1px;
        background: linear-gradient(90deg, #9c27b0, #7b1fa2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        transition: all 0.3s ease;
    }

    .logo:hover {
        transform: scale(1.05);
        text-shadow: 0 0 15px rgba(124, 77, 255, 0.9);
    }

    .nav-links {
        display: flex;
        align-items: center;
        gap: 25px;
    }

    .nav-link {
        color: white;
        text-decoration: none;
        font-weight: 500;
        font-size: 16px;
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.3s ease;
        position: relative;
    }
        .nav-link:hover {
        color: #9c27b0;
        background: rgba(255, 255, 255, 0.1);
    }

    .nav-link::after {
        content: '';
        position: absolute;
        width: 0;
        height: 2px;
        bottom: 0;
        left: 50%;
        background: linear-gradient(90deg, #9c27b0, #7b1fa2);
        transition: all 0.3s ease;
        transform: translateX(-50%);
    }

    .nav-link:hover::after {
        width: 80%;
    }
    
    /* Enhanced navbar */
    .navbar {
        background: rgba(30, 30, 40, 0.7);
        border-radius: 12px;
        padding: 8px;
        margin-bottom: 20px;
        border: 1px solid rgba(124, 77, 255, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }
    
    .navbar-btn {
        background: transparent;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 500;
        font-size: 15px;
        transition: all 0.3s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    
    .navbar-btn:hover {
        background: rgba(124, 77, 255, 0.2);
        transform: translateY(-2px);
    }
    
    .navbar-btn.active {
        background: linear-gradient(135deg, rgba(100, 65, 165, 0.3), rgba(156, 39, 176, 0.3));
        box-shadow: 0 0 15px rgba(124, 77, 255, 0.3);
    }
    
    .navbar-btn.exit {
        background: rgba(200, 50, 70, 0.2);
    }
    
    .navbar-btn.exit:hover {
        background: rgba(200, 50, 70, 0.3);
    }
    
    /* Hero section with enhanced typography */
    .hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 65vh;
        text-align: center;
        padding: 20px;
        position: relative;
        z-index: 10;
    }
    
        .brand-title {
        font-size: 80px;
        font-weight: bold;
        background: linear-gradient(90deg, #9c27b0, #7b1fa2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 20px rgba(124, 77, 255, 0.3);
        letter-spacing: 2px;
        margin-bottom: 10px;
        position: relative;
        display: inline-block;
        transition: all 0.3s ease;
        cursor: pointer;
        padding: 10px 20px;
        border-radius: 15px;
    }
    
    .brand-title:hover {
        background: #9c27b0;
        -webkit-text-fill-color: white;
        text-shadow: 0 0 30px rgba(124, 77, 255, 0.7);
    }
    */
    
    /* Add the typing animation styles from the first file */
    .typing-container {
        display: inline-block;
        margin-bottom: 20px;
    }
    
    .typing-text {
        font-size: 64px;
        font-weight: bold;
        background: linear-gradient(90deg, #9c27b0, #7b1fa2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 20px rgba(124, 77, 255, 0.3);
        letter-spacing: 2px;
        overflow: hidden;
        border-right: 0.15em solid #9c27b0;
        white-space: nowrap;
        margin: 0 auto;
        width: 0;
        animation: 
            typing 8s steps(14, end) infinite forwards,
            blink-caret 0.75s step-end infinite;
    }
    .typing-text:hover {
    text-shadow: 0 0 30px rgba(156, 39, 176, 0.8);
    letter-spacing: 3px;
    transform: scale(1.05);
}
.multilingual:hover span {
    text-shadow: 0 0 15px rgba(156, 39, 176, 0.8);
    transform: translateY(0) scale(1.1) !important;
}
.tagline:hover {
    text-shadow: 0 0 20px rgba(156, 39, 176, 0.7);
    letter-spacing: 1.2px;
}
    @keyframes typing {
        0% { width: 0; }
        50% { width: 100%; }
        70% { width: 100%; }
        100% { width: 0; }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent; }
        50% { border-color: #9c27b0; }
    }
    
    /* Multi-language tagline */
    .tagline {
        font-size: 54px;
        margin: 15px 0 40px 0;
        color: white;
    }
    

    /* Clean sequential language rotation with no overlap */
    .multilingual {
        position: relative;
        display: inline-block;
        height: 34px;
        min-width: 102px;
        font-weight: bold;
        vertical-align: middle;
        overflow: hidden;
    }

    .multilingual span {
        color: #9c27b0;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        opacity: 0;
        width: 100%;
        display: block;
        text-align: center;
        font-size: 34px !important;
    }

    /* Using a single animation for all spans with specific delays */
    .multilingual span {
        animation: rotate-single-language 16s ease-in-out infinite;
    }

    .multilingual span:nth-child(1) { animation-delay: 0s; }
    .multilingual span:nth-child(2) { animation-delay: 4s; }
    .multilingual span:nth-child(3) { animation-delay: 8s; }
    .multilingual span:nth-child(4) { animation-delay: 12s; }

    @keyframes rotate-single-language {
        0%, 1%, 24%, 100% { 
            opacity: 0; 
            transform: translateY(20px); 
        }
        3%, 22% { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
            

    /* Override Streamlit's default text styling */
    .st-emotion-cache-seewz2 p,
    .st-emotion-cache-seewz2 .tagline,
    .st-emotion-cache-seewz2 .multilingual span {
        font-size: 20px !important;
    }
    /* Custom styling for the Explore Plans button */
div[data-testid="stButton"] {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #6441a5, #9c27b0) !important;
    color: white !important;
    padding: 12px 35px !important;
    border-radius: 50px !important;
    border: none !important;
    font-weight: bold !important;
    font-size: 18px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2) !important;
    min-width: 200px !important;
}

div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #7e57c2, #b039c3) !important;
    box-shadow: 0 5px 20px rgba(124, 77, 255, 0.4) !important;
    transform: translateY(-2px) !important;
}
    /* Form styles */
    .subscribe-form {
        display: flex;
        max-width: 600px;
        width: 100%;
        margin: 0 auto;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        border-radius: 4px;
        overflow: hidden;
    }
    
    .email-input {
        flex-grow: 1;
        padding: 16px 20px;
        border-radius: 4px 0 0 4px;
        border: 1px solid rgba(124, 77, 255, 0.3);
        background-color: rgba(30, 30, 40, 0.6);
        color: white;
        font-size: 16px;
        backdrop-filter: blur(5px);
    }
    
    .subscribe-button {
        background: linear-gradient(135deg, #6441a5, #9c27b0);
        color: white;
        padding: 16px 28px;
        border-radius: 0 4px 4px 0;
        border: none;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 16px;
        letter-spacing: 0.5px;
    }
    
    .subscribe-button:hover {
        background: linear-gradient(135deg, #7e57c2, #b039c3);
        box-shadow: 0 0 15px rgba(124, 77, 255, 0.5);
        transform: translateY(-2px);
    }
    
    /* Subscription plans */
    .subscription-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 60px;
        flex-wrap: wrap;
        position: relative;
        z-index: 10;
    }
    
    .subscription-card {
        background: rgba(30, 30, 40, 0.7);
        border: 1px solid rgba(124, 77, 255, 0.3);
        border-radius: 16px;
        padding: 35px;
        max-width: 320px;
        width: 100%;
        transition: all 0.4s ease;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .subscription-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #6441a5, #9c27b0);
        opacity: 0.7;
    }
    
    .subscription-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(124, 77, 255, 0.2);
        border-color: rgba(124, 77, 255, 0.6);
    }
    
    .plan-badge {
        position: absolute;
        top: 15px;
        right: 15px;
        background: linear-gradient(135deg, #6441a5, #9c27b0);
        color: white;
        font-size: 12px;
        font-weight: bold;
        padding: 5px 10px;
        border-radius: 20px;
        letter-spacing: 0.5px;
    }
    
    .plan-title {
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 10px;
        color: white;
        letter-spacing: 0.5px;
    }
    
    .plan-price {
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 20px;
        background: linear-gradient(90deg, #6441a5, #9c27b0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .plan-price span {
        font-size: 16px;
        opacity: 0.8;
    }
    
    .plan-description {
        margin-bottom: 30px;
        color: rgba(255, 255, 255, 0.7);
        line-height: 1.6;
        font-size: 15px;
    }
    
    .plan-features {
        margin-bottom: 30px;
    }
    
    .feature-item {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        color: rgba(255, 255, 255, 0.8);
    }
    
    .feature-icon {
        color: #9c27b0;
        margin-right: 10px;
    }
    
    .get-plan-button {
        background: linear-gradient(135deg, #6441a5, #9c27b0);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        display: block;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        letter-spacing: 0.5px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .get-plan-button:hover {
        background: linear-gradient(135deg, #7e57c2, #b039c3);
        box-shadow: 0 5px 20px rgba(124, 77, 255, 0.4);
        transform: translateY(-2px);
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
        background-color: rgba(30, 30, 40, 0.7);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 25px;
        border: 1px solid rgba(124, 77, 255, 0.2);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Utility classes */
    .text-center {
        text-align: center;
    }
    
    .mt-20 {
        margin-top: 20px;
    }
    
    .sign-up-button {
        background: linear-gradient(135deg, #6441a5, #9c27b0);
        color: white !important;
        padding: 10px 24px;
        border-radius: 50px;
        border: none;
        font-weight: 600;
        font-size: 16px;
        cursor: pointer;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        display: inline-block;
        text-align: center;
        margin-left:77px;
    }

    .sign-up-button:hover {
        background: linear-gradient(135deg, #7e57c2, #b039c3);
        box-shadow: 0 5px 20px rgba(124, 77, 255, 0.4);
        transform: translateY(-2px) scale(1.03);
    }
    
    /* Navigation bar */
    .stButton button {
        background-color: rgba(30, 30, 40, 0.7) !important;
        border: 1px solid rgba(124, 77, 255, 0.2) !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background-color: rgba(124, 77, 255, 0.2) !important;
        border-color: rgba(124, 77, 255, 0.5) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Hero subtitle for better visibility */
    .hero-subtitle {
        color: #ffffff;
        font-size: 38px;
        margin-bottom: 30px;
        max-width: 600px;
        line-height: 1.6;
    }
</style>

""", unsafe_allow_html=True)


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

try:
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
        st.query_params.clear()
        
        st.session_state.authenticated = True
        st.session_state.page = "main"  
        st.session_state.username = "user@example.com"  
        st.session_state.email = "user@example.com"  
        
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
        st.markdown('<div class="logo">Turning code into clarity!</div>', unsafe_allow_html=True)
    st.markdown(
        '''
        <div class="hero-section">
            <div class="typing-container">
                <div class="typing-text">VIKSIT.AI</div>
            </div>
            <p class="tagline">Built in <span class="multilingual">
                <span>INDIA</span>
                <span>ভাৰত</span>
                <span>ଭାରତ</span>
                <span>భారత్</span>
            </span>, for the World!</p>
            <p class="hero-subtitle">Your AI coding guru that explains code and generates documentation for your codebase.</p>
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    # Button to show subscription plans (using Streamlit button instead of JavaScript)
    if st.button("Explore plans", key="subscribe_button", type="primary"):
        show_subscription_plans()
    
    # Show subscription plans if the button was clicked
    if st.session_state.show_subscription:
        st.markdown('<div class="subscription-container">', unsafe_allow_html=True)
        
        # Free Tier
        col1, col2, col3 = st.columns(3)
        
        with col1:
            auth_url = get_authorization_url()
            st.markdown(
        '<div class="subscription-card">'
        '<span class="plan-badge">POPULAR</span>'
        '<h3 class="plan-title">FREE TIER</h3>'
        '<p class="plan-price">$0<span>/month</span></p>'
        '<p class="plan-description">Get started with basic features. Perfect for beginners and casual users.</p>'
        '<div class="plan-features">'
        '<div class="feature-item"><span class="feature-icon">✓</span> Basic code analysis</div>'
        '<div class="feature-item"><span class="feature-icon">✓</span> Limited repository access</div>'
        '<div class="feature-item"><span class="feature-icon">✓</span> Community support</div>'
        '</div>'
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
        '</a>'
        '</div>',
        unsafe_allow_html=True
    )
            
        with col2:
            st.markdown(
                '<div class="subscription-card">'
                '<h3 class="plan-title">SOCIALLY BACKWARDS</h3>'
                '<p class="plan-price">$9<span>/month</span></p>'
                '<p class="plan-description">Advanced features for small teams. Includes premium support and functionality</p>'
                '<div class="plan-features">'
                '<div class="feature-item"><span class="feature-icon">✓</span> Advanced code analysis</div>'
                '<div class="feature-item"><span class="feature-icon">✓</span> Unlimited repositories</div>'                '<div class="feature-item"><span class="feature-icon">✓</span> Custom documentation</div>'
                '</div>'
                '<a href="#" class="get-plan-button">Coming Soon</a>'
                '</div>',
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                '<div class="subscription-card">'
                '<span class="plan-badge">PRO</span>'
                '<h3 class="plan-title">PRO</h3>'
                '<p class="plan-price">$29<span>/month</span></p>'
                '<p class="plan-description">Enterprise-grade features for professional developers. Unlimited access to all tools.</p>'
                '<div class="plan-features">'
                '<div class="feature-item"><span class="feature-icon">✓</span> Enterprise-level support</div>'
                '<div class="feature-item"><span class="feature-icon">✓</span> Team collaboration</div>'
                '<div class="feature-item"><span class="feature-icon">✓</span> Custom integration</div>'
                '<div class="feature-item"><span class="feature-icon">✓</span> Dedicated account manager</div>'
                '</div>'
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
    
    if st.sidebar.checkbox("Show state"):
        st.sidebar.write(st.session_state)
    
    
    if not st.session_state.authenticated:
        landing_page()
    else:
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