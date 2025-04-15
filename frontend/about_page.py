import streamlit as st

def about_page():
    """About page for GitHub Repository Browser application"""
    
    st.markdown('<h1 style="text-align: center;">About GitHub Repository Browser</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Overview
    
    GitHub Repository Browser is a comprehensive tool for developers to explore, analyze, and interact with GitHub repositories. 
    Built with Streamlit and powered by AI, this application provides an intuitive interface for repository exploration, 
    code editing, and related resource discovery.
    
    ## Features
    
    ### Repository Structure Explorer
    - View file and directory structure
    - Browse through repository contents
    - Analyze repository organization
    
    ### Code Editor
    - View and edit code files
    - Syntax highlighting for various programming languages
    - Create new files and folders
    
    ### Resource Finder
    - Discover tutorials related to repository technologies
    - Find official documentation
    - Browse similar projects and examples
    - Custom search with AI-enhanced results
    
    ### AI-Powered Features
    - Smart search suggestions
    - Code analysis and insights
    - Repository context awareness
    
    ## Technology Stack
    
    - **Frontend**: Streamlit for interactive web interface
    - **Backend**: Python with FastAPI
    - **AI Components**: Groq API for enhanced search results
    - **External APIs**: GitHub API, Google Custom Search
    
    ## Getting Started
    
    1. Sign in with your GitHub credentials
    2. Search for a repository by username and repository name
    3. Explore the repository structure
    4. Use the code editor to view and modify files
    5. Find related resources using the Resource Finder
    
    ## Contact
    
    For questions, suggestions, or bug reports, please reach out to us on GitHub or via email at support@githubrepoexplorer.com.
    
    ## Version
    
    Current Version: 1.0.0
    """)
    
    # Team information
    st.markdown("## Meet the Team")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### Lead Developer
        
        **Alex Johnson**
        
        Full-stack developer with expertise in Python and web technologies.
        
        [GitHub Profile](https://github.com/)
        """)
    
    with col2:
        st.markdown("""
        ### UX Designer
        
        **Sarah Williams**
        
        Experienced UX designer focused on creating intuitive user interfaces.
        
        [Portfolio](https://example.com)
        """)
    
    with col3:
        st.markdown("""
        ### AI Engineer
        
        **Michael Chen**
        
        Specialist in AI integration and natural language processing.
        
        [LinkedIn](https://linkedin.com)
        """)
    
    # Disclaimer
    st.markdown("---")
    st.markdown("""
    ## Disclaimer
    
    This application is not affiliated with GitHub. It's an independent tool designed to enhance the GitHub experience.
    All GitHub data is accessed through official GitHub APIs in accordance with their terms of service.
    """)