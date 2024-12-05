import openai, os.path, json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Project
from planz import settings
from django.views.decorators.csrf import csrf_exempt  

openai.api_key = settings.OPENAI_API_KEY

def index(request):
    return render(request, 'suggest/index.html')

def recommend_topics_page(request):
    return render(request, 'suggest/recommend_topics.html')

@csrf_exempt
def recommend_topics(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            keywords = data.get('keywords', [])

            if not (3 <= len(keywords) <= 5):
                return JsonResponse({
                    "status": "error",
                    "message": "Please provide between 3 and 5 keywords."
                })

            # GPT 호출
            recommendations = get_topic_and_outline_with_gpt(keywords)
            print("Recommendations from GPT:", recommendations)  # 디버깅

            # recommendations가 None인지 확인
            if recommendations is None:
                return JsonResponse({
                    "status": "error",
                    "message": "GPT did not return valid recommendations."
                })

            return JsonResponse({
                "status": "success",
                "recommendations": recommendations
            })

        except Exception as e:
            print("Unexpected Error in recommend_topics:", e)  # 오류 로그
            return JsonResponse({"status": "error", "message": f"An unexpected error occurred: {str(e)}"})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def save_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_title = data.get('title')
            selected_produce = data.get('produce')
            keywords = data.get('keywords', [])

            if not selected_title or not selected_produce:
                return JsonResponse({
                    "status": "error",
                    "message": "Title and produce are required to save the project."
                })

            # 데이터베이스에 저장
            project = Project.objects.create(
                title=selected_title,
                produce=selected_produce,
                keywords=keywords
            )

            return JsonResponse({"status": "success", "project_id": project.id})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"An unexpected error occurred: {str(e)}"})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def get_topic_and_outline_with_gpt(keywords):
    # 키워드 배열을 문자열로 변환
    prompt_keywords = ', '.join(keywords)

    # GPT API 프롬프트 생성
    prompt = f"""
    다음 키워드를 기반으로 5개의 주제와 개요를 추천해주세요:
    키워드를 합쳤을 때 재밌는 주제가 나올 것 같으면 최우선적으로 추천해주세요.
    키워드: {prompt_keywords}

    결과는 반드시 JSON 배열로 제공해주세요. 예:
    [
        {{"title": "주제 제목 1", "produce": "주제 개요 1"}},
        {{"title": "주제 제목 2", "produce": "주제 개요 2"}},
        ...
    ]
    """

    try:
        # GPT 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        # GPT 응답 텍스트 추출
        gpt_response_text = response['choices'][0]['message']['content']
        print("GPT Response (Raw):", gpt_response_text)  # GPT 원본 응답 디버깅

        # JSON 파싱
        gpt_response_json = json.loads(gpt_response_text)
        print("GPT Response (Parsed):", gpt_response_json)  # 파싱된 JSON 디버깅

        return gpt_response_json

    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)  # JSON 파싱 오류 로그
        return None

    except Exception as e:
        print("Unexpected Error:", e)  # 기타 오류 로그
        return None
    
def list_projects(request):
    if request.method == 'GET':
        # 데이터베이스에서 모든 프로젝트 가져오기
        #projects = Project.objects.all().values("id", "title", "produce", "keywords", "created_at")
        projects = Project.objects.all().order_by('-created_at')
        return render(request, 'suggest/list_projects.html', {'projects': projects})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def project_detail(request, project_id):
    # try:
    #     project = Project.objects.get(id=project_id)
    #     return JsonResponse({
    #         "status": "success",
    #         "id": project.id,
    #         "title": project.title,
    #         "produce": project.produce,
    #         "keywords": project.keywords,
    #         "created_at": project.created_at
    #     })
    # except Project.DoesNotExist:
    #     return JsonResponse({"status": "error", "message": "Project not found"})
    try:
        project = Project.objects.get(id=project_id)
        return render(request, 'suggest/project_detail.html', {'project': project})
    except Project.DoesNotExist:
        return render(request, '404.html', status=404)

#해야할 일 : 변경된 주제에 맞게 변수 명 변경 / model 재설계 / SQL과 연동 고려 / 동장 방식 재설계 / html 수정