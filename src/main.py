import os.path
import sys

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from MainWindow import MainWindow


def main() -> int:
	app = QApplication(sys.argv)
	main_window = MainWindow()

	bundle_dir = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
	path_to_icon = os.path.abspath(os.path.join(bundle_dir, "assets/icon.ico"))

	app.setWindowIcon(QIcon(path_to_icon))

	main_window.show()

	return app.exec()


if __name__ == '__main__':
	sys.exit(main())
