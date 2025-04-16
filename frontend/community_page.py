import streamlit as st
import datetime
import random
import uuid

def community_page():
    # Remove default Streamlit margins and padding
    st.markdown("""
        <style>
            .main .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
                max-width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state for messages if it doesn't exist
    if "community_messages" not in st.session_state:
        st.session_state.community_messages = generate_default_messages()
    
    # Layout with two columns
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("<h2 class='page-title'>Developer Community</h2>", unsafe_allow_html=True)
        
        # Message container with custom scrolling
        st.markdown("<div class='messages-container'>", unsafe_allow_html=True)
        display_messages(st.session_state.community_messages)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Message input area
        st.markdown("<div class='message-form-container'>", unsafe_allow_html=True)
        st.text_input("Write your message:", key="message_placeholder", disabled=True, label_visibility="collapsed")
        
        with st.form(key="message_form", clear_on_submit=True):
            message_input = st.text_area("Write your message:", height=120, key="message_text", label_visibility="collapsed", 
                                        placeholder="Share your thoughts with the community...")
            
            cols = st.columns([4, 1])
            with cols[1]:
                submit_button = st.form_submit_button("Send Message", use_container_width=True)
            
            if submit_button and message_input.strip():
                new_message = {
                    "id": str(uuid.uuid4()),
                    "user": st.session_state.username if st.session_state.username else "GuestUser",
                    "content": message_input,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "likes": 0,
                    "replies": []
                }
                st.session_state.community_messages.append(new_message)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='community-sidebar'>", unsafe_allow_html=True)
        st.markdown("<h3 class='sidebar-title'>Community Stats</h3>", unsafe_allow_html=True)
        
        # Stats in a more visual way
        active_members = random.randint(120, 250)
        topics = random.randint(30, 50)
        messages_today = random.randint(25, 100)
        
        st.markdown(f"""
        <div class='stat-container'>
            <div class='stat-value'>{active_members}</div>
            <div class='stat-label'>Active Members</div>
        </div>
        
        <div class='stat-container'>
            <div class='stat-value'>{topics}</div>
            <div class='stat-label'>Topics</div>
        </div>
        
        <div class='stat-container'>
            <div class='stat-value'>{messages_today}</div>
            <div class='stat-label'>Messages Today</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 class='sidebar-title'>Trending Tags</h3>", unsafe_allow_html=True)
        
        tags = ["#python", "#react", "#machinelearning", "#webdev", "#github", "#opensource"]
        st.markdown("<div class='tag-container'>", unsafe_allow_html=True)
        for tag in tags:
            st.markdown(f"<span class='tag'>{tag}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<h3 class='sidebar-title'>Community Guidelines</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class='guidelines'>
            <div class='guideline-item'>
                <div class='guideline-icon'>✓</div>
                <div>Be respectful and supportive</div>
            </div>
            <div class='guideline-item'>
                <div class='guideline-icon'>✓</div>
                <div>Share knowledge freely</div>
            </div>
            <div class='guideline-item'>
                <div class='guideline-icon'>✓</div>
                <div>Give credit where it's due</div>
            </div>
            <div class='guideline-item'>
                <div class='guideline-icon'>✓</div>
                <div>Keep discussions constructive</div>
            </div>
            <div class='guideline-item'>
                <div class='guideline-icon'>✓</div>
                <div>Help others grow</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def display_messages(messages):
    for msg in messages:
        with st.container():
            st.markdown(f"""
            <div class='message-card'>
                <div class='message-header'>
                    <div class='message-avatar'>{msg['user'][0].upper()}</div>
                    <div class='message-user-info'>
                        <div class='message-user'>{msg['user']}</div>
                        <div class='message-time'>{msg['timestamp']}</div>
                    </div>
                </div>
                <div class='message-content'>{msg['content']}</div>
                <div class='message-actions'>
                    <span class='action-btn like-btn'>👍 {msg['likes']}</span>
                    <span class='action-btn reply-btn'>💬 {len(msg['replies'])}</span>
                    <span class='action-btn share-btn'>📤 Share</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display replies if any
            if msg['replies']:
                for reply in msg['replies']:
                    st.markdown(f"""
                    <div class='message-reply'>
                        <div class='reply-header'>
                            <div class='reply-avatar'>{reply['user'][0].upper()}</div>
                            <div class='reply-user-info'>
                                <div class='reply-user'>{reply['user']}</div>
                                <div class='reply-time'>{reply['timestamp']}</div>
                            </div>
                        </div>
                        <div class='reply-content'>{reply['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)

def generate_default_messages():
    """Generate some default messages for the community page"""
    return [
        {
            "id": "1",
            "user": "SarahDev",
            "content": "Has anyone worked with GitHub Actions for CI/CD pipelines? I'm trying to set up automated testing for my Python project, but I'm running into some configuration issues.",
            "timestamp": "2025-04-15 09:45",
            "likes": 12,
            "replies": [
                {
                    "user": "DevOpsGuru",
                    "content": "I've implemented several pipelines with GitHub Actions. What specific error are you getting? Make sure your yaml file has the correct indentation and that your test environment matches your development environment.",
                    "timestamp": "2025-04-15 10:03"
                },
                {
                    "user": "PythonMaster",
                    "content": "Also check if your tests require any environment variables that might not be available in the GitHub Actions environment. You can set secrets in your repository settings.",
                    "timestamp": "2025-04-15 10:15"
                }
            ]
        },
        {
            "id": "2", 
            "user": "NewbieCode",
            "content": "I'm new to open source and would like to start contributing. Any recommendations for beginner-friendly repositories or projects that welcome new contributors?",
            "timestamp": "2025-04-16 08:30",
            "likes": 24,
            "replies": [
                {
                    "user": "OpenSourceAdvocate",
                    "content": "Welcome to open source! Check out repositories tagged with 'good-first-issue' or 'beginner-friendly'. The Python Software Foundation and Mozilla have great onboarding for new contributors. Also, documentation improvements are always appreciated!",
                    "timestamp": "2025-04-16 09:12"
                }
            ]
        },
        {
            "id": "3",
            "user": "FrontendDev",
            "content": "Just released a new React component library that integrates with GitHub's API for visualizing repository data. It's open source and looking for contributors! Check it out: github.com/frontenddev/react-github-vis",
            "timestamp": "2025-04-16 11:20",
            "likes": 15,
            "replies": []
        },
        {
            "id": "4",
            "user": "CodeReviewer",
            "content": "What are your code review best practices? I'm trying to improve our team's process to make reviews more effective without becoming bottlenecks.",
            "timestamp": "2025-04-16 12:05",
            "likes": 18,
            "replies": [
                {
                    "user": "SeniorArchitect",
                    "content": "We've had success with a tiered approach: automated checks for style/linting, then focused reviews on logic and architecture. Set clear expectations for response times (24 hours max) and keep reviews small (<300 lines when possible).",
                    "timestamp": "2025-04-16 12:38"
                }
            ]
        }
    ]