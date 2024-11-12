import openai, os.path
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import MindMap
from .forms import MindMapForm
from gensim.models import FastText
from planz import settings
from django.views.decorators.csrf import csrf_exempt  # For simplicity in testingfrom .models import MindMap

# Load the Word2Vec model
# Assuming you've trained your Word2Vec model and saved it as 'word2vec.model'
#fasttext_model = FastText.load_fasttext_format('images/cc.ko.300.bin')

# Set OpenAI API Key (from your settings.py)
openai.api_key = settings.OPENAI_API_KEY

def index(request):
    form = MindMapForm()
    return render(request, 'mindmap/index.html', {'form': form})

def load_map(request, keyword):
    mindmap = get_object_or_404(MindMap, main_keyword=keyword)
    return JsonResponse({'main_keyword': mindmap.main_keyword, 'sub_keywords': mindmap.sub_keywords})

@csrf_exempt
def add_keyword(request):
    if request.method == 'POST':
        main_keyword = request.POST.get('main_keyword')
        sub_keyword = request.POST.get('sub_keyword', '')

        if main_keyword:
            # Chat GPT 3.5 API가 메인 키워드를 기반으로 서브 키워드 추천
            recommended_keywords = get_recommended_keywords_with_gpt(main_keyword)

            # 메인 키워드를 통해 마인드맵의 object를 가져오거나 생성
            mindmap, created = MindMap.objects.get_or_create(main_keyword=main_keyword)

            # 이용자가 임의로 서브 키워드를 추가하면 서브 키워드 array에 추가
            if sub_keyword:
                mindmap.sub_keywords.append(sub_keyword)
                mindmap.save()

            return JsonResponse({'status': 'success', 'sub_keywords': mindmap.sub_keywords, 'recommended_keywords': recommended_keywords})

    return JsonResponse({'status': 'error'})

def get_recommended_keywords_with_gpt(main_keyword):
    prompt = (f"Suggest a list(only 10 suggest please) of relevant keywords that would be useful for someone organizing or participating in a '{main_keyword}'. "
              f"If the '{main_keyword}' is Korean, please suggested keywords translate in to Korean and write like this keyword - 키워드"
              f"Just return the keywords, separated by commas.")
    
    print("GPT Prompt:", prompt)  # Debug: Check the prompt being sent to GPT

    try:
        # Use GPT-3.5 Turbo to generate recommendations
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            n=1,
            temperature=0.7
        )
        
        # Extract the content (expected to be a comma-separated list of keywords)
        gpt_response = response['choices'][0]['message']['content'].strip()

        # Now, split the response into individual keywords
        # Remove any unnecessary numbers or bullet points
        recommended_keywords = [word.strip() for word in gpt_response.split(',') if word.strip() and not word[0].isdigit()]
        print("GPT Response (Keywords Only):", recommended_keywords)  # Debug: Check GPT response with only keywords
        file_path = "keywords.txt"
        file = "C:\\planz\keywords.txt"
        if os.path.isfile(file):
            with open(file_path, "a") as file:
                file.write("main keyword : " + main_keyword + "\n\n")
                file.write("recommended keywords : " + "\n")
                for item in recommended_keywords:
                    file.write(item+"\n")
                file.write("-"*40 + "\n")
        else:
            with open(file_path, "w") as file:
                file.write("main keyword : " + main_keyword + "\n")
                file.write("recommended keywords : " + "\n")
                for item in recommended_keywords:
                    file.write(item+"\n")
                file.write("-"*40 + "\n")
        return recommended_keywords

    except Exception as e:
        print("GPT Error:", e)  # Debug: Print GPT error
        return []
    
    