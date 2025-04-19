import streamlit as st
import requests
from utils import get_repo_structure, render_interactive_directory_structure, get_file_content
from urllib.parse import urljoin
import time
from utils import BACKEND_URL
import os
from utils import get_documentation
import json
from dotenv import load_dotenv
import base64
import re

load_dotenv()

def translate_documentation(documentation, target_language_code):
    """
    Translate documentation to the specified language using Sarvam API
    
    Args:
        documentation (str): Original documentation text
        target_language_code (str): Target language code for translation
        
    Returns:
        str: Translated documentation
    """
    try:
        # Get API key from environment variables
        api_key = os.environ.get('SARVAM_API_KEY')
        if not api_key:
            st.warning("Sarvam API key not found. Please set SARVAM_API_KEY in environment variables.")
            return documentation

        # Prepare the request payload as per Sarvam API specs
        url = "https://api.sarvam.ai/translate"
        payload = {
            "input": documentation,
            "source_language_code": "en-IN",  # Assuming original documentation is in English
            "target_language_code": target_language_code
        }
        
        headers = {
            "Content-Type": "application/json",
            "api-subscription-key": api_key
        }
        
        # Make API request to Sarvam
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("translated_text", documentation)
        else:
            # Fallback to adding a note about translation failure
            st.error(f"Translation failed: {response.text}")
            return f"[Translation to {target_language_code} failed - showing English version]\n\n{documentation}"
    except Exception as e:
        # Return original with error note if translation fails
        st.error(f"Translation error: {str(e)}")
        return f"[Translation error: {str(e)}]\n\n{documentation}"

def text_to_speech(text, language_code, speaker="meera"):
    """
    Convert text to speech using Sarvam API
    
    Args:
        text (str): Text to convert to speech
        language_code (str): Target language code
        speaker (str): Speaker voice to use
        
    Returns:
        bytes: Audio data in base64 encoded format or None if error
    """
    try:
        api_key = os.environ.get('SARVAM_API_KEY')
        if not api_key:
            st.warning("Sarvam API key not found. Please set SARVAM_API_KEY in environment variables.")
            return None

        # Limit text to first 1000 characters
        text_to_speak = text[:1000]
        
        # Prepare the request payload
        url = "https://api.sarvam.ai/text-to-speech"
        payload = {
            "inputs": [text_to_speak],  # Using only first 1000 chars
            "target_language_code": language_code,
            "speaker": "meera",
            "pitch": 1.0,
            "pace": 1.0,
            "loudness": 1.0,
            "speech_sample_rate": 16000,
            "enable_preprocessing": True,
            "model": "bulbul:v1"
        }
        
        headers = {
            "Content-Type": "application/json",
            "api-subscription-key": api_key
        }
        
        # Make API request to Sarvam
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            # Return the audio content (base64 encoded)
            return result.get("audios", [None])[0]
        else:
            st.error(f"Text-to-speech failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Text-to-speech error: {str(e)}")
        return None
    
    
def get_audio_player_html(audio_data):
    """Generate HTML for audio player with base64 encoded audio data"""
    audio_html = f"""
        <audio controls autoplay="false">
            <source src="data:audio/wav;base64,{audio_data}" type="audio/wav">
            Your browser does not support the audio element.
        </audio>
    """
    return audio_html

def extract_overview_content(documentation_text):
    """
    Extract the content under the Overview heading, and only that content.
    
    Args:
        documentation_text (str): The full documentation text
        
    Returns:
        str: Just the content under the Overview heading
    """
    # First try to match the Overview section using regex
    # This looks for any level of heading with "Overview" text and captures the content until the next heading
    overview_pattern = re.compile(r'#{1,6}\s+Overview\s*\n+(.*?)(?=\n#{1,6}\s+|\Z)', re.DOTALL)
    overview_match = overview_pattern.search(documentation_text)
    
    if overview_match:
        # Return the content under the Overview heading, cleaned up
        return overview_match.group(1).strip()
    
    # If regex approach fails, try the split approach
    if "# Overview" in documentation_text or "## Overview" in documentation_text or "### Overview" in documentation_text:
        for heading_level in range(1, 7):  # Try different heading levels (# to ######)
            heading = '#' * heading_level + ' Overview'
            if heading in documentation_text:
                parts = documentation_text.split(heading, 1)
                if len(parts) > 1:
                    # Get content after the heading
                    content_after_heading = parts[1].strip()
                    
                    # Find the next heading
                    next_heading_match = re.search(r'\n#{1,6}\s+', content_after_heading)
                    if next_heading_match:
                        # Extract content up to the next heading
                        return content_after_heading[:next_heading_match.start()].strip()
                    else:
                        # If no next heading, use all the remaining content
                        return content_after_heading.strip()
    
    # Fallback to looking for "Overview" text as a paragraph header (not a markdown heading)
    if "\nOverview\n" in documentation_text:
        parts = documentation_text.split("\nOverview\n", 1)
        if len(parts) > 1:
            content_after_header = parts[1].strip()
            
            # Find the next blank line (paragraph break)
            next_para_match = re.search(r'\n\s*\n', content_after_header)
            if next_para_match:
                return content_after_header[:next_para_match.start()].strip()
            else:
                return content_after_header.strip()
    
    # If all else fails, try to find paragraphs after title sections
    paragraphs = documentation_text.split('\n\n')
    for i, para in enumerate(paragraphs):
        if "Overview" in para and i+1 < len(paragraphs):
            return paragraphs[i+1].strip()
    
    # Last resort: just return the first paragraph that's not a heading
    for para in paragraphs:
        if not para.strip().startswith('#') and len(para.strip()) > 30:  # Likely a real paragraph
            return para.strip()
    
    # Ultimate fallback: just the first 500 chars if nothing else works
    return documentation_text[:500].strip()

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
    
    # Initialize session state variables for documentation
    if 'repo_documentation' not in st.session_state:
        st.session_state.repo_documentation = None
    if 'overview_text' not in st.session_state:
        st.session_state.overview_text = None
    if 'audio_cache' not in st.session_state:
        st.session_state.audio_cache = {}

    # Documentation Section
    st.markdown("## Repository Documentation")
    
    # Generate documentation if it doesn't exist
    if st.session_state.repo_documentation is None:
        with st.spinner("Generating documentation..."):
            try:
                # Get documentation in English
                english_documentation = get_documentation(username, repo_name)
                st.session_state.repo_documentation = english_documentation
                
                # Extract overview section for TTS and cache it
                st.session_state.overview_text = extract_overview_content(english_documentation)
            except Exception as e:
                st.error(f"Error generating documentation: {str(e)}")
                st.session_state.repo_documentation = "Documentation unavailable due to an error."
                st.session_state.overview_text = "Documentation unavailable due to an error."
    
    # Display documentation
    documentation_text = st.session_state.repo_documentation
    overview_text = st.session_state.overview_text
    
    # Display documentation
    st.markdown(documentation_text)
    
    # Text-to-speech section for the documentation overview
    # Create cache key for the audio
    cache_key = f"overview_{hash(overview_text[:500])}"
    
    # Add Text-to-Speech button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🔊 Listen", key="tts_button"):
            with st.spinner("Generating audio..."):
                # Check if we have cached audio
                if cache_key in st.session_state.audio_cache:
                    audio_data = st.session_state.audio_cache[cache_key]
                else:
                    # Get audio data
                    audio_data = text_to_speech(
                        overview_text,
                        language_code="en-IN",
                        speaker="sonia"
                    )
                    
                    # Cache the audio if successful
                    if audio_data:
                        st.session_state.audio_cache[cache_key] = audio_data
                
                # Store current audio in session state to display
                if audio_data:
                    st.session_state.current_audio = audio_data
                    st.rerun()
    
    # Display audio player if audio is available
    if 'current_audio' in st.session_state and st.session_state.current_audio:
        st.markdown("### Audio Overview")
        st.markdown(get_audio_player_html(st.session_state.current_audio), unsafe_allow_html=True)
        if st.button("❌ Close Audio"):
            del st.session_state.current_audio
            st.rerun()
    
    # Initialize session state variables for AI analysis
    if 'groq_history' not in st.session_state:
        st.session_state.groq_history = []
    
    # Repository Information Section
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