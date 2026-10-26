import sys

if sys.argv[1:2] == ["sweep"]:   # python -m train sweep --config <묶음.json>
    from .sweep import main

    main(sys.argv[2:])
elif sys.argv[1:2] == ["rescore"]:   # python -m train rescore <workdir|결과 폴더> ...
    from .rescore import main

    main(sys.argv[2:])
elif sys.argv[1:2] == ["summary"]:   # python -m train summary <묶음.json|결과 폴더> ... --out <html>
    from .summary import main

    main(sys.argv[2:])
elif sys.argv[1:2] == ["answers"]:   # python -m train answers <묶음.json|결과 폴더|workdir> [--per-task N]
    from .answers import main

    main(sys.argv[2:])
else:
    from .pipeline import main

    main()
