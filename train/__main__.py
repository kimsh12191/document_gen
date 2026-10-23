import sys

if sys.argv[1:2] == ["sweep"]:   # python -m train sweep --config <묶음.json>
    from .sweep import main

    main(sys.argv[2:])
else:
    from .pipeline import main

    main()
