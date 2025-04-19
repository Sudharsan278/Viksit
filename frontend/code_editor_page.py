import streamlit as st
import os
import json
import requests
import time
import base64 
import utils
from urllib.parse import urljoin
from utils import get_file_content, get_repo_structure, get_file_icon, BACKEND_URL
import pyperclip

def code_editor_page():
    """Interactive code editor page for viewing and editing repository files with Groq AI assistant integration"""
    
    # Check if username and repo_name are set
    if not st.session_state.get("username") or not st.session_state.get("repo_name"):
        st.warning("No repository selected. Please select a repository from the main page first.")
        if st.button("Go to Main Page"):
            st.session_state.page = "main"
            st.rerun()
        return
    
    username = st.session_state.username
    repo_name = st.session_state.repo_name
    
    # Clear edited files if repository has changed
    if 'previous_repo' not in st.session_state:
        st.session_state.previous_repo = f"{username}/{repo_name}"
    elif st.session_state.previous_repo != f"{username}/{repo_name}":
        # Repo has changed, reset all file-related state
        if 'edited_files' in st.session_state:
            st.session_state.edited_files = {}
        if 'current_file' in st.session_state:
            st.session_state.current_file = None
        if 'file_content' in st.session_state:
            st.session_state.file_content = ""
        if 'file_path' in st.session_state:
            st.session_state.file_path = None
        if 'view_file' in st.session_state:
            st.session_state.view_file = False
        # Force fetch the new repository structure
        st.session_state.file_tree = get_repo_structure(username, repo_name)
        # Update the previous repo marker
        st.session_state.previous_repo = f"{username}/{repo_name}"
    
    st.markdown('<h1 style="text-align: center;">Code Editor</h1>', unsafe_allow_html=True)
    
    # Repository header with user and repo info
    st.markdown(
        f'''<div class="repo-header">
            <h1>{repo_name}</h1>
            <p>Repository by <a href="https://github.com/{username}" target="_blank">{username}</a></p>
        </div>''',
        unsafe_allow_html=True
    )
    
    # Initialize session state for editor
    if 'current_file' not in st.session_state:
        st.session_state.current_file = None
    if 'file_content' not in st.session_state:
        st.session_state.file_content = ""
    if 'edited_files' not in st.session_state:
        # Dictionary to store locally edited file contents
        st.session_state.edited_files = {}
    if 'file_tree' not in st.session_state:
        # Use the repository structure from repo_structure_page
        if 'top_level_structure' in st.session_state:
            st.session_state.file_tree = st.session_state.top_level_structure
        else:
            # If not available, fetch it
            st.session_state.file_tree = get_repo_structure(username, repo_name)
    # Initialize view file state
    if 'view_file' not in st.session_state:
        st.session_state.view_file = False
    if 'file_path' not in st.session_state:
        st.session_state.file_path = None
    # Initialize Groq history if not present
    if 'groq_history' not in st.session_state:
        st.session_state.groq_history = []
    
    # Back button
    if st.button("⬅ Back to Repository Structure", key="back_to_repo"):
        st.session_state.page = "repo_structure"
        st.rerun()
    
    # Create layout with file explorer and editor
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### File Explorer")
        
        # Function from utils.py to render the interactive directory structure
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
                            st.session_state.current_file = item_path
                            
                            # Check if we've already fetched and possibly edited this file
                            if item_path in st.session_state.edited_files:
                                st.session_state.file_content = st.session_state.edited_files[item_path]
                            else:
                                # Fetch the actual file content from GitHub
                                content, _ = get_file_content(username, repo_name, item_path)
                                st.session_state.file_content = content
                                # Store the original content
                                st.session_state.edited_files[item_path] = content
                            
                            st.session_state.view_file = True
                            st.rerun()
        
        # Render the interactive directory structure if file tree exists
        if st.session_state.file_tree:
            render_interactive_directory_structure(st.session_state.file_tree)
        else:
            st.warning("No repository structure available. Fetching now...")
            # Attempt to fetch repository structure
            try:
                st.session_state.file_tree = get_repo_structure(username, repo_name)
                st.rerun()
            except Exception as e:
                st.error(f"Error fetching repository structure: {str(e)}")
    
    with col2:
        if st.session_state.view_file and st.session_state.current_file:
            st.markdown(f"### Editing: {st.session_state.current_file}")
            
            # Get file extension for compiler
            file_ext = os.path.splitext(st.session_state.current_file)[1]
            
            # Tabs for Editor and Groq Assistant
            editor_tab, groq_tab = st.tabs(["Code Editor", "Groq Assistant"])
            
            with editor_tab:
                # Determine language for syntax highlighting
                lang_map = {
                    '.py': 'python',
                    '.js': 'javascript',
                    '.html': 'html',
                    '.css': 'css',
                    '.json': 'json',
                    '.md': 'markdown',
                    '.txt': 'text'
                }
                language = lang_map.get(file_ext.lower(), 'text')
                
                # Code editor
                new_content = st.text_area(
                    "File Content",
                    value=st.session_state.file_content,
                    height=400,
                    key="code_editor"
                )
                
                # Update button
                col_a, col_b = st.columns([1, 4])
                with col_a:
                    if st.button("Save Changes"):
                        # Save changes locally in session state
                        st.session_state.edited_files[st.session_state.current_file] = new_content
                        st.session_state.file_content = new_content
                        st.success(f"Changes to {st.session_state.current_file} saved locally!")
                with col_b:
                    if st.button("Discard Changes"):
                        # Check if we have the original content (from first fetch)
                        if st.session_state.current_file in st.session_state.edited_files:
                            # Refetch content from GitHub
                            content, _ = get_file_content(username, repo_name, st.session_state.current_file)
                            st.session_state.file_content = content
                            st.session_state.edited_files[st.session_state.current_file] = content
                            st.success("Changes discarded. Reverted to original content.")
                        st.rerun()
            
            with groq_tab:
                st.markdown("### Groq AI Assistant")
                st.markdown("Ask questions about this code file, upload images, or get AI-assisted suggestions.")
                
                # Code analysis query
                query = st.text_area(
                    "What would you like to ask about this code?",
                    height=100,
                    help="Example: 'Explain what this code does', 'Suggest optimizations', or 'Generate a similar function'"
                )
                
                # Add image upload capability
                uploaded_image = st.file_uploader("Upload an image (optional)", type=['png', 'jpg', 'jpeg'])
                
                # Submit Query button
                if st.button("Submit Query"):
                    if not query.strip() and uploaded_image is None:
                        st.warning("Please enter a query or upload an image before submitting.")
                    else:
                        with st.spinner("Processing your query with Groq..."):
                            try:
                                # Use the current file content in the editor
                                current_content = st.session_state.edited_files.get(
                                    st.session_state.current_file, 
                                    st.session_state.file_content
                                )
                                
                                # Generate a fallback URL for compatibility with backend
                                file_url = f"https://raw.githubusercontent.com/{username}/{repo_name}/main/{st.session_state.current_file}"
                                
                                # Prepare payload with all required fields
                                payload = {
                                    "file_url": file_url,  # Keep the URL format as backend expects it
                                    "query": query,
                                    "file_content": current_content  # Send the content directly
                                }
                                
                                # Add image data to payload if image was uploaded
                                if uploaded_image is not None:
                                    # Read image bytes and encode to base64
                                    image_bytes = uploaded_image.getvalue()
                                    payload["image"] = base64.b64encode(image_bytes).decode('utf-8')
                                
                                # Send query to backend
                                response = requests.post(
                                    urljoin(BACKEND_URL, "query-code/"),
                                    json=payload,
                                    timeout=60  # Increase timeout for larger files
                                )
                                
                                if response.status_code == 200:
                                    result = response.json()
                                    
                                    # Add to history with image info if present
                                    history_entry = {
                                        "query": f"[File: {st.session_state.current_file}] {query}",
                                        "response": result["response"],
                                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                                        "has_image": uploaded_image is not None
                                    }
                                    
                                    # If there was an image, save thumbnail info
                                    if uploaded_image is not None:
                                        # Store image name in history for reference
                                        history_entry["image_name"] = uploaded_image.name
                                    
                                    st.session_state.groq_history.append(history_entry)
                                    
                                    # Force a rerun to show the new response
                                    st.rerun()
                                else:
                                    error_msg = response.text
                                    try:
                                        error_json = response.json()
                                        if "error" in error_json:
                                            error_msg = error_json["error"]
                                    except:
                                        pass
                                    
                                    st.error(f"Error: {error_msg}")
                            except requests.exceptions.RequestException as e:
                                st.error(f"Connection error: {str(e)}")
                                st.info("Check your internet connection or the backend service status.")
                            except Exception as e:
                                st.error(f"Unexpected error: {str(e)}")
                                st.write(f"Debug info: {type(e).__name__}")
                
                # Display query history
                if st.session_state.groq_history:
                    st.markdown("## Conversation History")
                    
                    # Start the conversation container with dark background
                    st.markdown('<div class="conversation-container">', unsafe_allow_html=True)
                    
                    for i, item in enumerate(st.session_state.groq_history):
                        # User query with image indicator if applicable
                        query_text = item["query"]
                        if item.get("has_image", False):
                            query_text += f' [with image: {item.get("image_name", "uploaded")}]'
                        
                        st.markdown(f'<div class="chat-message user">'
                                  f'<div><strong>You asked:</strong></div>'
                                  f'<div class="message">{query_text}</div>'
                                  f'</div>', unsafe_allow_html=True)
                        
                        # AI response
                        st.markdown(f'<div class="chat-message assistant">'
                                  f'<div><strong>AI response:</strong></div>'
                                  f'<div class="message">{item["response"]}</div>'
                                  f'</div>', unsafe_allow_html=True)
                        
                        # Apply button to apply changes if response contains code
                        if "```" in item["response"]:
                            if st.button(f"Apply this code", key=f"apply_{i}"):
                                # Extract code from markdown code blocks
                                code_blocks = []
                                lines = item["response"].split('\n')
                                in_code_block = False
                                current_block = []
                                
                                for line in lines:
                                    if line.startswith('```'):
                                        if in_code_block:
                                            code_blocks.append('\n'.join(current_block))
                                            current_block = []
                                        in_code_block = not in_code_block
                                    elif in_code_block:
                                        current_block.append(line)
                                
                                if code_blocks:
                                    # Use the largest code block (most likely the main implementation)
                                    main_code = max(code_blocks, key=len)
                                    # Update the file content
                                    st.session_state.file_content = main_code
                                    st.session_state.edited_files[st.session_state.current_file] = main_code
                                    st.success("Applied AI-generated code to the editor!")
                                    st.rerun()
                    
                    # Close the conversation container
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    if st.button("Clear History"):
                        st.session_state.groq_history = []
                        st.rerun()
            
        else:
            st.info("Select a file from the explorer to start editing")