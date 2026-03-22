import textwrap

from llm import call_local_llm
import re
from test_code import extract_function_info

def inject_code_to_file(file_path, func_name, raw_llm_response):
    pure_code = extract_pure_code(raw_llm_response)
    final_code = adjust_indent(pure_code, indent_level=0) # 0マスで整列

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # タグの間を、AIが書いた「def ...」から始まるコードで完全に置き換える
    pattern = rf"(# \[AI_START:{func_name}\]).*?(# \[AI_END:{func_name}\])"
    replacement = rf"\1\n{final_code}\n\2"
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✨ Clean code injected into {func_name}")

def extract_pure_code(raw_text):
    # 正規表現で ```python (改行) [中身] (改行) ``` を探す
    # (.*?) は最小一致、re.DOTALL は改行をまたいで検索するフラグ
    match = re.search(r'```python\n(.*?)\n```', raw_text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    # もしバッククォートがなければ、そのまま（または全体）を返す
    # ※LLMがバッククォートを忘れた時用の保険
    return raw_text.strip()

# adjust_indent 内
def adjust_indent(code_text, indent_level=0): # 0にする
    if not code_text.strip():
        return "pass"
    # AIがつけてきた余計な外側の空白だけを消し、構造を維持して左端に寄せる
    return textwrap.dedent(code_text).strip()

def generate_codes(project_name, blueprint):
    for module in blueprint['modules']:
        file_path = f"outputs/{project_name}/{module['path']}"
        
        # --- 1. ここで「カンニングペーパー」を準備 ---
        context_info = ""
        if 'depends_on' in module:
            for dep_file in module['depends_on']:
                dep_path = f"outputs/{project_name}/{dep_file}"
                # 前のステップで作った AST解析関数を呼び出す
                funcs = extract_function_info(dep_path) 
                filtered_funcs = [f for f in funcs if not f.startswith(func['name'])]
                if filtered_funcs:
                        context_info += f"\nFunctions available in '{dep_file}': {', '.join(filtered_funcs)}"

        for func in module['functions']:
            print(f"🛠️ Implementing {func['name']}...")
            current_module_path = module['path']
            
            # --- 2. LLMに「カンニングペーパー(context_info)」も渡す！ ---
            generated_code = call_local_llm(
                func['name'], 
                func['params'], 
                module['description'], 
                blueprint,
                context_info,
                current_module_path,
                requirements=blueprint.get('requirements', [])
            )
            
            inject_code_to_file(file_path, func['name'], generated_code)
