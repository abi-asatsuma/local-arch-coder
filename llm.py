import ollama
import os

def call_local_llm(func_name, params, description, blueprint):
    # Blueprintから利用可能なモジュール名を抽出
    module_names = [m['path'].replace('.py', '').replace('/', '.') for m in blueprint['modules']]
    
    with open('prompts/instruction.md', 'r') as f:
        template = f.read()

    prompt = template.format(
        func_name=func_name,
        params=params,
        description=description,
        available_modules=", ".join(module_names)
    )

    response = ollama.generate(
        model='llama3.1:8b-instruct-q4_K_M', 
        prompt=prompt
    )

    return response['response'].strip()
