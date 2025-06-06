import os
import json
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class PromptManager:
    """Менеджер для управления промптами и их версиями"""
    
    def __init__(self, base_path: str = "./prompts"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True, parents=True)
        self.templates_path = self.base_path / "templates"
        self.templates_path.mkdir(exist_ok=True)
        self.versions_path = self.base_path / "versions"
        self.versions_path.mkdir(exist_ok=True)
    
    def create_template(self, name: str, template: str, description: str = "", 
                       variables: Optional[List[str]] = None) -> str:
        """Создает новый шаблон промпта"""
        template_id = self._generate_id(name)
        template_path = self.templates_path / f"{template_id}.json"
        
        template_data = {
            "id": template_id,
            "name": name,
            "description": description,
            "template": template,
            "variables": variables or [],
            "created_at": datetime.datetime.now().isoformat()
        }
        
        with open(template_path, "w", encoding="utf-8") as f:
            json.dump(template_data, f, ensure_ascii=False, indent=2)
        
        return template_id
    
    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Получает шаблон промпта по ID"""
        template_path = self.templates_path / f"{template_id}.json"
        
        if not template_path.exists():
            raise FileNotFoundError(f"Шаблон с ID {template_id} не найден")
        
        with open(template_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """Возвращает список всех шаблонов"""
        templates = []
        for file in self.templates_path.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                template_data = json.load(f)
                templates.append({
                    "id": template_data["id"],
                    "name": template_data["name"],
                    "description": template_data["description"],
                    "created_at": template_data["created_at"]
                })
        return sorted(templates, key=lambda x: x["created_at"], reverse=True)
    
    def render_prompt(self, template_id: str, variables: Dict[str, str]) -> str:
        """Рендерит промпт, подставляя переменные в шаблон"""
        template_data = self.get_template(template_id)
        template = template_data["template"]
        
        # Проверяем, что все необходимые переменные предоставлены
        for var in template_data["variables"]:
            if var not in variables:
                raise ValueError(f"Отсутствует обязательная переменная: {var}")
        
        # Подставляем переменные
        for var_name, var_value in variables.items():
            template = template.replace(f"{{{{{var_name}}}}}", var_value)
        
        # Создаем версию промпта
        version_id = self._create_version(template_id, variables, template)
        
        return template
    
    def get_version(self, version_id: str) -> Dict[str, Any]:
        """Получает версию промпта по ID"""
        version_path = self.versions_path / f"{version_id}.json"
        
        if not version_path.exists():
            raise FileNotFoundError(f"Версия с ID {version_id} не найдена")
        
        with open(version_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def list_versions(self, template_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Возвращает список всех версий промптов"""
        versions = []
        for file in self.versions_path.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                version_data = json.load(f)
                if template_id is None or version_data["template_id"] == template_id:
                    versions.append({
                        "id": version_data["id"],
                        "template_id": version_data["template_id"],
                        "created_at": version_data["created_at"]
                    })
        return sorted(versions, key=lambda x: x["created_at"], reverse=True)
    
    def _create_version(self, template_id: str, variables: Dict[str, str], 
                       rendered_prompt: str) -> str:
        """Создает версию промпта"""
        version_id = hashlib.md5(rendered_prompt.encode()).hexdigest()[:10]
        version_path = self.versions_path / f"{version_id}.json"
        
        version_data = {
            "id": version_id,
            "template_id": template_id,
            "variables": variables,
            "rendered_prompt": rendered_prompt,
            "created_at": datetime.datetime.now().isoformat()
        }
        
        with open(version_path, "w", encoding="utf-8") as f:
            json.dump(version_data, f, ensure_ascii=False, indent=2)
        
        return version_id
    
    def _generate_id(self, name: str) -> str:
        """Генерирует ID на основе имени"""
        base = name.lower().replace(" ", "_")
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{base}_{timestamp}"

