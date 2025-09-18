from abc import ABC, abstractmethod


class AbstractOpenAIClient(ABC): 
    @abstractmethod
    def create_response(self, prompt: str) -> str: ...

    @abstractmethod
    def get_screenshot_for_promtp(self) -> str: ...
