from django.urls import path, include

urlpatterns = [
    path('api/', include('github_app.urls')),
]