from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import process_repository_query, process_code_query, process_google_search_results, perform_google_search
import requests
import json
import os
import base64
from groq import Groq
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from django.shortcuts import render


def get_github_token():
    """Helper function to get GitHub token from environment variable"""
    return os.environ.get('GITHUB_TOKEN')


@api_view(['GET'])
def repositories(request, username):
    """Get all repositories for a GitHub user"""
    try:
        token = get_github_token()
        
        headers = {}
        if token:
            headers['Authorization'] = f'token {token}'
        
        response = requests.get(f'https://api.github.com/users/{username}/repos', headers=headers)
        
        if response.status_code == 200:
            repos = response.json()
            repo_list = [{'name': repo['name'], 'id': repo['id']} for repo in repos]
            return JsonResponse({'repos': repo_list})
        else:
            return JsonResponse({'error': f'Error fetching repositories: {response.status_code}'}, status=response.status_code)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def repo_structure(request, username, repo_name):
    """Get the structure of a specific repository with support for subpaths"""
    try:
        token = get_github_token()
        
        headers = {}
        if token:
            headers['Authorization'] = f'token {token}'
        
        path = request.GET.get('path', '')
        
        url = f'https://api.github.com/repos/{username}/{repo_name}/contents'
        if path:
            url += f'/{path}'
            
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            contents = response.json()
            
            if not isinstance(contents, list):
                contents = [contents]
                
            structure = []
            
            for item in contents:
                structure.append({
                    'name': item['name'],
                    'path': item['path'],
                    'type': item['type'],
                    'download_url': item.get('download_url'),
                    'url': item.get('url'),
                    'git_url': item.get('git_url')
                })
                
            return JsonResponse({'structure': structure})
        else:
            return JsonResponse({'error': f'Error fetching repository structure: {response.status_code}'}, status=response.status_code)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def encode_image(image_data):
    """Encode image data to base64 string"""
    if isinstance(image_data, str) and os.path.isfile(image_data):
        with open(image_data, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    elif not isinstance(image_data, str):
        return base64.b64encode(image_data).decode('utf-8')
    else:
        return image_data


def process_query_with_groq(text_query, image_data=None):
    """Process a query using Groq, with optional image data"""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    message_content = []
    
    if text_query:
        message_content.append({"type": "text", "text": text_query})
    
    if image_data:
        base64_image = encode_image(image_data)
        
        message_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
            },
        })
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message_content,
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )
    
    return chat_completion.choices[0].message.content

@api_view(['POST'])
def query_repository(request):
    try:
        data = request.data
        username = data.get('username')
        repo_name = data.get('repo_name')
        text_query = data.get('query')
        image_data = data.get('image')
        
        if not all([username, repo_name]) or (not text_query and not image_data):
            return Response({
                "error": "Username, repository name, and at least one of text query or image are required"
            }, status=400)
        
        token = get_github_token()
        headers = {}
        if token:
            headers['Authorization'] = f'token {token}'
            
        repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
        repo_response = requests.get(repo_url, headers=headers)
        
        if repo_response.status_code != 200:
            return Response({"error": "Repository not found"}, status=404)
        
        repo_data = repo_response.json()
        
        contents_url = f"https://api.github.com/repos/{username}/{repo_name}/contents"
        contents_response = requests.get(contents_url, headers=headers)
        
        repo_context = f"Repository: {repo_data['full_name']}\nDescription: {repo_data['description'] or 'No description'}\n"
        
        if contents_response.status_code == 200:
            contents = contents_response.json()
            repo_context += "\nRepository structure:\n"
            for item in contents:
                repo_context += f"- {item['name']} ({item['type']})\n"
        
        readme_url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
        try:
            readme_response = requests.get(readme_url, headers=headers)
            if readme_response.status_code == 200:
                readme_data = readme_response.json()
                readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
                repo_context += f"\nREADME content:\n{readme_content[:1000]}..."  
        except Exception:
            pass  

        full_text_query = f"{repo_context}\n\nUser query: {text_query}" if text_query else repo_context
        
        response = process_query_with_groq(full_text_query, image_data)
        
        return Response({"response": response})
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)    

@api_view(['POST'])
def query_code(request):
    try:
        data = request.data
        file_url = data.get('file_url')
        text_query = data.get('query')
        file_content = data.get('file_content')
        image_data = data.get('image')
        
        if (not text_query and not image_data):
            return Response({"error": "At least one of text query or image is required"}, status=400)
        
        if not file_content:
            if not file_url:
                return Response({"error": "Either file_content or file_url is required"}, status=400)
            
            token = get_github_token()
            headers = {}
            if token and 'github.com' in file_url:
                headers['Authorization'] = f'token {token}'
                
            try:
                file_response = requests.get(file_url, headers=headers)
                
                if file_response.status_code != 200:
                    return Response({"error": "File not found"}, status=404)
                
                file_content = file_response.text
            except Exception as e:
                return Response({"error": f"Failed to fetch file: {str(e)}"}, status=500)
        
        code_context = f"Code file content:\n{file_content}\n"
        full_text_query = f"{code_context}\n{text_query}" if text_query else code_context
          
        response = process_query_with_groq(full_text_query, image_data)
        
        return Response({"response": response})
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def google_search(request):
    try:
        data = request.data
        query = data.get('query')
        username = data.get('username', '')
        repo_name = data.get('repo_name', '')
        search_type = data.get('search_type', 'Custom Search')
        
        if not query:
            return Response({"error": "Search query is required"}, status=400)
        
        api_key = os.environ.get('GOOGLE_API_KEY')
        cx_id = os.environ.get('GOOGLE_CSE_ID')
        
        search_results = perform_google_search(
            query=query,
            api_key=api_key,
            cx_id=cx_id,
            num_results=10
        )
        
        enhanced_results = process_google_search_results(search_results, query)
        
        return Response({
            "response": enhanced_results,
            "raw_results": search_results.get("items", []),
            "query": query,
            "search_type": search_type,
            "timestamp": None
        })
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

def resources_page(request):
    username = request.GET.get('username', '')
    repo_name = request.GET.get('repo_name', '')
    
    context = {
        'username': username,
        'repo_name': repo_name,
    }
    
    if username and repo_name:
        try:
            token = get_github_token()
            headers = {}
            if token:
                headers['Authorization'] = f'token {token}'
                
            repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
            repo_response = requests.get(repo_url, headers=headers)
            
            if repo_response.status_code == 200:
                repo_data = repo_response.json()
                context.update({
                    'repo_description': repo_data.get('description', ''),
                    'repo_language': repo_data.get('language', ''),
                    'repo_stars': repo_data.get('stargazers_count', 0),
                    'repo_forks': repo_data.get('forks_count', 0)
                })
        except Exception:
            pass
    
    return render(request, 'github_app/resources.html', context)


@api_view(['GET'])
def get_repo_info(request, username, repo_name):
    """Get repository information for the resources page"""
    try:
        token = get_github_token()
        headers = {}
        if token:
            headers['Authorization'] = f'token {token}'
            
        repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
        repo_response = requests.get(repo_url, headers=headers)
        
        if repo_response.status_code == 200:
            repo_data = repo_response.json()
            return Response({
                'description': repo_data.get('description', ''),
                'language': repo_data.get('language', ''),
                'stars': repo_data.get('stargazers_count', 0),
                'forks': repo_data.get('forks_count', 0)
            })
        else:
            return Response({"error": "Repository not found"}, status=404)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def generate_documentation(request):
    """API endpoint to generate comprehensive documentation for a repository"""
    try:
        data = request.data
        username = data.get('username')
        repo_name = data.get('repo_name')
        
        if not all([username, repo_name]):
            return Response({"error": "Username and repository name are required"}, status=400)
        
        token = get_github_token()
        headers = {}
        if token:
            headers['Authorization'] = f'token {token}'
            
        repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
        repo_response = requests.get(repo_url, headers=headers)
        
        if repo_response.status_code != 200:
            return Response({"error": "Repository not found"}, status=404)
        
        repo_data = repo_response.json()
        
        readme_url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
        readme_response = requests.get(readme_url, headers=headers)
        readme_content = ""
        
        if readme_response.status_code == 200:
            readme_data = readme_response.json()
            readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
        
        structure_url = f"https://api.github.com/repos/{username}/{repo_name}/contents"
        structure_response = requests.get(structure_url, headers=headers)
        structure_info = ""
        
        if structure_response.status_code == 200:
            structure_data = structure_response.json()

            structure_info = "\nRepository Structure:\n"
            for item in structure_data:
                structure_info += f"- {item['name']} ({item['type']})\n"
        
        
        documentation = generate_repo_documentation(
            repo_data, 
            readme_content, 
            structure_info
        )
        
        return Response({"documentation": documentation})
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)

def get_groq_llm(model_name="llama3-8b-8192"):
    """Initialize and return a Groq LLM instance"""
    api_key = os.environ.get('GROQ_API_KEY')
    
    if not api_key:
        raise ValueError("Groq API key not found. Please set GROQ_API_KEY in environment variables.")
    
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name=model_name
    )
    
    return llm

def generate_repo_documentation(repo_data, readme_content, structure_info):
    """
    Generate comprehensive documentation for a repository using Groq
    
    Args:
        repo_data (dict): Repository information from GitHub API
        readme_content (str): Content of README file
        structure_info (str): Information about repository structure
        
    Returns:
        str: Comprehensive documentation in markdown format
    """
    llm = get_groq_llm()
    
    # prompt template
    template = """
    You are an AI documentation specialist for GitHub repositories.
    
    Repository Information:
    Name: {repo_name}
    Owner: {repo_owner}
    Description: {repo_description}
    Primary Language: {repo_language}
    Stars: {stars}
    Forks: {forks}
    Open Issues: {issues}
    Created: {created_date}
    Last Updated: {updated_date}
    
    {structure_info}
    
    README Content:
    {readme_content}
    
    Your task is to create comprehensive documentation for this repository that includes:
    1. A clear and detailed overview of what the repository does within 900 characters
    2. The main purpose and use cases
    3. Key features or components
    4. Technology stack (based on the language and files/structure)
    5. Any installation or usage instructions that can be inferred
    6. Project structure explanation
    
    Format the documentation in clean markdown with appropriate headings, lists, and emphasis.
    Be concise but informative. Focus on providing valuable information for developers who want to understand and use this repository.
    Do not generate fictional information - if certain details are not available, mention that they are not provided.
    """
    
    prompt = PromptTemplate(
        input_variables=["repo_name", "repo_owner", "repo_description", "repo_language", 
                         "stars", "forks", "issues", "created_date", "updated_date", 
                         "structure_info", "readme_content"],
        template=template
    )
    
    # Create chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Run chain
    response = chain.run(
        repo_name=repo_data.get('name', 'Unknown'),
        repo_owner=repo_data.get('owner', {}).get('login', 'Unknown'),
        repo_description=repo_data.get('description', 'No description available'),
        repo_language=repo_data.get('language', 'Unknown'),
        stars=repo_data.get('stargazers_count', 0),
        forks=repo_data.get('forks_count', 0),
        issues=repo_data.get('open_issues_count', 0),
        created_date=repo_data.get('created_at', '').split('T')[0],
        updated_date=repo_data.get('updated_at', '').split('T')[0],
        structure_info=structure_info,
        readme_content=readme_content if readme_content else "No README available"
    )
    
    return response

@api_view(['POST'])
def execute_code(request):
    try:
        data = request.data
        script = data.get('script')
        language = data.get('language')
        stdin = data.get('stdin', '')
        version_index = data.get('versionIndex', '0')
        compile_only = data.get('compileOnly', False)
        
        if not script:
            return Response({"error": "script is required"}, status=400)
        
        if not language:
            return Response({"error": "language is required"}, status=400)
        
        # Get JDoodle credentials from environment
        client_id = os.getenv('JDOODLE_CLIENT_ID')
        client_secret = os.getenv('JDOODLE_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            return Response({"error": "JDoodle credentials not configured"}, status=500)
        
        # Prepare payload for JDoodle API
        payload = {
            'clientId': client_id,
            'clientSecret': client_secret,
            'script': script,
            'stdin': stdin,
            'language': language,
            'versionIndex': version_index,
            'compileOnly': compile_only
        }
        
        # Make request to JDoodle API
        try:
            response = requests.post(
                'https://api.jdoodle.com/v1/execute',
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code != 200:
                return Response({"error": "JDoodle API error"}, status=response.status_code)
            
            result = response.json()
            return Response(result)
            
        except Exception as e:
            return Response({"error": f"Failed to execute code: {str(e)}"}, status=500)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)