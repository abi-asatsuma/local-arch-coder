import json
import sys
from base import generate_scaffold
from generate_codes import generate_codes

def run_agent(blueprint_file):
    
    # blueprints/ フォルダから指定されたファイルを読み込む
    path = f"blueprints/{blueprint_file}.json"
    with open(path, 'r', encoding='utf-8') as f:
        blueprint = json.load(f)
    
    # プロジェクト構造の生成
    generate_scaffold(blueprint['project_name'])
    
    print(f"Project started: {blueprint['project_name']}")
    
    with open(path, 'r', encoding='utf-8') as f:
        blueprint = json.load(f)
    generate_codes(blueprint['project_name'], blueprint)

if __name__ == "__main__":
    # 例: python main.py greeting_app
    target = sys.argv[1] if len(sys.argv) > 1 else 'example'
    run_agent(target)