import ast

def extract_function_info(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

        if "```" in content:
            # バッククォートで囲まれた中身だけを抽出、または単に削除
            lines = content.splitlines()
            clean_lines = [line for line in lines if not line.strip().startswith("```")]
            content = "\n".join(clean_lines)

        node = ast.parse(content)

    functions = []
    # ファイル内の「関数定義」だけをループで探す
    for n in ast.walk(node):
        if isinstance(n, ast.FunctionDef):
            # 関数名と引数を取得
            arg_names = [arg.arg for arg in n.args.args]
            functions.append(f"{n.name}({', '.join(arg_names)})")
            
    return functions

if __name__ == "__main__":
    # テスト実行（第1回で作った logic.py を指定してみる）
    info = extract_function_info("outputs/greeting_app/core/logic.py")
    print(f"発見された関数: {info}")

