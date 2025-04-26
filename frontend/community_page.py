import streamlit as st
import datetime
import random
import uuid
import json
import time
import pandas as pd
import requests
import os

def generate_default_messages():
    """Generate default messages for the community page"""
    return [
        {
            "id": "1",
            "user": "SarahDev",
            "content": "Has anyone worked with GitHub Actions for CI/CD pipelines? I'm trying to set up automated testing for my Python project.",
            "timestamp": "2025-04-15 09:45",
            "likes": 12,
            "replies": [
                {
                    "user": "DevOpsGuru",
                    "content": "I've implemented several pipelines with GitHub Actions. What specific error are you getting? Make sure your yaml file has the correct indentation.",
                    "timestamp": "2025-04-15 10:03"
                },
                {
                    "user": "PythonMaster",
                    "content": "Also check if your tests require any environment variables that might not be available in the GitHub Actions environment.",
                    "timestamp": "2025-04-15 10:15"
                }
            ]
        },
        {
            "id": "2", 
            "user": "NewbieCode",
            "content": "I'm new to open source and would like to start contributing. Any recommendations for beginner-friendly repositories or projects?",
            "timestamp": "2025-04-16 08:30",
            "likes": 24,
            "replies": [
                {
                    "user": "OpenSourceAdvocate",
                    "content": "Welcome to open source! Check out repositories tagged with 'good-first-issue' or 'beginner-friendly'. The Python Software Foundation and Mozilla have great onboarding for new contributors.",
                    "timestamp": "2025-04-16 09:12"
                }
            ]
        },
        {
            "id": "3",
            "user": "FrontendDev",
            "content": "Just released a new React component library that integrates with GitHub's API for visualizing repository data. It's open source and looking for contributors!",
            "timestamp": "2025-04-16 11:20",
            "likes": 15,
            "replies": []
        }
    ]

def get_supported_languages():
    """Return a dictionary of supported languages and their codes"""
    return {
        "English": "en-IN",
        "Hindi": "hi-IN",
        "Bengali": "bn-IN",
        "Telugu": "te-IN",
        "Tamil": "ta-IN",
        "Marathi": "mr-IN",
        "Gujarati": "gu-IN",
        "Kannada": "kn-IN",
        "Malayalam": "ml-IN",
        "Punjabi": "pa-IN"
    }

def translate_text(text, target_language_code):
    """
    Translate text to the specified language using Sarvam API
    
    Args:
        text (str): Original text
        target_language_code (str): Target language code for translation
        
    Returns:
        str: Translated text
    """
    if target_language_code == "en-IN" or not text:
        return text
        
    try:
        api_key = os.environ.get('SARVAM_API_KEY')
        if not api_key:
            st.warning("Sarvam API key not found. Please set SARVAM_API_KEY in environment variables.")
            return text

        url = "https://api.sarvam.ai/translate"
        payload = {
            "input": text,
            "source_language_code": "en-IN",  
            "target_language_code": target_language_code
        }
        
        headers = {
            "Content-Type": "application/json",
            "api-subscription-key": api_key
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("translated_text", text)
        else:
            return text
    except Exception as e:
        return text

def load_css():
    st.markdown("""
    <style>
        /* Global Styles */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        .main .block-container {
            padding-top: 0.5rem;
            padding-bottom: 1rem;
            max-width: 100%;
            margin: 0 auto;
        }
        
        /* Header styles */
        .page-title {
            font-weight: 700;
            background: linear-gradient(90deg, #3a7bd5 0%, #6c5ce7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.75rem;
            font-size: 2.5rem;
            text-align: center;
        }
        
        /* Message cards */
        .message-card {
            background: rgba(40, 40, 60, 0.9);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .message-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }
        
        /* Message header */
        .message-header {
            display: flex;
            align-items: center;
            margin-bottom: 0.75rem;
        }
        
        /* Avatar styles */
        .message-avatar {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: linear-gradient(135deg, #3a7bd5, #6c5ce7);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 16px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        /* User info styles */
        .message-user-info {
            margin-left: 10px;
        }
        
        .message-user {
            font-weight: 600;
            color: rgba(255, 255, 255, 0.95);
            font-size: 14px;
        }
        
        .message-time {
            color: rgba(255, 255, 255, 0.6);
            font-size: 12px;
        }
        
        /* Message content */
        .message-content {
            color: rgba(255, 255, 255, 0.85);
            line-height: 1.5;
            margin-bottom: 0.75rem;
            font-size: 14px;
        }
        
        /* Reply styles */
        .message-reply {
            margin-left: 30px;
            margin-bottom: 8px;
            padding: 8px 12px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
            border-left: 2px solid rgba(255, 255, 255, 0.2);
        }
        
        .reply-header {
            display: flex;
            align-items: center;
            margin-bottom: 6px;
        }
        
        .reply-avatar {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: linear-gradient(135deg, #3a7bd5, #00b894);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 12px;
        }
        
        .reply-user-info {
            margin-left: 8px;
        }
        
        .reply-user {
            font-weight: 600;
            font-size: 13px;
            color: rgba(255, 255, 255, 0.9);
        }
        
        .reply-time {
            color: rgba(255, 255, 255, 0.6);
            font-size: 11px;
        }
        
        .reply-content {
            color: rgba(255, 255, 255, 0.8);
            font-size: 13px;
            line-height: 1.4;
        }
        
        /* Stats styles */
        @keyframes pulse {
            0% {
                box-shadow: 0 4px 15px rgba(58, 123, 213, 0.4);
            }
            100% {
                box-shadow: 0 4px 20px rgba(108, 92, 231, 0.6);
            }
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin: 1.5rem auto;
            max-width: 800px;
        }
        
        .stat-container {
            padding: 1.5rem;
            border-radius: 12px;
            background: rgba(40, 40, 60, 0.85);
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 150px;
        }
        
        .stat-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }
        
        .stat-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
            transform: rotate(0deg);
            animation: rotate 8s linear infinite;
            pointer-events: none;
        }
        
        @keyframes rotate {
            0% {
                transform: rotate(0deg);
            }
            100% {
                transform: rotate(360deg);
            }
        }
        
        .stat-value {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(90deg, #3a7bd5, #6c5ce7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            position: relative;
            z-index: 10;
        }
        
        .stat-label {
            color: rgba(255, 255, 255, 0.85);
            font-size: 1.1rem;
            font-weight: 500;
            letter-spacing: 0.5px;
            position: relative;
            z-index: 10;
        }
        
        /* New Tags Style */
        .tags-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin: 1rem 0;
        }
        
        .tag-pill {
            padding: 6px 14px;
            border-radius: 20px;
            background: linear-gradient(135deg, rgba(58, 123, 213, 0.3), rgba(108, 92, 231, 0.3));
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.3s;
            display: inline-block;
            border: 1px solid rgba(58, 123, 213, 0.5);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .tag-pill:hover {
            transform: translateY(-3px) scale(1.05);
            background: linear-gradient(135deg, rgba(58, 123, 213, 0.5), rgba(108, 92, 231, 0.5));
            box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
            cursor: pointer;
        }
        
        /* Section titles */
        .section-title {
            font-weight: 700;
            margin-bottom: 1rem;
            font-size: 1.8rem;
            color: rgba(255, 255, 255, 0.95);
            text-align: center;
            background: linear-gradient(90deg, #3a7bd5, #6c5ce7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Input area */
        .stTextArea textarea {
            background-color: rgba(40, 40, 60, 0.9);
            color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
        }
        
        .stTextInput input {
            background-color: rgba(40, 40, 60, 0.9);
            color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
        }
        
        /* Button styles */
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            border-radius: 5px;
            transition: all 0.3s;
        }
        
        button:not(:disabled), [role="button"]:not(:disabled) {
            cursor: pointer;
        }

        /* Language selector */
        .language-selector {
            background: rgba(40, 40, 60, 0.8);
            border-radius: 8px;
            padding: 0.75rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }
        
        .language-label {
            color: rgba(255, 255, 255, 0.8);
            font-weight: 500;
            font-size: 0.9rem;
        }

        /* Comment section styles */
        .comment-section {
            margin-top: 1rem;
            background: rgba(40, 40, 60, 0.7);
            border-radius: 8px;
            padding: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .comment-header {
            font-weight: 600;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 0.5rem;
            font-size: 1rem;
        }
        
        .select-post {
            margin-bottom: 0.5rem;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(40, 40, 60, 0.5);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(100, 100, 140, 0.5);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(100, 100, 140, 0.7);
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .page-title {
                font-size: 1.8rem;
            }
            
            .stat-value {
                font-size: 2.5rem;
            }
        }

        /* Fix standard Streamlit elements */
        .stAlert {
            background-color: rgba(40, 40, 60, 0.9);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .stAlert a {
            color: #3a7bd5;
        }
        
        /* Fix the header padding */
        .css-18e3th9 {
            padding-top: 0 !important;
        }
        
        /* Fix the sidebar */
        .css-1d391kg {
            background-color: rgba(35, 35, 50, 0.95);
        }

        /* Translation toggle button */
        .translate-toggle {
            display: inline-block;
            margin-left: 10px;
            padding: 3px 8px;
            background: linear-gradient(135deg, rgba(58, 123, 213, 0.5), rgba(108, 92, 231, 0.5));
            border-radius: 4px;
            color: white;
            font-size: 0.7rem;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }
        
        .translate-toggle:hover {
            background: linear-gradient(135deg, rgba(58, 123, 213, 0.7), rgba(108, 92, 231, 0.7));
        }

        /* Language dropdown container */
        .language-dropdown-container {
            background: rgba(40, 40, 60, 0.9);
            border-radius: 8px;
            padding: 10px 15px;
            margin-bottom: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
        }
        
        .language-icon {
            margin-right: 10px;
            color: rgba(255, 255, 255, 0.8);
        }
    </style>
    """, unsafe_allow_html=True)

def display_messages(messages, target_language_code):
    """Display messages with optimized styling and translation capability"""
    for idx, msg in enumerate(messages):
        msg_id = f"msg_{msg['id']}"
        
        translated_content = translate_text(msg['content'], target_language_code)
        
        st.markdown(f"""
        <div class='message-card' id='{msg_id}'>
            <div class='message-header'>
                <div class='message-avatar'>{msg['user'][0].upper()}</div>
                <div class='message-user-info'>
                    <div class='message-user'>{msg['user']}</div>
                    <div class='message-time'>{msg['timestamp']}</div>
                </div>
            </div>
            <div class='message-content'>{translated_content}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if msg['replies']:
            for reply in msg['replies']:

                translated_reply = translate_text(reply['content'], target_language_code)
                
                st.markdown(f"""
                <div class='message-reply'>
                    <div class='reply-header'>
                        <div class='reply-avatar'>{reply['user'][0].upper()}</div>
                        <div class='reply-user-info'>
                            <div class='reply-user'>{reply['user']}</div>
                            <div class='reply-time'>{reply['timestamp']}</div>
                        </div>
                    </div>
                    <div class='reply-content'>{translated_reply}</div>
                </div>
                """, unsafe_allow_html=True)

def community_page():
    load_css()
    
    if "username" not in st.session_state:
        st.session_state.username = "Dev" + str(random.randint(1000, 9999))
    
    if "community_messages" not in st.session_state:
        st.session_state.community_messages = generate_default_messages()
    
    if "joined_community" not in st.session_state:
        st.session_state.joined_community = False
    
    if "language" not in st.session_state:
        st.session_state.language = "en-IN"  
    
    languages = get_supported_languages()
    
    lang_code = st.session_state.language
    
    stats_title = translate_text("Community Stats", lang_code)
    members_label = translate_text("Members", lang_code)
    online_label = translate_text("Online", lang_code)
    tags_title = translate_text("Popular Tags", lang_code)
    discussions_title = translate_text("Developer Discussions", lang_code)
    join_button_text = translate_text("Join Community", lang_code)
    welcome_text = translate_text("Welcome", lang_code)
    language_selector_text = translate_text("Select Language", lang_code)
    share_placeholder = translate_text("What's on your mind?", lang_code)
    post_button_text = translate_text("Post", lang_code)
    join_info_text = translate_text("Join the community to participate in discussions!", lang_code)
    comment_header_text = translate_text("Add a comment to an existing discussion", lang_code)
    select_post_text = translate_text("Select a discussion to comment on", lang_code)
    comment_placeholder = translate_text("Add your thoughts here...", lang_code)
    comment_button_text = translate_text("Comment", lang_code)
    
    st.markdown(f'<div class="section-title">{stats_title}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="stats-section">', unsafe_allow_html=True)
    
    cols = st.columns(2)
    
    with cols[0]:
       
        st.markdown(f"""
        <div class="stat-container">
            <div class="stat-value">2,453</div>
            <div class="stat-label">{members_label}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with cols[1]:
        
        st.markdown(f"""
        <div class="stat-container">
            <div class="stat-value">187</div>
            <div class="stat-label">{online_label}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    
    st.markdown(f'<div class="section-title">{tags_title}</div>', unsafe_allow_html=True)
    
    
    tag_names = ["#Python", "#WebDev", "#ML", "#GitHub", "#JavaScript", "#ReactJS"]
    translated_tags = [tag if "#" not in tag else tag for tag in tag_names]  
    
   
    tags_html = '<div class="tags-container">'
    for tag in translated_tags:
        tags_html += f'<div class="tag-pill">{tag}</div>'
    tags_html += '</div>'
    
    st.markdown(tags_html, unsafe_allow_html=True)
    
    st.markdown(f'<h2 class="page-title">{discussions_title}</h2>', unsafe_allow_html=True)
    
    if not st.session_state.joined_community:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(join_button_text, use_container_width=True):
                st.session_state.joined_community = True
                st.rerun()
    else:
        st.success(f"{welcome_text}, {st.session_state.username}!")
    
    st.markdown(f'<div class="language-dropdown-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown(f"<div class='language-label'>{language_selector_text}:</div>", unsafe_allow_html=True)
    
    with col2:
        selected_language = st.selectbox(
            "",  
            options=list(languages.keys()),
            index=list(languages.keys()).index("English" if "English" in languages else list(languages.keys())[0]),
            key="language_dropdown",
            label_visibility="collapsed"  
        )
        
        
        if st.session_state.language != languages[selected_language]:
            st.session_state.language = languages[selected_language]
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    
    display_messages(st.session_state.community_messages, st.session_state.language)
    
    
    if st.session_state.joined_community:
        new_message = st.text_area("Share your thoughts", height=80, max_chars=500, placeholder=share_placeholder)
        
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button(post_button_text):
                if new_message:
                    
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    new_post = {
                        "id": str(uuid.uuid4()),
                        "user": st.session_state.username,
                        "content": new_message,
                        "timestamp": current_time,
                        "likes": 0,
                        "replies": []
                    }
                    st.session_state.community_messages.insert(0, new_post)
                    st.rerun()
    else:
        st.info(join_info_text)    
        
        st.markdown('<div class="comment-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="comment-header">{comment_header_text}</div>', unsafe_allow_html=True)
        
        post_options = {}
        for msg in st.session_state.community_messages:
           
            display_text = msg['content'][:30] + "..." if len(msg['content']) > 30 else msg['content']
            
            
            post_options[msg['id']] = f"{msg['user']}: {display_text}"
        
        selected_post_id = st.selectbox(select_post_text, 
                                        options=list(post_options.keys()),
                                        format_func=lambda x: post_options[x],
                                        key="comment_post_selector")
        

        comment_text = st.text_area("Your comment", height=68, max_chars=300, 
                                   placeholder=comment_placeholder,
                                   key="comment_textarea")
        

        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button(comment_button_text):
                if comment_text:

                    for msg in st.session_state.community_messages:
                        if msg['id'] == selected_post_id:
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                            new_reply = {
                                "user": st.session_state.username,
                                "content": comment_text,
                                "timestamp": current_time
                            }
                            msg['replies'].append(new_reply)
                            st.rerun()
                            break
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    community_page()