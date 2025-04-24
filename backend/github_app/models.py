from django.db import models
    
class GroqQuery(models.Model):
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"Query: {self.query[:50]}..."

class GoogleSearchAPIKey(models.Model):
    api_key = models.CharField(max_length=255)
    cx_id = models.CharField(max_length=255, help_text="The Custom Search Engine ID")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Google Search API Key (created {self.created_at})"