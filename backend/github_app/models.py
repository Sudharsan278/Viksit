from django.db import models

class GithubToken(models.Model):
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"Token created at {self.created_at}"
    
class GroqQuery(models.Model):
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"Query: {self.query[:50]}..."