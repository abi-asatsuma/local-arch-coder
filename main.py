# main.py (エージェントの完成形)
from base import generate_scaffold
from generate_codes import generate_codes
import json

def run_agent(blueprint_name):
    # 1. 足場を作る
    generate_scaffold(blueprint_name)
    
    # 2. 設計図を読み込み直してAI実装
    with open(f'blueprint/{blueprint_name}.json', 'r') as f:
        blueprint = json.load(f)
    generate_codes(blueprint['project_name'], blueprint)

if __name__ == "__main__":
    run_agent('example')
