import streamlit as st
import requests
import base64
from urllib.parse import urljoin
import os
import json

# Constants
BACKEND_URL = "http://localhost:8080/api/"

def load_css(css_file):
    """Load CSS from a file using a more robust path resolution"""
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Build path to CSS file
        css_path = os.path.join(current_dir, css_file)
        
        with open(css_path, 'r') as f:
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

def get_sarvam_api_key():
    """Get the Sarvam API key from environment variables"""
    api_key = os.environ.get('SARVAM_API_KEY')
    if not api_key:
        raise ValueError("Sarvam API key not found. Please set SARVAM_API_KEY in environment variables.")
    return api_key

def get_documentation(username, repo_name):
    """
    Generate comprehensive documentation for a repository using the backend API
    
    Args:
        username (str): GitHub username
        repo_name (str): Repository name
        
    Returns:
        str: Markdown-formatted documentation
    """
    try:
        # Send request to backend
        response = requests.post(
            urljoin(BACKEND_URL, "generate-documentation/"),
            json={
                "username": username,
                "repo_name": repo_name
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["documentation"]
        else:
            # Fallback to generate documentation directly
            return generate_documentation_fallback(username, repo_name)
    except Exception as e:
        # Fallback if backend request fails
        return generate_documentation_fallback(username, repo_name)

def generate_documentation_fallback(username, repo_name):
    """
    Fallback method to generate documentation using GitHub API directly
    
    Args:
        username (str): GitHub username
        repo_name (str): Repository name
        
    Returns:
        str: Markdown-formatted documentation
    """
    try:
        # Get repository information
        repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
        repo_response = requests.get(repo_url)
        
        if repo_response.status_code != 200:
            return "Unable to fetch repository information."
        
        repo_data = repo_response.json()
        
        # Get README content if available
        readme_url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
        readme_response = requests.get(readme_url)
        readme_content = ""
        
        if readme_response.status_code == 200:
            # GitHub returns README content in base64, decode it
            import base64
            readme_data = readme_response.json()
            readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
        
        # Format documentation
        documentation = f"""# {repo_data.get('name')} Documentation

## Overview
{repo_data.get('description', 'No description provided')}

### Repository Information
- **Owner:** {repo_data.get('owner', {}).get('login', 'Unknown')}
- **Stars:** {repo_data.get('stargazers_count', 0)}
- **Forks:** {repo_data.get('forks_count', 0)}
- **Open Issues:** {repo_data.get('open_issues_count', 0)}
- **Primary Language:** {repo_data.get('language', 'Not specified')}
- **Created:** {repo_data.get('created_at', '').split('T')[0]}
- **Last Updated:** {repo_data.get('updated_at', '').split('T')[0]}

## Purpose
This repository appears to be focused on {repo_data.get('language', 'software development')} 
and may be used for {get_repo_purpose(repo_data)}.

## README Content
{readme_content if readme_content else "No README found in this repository."}
"""
        return documentation
    except Exception as e:
        return f"Documentation generation failed: {str(e)}"

def get_repo_purpose(repo_data):
    """Determine repository purpose based on name and description"""
    name = repo_data.get('name', '').lower()
    description = repo_data.get('description', '').lower()
    language = repo_data.get('language', '').lower()
    
    if 'api' in name or 'api' in description:
        return "creating or consuming APIs"
    elif 'web' in name or 'site' in description:
        return "web development"
    elif 'app' in name or 'mobile' in description:
        return "application development"
    elif 'tool' in name or 'utility' in description:
        return "providing developer tools or utilities"
    elif 'data' in name or 'analysis' in description:
        return "data analysis or processing"
    elif 'ml' in name or 'machine learning' in description:
        return "machine learning or AI development"
    elif language == 'python':
        return "Python-based software development"
    elif language == 'javascript':
        return "JavaScript-based software development"
    else:
        return "software development or research"