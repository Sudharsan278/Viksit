import streamlit as st
import requests
import time
from urllib.parse import urljoin
from utils import get_repo_structure, BACKEND_URL

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