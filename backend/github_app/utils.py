from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from django.conf import settings
import requests

def get_github_token():
    """Helper function to get GitHub token from environment variable"""
    return os.environ.get('GITHUB_TOKEN')

def get_groq_llm(model_name="llama3-8b-8192"):
    """Initialize and return a Groq LLM instance"""
    api_key = getattr(settings, 'GROQ_API_KEY', os.environ.get('GROQ_API_KEY'))
    
    if not api_key:
        raise ValueError("Groq API key not found. Please set GROQ_API_KEY in environment variables or settings.")
    
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name=model_name
    )
    
    return llm

def process_repository_query(repository_details, query):
    """
    Process a query about a GitHub repository using Groq
    
    Args:
        repository_details (dict): Dictionary containing repository information
        query (str): User's query about the repository
        
    Returns:
        str: Response from Groq
    """
    # Initialize LLM
    llm = get_groq_llm()
    
    # Create prompt template
    template = """
    You are an AI assistant specialized in analyzing GitHub repositories.
    
    Repository Details:
    Name: {repo_name}
    Owner: {repo_owner}
    Description: {repo_description}
    Primary Language: {repo_language}
    
    User Query: {query}
    
    Please provide a helpful, accurate, and concise response to the query based on the repository information.
    """
    
    prompt = PromptTemplate(
        input_variables=["repo_name", "repo_owner", "repo_description", "repo_language", "query"],
        template=template
    )
    
    # Create chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Run chain
    response = chain.run(
        repo_name=repository_details.get('name', 'Unknown'),
        repo_owner=repository_details.get('owner', {}).get('login', 'Unknown'),
        repo_description=repository_details.get('description', 'No description available'),
        repo_language=repository_details.get('language', 'Unknown'),
        query=query
    )
    
    return response

def fetch_repository_details(username, repo_name):
    """
    Fetch repository details from GitHub API
    
    Args:
        username (str): GitHub username
        repo_name (str): Repository name
        
    Returns:
        dict: Repository details
    """
    # Get GitHub token
    token = get_github_token()
    
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
        
    url = f'https://api.github.com/repos/{username}/{repo_name}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching repository details: {response.status_code}")

def fetch_file_content(file_url):
    """
    Fetch file content from URL with GitHub token if needed
    
    Args:
        file_url (str): URL to fetch content from
        
    Returns:
        str: File content
    """
    headers = {}
    
    # Add GitHub token if it's a GitHub URL
    if 'github.com' in file_url:
        token = get_github_token()
        if token:
            headers['Authorization'] = f'token {token}'
    
    response = requests.get(file_url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error fetching file content: {response.status_code}")

def process_code_query(code_content, query):
    """
    Process a query about specific code using Groq
    
    Args:
        code_content (str): Content of the code file
        query (str): User's query about the code
        
    Returns:
        str: Response from Groq
    """
    # Initialize LLM
    llm = get_groq_llm()
    
    # Create prompt template
    template = """
    You are an AI coding assistant specialized in analyzing code.
    
    Code Content:
    
    {code_content}
    
    
    User Query: {query}
    
    Please provide a helpful, accurate, and concise response to the query based on the provided code.
    """
    
    prompt = PromptTemplate(
        input_variables=["code_content", "query"],
        template=template
    )
    
    # Create chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Run chain
    response = chain.run(
        code_content=code_content,
        query=query
    )
    
    return response

def process_google_search_results(search_results, query):
    """
    Process Google search results using Groq for better formatting and summarization
    
    Args:
        search_results (dict): Search results from Google Custom Search API
        query (str): User's original search query
        
    Returns:
        str: Formatted and enhanced response from Groq
    """
    # Initialize LLM
    llm = get_groq_llm()
    
    items = search_results.get('items', [])
    formatted_results = []
    
    for item in items[:5]:  
        formatted_results.append({
            'title': item.get('title', ''),
            'link': item.get('link', ''),
            'snippet': item.get('snippet', '')
        })
    
    
    results_text = ""
    for i, result in enumerate(formatted_results, 1):
        results_text += f"Result {i}:\n"
        results_text += f"Title: {result['title']}\n"
        results_text += f"Link: {result['link']}\n"
        results_text += f"Snippet: {result['snippet']}\n\n"
    
    # prompt template
    template = """
    You are an AI research assistant that helps format and enhance search results.
    
    Original Search Query: {query}
    
    Search Results:
    {results}
    
    Your task is to:
    1. Provide a brief summary of what these search results tell us about the query
    2. Identify the most relevant information from these results
    3. Format the information in a clear, structured way with markdown formatting
    4. Include any relevant links from the search results
    5. If the results don't seem to answer the query well, suggest alternative search terms
    
    Please provide your response in markdown format with appropriate headings, bullet points, and formatting to make it easy to read.
    """
    
    prompt = PromptTemplate(
        input_variables=["query", "results"],
        template=template
    )
    
    # Create chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Run chain
    response = chain.run(
        query=query,
        results=results_text
    )
    
    return response

def perform_google_search(query, api_key, cx_id, num_results=10):
    """
    Perform a Google search using the Custom Search JSON API
    
    Args:
        query (str): Search query
        api_key (str): Google API Key
        cx_id (str): Custom Search Engine ID
        num_results (int): Number of results to return
        
    Returns:
        dict: Search results
    """
    base_url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        'q': query,
        'key': api_key,
        'cx': cx_id,
        'num': num_results
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Search API error: {response.status_code}, {response.text}")