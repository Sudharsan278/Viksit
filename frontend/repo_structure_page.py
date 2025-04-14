import streamlit as st
import requests
from utils import get_repo_structure, render_interactive_directory_structure
from file_view_page import file_view_page

def repo_structure_page():
    """Page to display repository structure in a premium UI"""
    username = st.session_state.username
    repo_name = st.session_state.repo_name
    
    # Check if we should display file content
    if st.session_state.get('view_file', False):
        file_view_page()
        return
    
    # Back button with icon
    if st.button("⬅ Back to Search", key="back_button"):
        st.session_state.page = "main"
        st.rerun()
    
    # Repository header with user and repo info
    st.markdown(
        f'''<div class="repo-header">
            <h1>{repo_name}</h1>
            <p>Repository by <a href="https://github.com/{username}" target="_blank">{username}</a></p>
        </div>''',
        unsafe_allow_html=True
    )
    
    # Add tabs for different views
    tab1, tab2 = st.tabs(["📁 File Structure", "ℹ Repository Info"])
    
    with tab1:
        # Display repository structure with interactive elements
        st.markdown('<div class="directory-structure">', unsafe_allow_html=True)
        st.markdown('<div class="structure-header">Directory Structure Summary</div>', unsafe_allow_html=True)
        
        # Get top-level structure
        if 'top_level_structure' not in st.session_state:
            st.session_state.top_level_structure = get_repo_structure(username, repo_name)
        
        if st.session_state.top_level_structure:
            render_interactive_directory_structure(st.session_state.top_level_structure)
        else:
            st.warning("No files found in this repository or access denied.")
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Repository Information")
        with st.spinner("Loading repository info..."):
            # Get basic repo info from GitHub API
            try:
                response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}")
                if response.status_code == 200:
                    repo_info = response.json()
                    
                    # Display repo stats in columns
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Stars", repo_info.get("stargazers_count", 0))
                    with col2:
                        st.metric("Forks", repo_info.get("forks_count", 0))
                    with col3:
                        st.metric("Watchers", repo_info.get("watchers_count", 0))
                    
                    # Display repo description and other info
                    st.markdown("#### Description")
                    st.write(repo_info.get("description", "No description provided"))
                    
                    st.markdown("#### Repository Details")
                    st.write(f"*Language:* {repo_info.get('language', 'Not specified')}")
                    st.write(f"*Created:* {repo_info.get('created_at', '').split('T')[0]}")
                    st.write(f"*Last Updated:* {repo_info.get('updated_at', '').split('T')[0]}")
                    
                    # Add links to GitHub
                    st.markdown("#### Links")
                    st.markdown(f"[View on GitHub]({repo_info.get('html_url')})")
                    if repo_info.get('homepage'):
                        st.markdown(f"[Homepage]({repo_info.get('homepage')})")
                    
                    # Show license info if available
                    if repo_info.get('license') and repo_info['license'].get('name'):
                        st.write(f"*License:* {repo_info['license'].get('name')}")
                else:
                    st.error("Could not fetch repository information")
            except Exception as e:
                st.error(f"Error: {str(e)}")