from django.urls import path
from . import views

urlpatterns = [
    path('repositories/<str:username>/', views.repositories, name='repositories'),
    path('repo-structure/<str:username>/<str:repo_name>/', views.repo_structure, name='repo_structure'),
    path('query-repository/', views.query_repository, name='query_repository'),
    path('query-code/', views.query_code, name='query_code'),
]