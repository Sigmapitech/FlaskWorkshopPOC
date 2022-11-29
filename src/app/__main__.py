import sys

from flask import Flask

from . import create_app


def main() -> int:
    app: Flask = create_app()
    app.run(debug=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
