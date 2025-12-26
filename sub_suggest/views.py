import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .services import SuggestService
from .openai_client import OpenAIClient
from planz import settings

service = SuggestService(ai_client=OpenAIClient(settings.OPENAI_API_KEY))

def index(request):
    return render(request, 'suggest/intro.html')

def recommend_topics_page(request):
    return render(request, 'suggest/recommend_topics.html')

@csrf_exempt
def recommend_topics(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    try:
        data = json.loads(request.body)
        keywords = data.get('keywords', [])
        recommendations = service.recommend_topics(keywords)
        return JsonResponse({"status": "success", "recommendations": recommendations})
    except ValueError as e:
        return JsonResponse({"status": "error", "message": str(e)})
    except RuntimeError as e:
        return JsonResponse({"status": "error", "message": str(e)})
    except Exception as e:
        # 실제 서비스에서는 로깅만 남기고 일반 메시지 반환
        return JsonResponse({"status": "error", "message": "An unexpected error occurred"})

@csrf_exempt
def save_project(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    try:
        data = json.loads(request.body)
        project = service.save_project(
            title=data.get('title'),
            produce=data.get('produce'),
            keywords=data.get('keywords', [])
        )
        return JsonResponse({"status": "success", "project_id": project.id})
    except ValueError as e:
        return JsonResponse({"status": "error", "message": str(e)})
    except Exception:
        return JsonResponse({"status": "error", "message": "An unexpected error occurred"})

def list_projects(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    projects = service.list_projects()
    return render(request, 'suggest/list_projects.html', {'projects': projects})

def project_detail(request, project_id):
    try:
        project = service.get_project(project_id)
        return render(request, 'suggest/project_detail.html', {'project': project})
    except Exception:
        return render(request, '404.html', status=404)

@csrf_exempt
@require_POST
def delete_project(request):
    try:
        data = json.loads(request.body)
        project_id = data.get('project_id')
        if not project_id:
            return JsonResponse({"status": "error", "message": "Project ID is required."})
        service.delete_project(project_id)
        return JsonResponse({"status": "success", "message": "Project deleted successfully."})
    except Exception:
        return JsonResponse({"status": "error", "message": "An unexpected error occurred"})