from django.http import JsonResponse
import requests
from .models import GithubToken, GoogleSearchAPIKey
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import process_repository_query, process_code_query, process_google_search_results, perform_google_search
from .models import GroqQuery
import requests
import json
import os
from django.shortcuts import render

@api_view(['GET'])
def repositories(request, username):
    """Get all repositories for a GitHub user"""
    try:

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
        file_content = data.get('file_content')  # Get the file content from the request
        
        if not query:
            return Response({"error": "Query is required"}, status=400)
        
        # Use provided file content if available, otherwise try to fetch from URL
        if not file_content:
            if not file_url:
                return Response({"error": "Either file_content or file_url is required"}, status=400)
            
            # Fetch file content from URL
            try:
                file_response = requests.get(file_url)
                
                if file_response.status_code != 200:
                    return Response({"error": "File not found"}, status=404)
                
                file_content = file_response.text
            except Exception as e:
                return Response({"error": f"Failed to fetch file: {str(e)}"}, status=500)
        
        # Process query using Groq with the file content
        response = process_code_query(file_content, query)
        
        # Save query and response
        GroqQuery.objects.create(
            query=query,
            response=response
        )
        
        return Response({"response": response})
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    
@api_view(['POST'])
def google_search(request):
    """API endpoint to perform Google search and enhance results with Groq"""
    try:
        # Get data from request
        data = request.data
        query = data.get('query')
        username = data.get('username', '')
        repo_name = data.get('repo_name', '')
        search_type = data.get('search_type', 'Custom Search')
        
        if not query:
            return Response({"error": "Search query is required"}, status=400)
        
        # Try to get Google API credentials from database first
        api_credentials = GoogleSearchAPIKey.objects.first()
        
        # If not in database, use environment variables as fallback
        if not api_credentials:
            api_key = os.environ.get('GOOGLE_API_KEY')
            cx_id = os.environ.get('GOOGLE_CSE_ID')
            
            if not api_key or not cx_id:
                return Response({"error": "Google Search API credentials not configured"}, status=500)
        else:
            api_key = api_credentials.api_key
            cx_id = api_credentials.cx_id
        
        # Perform Google search
        search_results = perform_google_search(
            query=query,
            api_key=api_key,
            cx_id=cx_id,
            num_results=10
        )
        
        # Process results with Groq
        enhanced_results = process_google_search_results(search_results, query)
        
        # Save query and response with repo context if available
        query_context = f"{search_type}: {query}"
        if username and repo_name:
            query_context = f"[{username}/{repo_name}] {query_context}"
            
        GroqQuery.objects.create(
            query=query_context,
            response=enhanced_results
        )
        
        return Response({
            "response": enhanced_results,
            "raw_results": search_results.get("items", []),
            "query": query,
            "search_type": search_type,
            "timestamp": GroqQuery.objects.latest('timestamp').timestamp.isoformat() if GroqQuery.objects.exists() else None
        })
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)

def resources_page(request):
    """Render the resources page template"""
    # Get repository context from query parameters if available
    username = request.GET.get('username', '')
    repo_name = request.GET.get('repo_name', '')
    
    context = {
        'username': username,
        'repo_name': repo_name,
    }
    
    # If we have a repo context, try to get additional info
    if username and repo_name:
        try:
            # Fetch repository information
            repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
            repo_response = requests.get(repo_url)
            
            if repo_response.status_code == 200:
                repo_data = repo_response.json()
                context.update({
                    'repo_description': repo_data.get('description', ''),
                    'repo_language': repo_data.get('language', ''),
                    'repo_stars': repo_data.get('stargazers_count', 0),
                    'repo_forks': repo_data.get('forks_count', 0)
                })
        except Exception:
            # If there's an error, we'll just use the basic context
            pass
    
    return render(request, 'github_app/resources.html', context)

@api_view(['GET'])
def get_repo_info(request, username, repo_name):
    """Get repository information for the resources page"""
    try:
        # Fetch repository information
        repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
        repo_response = requests.get(repo_url)
        
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

@api_view(['GET'])
def search_history(request, count=5):
    """Get recent search history for the resources page"""
    try:
        # Get most recent queries
        recent_queries = GroqQuery.objects.filter(
            query__startswith="Google Search"
        ).order_by('-timestamp')[:int(count)]
        
        results = []
        for query in recent_queries:
            # Extract the actual query from the saved query string
            query_text = query.query.replace("Google Search: ", "")
            results.append({
                'id': query.id,
                'query': query_text,
                'response': query.response,
                'timestamp': query.timestamp.isoformat()
            })
        
        return Response({"history": results})
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)