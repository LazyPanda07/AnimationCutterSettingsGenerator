import json.encoder
import threading

from PyQt6.QtWidgets import *


class SettingsChildWindow(QWidget):
	__WIDTH_STEP = 100

	__largest_width = 0

	__settings = {
		"step": [QTextEdit, "Step in frames between cuts"],
		"animationLength": [QTextEdit, "Length of each animation in frames"],
		"isRelative": [QComboBox, "false", "true"],
		"outPath": [QFileDialog, "Choose out path"],
		"animationType": [QComboBox, "localSpace", "meshSpace", "none"],
		"basePoseType": [QComboBox, "skeletonReferencePose", "animationScaled", "animationFrame", "none"],
		"interpolationType": [QComboBox, "linear", "step"],
		"generationType": [QComboBox, "standard", "prefixes", "postfixes"]
	}

	def __choose_out_path(self, open_file_dialog: QPushButton):
		if self.file_dialog.exec():
			open_file_dialog.setToolTip(self.file_dialog.selectedFiles()[0])

		self.parent().activateWindow()

	def __add_label_widget(self, text: str):
		x = 5
		y = 5
		height = 0

		if len(self.children()) != 0:
			reverse = self.children()

			reverse.reverse()

			for widget in reverse:
				if isinstance(widget, QLabel):
					geometry = widget.geometry()

					y = geometry.y()
					height = geometry.height()

					break

		label = QLabel(f"{text}:", self)

		label.setObjectName(text)

		label.move(x, y + height)

		if label.geometry().width() > SettingsChildWindow.__largest_width:
			SettingsChildWindow.__largest_width = label.geometry().width()

	def __create_widget(self, data: list) -> QWidget:
		if issubclass(data[0], QTextEdit):
			text_edit = QTextEdit(self)

			text_edit.setPlaceholderText(data[1])

			return text_edit

		elif issubclass(data[0], QComboBox):
			combo_box = QComboBox(self)

			for i in range(1, len(data)):
				combo_box.addItem(data[i])

			return combo_box

		else:
			self.file_dialog = QFileDialog(self)

			self.file_dialog.setFileMode(QFileDialog.FileMode.Directory)

			self.file_dialog.setWindowTitle(data[1])

			open_file_dialog = QPushButton(data[1], self)

			open_file_dialog.clicked.connect(lambda state, x=id: self.__choose_out_path(open_file_dialog))

			return open_file_dialog

	def __init_widget(self, label_name: str, widget: QWidget):
		label = self.findChild(QLabel, label_name)
		geometry = label.geometry()

		widget.move(geometry.x() + SettingsChildWindow.__largest_width + SettingsChildWindow.__WIDTH_STEP, geometry.y())

		widget.setFixedHeight(geometry.height())

		label.setObjectName("")

		widget.setObjectName(label_name)

	def __get_value_from_widget(self, widget_name: str):
		widget = self.findChild(QWidget, widget_name)

		if isinstance(widget, QTextEdit):
			if widget.objectName() == "outPath":
				return widget.toPlainText()

			return int(widget.toPlainText())

		elif isinstance(widget, QComboBox):
			text = widget.currentText()

			if text == "true" or text == "false":
				return bool(text)

			return text

		elif isinstance(widget, QPushButton):
			return widget.toolTip()

	def __init_out_path(self):
		self.out_path_button = self.findChild(QPushButton, "outPath")
		self.out_path_edit_text = QTextEdit(self)

		geometry = self.out_path_button.geometry()

		self.out_path_edit_text.setPlaceholderText("Relative path")

		self.out_path_edit_text.move(geometry.x(), geometry.y())

		self.out_path_edit_text.setFixedHeight(geometry.height())

		self.out_path_edit_text.hide()

	def __is_relative_path(self, index: int):
		if index == 0:
			self.out_path_button.show()

			self.out_path_edit_text.hide()

			self.out_path_button.setObjectName(self.out_path_edit_text.objectName())

			self.out_path_edit_text.setObjectName("")

		elif index == 1:
			self.out_path_button.hide()

			self.out_path_edit_text.show()

			self.out_path_edit_text.setObjectName(self.out_path_button.objectName())

			self.out_path_button.setObjectName("")

	def __init(self):
		for text, _ in SettingsChildWindow.__settings.items():
			self.__add_label_widget(text)

		for text, data in SettingsChildWindow.__settings.items():
			self.__init_widget(text, self.__create_widget(data))

		self.__init_out_path()

		self.findChild(QComboBox, "isRelative").currentIndexChanged.connect(lambda index: self.__is_relative_path(index))

	def generate_json(self):
		with open("settings.json", "w", encoding="utf-8") as settings_file:
			json_data = dict()

			for widget_name, _ in SettingsChildWindow.__settings.items():
				json_data[widget_name] = self.__get_value_from_widget(widget_name)

			json.dump(json_data, settings_file, ensure_ascii=False, indent=4)

	def __init__(self, parent: QWidget):
		super().__init__(parent)

		self.__init()

		bottom_left_corner = parent.geometry().bottomLeft()

		generate_button = QPushButton("Generate", self)

		bottom_left_corner.setY(bottom_left_corner.y() - generate_button.size().height())

		generate_button.move(bottom_left_corner)

		generate_button.clicked.connect(lambda state, x=id: self.generate_json())
