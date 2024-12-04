from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=255)  # 주제 제목
    produce = models.TextField()  # 주제 개요
    keywords = models.JSONField()  # 입력된 키워드 (JSON 배열로 저장)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True)  # 업데이트 날짜

    def __str__(self):
        return self.title
