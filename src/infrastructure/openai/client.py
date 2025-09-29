import base64
import os
from pathlib import Path

import openai

from src.domain.interfaces import AbstractOpenAIClient
from src.config import settings
from src.logger import log


class OpenAIClient(AbstractOpenAIClient): 
    def __init__(self) -> None: 
        self.client = openai.Client(api_key=settings.OPENAI_API_KEY)
        self.path = Path(settings.DOWNLOAD_DIR)

    @log
    def create_response(self, prompt: str) -> str:
        screenshots_b64 = self.get_screenshot_for_promtp()
        response = self.client.responses.create(
            model="gpt-4.1", 
            input=[
                {
                    "role": "system", 
                    "content": [
                        {"type": "input_text", "text": "Представь, что ты — профессиональный технический аналитик и трейдер с 10-летним опытом работы на криптовалютном рынке. Твой анализ должен быть максимально объективным, подробным и структурированным, как если бы ты готовил его для инвестиционного фонда."}
                    ]
                },
                {
                    "role": "user", 
                    "content": [
                        {"type": "input_text", "text": prompt}, 
                        {"type": "input_image", "image_url": screenshots_b64[0]},
                        {"type": "input_image", "image_url": screenshots_b64[1]}, 
                        {"type": "input_image", "image_url": screenshots_b64[2]}, 
                        {"type": "input_image", "image_url": screenshots_b64[3]}, 
                        {"type": "input_image", "image_url": screenshots_b64[4]}, 
                        {"type": "input_image", "image_url": screenshots_b64[5]}
                    ]
                }
            ]
        )
        return response.output[0].content[0].text

    @log
    def get_screenshot_for_promtp(self) -> list[str]:
        # Get screenshot name
        screenshots_name = list(self.path.walk())[0][-1]
        screenshots_b64 = []

        # # Decode screenshots
        for screenshot_name in screenshots_name:
            with open(fr"{settings.DOWNLOAD_DIR}\{screenshot_name}", "rb") as image_file: 
                b64_image = base64.b64encode(image_file.read()).decode("utf-8")
                screenshots_b64.append(f"data:image/png;base64,{b64_image}")

            # Delete it
            os.remove(fr"{settings.DOWNLOAD_DIR}\{screenshot_name}")

        return screenshots_b64
