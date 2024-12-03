#mindmap/models.py
from django.db import models

class Sub_Suggest(models.Model):
    main_keyword = models.CharField(max_length=100)
    sub_keywords = models.JSONField(default=list)  # 서브 키워드들을 JSON 형태로 저장
