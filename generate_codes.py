from llm import call_local_llm
import re

def inject_code_to_file(file_path, func_name, raw_llm_response):
    # ステップ1: 余計なチャットやバッククォートを消す
    pure_code = extract_pure_code(raw_llm_response)
    
    # ステップ2: インデントを整える
    final_code = adjust_indent(pure_code)

    # ステップ3: 書き込み（とりあえず今は追記モード 'a' のままでもOK）
    with open(file_path, 'r', encoding='utf-8') as f:
        old_content = f.read()

    target_placeholder = f"# [AI_START:{func_name}]\n    pass\n    # [AI_END:{func_name}]"
    
    # 3. 新しい中身（AIコード入り）を作る
    new_implementation = f"# [AI_START:{func_name}]\n{final_code}\n    # [AI_END:{func_name}]"
    
    # 4. 中身を入れ替える
    new_content = old_content.replace(target_placeholder, new_implementation)

    # 5. 上書き保存する
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

def adjust_indent(code_text, indent_level=4):
    spaces = " " * indent_level
    # 各行の先頭にスペースを追加する
    lines = code_text.splitlines()
    indented_lines = [f"{spaces}{line}" for line in lines]
    
    return "\n".join(indented_lines)

def generate_codes(project_name, blueprint):

    for module in blueprint['modules']:
        file_path = f"outputs/{project_name}/{module['path']}"
        
        for func in module['functions']:
            # ここで呼び出す！
            print(f"🛠️ Implementing {func['name']}...")
            
            # 2. LLMを呼び出してコードを受け取る
            generated_code = call_local_llm(func['name'], func['params'], module['description'], blueprint)
            
            # 3. 生成されたコードをファイルに書き込む
            inject_code_to_file(file_path, func['name'], generated_code)
