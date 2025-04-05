from django.core.management.base import BaseCommand
from github_app.models import GithubToken

class Command(BaseCommand):
    help = 'Set GitHub token for API authentication'

    def add_arguments(self, parser):
        parser.add_argument('token', type=str, help='GitHub token')

    def handle(self, *args, **kwargs):
        token = kwargs['token']
        
        # Delete any existing tokens
        GithubToken.objects.all().delete()
        
        # Create new token
        GithubToken.objects.create(token=token)
        
        self.stdout.write(self.style.SUCCESS('Successfully set GitHub token'))