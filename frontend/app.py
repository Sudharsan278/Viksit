import streamlit as st
import requests
from urllib.parse import urljoin
import json
import time

# Set page configuration with a premium look
st.set_page_config(
    page_title="GitHub Repository Browser",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium look and feel
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .repo-header {
        background-color: #1e2230;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 4px solid #4CAF50;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .file-item {
        background-color: #1e2230;
        padding: 10px 15px;
        border-radius: 5px;
        margin: 5px 0;
        transition: all 0.3s;
        border-left: 2px solid transparent;
    }
    .file-item:hover {
        border-left: 2px solid #4CAF50;
        background-color: #2d3748;
        cursor: pointer;
    }
    .file-icon {
        margin-right: 10px;
        font-size: 1.2em;
    }
    .folder-content {
        margin-left: 25px;
        border-left: 1px dashed #4a5568;
        padding-left: 15px;
    }
    .breadcrumb {
        display: flex;
        flex-wrap: wrap;
        padding: 8px 0;
        margin-bottom: 20px;
        background-color: #1e2230;
        border-radius: 5px;
        padding: 10px;
    }
    .breadcrumb-item {
        display: inline-block;
        margin-right: 5px;
    }
    .breadcrumb-item:after {
        content: '>';
        margin-left: 5px;
        color: #718096;
    }
    .breadcrumb-item:last-child:after {
        content: '';
    }
    .breadcrumb-item a {
        color: #63b3ed;
        text-decoration: none;
    }
    .breadcrumb-item a:hover {
        text-decoration: underline;
    }
    .breadcrumb-item.active {
        color: #e2e8f0;
    }
    .back-button {
        background-color: #2d3748;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
        margin-bottom: 20px;
        display: inline-flex;
        align-items: center;
        transition: all 0.3s;
    }
    .back-button:hover {
        background-color: #4a5568;
    }
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 40px;
    }
    .search-container {
        background-color: #1e2230;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stTextInput>div>div>input {
        background-color: #2d3748;
        color: white;
        border: 1px solid #4a5568;
    }
    .stSelectbox>div>div>div {
        background-color: #2d3748;
        color: white;
        border: 1px solid #4a5568;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        border-radius: 5px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #3d8b40;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2d3748;
        border-left: 4px solid #4299e1;
    }
    .chat-message.assistant {
        background-color: #1e2230;
        border-left: 4px solid #4CAF50;
    }
    .chat-message .message {
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Constants
BACKEND_URL = "http://localhost:8080/api/"

def get_repositories(username):
    """Fetch repositories for the given username from the Django backend"""
    with st.spinner("Fetching repositories..."):
        response = requests.get(urljoin(BACKEND_URL, f"repositories/{username}/"))
        if response.status_code == 200:
            return response.json()["repos"]
        else:
            st.error(f"Error fetching repositories: {response.text}")
            return []

def get_repo_structure(username, repo_name, path=""):
    """Fetch repository structure from the Django backend"""
    with st.spinner("Loading repository structure..."):
        url = urljoin(BACKEND_URL, f"repo-structure/{username}/{repo_name}/")
        if path:
            url += f"?path={path}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["structure"]
        else:
            st.error(f"Error fetching repository structure: {response.text}")
            return []

def render_tree_structure(username, repo_name, structure, current_path="", expanded_paths=None):
    """Render the repository structure as an interactive tree"""
    if expanded_paths is None:
        expanded_paths = st.session_state.get('expanded_paths', set())
    
    for item in structure:
        item_path = f"{current_path}/{item['name']}" if current_path else item['name']
        item_key = f"{username}/{repo_name}/{item_path}"
        
        if item["type"] == "dir":
            is_expanded = item_key in expanded_paths
            
            # Directory header with expand/collapse functionality
            col1, col2 = st.columns([0.95, 0.05])
            with col1:
                expander_icon = "📂" if not is_expanded else "📁"
                if st.button(f"{expander_icon} {item['name']}", key=f"dir_{item_key}", help="Click to expand/collapse"):
                    if item_key in expanded_paths:
                        expanded_paths.remove(item_key)
                    else:
                        expanded_paths.add(item_key)
                        # Fetch subdirectory content if not already fetched
                        if item_key not in st.session_state.get('fetched_paths', {}):
                            subfolder_structure = get_repo_structure(username, repo_name, item_path)
                            st.session_state.setdefault('fetched_paths', {})[item_key] = subfolder_structure
                    
                    st.session_state['expanded_paths'] = expanded_paths
                    st.rerun()
            
            # If directory is expanded, show its contents
            if is_expanded:
                with st.container():
                    st.markdown('<div class="folder-content">', unsafe_allow_html=True)
                    
                    # Use cached subfolder structure if available
                    subfolder_structure = st.session_state.get('fetched_paths', {}).get(item_key)
                    if subfolder_structure:
                        render_tree_structure(username, repo_name, subfolder_structure, item_path, expanded_paths)
                    else:
                        with st.spinner(f"Loading {item['name']}..."):
                            subfolder_structure = get_repo_structure(username, repo_name, item_path)
                            st.session_state.setdefault('fetched_paths', {})[item_key] = subfolder_structure
                            render_tree_structure(username, repo_name, subfolder_structure, item_path, expanded_paths)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            # File item with icon based on file type
            file_extension = item['name'].split('.')[-1].lower() if '.' in item['name'] else ''
            icon = get_file_icon(file_extension)
            
            col1, col2 = st.columns([0.95, 0.05])
            with col1:
                st.markdown(
                    f'<div class="file-item"><span class="file-icon">{icon}</span> {item["name"]}</div>',
                    unsafe_allow_html=True
                )
            
            # If the file has a download URL, provide it
            if item.get("download_url"):
                with st.expander("File Options", expanded=False):
                    st.markdown(f"[View Raw File]({item['download_url']})")
                    st.markdown(f"[Download]({item['download_url']})")

def get_file_icon(extension):
    """Return appropriate icon based on file extension"""
    icons = {
        'py': '🐍',
        'js': '📜',
        'html': '🌐',
        'css': '🎨',
        'md': '📝',
        'json': '📋',
        'yml': '⚙',
        'yaml': '⚙',
        'txt': '📄',
        'gitignore': '🔒',
        'sh': '⚡',
        'bat': '⚡',
        'jpg': '🖼',
        'jpeg': '🖼',
        'png': '🖼',
        'gif': '🖼',
        'svg': '🖼',
        'pdf': '📕',
        'doc': '📘',
        'docx': '📘',
        'xls': '📊',
        'xlsx': '📊',
        'csv': '📊',
        'zip': '📦',
        'rar': '📦',
        'tar': '📦',
        'gz': '📦',
    }
    return icons.get(extension, '📄')

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
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Explore Repository Structure", help="View the repository's file structure"):
                            # Reset any previously stored structures
                            if 'fetched_paths' in st.session_state:
                                del st.session_state['fetched_paths']
                            if 'expanded_paths' in st.session_state:
                                del st.session_state['expanded_paths']
                                
                            # Store selection for structure page
                            st.session_state.username = username
                            st.session_state.repo_name = selected_repo
                            st.session_state.page = "repo_structure"
                            st.rerun()
                    with col2:
                        if st.button("Ask AI About This Repo", help="Use Groq to analyze this repository"):
                            # Store selection for Groq page
                            st.session_state.username = username
                            st.session_state.repo_name = selected_repo
                            st.session_state.page = "groq_assistant"
                            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Adding some information about the application
        with st.expander("About this App"):
            st.markdown("""
            This GitHub Repository Explorer allows you to:
            - Browse any public GitHub repository
            - Explore its file structure in an interactive tree view
            - View and download files
            - Analyze repositories and code using Groq AI
            
            The application uses GitHub's API to fetch repository data in real time.
            """)

def repo_structure_page():
    """Page to display repository structure in a premium UI"""
    username = st.session_state.username
    repo_name = st.session_state.repo_name
    
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
        # Initialize repository structure if not already fetched
        if 'root_structure' not in st.session_state:
            with st.spinner("Loading repository structure..."):
                st.session_state.root_structure = get_repo_structure(username, repo_name)
        
        # Render the tree structure
        if st.session_state.root_structure:
            st.markdown("### Repository Contents")
            render_tree_structure(username, repo_name, st.session_state.root_structure)
        else:
            st.warning("No files found in this repository or access denied.")
    
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

def groq_assistant_page():
    """Page for Groq AI assistant to analyze repositories and code"""
    username = st.session_state.username
    repo_name = st.session_state.repo_name
    
    # Back button
    if st.button("⬅ Back to Search", key="back_from_groq"):
        st.session_state.page = "main"
        st.rerun()
    
    st.markdown('<h1 style="text-align: center;">Groq Repository Assistant</h1>', unsafe_allow_html=True)
    
    # Repository header with user and repo info
    st.markdown(
        f'''<div class="repo-header">
            <h1>{repo_name}</h1>
            <p>Repository by <a href="https://github.com/{username}" target="_blank">{username}</a></p>
        </div>''',
        unsafe_allow_html=True
    )
    
    # Initialize session state variables if not already present
    if 'groq_history' not in st.session_state:
        st.session_state.groq_history = []
    
    # Query section
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Query type selection
    query_type = st.radio(
        "Query Type",
        ["Repository Analysis", "Code File Analysis"],
        horizontal=True
    )
    
    if query_type == "Repository Analysis":
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
                with st.spinner("Processing your query with Groq..."):
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
    
    else:  # Code File Analysis
        # Fetch repository structure for file selection
        try:
            if 'root_structure' not in st.session_state:
                with st.spinner("Loading repository structure..."):
                    response = requests.get(urljoin(BACKEND_URL, f"repo-structure/{username}/{repo_name}/"))
                    if response.status_code == 200:
                        st.session_state.root_structure = response.json()["structure"]
            
            # Extract file list for selection
            if 'file_list' not in st.session_state:
                st.session_state.file_list = []
                
                def extract_files(structure, path=""):
                    files = []
                    for item in structure:
                        item_path = f"{path}/{item['name']}" if path else item['name']
                        if item["type"] == "file" and item.get("download_url"):
                            files.append({
                                "path": item_path,
                                "url": item["download_url"]
                            })
                        elif item["type"] == "dir":
                            # Fetch directory contents if needed
                            dir_structure = get_repo_structure(username, repo_name, item_path)
                            if dir_structure:
                                files.extend(extract_files(dir_structure, item_path))
                    return files
                
                with st.spinner("Building file list..."):
                    if 'root_structure' in st.session_state:
                        st.session_state.file_list = extract_files(st.session_state.root_structure)
            
            # File selection dropdown
            if st.session_state.file_list:
                file_paths = [file["path"] for file in st.session_state.file_list]
                selected_file = st.selectbox("Select a file to analyze", file_paths)
                
                # Find the URL for the selected file
                selected_file_url = next((file["url"] for file in st.session_state.file_list if file["path"] == selected_file), None)
                
                if selected_file_url:
                    # Code analysis query
                    query = st.text_area(
                        "Ask about this code file",
                        height=100,
                        help="Example: 'Explain what this code does' or 'How can I optimize this code?'"
                    )
                    
                    if st.button("Submit Code Query"):
                        if not query.strip():
                            st.warning("Please enter a query before submitting.")
                        else:
                            with st.spinner("Processing your query with Groq..."):
                                try:
                                    # Send query to backend
                                    response = requests.post(
                                        urljoin(BACKEND_URL, "query-code/"),
                                        json={
                                            "file_url": selected_file_url,
                                            "query": query
                                        }
                                    )
                                    
                                    if response.status_code == 200:
                                        result = response.json()
                                        
                                        # Add to history
                                        st.session_state.groq_history.append({
                                            "query": f"[File: {selected_file}] {query}",
                                            "response": result["response"],
                                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                                        })
                                        
                                        # Force a rerun to show the new response
                                        st.rerun()
                                    else:
                                        st.error(f"Error: {response.text}")
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
            else:
                st.warning("No files found in this repository or structure not loaded.")
        except Exception as e:
            st.error(f"Error loading repository structure: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display query history
    if st.session_state.groq_history:
        st.markdown("## Conversation History")
        
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
    
    # About section
    with st.expander("About Groq Integration"):
        st.markdown("""
        This feature integrates Groq's powerful language models to analyze repositories and code files.
        
        You can:
        - Ask questions about repository purpose, structure, and potential improvements
        - Analyze specific code files for understanding, optimization, or debugging
        - Track your query history for future reference
        
        This integration uses LangChain to connect with Groq's API and process your queries.
        """)

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