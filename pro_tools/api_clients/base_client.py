import os
import json
import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pathlib import Path

class LLMClient(ABC):
    """Базовый абстрактный класс для клиентов языковых моделей"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get(self._get_api_key_env_var())
        if not self.api_key:
            raise ValueError(f"API ключ не найден. Установите переменную окружения {self._get_api_key_env_var()} или передайте ключ напрямую.")
        
        # Создаем директорию для логов
        self.log_dir = Path("./logs")
        self.log_dir.mkdir(exist_ok=True, parents=True)
    
    @abstractmethod
    def _get_api_key_env_var(self) -> str:
        """Возвращает имя переменной окружения для API ключа"""
        pass
    
    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> str:
        """Выполняет запрос на завершение текста"""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Выполняет запрос в формате чата"""
        pass
    
    def log_request(self, endpoint: str, payload: Dict[str, Any]) -> None:
        """Логирует запрос к API"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = self.log_dir / f"request_{timestamp}.json"
        
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": timestamp,
                "endpoint": endpoint,
                "payload": payload
            }, f, ensure_ascii=False, indent=2)
    
    def log_response(self, endpoint: str, response: Dict[str, Any]) -> None:
        """Логирует ответ от API"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = self.log_dir / f"response_{timestamp}.json"
        
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": timestamp,
                "endpoint": endpoint,
                "response": response
            }, f, ensure_ascii=False, indent=2)

