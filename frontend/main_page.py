import streamlit as st
from utils import get_repositories

def main_page():
    """Main page to enter GitHub username and select repository"""
    st.markdown('<h1 style="text-align: center;">GitHub Repository Explorer</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        username = st.text_input("Enter GitHub Username", help="Type a GitHub username to see their repositories")
        
        if username:
            repos = get_repositories(username)
            
            if repos:
                repo_names = [repo["name"] for repo in repos]
                selected_repo = st.selectbox("Select Repository", repo_names, help="Choose a repository to explore")
                
                if selected_repo:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("Explore Repository Structure", help="View the repository's file structure"):
                            # Reset any previously stored structures
                            if 'top_level_structure' in st.session_state:
                                del st.session_state['top_level_structure']
                            # Clear folder states
                            for key in list(st.session_state.keys()):
                                if key.startswith('folder_'):
                                    del st.session_state[key]
                            
                            # Store selection for structure page
                            st.session_state.username = username
                            st.session_state.repo_name = selected_repo
                            st.session_state.page = "repo_structure"
                            st.session_state.view_file = False
                            st.rerun()
                    with col2:
                        if st.button("Ask AI About This Repo", help="Use Groq to analyze this repository"):
                            # Store selection for Groq page
                            st.session_state.username = username
                            st.session_state.repo_name = selected_repo
                            st.session_state.page = "groq_assistant"
                            st.rerun()
                    with col3:
                        if st.button("Find Resources", help="Search for related resources"):
                            # Store selection for Resources page
                            st.session_state.username = username
                            st.session_state.repo_name = selected_repo
                            st.session_state.page = "resources"
                            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Feature cards for users without a username entered
        if not username:
            st.markdown("<h2>Explore our features</h2>", unsafe_allow_html=True)
            
            st.markdown('<div class="feature-cards">', unsafe_allow_html=True)
            
            # Repository Explorer card
            st.markdown("""
            <div class="feature-card" onclick="document.querySelector('.stTextInput input').focus()">
                <div class="feature-icon">📁</div>
                <div class="feature-title">Repository Explorer</div>
                <div class="feature-description">
                    Browse any GitHub repository with our interactive file explorer.
                    Navigate through folders and view files with ease.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # AI Assistant card
            st.markdown("""
            <div class="feature-card" onclick="document.querySelector('.stTextInput input').focus()">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI Repository Analysis</div>
                <div class="feature-description">
                    Get AI-powered insights and analysis of repositories.
                    Understand code structure and purpose through natural language.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Resources card
            st.markdown("""
            <div class="feature-card" onclick="document.querySelector('.stTextInput input').focus()">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Find Related Resources</div>
                <div class="feature-description">
                    Discover tutorials, documentation, and related content
                    to help you understand and work with repositories better.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Adding some information about the application
        with st.expander("About this App"):
            st.markdown("""
            This GitHub Repository Explorer allows you to:
            - Browse any public GitHub repository
            - Explore its file structure in an interactive tree view
            - View and download files
            - Analyze repositories and code using Groq AI
            - Find related resources and documentation
            
            The application uses GitHub's API to fetch repository data in real time.
            """)