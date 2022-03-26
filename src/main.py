import sys

from PyQt6.QtWidgets import *
from MainWindow import MainWindow
from OSWrapper import OSWrapper


def main() -> int:
	app = QApplication(sys.argv)
	main_window = MainWindow()

	app.setWindowIcon(OSWrapper().get_icon())

	main_window.show()

	return app.exec()


if __name__ == '__main__':
	sys.exit(main())
