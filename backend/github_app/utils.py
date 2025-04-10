from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from django.conf import settings

def get_groq_llm(model_name="llama3-8b-8192"):
    """Initialize and return a Groq LLM instance"""
    # Retrieve API key from Django settings or environment variable
    api_key = getattr(settings, 'GROQ_API_KEY', os.environ.get('GROQ_API_KEY'))
    
    if not api_key:
        raise ValueError("Groq API key not found. Please set GROQ_API_KEY in environment variables or settings.")
    
    # Create Groq LLM instance
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