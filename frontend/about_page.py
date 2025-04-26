import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json
import time

def load_lottie_url(url):
    """Load lottie animation from URL with proper error handling"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        st.error(f"Error loading animation: {e}")
        return None

def about_page():
    """About page for GitHub Repository Browser application"""
    
    # custom styling 
    st.markdown("""
    <style>
    /* Color scheme - GitHub dark theme inspired */
    :root {
        --primary-bg: #0d1117;
        --secondary-bg: #161b22;
        --card-bg: #21262d;
        --text-primary: #f0f6fc;
        --text-secondary: #8b949e;
        --accent-blue: #58a6ff;
        --accent-teal: #56d4bc;
        --accent-purple: #bc8cff;
        --accent-orange: #f0883e;
        --accent-green: #3fb950;
    }
    
    /* Global styles */
    .stApp {
        background-color: var(--primary-bg);
        color: var(--text-primary);
    }
    
    /* Main header styling with animation */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
        background: linear-gradient(90deg, var(--accent-teal), var(--accent-blue), var(--accent-purple));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: gradientShift 8s ease infinite;
    }
    
    @keyframes gradientShift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    /* Section titles with animation */
    .section-title {
        color: var(--accent-blue);
        font-weight: 600;
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-left: 4px solid var(--accent-blue);
        padding-left: 0.8rem;
        animation: fadeInUp 0.8s ease-out forwards;
        opacity: 0;
        transform: translateY(20px);
    }
    
    /* Cards for features and team with hover effects and animations */
    .card {
        background-color: var(--card-bg);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        animation: fadeIn 0.8s ease-out forwards;
        opacity: 0;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
    }
    
    .card-title {
        color: var(--accent-teal);
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    
    .card-content {
        color: var(--text-secondary);
    }
    
    /* Tech stack styling with animations */
    .tech-category {
        background-color: var(--card-bg);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        animation: fadeIn 0.8s ease-out forwards;
        opacity: 0;
        transition: all 0.3s ease;
    }
    
    .tech-category:hover {
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .tech-category-title {
        color: var(--text-primary);
        font-weight: 600;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .tech-item {
        background-color: var(--secondary-bg);
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .tech-item:hover {
        background-color: var(--accent-blue);
        color: var(--primary-bg);
        transform: scale(1.05);
    }
    
    /* Steps styling with animations */
    .steps-container {
        margin: 2rem 0;
    }
    
    .step-item {
        background-color: var(--card-bg);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        transition: all 0.3s ease;
        animation: fadeInLeft 0.8s ease-out forwards;
        opacity: 0;
        transform: translateX(-20px);
    }
    
    .step-item:hover {
        background-color: rgba(88, 166, 255, 0.1);
        border-left: 4px solid var(--accent-blue);
    }
    
    .step-number {
        background-color: var(--secondary-bg);
        color: var(--accent-blue);
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 1rem;
        transition: all 0.3s ease;
    }
    
    .step-item:hover .step-number {
        background-color: var(--accent-blue);
        color: var(--primary-bg);
    }
    
    /* Team styling with animations */
    .team-avatar {
        border-radius: 50%;
        width: 120px;
        height: 120px;
        object-fit: cover;
        border: 3px solid var(--accent-purple);
        transition: all 0.3s ease;
    }
    
    .team-card:hover .team-avatar {
        transform: scale(1.1);
        border-color: var(--accent-teal);
    }
    
    /* Buttons with animations */
    .contact-button {
        background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .contact-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(88, 166, 255, 0.4);
    }
    
    .contact-button::after {
        content: "";
        display: block;
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        pointer-events: none;
        background-image: radial-gradient(circle, #fff 10%, transparent 10.01%);
        background-repeat: no-repeat;
        background-position: 50%;
        transform: scale(10, 10);
        opacity: 0;
        transition: transform .5s, opacity 1s;
    }
    
    .contact-button:active::after {
        transform: scale(0, 0);
        opacity: 0.3;
        transition: 0s;
    }
    


    

    
    /* Disclaimer */
    .disclaimer {
        background-color: var(--card-bg);
        border-left: 4px solid var(--accent-orange);
        padding: 1rem;
        margin-top: 2rem;
        border-radius: 4px;
        animation: fadeIn 1s ease-out forwards;
        opacity: 0;
    }
    
    /* Version badge with pulse animation */
    .version-badge {
        background-color: rgba(240, 136, 62, 0.2);
        color: var(--accent-orange);
        font-size: 0.9rem;
        padding: 0.3rem 0.8rem;
        border-radius: 16px;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(240, 136, 62, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(240, 136, 62, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(240, 136, 62, 0);
        }
    }
    
    /* Scroll animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Staggered animations for cards */
    .card:nth-child(1) { animation-delay: 0.1s; }
    .card:nth-child(2) { animation-delay: 0.2s; }
    .card:nth-child(3) { animation-delay: 0.3s; }
    .card:nth-child(4) { animation-delay: 0.4s; }
    
    .tech-category:nth-child(1) { animation-delay: 0.1s; }
    .tech-category:nth-child(2) { animation-delay: 0.2s; }
    .tech-category:nth-child(3) { animation-delay: 0.3s; }
    .tech-category:nth-child(4) { animation-delay: 0.4s; }
    
    .step-item:nth-child(1) { animation-delay: 0.1s; }
    .step-item:nth-child(2) { animation-delay: 0.2s; }
    .step-item:nth-child(3) { animation-delay: 0.3s; }
    .step-item:nth-child(4) { animation-delay: 0.4s; }
    .step-item:nth-child(5) { animation-delay: 0.5s; }

    /* Progress bar animation styles */
    .progress-container {
        width: 100%;
        background-color: var(--secondary-bg);
        border-radius: 10px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 8px;
        border-radius: 10px;
        background: linear-gradient(90deg, var(--accent-teal), var(--accent-blue), var(--accent-purple));
        background-size: 200% 100%;
        animation: progressAnimation 2s linear infinite;
        width: 0;
        transition: width 1s ease;
    }
    
    @keyframes progressAnimation {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    /* Floating animation for icons */
    .floating-icon {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
        100% {
            transform: translateY(0px);
        }
    }

    /* Slide-in animation for sections */
    .section-container {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.8s ease, transform 0.8s ease;
    }
    
    .section-visible {
        opacity: 1;
        transform: translateY(0);
    }
    </style>
    
    <!-- JavaScript for scroll animations -->
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Function to check if an element is in the viewport
        function isElementInViewport(el) {
            var rect = el.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        }
        
        // Function to handle scroll animations
        function handleScrollAnimations() {
            var sections = document.querySelectorAll('.section-container');
            
            sections.forEach(function(section) {
                if (isElementInViewport(section)) {
                    section.classList.add('section-visible');
                }
            });
        }
        
        // Add scroll event listener
        window.addEventListener('scroll', handleScrollAnimations);
        
        // Trigger once on load
        handleScrollAnimations();
        
        // Animate progress bars
        setTimeout(function() {
            var progressBars = document.querySelectorAll('.progress-bar');
            progressBars.forEach(function(bar) {
                var width = bar.getAttribute('data-width');
                bar.style.width = width;
            });
        }, 500);
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown('<h1 class="main-header">GitHub Repository Browser</h1>', unsafe_allow_html=True)
    
   
    lottie_urls = {
        "github": "https://assets3.lottiefiles.com/packages/lf20_6e0qqtpa.json",
        "code": "https://assets2.lottiefiles.com/private_files/lf30_wqypnpu5.json",
        "browser": "https://assets4.lottiefiles.com/packages/lf20_khzniaya.json"
    }
    
    lottie_animations = {}
    for key, url in lottie_urls.items():
        lottie_animations[key] = load_lottie_url(url)
    
    
    if lottie_animations["github"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st_lottie(lottie_animations["github"], height=200, key="github_animation")
    else:
        
        st.markdown("""
        <div style="text-align: center; font-size: 3rem; margin: 2rem 0;">
          <span style="color: #58a6ff;">🚀</span>
        </div>
        """, unsafe_allow_html=True)
    
    
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Overview</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p class="card-content">
        GitHub Repository Browser is a comprehensive tool for developers to explore, analyze, and interact with GitHub repositories. 
        Built with Streamlit and powered by AI, this application provides an intuitive interface for repository exploration, 
        code editing, and related resource discovery.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Features Section 
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title"> Features</h2>', unsafe_allow_html=True)
    
    features = [
        {
            "title": "Repository Structure Explorer",
            "icon": "📂",
            "description": "View file and directory structure, browse through repository contents, and analyze repository organization."
        },
        {
            "title": "Code Editor",
            "icon": "💻",
            "description": "View and edit code files with syntax highlighting for various programming languages. Create new files and folders."
        },
        {
            "title": "Resource Finder",
            "icon": "🔍",
            "description": "Discover tutorials related to repository technologies, find official documentation, and browse similar projects and examples."
        },
        {
            "title": "AI-Powered Features",
            "icon": "🤖",
            "description": "Smart search suggestions, code analysis and insights, and repository context awareness."
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for i, feature in enumerate(features):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class="card">
                <div class="floating-icon" style="font-size: 2rem; margin-bottom: 0.8rem;">{feature["icon"]}</div>
                <h3 class="card-title">{feature["title"]}</h3>
                <p class="card-content">{feature["description"]}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
   
    if lottie_animations["code"]:
        st.markdown('<div class="section-container" style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st_lottie(lottie_animations["code"], height=150, key="code_animation")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tech Stack 
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title"> Technology Stack</h2>', unsafe_allow_html=True)
    
    tech_categories = {
        "Backend": ["Python", "Django"],
        "Frontend": ["Streamlit"],
        "AI Components": ["Groq API"],
        "External APIs": ["GitHub API", "Google Custom Search", "Sarvam API"]
    }
    
    # 2x2 grid 
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    cols = [row1_col1, row1_col2, row2_col1, row2_col2]
    
    for i, (category, technologies) in enumerate(tech_categories.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="tech-category">
                <h3 class="tech-category-title">{category}</h3>
                <div style="display: flex; flex-wrap: wrap; justify-content: center;">
                    {"".join([f'<div class="tech-item">{tech}</div>' for tech in technologies])}
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title"> Getting Started</h2>', unsafe_allow_html=True)
    
    steps = [
        "Sign in with your GitHub credentials",
        "Search for a repository by username and repository name",
        "Explore the repository structure",
        "Use the code editor to view and modify files",
        "Find related resources using the Resource Finder"
    ]
    
    st.markdown('<div class="steps-container">', unsafe_allow_html=True)
    
    for i, step in enumerate(steps):
        st.markdown(f"""
        <div class="step-item">
            <div class="step-number">{i+1}</div>
            <div>{step}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    

    # Contact Section 
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title"> Contact</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p class="card-content">For questions, suggestions, or bug reports, please reach out to us on GitHub or via email at support@githubrepoexplorer.com.</p>
        <div style="text-align: center; margin-top: 1rem;">
            <button class="contact-button">Get in Touch</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
        <span class="version-badge">Version 1.0.0</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
        <h3 style="color: var(--accent-orange);">Disclaimer</h3>
        <p>This application is not affiliated with GitHub. It's an independent tool designed to enhance the GitHub experience.
        All GitHub data is accessed through official GitHub APIs in accordance with their terms of service.</p>
    </div>
    """, unsafe_allow_html=True)
    
    
    st.markdown("""
    <script>
        // This script will be executed to handle scroll animations
        const observer = new IntersectionObserver((entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add('section-visible');
            }
          });
        });
        
        document.querySelectorAll('.section-container').forEach((section) => {
          observer.observe(section);
        });
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    about_page()