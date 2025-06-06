import os
import re
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Импортируем необходимые классы из обоих подходов
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from dialog_system.utils import DialogManager
from pro_tools.prompt_manager import PromptManager

class ContextBridge:
    """Мост между системой диалогов и профессиональными инструментами"""
    
    def __init__(self):
        self.dialog_manager = DialogManager()
        self.prompt_manager = PromptManager()
    
    def dialog_to_prompt_template(self, dialog_path: str, template_name: str) -> str:
        """Преобразует диалог в шаблон промпта"""
        dialog_content = Path(dialog_path).read_text(encoding="utf-8")
        
        # Извлекаем системный промпт
        system_prompt = ""
        system_match = re.search(r"## Системный промпт\n\n(.*?)(?=\n\n##|\Z)", dialog_content, re.DOTALL)
        if system_match:
            system_prompt = system_match.group(1).strip()
        
        # Извлекаем сообщения диалога
        dialog_match = re.search(r"## Диалог\n\n(.*?)(?=\n\n##|\Z)", dialog_content, re.DOTALL)
        if not dialog_match:
            raise ValueError("Не удалось найти секцию диалога")
        
        dialog_text = dialog_match.group(1).strip()
        
        # Парсим сообщения
        messages = []
        for line in dialog_text.split("\n\n"):
            if line.startswith("**user**:"):
                messages.append({
                    "role": "user",
                    "content": line.replace("**user**:", "").strip()
                })
            elif line.startswith("**assistant**:"):
                messages.append({
                    "role": "assistant",
                    "content": line.replace("**assistant**:", "").strip()
                })
        
        # Создаем шаблон промпта
        template = ""
        variables = []
        
        if system_prompt:
            template += "# Системный промпт\n{{system_prompt}}\n\n"
            variables.append("system_prompt")
        
        template += "# Диалог\n\n"
        
        for i, message in enumerate(messages):
            if message["role"] == "user":
                template_var = f"user_message_{i+1}"
                template += f"**user**: {{{{{template_var}}}}}\n\n"
                variables.append(template_var)
            else:
                template_var = f"assistant_message_{i+1}"
                template += f"**assistant**: {{{{{template_var}}}}}\n\n"
                variables.append(template_var)
        
        # Создаем шаблон промпта
        template_id = self.prompt_manager.create_template(
            name=template_name,
            template=template,
            description=f"Шаблон, созданный из диалога {Path(dialog_path).stem}",
            variables=variables
        )
        
        return template_id
    
    def prompt_template_to_dialog(self, template_id: str, dialog_title: str) -> str:
        """Преобразует шаблон промпта в диалог"""
        template_data = self.prompt_manager.get_template(template_id)
        
        # Создаем новый диалог
        system_prompt = ""
        if "system_prompt" in template_data["variables"]:
            system_prompt = "Системный промпт из шаблона"
        
        dialog_path = self.dialog_manager.create_dialog(dialog_title, system_prompt)
        
        # Добавляем сообщения из шаблона
        for var in template_data["variables"]:
            if var == "system_prompt":
                continue
                
            if var.startswith("user_message_"):
                self.dialog_manager.add_message(dialog_path, "user", f"[Переменная: {var}]")
            elif var.startswith("assistant_message_"):
                self.dialog_manager.add_message(dialog_path, "assistant", f"[Переменная: {var}]")
        
        return str(dialog_path)
    
    def test_prompt_with_dialog(self, template_id: str, variables: Dict[str, str], 
                              dialog_title: str) -> str:
        """Тестирует промпт и сохраняет результат как диалог"""
        # Рендерим промпт с переменными
        rendered_prompt = self.prompt_manager.render_prompt(template_id, variables)
        
        # Создаем новый диалог
        system_prompt = variables.get("system_prompt", "")
        dialog_path = self.dialog_manager.create_dialog(dialog_title, system_prompt)
        
        # Добавляем сообщения из переменных
        for var_name, var_value in variables.items():
            if var_name == "system_prompt":
                continue
                
            if var_name.startswith("user_message_"):
                self.dialog_manager.add_message(dialog_path, "user", var_value)
            elif var_name.startswith("assistant_message_"):
                self.dialog_manager.add_message(dialog_path, "assistant", var_value)
        
        # Добавляем информацию о тестировании
        with open(dialog_path, "a", encoding="utf-8") as f:
            f.write("\n\n## Информация о тестировании\n\n")
            f.write(f"Шаблон: {template_id}\n\n")
            f.write(f"Дата тестирования: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Переменные:\n")
            for var_name, var_value in variables.items():
                f.write(f"- {var_name}: {var_value}\n")
        
        return str(dialog_path)

