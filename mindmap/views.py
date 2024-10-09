from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import MindMap
from .forms import MindMapForm

def index(request):
    form = MindMapForm()
    return render(request, 'mindmap/index.html', {'form': form})

def add_keyword(request):
    # Django 3.1 이상에서 request.is_ajax()가 제거되었으므로, 헤더로 확인
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        main_keyword = request.POST.get('main_keyword')
        sub_keyword = request.POST.get('sub_keyword', '')  # sub_keyword가 없을 경우 빈 문자열로 처리
        if main_keyword:
            mindmap, created = MindMap.objects.get_or_create(main_keyword=main_keyword)
            if sub_keyword:
                mindmap.sub_keywords.append(sub_keyword)
            mindmap.save()
            return JsonResponse({'status': 'success', 'sub_keywords': mindmap.sub_keywords})
    return JsonResponse({'status': 'error'})

def load_map(request, keyword):
    mindmap = get_object_or_404(MindMap, main_keyword=keyword)
    return JsonResponse({'main_keyword': mindmap.main_keyword, 'sub_keywords': mindmap.sub_keywords})
