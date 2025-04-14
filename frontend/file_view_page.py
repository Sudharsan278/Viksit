import streamlit as st
from utils import get_file_content

def file_view_page():
    """Page to display file content"""
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