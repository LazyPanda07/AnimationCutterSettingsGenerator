from SettingsChildWindow import *


class MainWindow(QMainWindow):
	def __init(self):
		self.setWindowTitle("AnimationCutter Settings Generator")

		self.setFixedSize(1280, 720)

		self.setCentralWidget(SettingsChildWindow(self))

	def __init__(self, parent=None):
		super().__init__(parent)

		self.__init()
