import ollama
import os

def call_local_llm(func_name, params, description, blueprint, context_info, current_file, requirements=[]):
    # 1. プロジェクト構造をテキスト化
    structure_lines = [f"  - {m['path']}" for m in blueprint.get('modules', [])]
    project_structure = "\n".join(structure_lines)
    req_text = "\n".join([f"- {r}" for r in requirements]) if requirements else "No specific requirements."

    # 2. テンプレート読み込み
    with open('prompts/instruction.md', 'r', encoding='utf-8') as f:
        template = f.read()

    
    # 3. すべての変数を注入
    # ※ params が空なら "no arguments" と書くとAIが迷いません
    prompt = template.format(
        project_name=blueprint.get('project_name', 'Unknown'),
        project_goal=blueprint.get('goal', 'No goal specified.'),
        current_file=current_file,
        func_name=func_name,
        params=params if params else "no arguments",
        project_structure=project_structure,
        context=context_info if context_info else "No external dependencies available.",
        description=description,
        requirements=req_text
    )
    
    # ... Ollama 呼び出し ...
    response = ollama.generate(
        model='llama3.1:8b', 
        prompt=prompt
    )

    return response['response'].strip()
