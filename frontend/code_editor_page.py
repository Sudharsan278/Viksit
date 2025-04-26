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
from dotenv import load_dotenv

load_dotenv()

def code_editor_page():
    """Interactive code editor page for viewing and editing repository files with Groq AI assistant integration"""
    
    
    if not st.session_state.get("username") or not st.session_state.get("repo_name"):
        st.warning("No repository selected. Please select a repository from the main page first.")
        if st.button("Go to Main Page"):
            st.session_state.page = "main"
            st.rerun()
        return
    
    username = st.session_state.username
    repo_name = st.session_state.repo_name
    
    
    if 'previous_repo' not in st.session_state:
        st.session_state.previous_repo = f"{username}/{repo_name}"
    elif st.session_state.previous_repo != f"{username}/{repo_name}":

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

        st.session_state.file_tree = get_repo_structure(username, repo_name)

        st.session_state.previous_repo = f"{username}/{repo_name}"
    
    st.markdown('<h1 style="text-align: center;">Code Editor</h1>', unsafe_allow_html=True)
    

    st.markdown(
        f'''<div class="repo-header">
            <h1>{repo_name}</h1>
            <p>Repository by <a href="https://github.com/{username}" target="_blank">{username}</a></p>
        </div>''',
        unsafe_allow_html=True
    )
    
    # Initialize session state 
    if 'current_file' not in st.session_state:
        st.session_state.current_file = None
    if 'file_content' not in st.session_state:
        st.session_state.file_content = ""
    if 'edited_files' not in st.session_state:
        
        st.session_state.edited_files = {}
    if 'file_tree' not in st.session_state:
        
        if 'top_level_structure' in st.session_state:
            st.session_state.file_tree = st.session_state.top_level_structure
        else:
            
            st.session_state.file_tree = get_repo_structure(username, repo_name)
    
    if 'view_file' not in st.session_state:
        st.session_state.view_file = False
    if 'file_path' not in st.session_state:
        st.session_state.file_path = None
    
    if 'groq_history' not in st.session_state:
        st.session_state.groq_history = []
    
    if 'compilation_result' not in st.session_state:
        st.session_state.compilation_result = None
    
   
    if st.button("⬅ Back to Repository Structure", key="back_to_repo"):
        st.session_state.page = "repo_structure"
        st.rerun()
    
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### File Explorer")
        
        
        def render_interactive_directory_structure(structure, path_prefix=""):
            """Render the repository structure with collapsible folders and file links"""
            for item in structure:
                item_path = f"{path_prefix}/{item['name']}" if path_prefix else item['name']
                item_id = f"tree_{item_path.replace('/', '_')}"
                
                if item["type"] == "dir":
                    
                    folder_key = f"folder_{item_id}"
                    
                   
                    if folder_key not in st.session_state:
                        st.session_state[folder_key] = False
                    
                   
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
                    
                    
                    if st.session_state[folder_key]:
                        
                        with st.container():
                            st.markdown('<div class="folder-contents">', unsafe_allow_html=True)
                            
                            if "children" in item and item["children"]:
                                
                                render_interactive_directory_structure(item["children"], item_path)
                            else:
                                
                                children = get_repo_structure(
                                    st.session_state.username, 
                                    st.session_state.repo_name, 
                                    item_path
                                )
                                render_interactive_directory_structure(children, item_path)
                                
                            st.markdown('</div>', unsafe_allow_html=True)
                else:
                    
                    file_extension = item['name'].split('.')[-1].lower() if '.' in item['name'] else ''
                    icon = get_file_icon(file_extension)
                    
                    
                    col1, col2, col3 = st.columns([0.05, 0.05, 0.9])
                    
                    with col1:
                        
                        st.write("")
                        
                    with col2:
                        
                        st.markdown(f"<span class='file-icon'>{icon}</span>", unsafe_allow_html=True)
                        
                    with col3:
                        
                        if st.button(f"{item['name']}", key=f"file_{item_id}", help=f"View {item['name']}"):
                            
                            st.session_state.file_path = item_path
                            st.session_state.current_file = item_path
                            
                            
                            if item_path in st.session_state.edited_files:
                                st.session_state.file_content = st.session_state.edited_files[item_path]
                            else:
                                
                                content, _ = get_file_content(username, repo_name, item_path)
                                st.session_state.file_content = content
                                
                                st.session_state.edited_files[item_path] = content
                            
                            st.session_state.view_file = True
                            st.rerun()
        
        
        if st.session_state.file_tree:
            render_interactive_directory_structure(st.session_state.file_tree)
        else:
            st.warning("No repository structure available. Fetching now...")
            
            try:
                st.session_state.file_tree = get_repo_structure(username, repo_name)
                st.rerun()
            except Exception as e:
                st.error(f"Error fetching repository structure: {str(e)}")
    
    with col2:
        if st.session_state.view_file and st.session_state.current_file:
            st.markdown(f"### Editing: {st.session_state.current_file}")
            
            
            file_ext = os.path.splitext(st.session_state.current_file)[1]
            
            # Tabs for Editor, Groq Assistant, and Code Compiler
            editor_tab, groq_tab, compiler_tab = st.tabs(["Code Editor", "Groq Assistant", "Compile & Run"])
            
            with editor_tab:
                
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
                
               
                new_content = st.text_area(
                    "File Content",
                    value=st.session_state.file_content,
                    height=400,
                    key="code_editor"
                )
                
                
                col_a, col_b = st.columns([1, 4])
                with col_a:
                    if st.button("Save Changes"):
                        
                        st.session_state.edited_files[st.session_state.current_file] = new_content
                        st.session_state.file_content = new_content
                        st.success(f"Changes to {st.session_state.current_file} saved locally!")
                with col_b:
                    if st.button("Discard Changes"):
                        
                        if st.session_state.current_file in st.session_state.edited_files:
                            
                            content, _ = get_file_content(username, repo_name, st.session_state.current_file)
                            st.session_state.file_content = content
                            st.session_state.edited_files[st.session_state.current_file] = content
                            st.success("Changes discarded. Reverted to original content.")
                        st.rerun()
            
            with groq_tab:
                st.markdown("### Groq AI Assistant")
                st.markdown("Ask questions about this code file, upload images, or get AI-assisted suggestions.")
                
                
                query = st.text_area(
                    "What would you like to ask about this code?",
                    height=100,
                    help="Example: 'Explain what this code does', 'Suggest optimizations', or 'Generate a similar function'"
                )
                
                
                uploaded_image = st.file_uploader("Upload an image (optional)", type=['png', 'jpg', 'jpeg'])
                

                if st.button("Submit Query"):
                    if not query.strip() and uploaded_image is None:
                        st.warning("Please enter a query or upload an image before submitting.")
                    else:
                        with st.spinner("Processing your query with Groq..."):
                            try:
                                
                                current_content = st.session_state.edited_files.get(
                                    st.session_state.current_file, 
                                    st.session_state.file_content
                                )
                                
                                
                                file_url = f"https://raw.githubusercontent.com/{username}/{repo_name}/main/{st.session_state.current_file}"
                                
                                
                                payload = {
                                    "file_url": file_url,  
                                    "query": query,
                                    "file_content": current_content  
                                }
                                
                                
                                if uploaded_image is not None:
                                
                                    image_bytes = uploaded_image.getvalue()
                                    payload["image"] = base64.b64encode(image_bytes).decode('utf-8')
                                
                                
                                response = requests.post(
                                    urljoin(BACKEND_URL, "query-code/"),
                                    json=payload,
                                    timeout=60  
                                )
                                
                                if response.status_code == 200:
                                    result = response.json()
                                    
                                    
                                    history_entry = {
                                        "query": f"[File: {st.session_state.current_file}] {query}",
                                        "response": result["response"],
                                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                                        "has_image": uploaded_image is not None
                                    }
                                    
                                    if uploaded_image is not None:

                                        history_entry["image_name"] = uploaded_image.name
                                    
                                    st.session_state.groq_history.append(history_entry)
                                    

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
                

                if st.session_state.groq_history:
                    st.markdown("## Conversation History")
                    

                    st.markdown('<div class="conversation-container">', unsafe_allow_html=True)
                    
                    for i, item in enumerate(st.session_state.groq_history):

                        query_text = item["query"]
                        if item.get("has_image", False):
                            query_text += f' [with image: {item.get("image_name", "uploaded")}]'
                        
                        st.markdown(f'<div class="chat-message user">'
                                  f'<div><strong>You asked:</strong></div>'
                                  f'<div class="message">{query_text}</div>'
                                  f'</div>', unsafe_allow_html=True)
                        

                        st.markdown(f'<div class="chat-message assistant">'
                                  f'<div><strong>AI response:</strong></div>'
                                  f'<div class="message">{item["response"]}</div>'
                                  f'</div>', unsafe_allow_html=True)
                        

                        if "```" in item["response"]:
                            if st.button(f"Apply this code", key=f"apply_{i}"):

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

                                    main_code = max(code_blocks, key=len)

                                    st.session_state.file_content = main_code
                                    st.session_state.edited_files[st.session_state.current_file] = main_code
                                    st.success("Applied AI-generated code to the editor!")
                                    st.rerun()
                    

                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    if st.button("Clear History"):
                        st.session_state.groq_history = []
                        st.rerun()
            

            with compiler_tab:
                st.markdown("### Compile & Run Code")
                

                language_map = {
                    '.py': ('python3', '4'),
                    '.js': ('nodejs', '4'),
                    '.java': ('java', '4'),
                    '.c': ('c', '5'),
                    '.cpp': ('cpp', '5'),
                    '.cs': ('csharp', '4'),
                    '.php': ('php', '4'),
                    '.rb': ('ruby', '4'),
                    '.go': ('go', '4'),
                    '.rs': ('rust', '4'),
                    '.ts': ('typescript', '4'),
                    '.sh': ('bash', '4'),
                    '.pl': ('perl', '4'),
                    '.swift': ('swift', '4'),
                    '.kt': ('kotlin', '4'),
                    '.r': ('r', '4')
                }
                
                current_ext = os.path.splitext(st.session_state.current_file)[1].lower()
                is_compilable = current_ext in language_map
                
                if not is_compilable:
                    st.warning(f"The current file type ({current_ext}) is not supported for compilation. Supported file types: {', '.join(language_map.keys())}")
                else:
                  
                    jdoodle_lang, version_index = language_map[current_ext]
                    
                    
                    stdin = st.text_area("Standard Input (optional)", height=100, 
                                         help="Enter any input required by your program")
                    
                    
                    client_id = os.getenv("JDOODLE_CLIENT_ID")
                    client_secret = os.getenv("JDOODLE_CLIENT_SECRET")
                    
                    if not client_id or not client_secret:
                        st.error("JDoodle API credentials not found in environment variables. Please add JDOODLE_CLIENT_ID and JDOODLE_CLIENT_SECRET to your .env file.")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            client_id = st.text_input("JDoodle Client ID", type="password")
                        with col2:
                            client_secret = st.text_input("JDoodle Client Secret", type="password")
                        
                        if not client_id or not client_secret:
                            st.info("Please enter your JDoodle API credentials to continue.")
                            return
                    
                    if st.button("Compile & Run"):
                        with st.spinner("Compiling and running code..."):
                            try:
                                current_content = st.session_state.edited_files.get(
                                    st.session_state.current_file, 
                                    st.session_state.file_content
                                )
                                
                                jdoodle_payload = {
                                    "clientId": client_id,
                                    "clientSecret": client_secret,
                                    "script": current_content,
                                    "stdin": stdin,
                                    "language": jdoodle_lang,
                                    "versionIndex": version_index,
                                    "compileOnly": False
                                }
                                
                               
                                jdoodle_response = requests.post(
                                    "https://api.jdoodle.com/v1/execute",
                                    json=jdoodle_payload,
                                    timeout=30  
                                )
                                
                                
                                if jdoodle_response.status_code == 200:
                                    result = jdoodle_response.json()
                                    st.session_state.compilation_result = result
                                    st.rerun()
                                else:
                                    st.error(f"Error from JDoodle API: {jdoodle_response.text}")
                                    
                            except requests.exceptions.RequestException as e:
                                st.error(f"Connection error with JDoodle: {str(e)}")
                            except Exception as e:
                                st.error(f"Unexpected error during compilation: {str(e)}")
                    
                    
                    if st.session_state.compilation_result:
                        result = st.session_state.compilation_result
                        
                        
                        with st.expander("Execution Results", expanded=True):
                            st.markdown("#### Program Output")
                            
                            
                            st.code(result.get("output", "No output"), language="text")
                            
                           
                            st.markdown("#### Execution Details")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Status Code", result.get("statusCode", "N/A"))
                            with col2:
                                st.metric("Memory Used", f"{result.get('memory', 'N/A')} KB")
                            with col3:
                                st.metric("CPU Time", f"{result.get('cpuTime', 'N/A')} sec")
                            
                           
                            if st.button("Copy Output to Clipboard"):
                                try:
                                    pyperclip.copy(result.get("output", ""))
                                    st.success("Output copied to clipboard!")
                                except Exception as e:
                                    st.error(f"Failed to copy to clipboard: {str(e)}")
                            
                            if st.button("Clear Results"):
                                st.session_state.compilation_result = None
                                st.rerun()
        else:
            st.info("Select a file from the explorer to start editing")