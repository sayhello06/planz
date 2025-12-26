# ...new file...
import json
import openai
from typing import List, Optional

class OpenAIClient:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model

    def generate_topics(self, keywords: List[str]) -> Optional[list]:
        prompt = (
            "다음 키워드를 기반으로 5개의 주제와 개요를 추천해주세요:\n"
            f"키워드: {', '.join(keywords)}\n\n"
            "결과는 반드시 JSON 배열로 제공해주세요. 예: "
            '[{"title":"제목","produce":"개요"}, ...]'
        )
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            text = resp["choices"][0]["message"]["content"]
            return json.loads(text)
        except Exception:
            # raise or return None; 서비스 레이어에서 처리
            return None