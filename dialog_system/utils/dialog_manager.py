import os
import json
import datetime
import uuid
from pathlib import Path

class DialogManager:
    def __init__(self, base_path="./dialogs"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True, parents=True)
        
    def create_dialog(self, title, system_prompt=""):
        """Создает новый диалог"""
        dialog_id = str(uuid.uuid4())[:8]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dialog_name = f"{timestamp}_{dialog_id}_{title.replace(' ', '_')}"
        
        dialog_path = self.base_path / f"{dialog_name}.md"
        
        with open(dialog_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"Dialog ID: {dialog_id}\n")
            f.write(f"Created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if system_prompt:
                f.write("## Системный промпт\n\n")
                f.write(f"{system_prompt}\n\n")
            
            f.write("## Диалог\n\n")
        
        return dialog_path
    
    def add_message(self, dialog_path, role, content):
        """Добавляет сообщение в диалог"""
        with open(dialog_path, "a", encoding="utf-8") as f:
            f.write(f"**{role}**: {content}\n\n")
    
    def create_checkpoint(self, dialog_path, checkpoint_name):
        """Создает контрольную точку диалога"""
        checkpoint_dir = Path("./checkpoints")
        checkpoint_dir.mkdir(exist_ok=True, parents=True)
        
        dialog_content = Path(dialog_path).read_text(encoding="utf-8")
        checkpoint_path = checkpoint_dir / f"{checkpoint_name}.md"
        
        with open(checkpoint_path, "w", encoding="utf-8") as f:
            f.write(dialog_content)
            f.write(f"\n\n## Контрольная точка: {checkpoint_name}\n")
            f.write(f"Создана: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        return checkpoint_path
    
    def branch_from_checkpoint(self, checkpoint_path, branch_name):
        """Создает ветку диалога из контрольной точки"""
        checkpoint_content = Path(checkpoint_path).read_text(encoding="utf-8")
        
        dialog_id = str(uuid.uuid4())[:8]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        branch_filename = f"{timestamp}_{dialog_id}_{branch_name.replace(' ', '_')}.md"
        branch_path = self.base_path / branch_filename
        
        with open(branch_path, "w", encoding="utf-8") as f:
            f.write(checkpoint_content)
            f.write(f"\n\n## Ветка: {branch_name}\n")
            f.write(f"Создана из контрольной точки: {Path(checkpoint_path).stem}\n\n")
        
        return branch_path
    
    def list_dialogs(self):
        """Возвращает список всех диалогов"""
        dialogs = []
        for file in self.base_path.glob("*.md"):
            dialogs.append({
                "path": str(file),
                "name": file.stem,
                "created": file.stat().st_ctime
            })
        return sorted(dialogs, key=lambda x: x["created"], reverse=True)
    
    def list_checkpoints(self):
        """Возвращает список всех контрольных точек"""
        checkpoint_dir = Path("./checkpoints")
        checkpoint_dir.mkdir(exist_ok=True, parents=True)
        
        checkpoints = []
        for file in checkpoint_dir.glob("*.md"):
            checkpoints.append({
                "path": str(file),
                "name": file.stem,
                "created": file.stat().st_ctime
            })
        return sorted(checkpoints, key=lambda x: x["created"], reverse=True)
    
    def get_dialog_content(self, dialog_path):
        """Возвращает содержимое диалога"""
        return Path(dialog_path).read_text(encoding="utf-8")

