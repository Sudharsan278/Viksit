import streamlit as st
import requests
import time
from urllib.parse import urljoin
from utils import BACKEND_URL

def resources_page():
    """Page for finding related resources using Google Custom Search API and Groq formatting"""
    username = st.session_state.username
    repo_name = st.session_state.repo_name
    
    st.markdown('<h1 style="text-align: center;">Find Related Resources</h1>', unsafe_allow_html=True)
    
    # Repository header with user and repo info
    st.markdown(
        f'''<div class="repo-header">
            <h1>{repo_name}</h1>
            <p>Repository by <a href="https://github.com/{username}" target="_blank">{username}</a></p>
        </div>''',
        unsafe_allow_html=True
    )
    
    # Initialize session state for search history
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    
    # Search section
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Get repository description to provide context
    try:
        if 'repo_description' not in st.session_state:
            with st.spinner("Fetching repository information..."):
                response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}")
                if response.status_code == 200:
                    repo_info = response.json()
                    st.session_state.repo_description = repo_info.get("description", "")
                    st.session_state.repo_language = repo_info.get("language", "")
                else:
                    st.session_state.repo_description = ""
                    st.session_state.repo_language = ""
    except Exception as e:
        st.error(f"Error fetching repository information: {str(e)}")
        st.session_state.repo_description = ""
        st.session_state.repo_language = ""
    
    # Search type selection
    search_type = st.radio(
        "Search Type",
        ["Tutorials", "Documentation", "Examples", "Custom Search"],
        horizontal=True
    )
    
    # Base search query with repo context
    base_query = f"{repo_name} {st.session_state.repo_language}"
    
    if search_type == "Tutorials":
        search_context = f"tutorials for {base_query}"
        placeholder = "Find tutorials for this repository's technology"
    elif search_type == "Documentation":
        search_context = f"documentation for {base_query}"
        placeholder = "Find official documentation for this repository's technology"
    elif search_type == "Examples":
        search_context = f"example projects using {base_query}"
        placeholder = "Find example projects using similar technology"
    else:  # Custom Search
        search_context = base_query
        placeholder = "Enter your custom search query"
    
    # Custom search input
    custom_query = st.text_input(f"Search query", 
                               value=search_context,
                               placeholder=placeholder)
    
    if st.button("Search for Resources"):
        if not custom_query.strip():
            st.warning("Please enter a search query before submitting.")
        else:
            with st.spinner("Searching for resources..."):
                try:
                    # Send query to backend
                    response = requests.post(
                        urljoin(BACKEND_URL, "google-search/"),
                        json={"query": custom_query}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Add to search history
                        st.session_state.search_history.append({
                            "query": custom_query,
                            "response": result["response"],
                            "raw_results": result.get("raw_results", []),
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                        # Force a rerun to show the new response
                        st.rerun()
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display search results
    if st.session_state.search_history:
        st.markdown("## Search Results")
        
        # Show most recent search result
        latest = st.session_state.search_history[-1]
        
        # Main results - formatted by Groq
        st.markdown(latest["response"])
        
        # Raw results in expandable section
        with st.expander("View Raw Search Results"):
            for i, raw_result in enumerate(latest["raw_results"]):
                st.markdown(
                    f'''<div class="search-result">
                        <div class="search-result-title">{raw_result.get("title", "No title")}</div>
                        <div class="search-result-link">{raw_result.get("link", "#")}</div>
                        <div class="search-result-snippet">{raw_result.get("snippet", "No description available")}</div>
                    </div>''',
                    unsafe_allow_html=True
                )
        
        # Previous searches
        if len(st.session_state.search_history) > 1:
            with st.expander("Previous Searches"):
                for i in range(len(st.session_state.search_history) - 2, -1, -1):
                    item = st.session_state.search_history[i]
                    st.markdown(f"### Search: {item['query']}")
                    st.markdown(f"*{item['timestamp']}*")
                    if st.button(f"Show Results", key=f"prev_search_{i}"):
                        # Move this item to the end of the list (make it current)
                        st.session_state.search_history.append(st.session_state.search_history.pop(i))
                        st.rerun()
        
        if st.button("Clear Search History"):
            st.session_state.search_history = []
            st.rerun()
    
    # About section
    with st.expander("About Resource Search"):
        st.markdown("""
        This feature helps you find valuable resources related to the repository by:
        
        - Automatically generating search queries based on repository context
        - Using Google's search API to find relevant content
        - Enhancing results with Groq's AI for better organization and relevance
        - Providing different search modes for tutorials, documentation, and examples
        
        Results are formatted for easy reading and include direct links to resources.
        """)