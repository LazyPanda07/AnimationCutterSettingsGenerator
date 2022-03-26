import sys
import platform
import os
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize


class OSWrapper:
	__linux_sizes = [
		QSize(8, 8),
		QSize(16, 16),
		QSize(20, 20),
		QSize(22, 22),
		QSize(24, 24),
		QSize(28, 28),
		QSize(32, 32),
		QSize(36, 36),
		QSize(40, 40),
		QSize(42, 42),
		QSize(48, 48),
		QSize(64, 64),
		QSize(72, 72),
		QSize(96, 96),
		QSize(128, 128),
		QSize(192, 192),
		QSize(256, 256),
		QSize(512, 512)
	]

	__platform_icon_name = {
		"Windows": "icon.ico",
		"Darwin": "icon.icns",
		"Linux": ""
	}

	def __get_icon_path(self):
		bundle_dir = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
		icon_path = os.path.abspath(os.path.join(bundle_dir, f"assets/{self.platform}/{OSWrapper.__platform_icon_name[self.platform]}"))

		if icon_path.__contains__("src"):
			icon_path = icon_path.replace(f"src{os.sep}", "")

		return icon_path

	def __init__(self):
		self.platform = platform.system()

	def get_icon(self) -> QIcon:
		if self.platform == "Windows" or self.platform == "Darwin":
			return QIcon(self.__get_icon_path())

		elif self.platform == "Linux":
			app_icon = QIcon()
			path_to_icon = self.__get_icon_path()

			for size in OSWrapper.__linux_sizes:
				app_icon.addFile(path_to_icon.join(size.width()).join('x').join(size.height()).join(".png"))

			return app_icon
