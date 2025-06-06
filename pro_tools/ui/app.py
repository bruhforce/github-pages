from flask import Flask, render_template, request, jsonify
import os
import sys
import json
from pathlib import Path

# Добавляем родительскую директорию в путь для импорта
sys.path.append(str(Path(__file__).parent.parent.parent))

from pro_tools.prompt_manager import PromptManager
from pro_tools.api_clients import OpenAIClient

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Инициализация менеджера промптов
prompt_manager = PromptManager()

@app.route('/')
def index():
    """Главная страница"""
    templates = prompt_manager.list_templates()
    return render_template('index.html', templates=templates)

@app.route('/templates')
def templates():
    """Страница со списком шаблонов"""
    templates = prompt_manager.list_templates()
    return render_template('templates.html', templates=templates)

@app.route('/template/<template_id>')
def template_detail(template_id):
    """Страница с деталями шаблона"""
    template = prompt_manager.get_template(template_id)
    versions = prompt_manager.list_versions(template_id)
    return render_template('template_detail.html', template=template, versions=versions)

@app.route('/create_template', methods=['GET', 'POST'])
def create_template():
    """Страница создания шаблона"""
    if request.method == 'POST':
        name = request.form['name']
        template = request.form['template']
        description = request.form['description']
        variables = request.form['variables'].split(',') if request.form['variables'] else []
        variables = [v.strip() for v in variables]
        
        template_id = prompt_manager.create_template(
            name=name,
            template=template,
            description=description,
            variables=variables
        )
        
        return jsonify({'success': True, 'template_id': template_id})
    
    return render_template('create_template.html')

@app.route('/render_prompt/<template_id>', methods=['GET', 'POST'])
def render_prompt(template_id):
    """Страница рендеринга промпта"""
    template = prompt_manager.get_template(template_id)
    
    if request.method == 'POST':
        variables = {}
        for var in template['variables']:
            variables[var] = request.form.get(var, '')
        
        rendered_prompt = prompt_manager.render_prompt(template_id, variables)
        
        return jsonify({
            'success': True, 
            'rendered_prompt': rendered_prompt
        })
    
    return render_template('render_prompt.html', template=template)

@app.route('/test_prompt/<template_id>', methods=['GET', 'POST'])
def test_prompt(template_id):
    """Страница тестирования промпта"""
    template = prompt_manager.get_template(template_id)
    
    if request.method == 'POST':
        variables = {}
        for var in template['variables']:
            variables[var] = request.form.get(var, '')
        
        rendered_prompt = prompt_manager.render_prompt(template_id, variables)
        
        # Проверяем наличие API ключа
        api_key = request.form.get('api_key', '')
        if not api_key and not os.environ.get('OPENAI_API_KEY'):
            return jsonify({
                'success': False,
                'error': 'API ключ не предоставлен. Укажите его в форме или установите переменную окружения OPENAI_API_KEY.'
            })
        
        try:
            client = OpenAIClient(api_key=api_key if api_key else None)
            model = request.form.get('model', 'gpt-3.5-turbo')
            
            if model.startswith('gpt-3.5-turbo-instruct') or model.startswith('text-davinci'):
                response = client.complete(
                    prompt=rendered_prompt,
                    model=model,
                    max_tokens=int(request.form.get('max_tokens', 500)),
                    temperature=float(request.form.get('temperature', 0.7))
                )
                result = response
            else:
                response = client.chat(
                    messages=[
                        {"role": "user", "content": rendered_prompt}
                    ],
                    model=model,
                    temperature=float(request.form.get('temperature', 0.7))
                )
                result = response['choices'][0]['message']['content']
            
            return jsonify({
                'success': True,
                'rendered_prompt': rendered_prompt,
                'result': result
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    return render_template('test_prompt.html', template=template)

if __name__ == '__main__':
    # Создаем директорию для шаблонов, если она не существует
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    # Запускаем приложение
    app.run(debug=True, host='0.0.0.0', port=5000)

