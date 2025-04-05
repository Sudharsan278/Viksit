# Updated github_app/views.py to support path parameter for nested structures

from django.http import JsonResponse
import requests
from .models import GithubToken
from rest_framework.decorators import api_view

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