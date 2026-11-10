import sys

COMMANDS = {"sweep": "sweep", "eval": "evaluate", "report": "report"}   # python -m train <명령> …

if sys.argv[1:2] and sys.argv[1] in COMMANDS:
    from importlib import import_module

    import_module(f"train.{COMMANDS[sys.argv[1]]}").main(sys.argv[2:])
elif sys.argv[1:2] in (["rescore"], ["summary"], ["answers"]):
    sys.exit(f"python -m train {sys.argv[1]} 은 없어졌습니다: python -m train report <결과 폴더> [--rescore] (train/README.md)")
else:
    from .pipeline import main

    main()
