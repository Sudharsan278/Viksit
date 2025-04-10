# Updated github_app/views.py to support path parameter for nested structures

from django.http import JsonResponse
import requests
from .models import GithubToken
from rest_framework.decorators import api_view


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import process_repository_query, process_code_query
from .models import GroqQuery
import requests
import json

@api_view(['GET'])
def repositories(request, username):
    """Get all repositories for a GitHub user"""
    try:
        # Get the token from the database
        token_obj = GithubToken.objects.first()
        token = token_obj.token if token_obj else None
        
        headers = {}
        if token:
            headers['Authorization'] = f'token {token}'
        
        # Get user repositories
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
        # Get the token from the database
        token_obj = GithubToken.objects.first()
        token = token_obj.token if token_obj else None
        
        headers = {}
        if token:
            headers['Authorization'] = f'token {token}'
        
        # Check if a specific path is requested
        path = request.GET.get('path', '')
        
        # Get repo contents (for the specified path or root level)
        url = f'https://api.github.com/repos/{username}/{repo_name}/contents'
        if path:
            url += f'/{path}'
            
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            contents = response.json()
            
            # Handle both single file case (dict) and directory (list)
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
    

@api_view(['POST'])
def query_repository(request):
    """API endpoint to query a repository using Groq"""
    try:
        # Get data from request
        data = request.data
        username = data.get('username')
        repo_name = data.get('repo_name')
        query = data.get('query')
        
        if not all([username, repo_name, query]):
            return Response({"error": "Username, repository name, and query are required"}, status=400)
        
        # Fetch repository information from GitHub API
        repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
        repo_response = requests.get(repo_url)
        
        if repo_response.status_code != 200:
            return Response({"error": "Repository not found"}, status=404)
        
        repo_data = repo_response.json()
        
        # Process query using Groq
        response = process_repository_query(repo_data, query)
        
        # Save query and response
        GroqQuery.objects.create(
            query=query,
            response=response
        )
        
        return Response({"response": response})
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def query_code(request):
    """API endpoint to query a specific code file using Groq"""
    try:
        # Get data from request
        data = request.data
        file_url = data.get('file_url')
        query = data.get('query')
        
        if not all([file_url, query]):
            return Response({"error": "File URL and query are required"}, status=400)
        
        # Fetch file content
        file_response = requests.get(file_url)
        
        if file_response.status_code != 200:
            return Response({"error": "File not found"}, status=404)
        
        file_content = file_response.text
        
        # Process query using Groq
        response = process_code_query(file_content, query)
        
        # Save query and response
        GroqQuery.objects.create(
            query=query,
            response=response
        )
        
        return Response({"response": response})
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)