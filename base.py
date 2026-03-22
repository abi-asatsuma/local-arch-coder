import os
import json
from jinja2 import Environment, FileSystemLoader

def generate_scaffold(blueprint_name):
    # 1. パスの設定
    base_dir = os.path.dirname(__file__)
    blueprint_path = os.path.join(base_dir, 'blueprints', f'example.json')
    template_dir = os.path.join(base_dir, 'templates')
    output_base_dir = os.path.join(base_dir, 'outputs')

    # 2. 設計図(JSON)の読み込み
    with open(blueprint_path, 'r', encoding='utf-8') as f:
        blueprint = json.load(f)

    project_name = blueprint['project_name']
    project_root = os.path.join(output_base_dir, project_name)

    # 3. Jinja2環境の設定
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('default_template.j2')

    print(f"Project loading started: {project_name}")

    # 4. 各モジュールの生成
    for module in blueprint['modules']:
        # 物理パスの決定
        file_relative_path = module['path']
        full_path = os.path.join(project_root, file_relative_path)
        
        # ディレクトリの作成
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # テンプレートに渡すデータの整理
        render_data = {
            "description": module.get("description", ""),
            "module_path": file_relative_path,
            "functions": module.get("functions", []),
            "params": module.get("params", []),
            "depends_on": module.get("depends_on", [])
        }

        # テンプレートのレンダリング
        output_code = template.render(render_data)

        # ファイル書き出し
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(output_code)
        
        print(f"  ✅ Generated: {file_relative_path}")

    print(f"\nloading complete! save: 'outputs/{project_name}' directory.")

if __name__ == "__main__":
    # blueprint/example.json を指定して実行
    generate_scaffold('example')