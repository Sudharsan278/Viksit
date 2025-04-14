import streamlit as st
import requests
import base64
from urllib.parse import urljoin

# Constants
BACKEND_URL = "http://localhost:8080/api/"

def load_css(css_file):
    """Load CSS from a file"""
    try:
        with open(css_file, 'r') as f:
            return f.read()
    except Exception as e:
        st.error(f"Error loading CSS file: {str(e)}")
        return ""

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

def get_file_content(username, repo_name, path):
    """Fetch file content from GitHub API"""
    with st.spinner("Loading file content..."):
        response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/contents/{path}")
        
        if response.status_code == 200:
            content_data = response.json()
            if content_data.get('encoding') == 'base64' and content_data.get('content'):
                try:
                    content = base64.b64decode(content_data['content']).decode('utf-8')
                    return content, content_data.get('name')
                except Exception as e:
                    return f"Error decoding content: {str(e)}", content_data.get('name')
            else:
                return "Content not available in text format.", content_data.get('name')
        else:
            return f"Error fetching file content: {response.text}", path

def get_file_icon(extension):
    """Return appropriate icon based on file extension"""
    icons = {
        'py': '📄',
        'js': '📄',
        'html': '📄',
        'css': '📄',
        'md': '📄',
        'json': '📄',
        'yml': '📄',
        'yaml': '📄',
        'txt': '📄',
        'gitignore': '📄',
        'sh': '📄',
        'bat': '📄',
        'jpg': '📄',
        'jpeg': '📄',
        'png': '📄',
        'gif': '📄',
        'svg': '📄',
        'pdf': '📄',
        'doc': '📄',
        'docx': '📄',
        'xls': '📄',
        'xlsx': '📄',
        'csv': '📄',
        'zip': '📄',
        'rar': '📄',
        'tar': '📄',
        'gz': '📄',
    }
    return icons.get(extension, '📄')

def render_interactive_directory_structure(structure, path_prefix=""):
    """Render the repository structure with collapsible folders and file links"""
    for item in structure:
        item_path = f"{path_prefix}/{item['name']}" if path_prefix else item['name']
        item_id = f"tree_{item_path.replace('/', '_')}"
        
        if item["type"] == "dir":
            # Create a unique key for this folder's state
            folder_key = f"folder_{item_id}"
            
            # Initialize folder state if not present
            if folder_key not in st.session_state:
                st.session_state[folder_key] = False
            
            # Create folder toggle header
            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                if st.button("➤", key=f"toggle_{folder_key}", help=f"Expand/Collapse {item['name']}"):
                    st.session_state[folder_key] = not st.session_state[folder_key]
                    st.rerun()
            
            with col2:
                st.markdown(
                    f"""
                    <div id="{item_id}" class="folder-toggle">
                        <span class="item-bullet">{'•' if not path_prefix else '◦'}</span>
                        <span class="tree-icon dir-icon">📁</span>
                        <span class="item-text">{item['name']}</span>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            # If folder is expanded, load and display children
            if st.session_state[folder_key]:
                # Create container for folder contents
                with st.container():
                    st.markdown('<div class="folder-contents">', unsafe_allow_html=True)
                    
                    if "children" in item and item["children"]:
                        # If we already have children data, use it
                        render_interactive_directory_structure(item["children"], item_path)
                    else:
                        # Fetch children if not loaded
                        children = get_repo_structure(
                            st.session_state.username, 
                            st.session_state.repo_name, 
                            item_path
                        )
                        render_interactive_directory_structure(children, item_path)
                        
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            # File with click functionality to view content
            file_extension = item['name'].split('.')[-1].lower() if '.' in item['name'] else ''
            icon = get_file_icon(file_extension)
            
            # Create columns for file item
            col1, col2, col3 = st.columns([0.05, 0.05, 0.9])
            
            with col1:
                # Empty space for alignment
                st.write("")
                
            with col2:
                # File icon
                st.markdown(f"<span class='file-icon'>{icon}</span>", unsafe_allow_html=True)
                
            with col3:
                # File name as a button but styled to look like text
                if st.button(f"{item['name']}", key=f"file_{item_id}", help=f"View {item['name']}"):
                    # Store file path to view content
                    st.session_state.file_path = item_path
                    st.session_state.view_file = True
                    st.rerun()