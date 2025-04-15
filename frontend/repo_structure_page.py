import streamlit as st
import requests
from utils import get_repo_structure, render_interactive_directory_structure, get_file_content
from urllib.parse import urljoin
import time
from utils import BACKEND_URL

def repo_structure_page():
    """Page to display repository structure with integrated AI analysis"""
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
    
    # Initialize session state variables for AI analysis
    if 'groq_history' not in st.session_state:
        st.session_state.groq_history = []
    
    # Repository Information Section at the top
    st.markdown("## Repository Information")
    with st.spinner("Loading repository info..."):
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
                
                # License info if available
                if repo_info.get('license') and repo_info['license'].get('name'):
                    st.write(f"*License:* {repo_info['license'].get('name')}")
            else:
                st.error("Could not fetch repository information")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # AI Analysis Section
    st.markdown("## Ask AI About This Repository")
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Repository analysis query
    query = st.text_area(
        "Ask about the repository structure, purpose, or potential improvements",
        height=100,
        help="Example: 'What is the main purpose of this repository?' or 'How could I improve the structure?'"
    )
    
    if st.button("Submit Repository Query"):
        if not query.strip():
            st.warning("Please enter a query before submitting.")
        else:
            with st.spinner("Processing your query with AI..."):
                try:
                    # Send query to backend
                    response = requests.post(
                        urljoin(BACKEND_URL, "query-repository/"),
                        json={
                            "username": username,
                            "repo_name": repo_name,
                            "query": query
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Add to history
                        st.session_state.groq_history.append({
                            "query": query,
                            "response": result["response"],
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                        # Force a rerun to show the new response
                        st.rerun()
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display query history
    if st.session_state.groq_history:
        st.markdown("### AI Analysis Results")
        
        for i, item in enumerate(st.session_state.groq_history):
            # User query
            st.markdown(f'<div class="chat-message user">'
                      f'<div><strong>You asked:</strong></div>'
                      f'<div class="message">{item["query"]}</div>'
                      f'</div>', unsafe_allow_html=True)
            
            # AI response
            st.markdown(f'<div class="chat-message assistant">'
                      f'<div><strong>AI response:</strong></div>'
                      f'<div class="message">{item["response"]}</div>'
                      f'</div>', unsafe_allow_html=True)
        
        if st.button("Clear History"):
            st.session_state.groq_history = []
            st.rerun()
    
    # Directory Structure Section
    st.markdown("## Repository Structure")
    # Display repository structure with interactive elements
    st.markdown('<div class="directory-structure">', unsafe_allow_html=True)
    st.markdown('<div class="structure-header">Directory Structure Explorer</div>', unsafe_allow_html=True)
    
    # Get top-level structure
    if 'top_level_structure' not in st.session_state:
        st.session_state.top_level_structure = get_repo_structure(username, repo_name)
    
    if st.session_state.top_level_structure:
        render_interactive_directory_structure(st.session_state.top_level_structure)
    else:
        st.warning("No files found in this repository or access denied.")
        
    st.markdown('</div>', unsafe_allow_html=True)


def file_view_page():
    """Page to display file content with integrated code analysis"""
    username = st.session_state.username
    repo_name = st.session_state.repo_name
    file_path = st.session_state.file_path
    
    # Back button
    if st.button("⬅ Back to Repository Structure", key="back_to_structure"):
        st.session_state.view_file = False
        st.rerun()
    
    # Get and display file content
    content, filename = get_file_content(username, repo_name, file_path)
    
    # Display file name and content
    st.markdown(f"""<div class="file-header">
        <h2>{filename}</h2>
    </div>""", unsafe_allow_html=True)
    
    # Initialize session state variables for code analysis
    if 'code_analysis_history' not in st.session_state:
        st.session_state.code_analysis_history = []
    
    # Display file content
    st.code(content, language="python")
    
    # Option to download file
    file_extension = filename.split('.')[-1].lower() if '.' in filename else 'txt'
    st.download_button(
        label="Download File",
        data=content,
        file_name=filename,
        mime=f"text/{file_extension}"
    )
    
    # Code Analysis Section
    st.markdown("## Ask AI About This Code")
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Code analysis query
    code_query = st.text_area(
        "Ask about this code file",
        height=100,
        help="Example: 'Explain what this code does' or 'How can I optimize this code?'"
    )
    
    if st.button("Submit Code Query"):
        if not code_query.strip():
            st.warning("Please enter a query before submitting.")
        else:
            with st.spinner("Processing your query with AI..."):
                try:
                    # Construct the file URL (GitHub raw content URL format)
                    file_url = f"https://raw.githubusercontent.com/{username}/{repo_name}/master/{file_path}"
                    
                    # Send query to backend
                    response = requests.post(
                        urljoin(BACKEND_URL, "query-code/"),
                        json={
                            "file_url": file_url,
                            "query": code_query
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Add to history
                        st.session_state.code_analysis_history.append({
                            "query": code_query,
                            "response": result["response"],
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                        # Force a rerun to show the new response
                        st.rerun()
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display code query history
    if st.session_state.code_analysis_history:
        st.markdown("### Code Analysis Results")
        
        for i, item in enumerate(st.session_state.code_analysis_history):
            # User query
            st.markdown(f'<div class="chat-message user">'
                      f'<div><strong>You asked:</strong></div>'
                      f'<div class="message">{item["query"]}</div>'
                      f'</div>', unsafe_allow_html=True)
            
            # AI response
            st.markdown(f'<div class="chat-message assistant">'
                      f'<div><strong>AI response:</strong></div>'
                      f'<div class="message">{item["response"]}</div>'
                      f'</div>', unsafe_allow_html=True)
        
        if st.button("Clear Code Analysis History"):
            st.session_state.code_analysis_history = []
            st.rerun()