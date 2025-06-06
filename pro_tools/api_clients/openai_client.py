import requests
import json
from typing import Dict, List, Any, Optional

from .base_client import LLMClient

class OpenAIClient(LLMClient):
    """Клиент для работы с OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.base_url = "https://api.openai.com/v1"
    
    def _get_api_key_env_var(self) -> str:
        return "OPENAI_API_KEY"
    
    def complete(self, prompt: str, model: str = "gpt-3.5-turbo-instruct", 
                max_tokens: int = 500, temperature: float = 0.7, **kwargs) -> str:
        """Выполняет запрос на завершение текста"""
        endpoint = f"{self.base_url}/completions"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            **kwargs
        }
        
        self.log_request("completions", payload)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()
            
            self.log_response("completions", response_data)
            
            return response_data["choices"][0]["text"]
        except Exception as e:
            error_msg = f"Ошибка при запросе к OpenAI API: {str(e)}"
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                    error_msg += f"\nОтвет API: {json.dumps(error_data, ensure_ascii=False)}"
                except:
                    error_msg += f"\nКод ответа: {e.response.status_code}"
            
            raise Exception(error_msg)
    
    def chat(self, messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo", 
            temperature: float = 0.7, **kwargs) -> Dict[str, Any]:
        """Выполняет запрос в формате чата"""
        endpoint = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            **kwargs
        }
        
        self.log_request("chat/completions", payload)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()
            
            self.log_response("chat/completions", response_data)
            
            return response_data
        except Exception as e:
            error_msg = f"Ошибка при запросе к OpenAI API: {str(e)}"
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                    error_msg += f"\nОтвет API: {json.dumps(error_data, ensure_ascii=False)}"
                except:
                    error_msg += f"\nКод ответа: {e.response.status_code}"
            
            raise Exception(error_msg)

