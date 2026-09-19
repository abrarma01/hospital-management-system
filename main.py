"""Hospital Management System — main entry point.

Run this file to start the application:
    python main.py
"""

from gui.main_window import MainWindow


def main() -> None:
    """Create and run the Hospital Management System GUI."""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()