from django.contrib import admin
from .models import GithubToken

@admin.register(GithubToken)
class GithubTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')