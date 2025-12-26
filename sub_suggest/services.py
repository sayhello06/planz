# ...new file...
from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from .models import Project
from .openai_client import OpenAIClient
from planz import settings

class SuggestService:
    def __init__(self, ai_client: OpenAIClient = None):
        self.ai = ai_client or OpenAIClient(settings.OPENAI_API_KEY)

    def recommend_topics(self, keywords: List[str]) -> List[dict]:
        if not (3 <= len(keywords) <= 5):
            raise ValueError("Please provide between 3 and 5 keywords.")
        result = self.ai.generate_topics(keywords)
        if result is None:
            raise RuntimeError("AI did not return valid recommendations.")
        return result

    def save_project(self, title: str, produce: str, keywords: List[str]) -> Project:
        if not title or not produce:
            raise ValueError("Title and produce are required.")
        project = Project.objects.create(title=title, produce=produce, keywords=keywords)
        return project

    def list_projects(self):
        return Project.objects.all().order_by('-created_at')

    def get_project(self, project_id: int) -> Project:
        try:
            return Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            raise

    def delete_project(self, project_id: int) -> None:
        project = self.get_project(project_id)
        project.delete()