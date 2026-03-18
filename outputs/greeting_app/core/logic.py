

# Description: 名前を受け取って挨拶文を生成するロジック


def make_greeting(name: str) -> str:
    """
    AI TODO: make_greeting の実装
    """
    # [AI_START:make_greeting]
    from . import main
    
    name = "John"
    greeting = f"こんにちは,{name}さん"
    
    main.greet(greeting)
    # [AI_END:make_greeting]

