import sys
from PySide6.QtWidgets import QApplication
from rollos.shell import RollShell


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("RollOS")
    app.setOrganizationName("RollOS")
    window = RollShell()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
