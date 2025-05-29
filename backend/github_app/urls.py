from django.urls import path
from . import views

urlpatterns = [
    path('repositories/<str:username>/', views.repositories, name='repositories'),
    path('repo-structure/<str:username>/<str:repo_name>/', views.repo_structure, name='repo_structure'),
    path('query-repository/', views.query_repository, name='query_repository'),
    path('query-code/', views.query_code, name='query_code'),
    path('google-search/', views.google_search, name='google_search'),
    path('resources/', views.resources_page, name='resources_page'),
    path('repo-info/<str:username>/<str:repo_name>/', views.get_repo_info, name='get_repo_info'),
    path('generate-documentation/', views.generate_documentation, name='generate_documentation'),
    path('execute-code/', views.execute_code, name='execute_code'),
]