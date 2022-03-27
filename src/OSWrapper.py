import sys
import platform
import os
from PyQt6.QtGui import QIcon


class OSWrapper:
	__linux_sizes = [
		"8x8",
		"16x16",
		"20x20",
		"22x22",
		"24x24",
		"28x28",
		"32x32",
		"36x36",
		"40x40",
		"42x42",
		"48x48",
		"64x64",
		"72x72",
		"96x96",
		"128x128",
		"192x192",
		"256x256",
		"512x512"
	]

	__mac_os_sizes = [
		"16x16",
		"32x32",
		"128x128",
		"256x256",
		"512x512",
		"1024x1024"
	]

	__platform_icon_name = {
		"Windows": "icon.ico",
		"Darwin": "",
		"Linux": ""
	}

	def __get_icon_path(self) -> str:
		bundle_dir = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
		icon_path = os.path.abspath(os.path.join(bundle_dir, f"assets/{self.platform}/{OSWrapper.__platform_icon_name[self.platform]}"))

		if icon_path.__contains__("src"):
			icon_path = icon_path.replace(f"src{os.sep}", "")

		return icon_path

	def __init_icon(self, data: list[str], extension: str) -> QIcon:
		app_icon = QIcon()
		path_to_icon = self.__get_icon_path()

		for size in data:
			app_icon.addFile(path_to_icon.join(size).join(extension))

		return app_icon

	def __init__(self):
		self.platform = platform.system()

	def get_icon(self) -> QIcon:
		if self.platform == "Windows":
			return QIcon(self.__get_icon_path())

		elif self.platform == "Darwin":
			return self.__init_icon(OSWrapper.__mac_os_sizes, ".icns")

		elif self.platform == "Linux":
			return self.__init_icon(OSWrapper.__linux_sizes, ".png")
