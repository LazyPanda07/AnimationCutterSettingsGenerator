import json.encoder

from PyQt6.QtWidgets import *
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QColor


class SettingsChildWindow(QWidget):
	__WIDTH_STEP = 100

	__largest_width = 0

	__settings = {
		"step": [QTextEdit, "Step in frames between cuts"],
		"animationLength": [QTextEdit, "Length of each animation in frames"],
		"threshold": [QTextEdit, "Cut that count of frames, 0 if you don't want to use this parameter"],
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
			elif widget.objectName() == "threshold":
				if len(widget.toPlainText()) == 0:
					return 0

			return int(widget.toPlainText())

		elif isinstance(widget, QComboBox):
			text = widget.currentText()

			if text == "true" or text == "false":
				return json.loads(text.lower())

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

	@staticmethod
	def __create_item():
		item = QStandardItem()

		item.setBackground(QColor(0x808080))

		return item

	def __init_generation_type(self):
		x_offset = 5
		types = ["postfixes", "prefixes"]
		reverse = self.children()
		geometry = QRect()
		self.generation_values = QListView(self)
		model = QStandardItemModel()

		reverse.reverse()

		for widget in reverse:
			if isinstance(widget, QLabel):
				geometry = widget.geometry()

				break

		for text in types:
			label = QLabel(f"{text}:", self)

			label.move(x_offset, geometry.y() + geometry.height())

			label.setObjectName(text)

			label.hide()

			if label.geometry().width() > SettingsChildWindow.__largest_width:
				SettingsChildWindow.__largest_width = label.geometry().width()

		self.setObjectName("generationValues")

		self.generation_values.move(geometry.x() + SettingsChildWindow.__largest_width + SettingsChildWindow.__WIDTH_STEP, geometry.y() + geometry.height())

		self.generation_values.setFixedHeight(400)

		self.generation_values.verticalScrollBar()

		self.generation_values.setModel(model)

		self.generation_values.hide()

		self.add_button = QPushButton("Add", self)
		self.delete_button = QPushButton("Delete", self)

		geometry = self.generation_values.geometry()

		self.add_button.move(geometry.x(), geometry.y() + geometry.height())

		self.delete_button.move(self.add_button.geometry().x() + 75, geometry.y() + geometry.height())

		self.add_button.clicked.connect(lambda state, x=id: model.appendRow(SettingsChildWindow.__create_item()))

		self.delete_button.clicked.connect(lambda state, x=id: model.removeRow(model.rowCount() - 1))

		self.add_button.hide()

		self.delete_button.hide()

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

	def __determine_generation_type(self, index: int):
		if index == 0:
			self.findChild(QLabel, "postfixes").hide()

			self.findChild(QLabel, "prefixes").hide()

			self.generation_values.hide()

			self.add_button.hide()

			self.delete_button.hide()

		elif index == 1:
			self.findChild(QLabel, "postfixes").hide()

			self.findChild(QLabel, "prefixes").show()

			self.generation_values.show()

			self.add_button.show()

			self.delete_button.show()

		elif index == 2:
			self.findChild(QLabel, "prefixes").hide()

			self.findChild(QLabel, "postfixes").show()

			self.generation_values.show()

			self.add_button.show()

			self.delete_button.show()

	def __get_values(self) -> list[str]:
		result = list()
		model = self.generation_values.model()

		for row in range(0, model.rowCount()):
			item = model.data(model.index(row, 0))

			result.append(str(item))

		return result

	def __validate(self) -> bool:
		error_message = str()
		threshold_text = self.findChild(QTextEdit, "threshold").toPlainText()
		is_relative = json.loads(self.findChild(QComboBox, "isRelative").currentText().lower())

		if not self.findChild(QTextEdit, "step").toPlainText().isdigit():
			error_message += "step field only works with integers\n"

		if not self.findChild(QTextEdit, "animationLength").toPlainText().isdigit():
			error_message += "animationLength field only works with integers\n"

		if not threshold_text.isdigit() and len(threshold_text) > 0:
			error_message += "threshold field only works with integers\n"

		if not is_relative and self.findChild(QPushButton, "outPath") is not None and len(self.findChild(QPushButton, "outPath").toolTip()) == 0:
			error_message += "Absolute path can not be empty"

		if len(error_message) > 0:
			raise TypeError(error_message)

	def __init(self):
		for text, _ in SettingsChildWindow.__settings.items():
			self.__add_label_widget(text)

		self.__init_generation_type()

		for text, data in SettingsChildWindow.__settings.items():
			self.__init_widget(text, self.__create_widget(data))

		self.__init_out_path()

		self.findChild(QComboBox, "isRelative").currentIndexChanged.connect(lambda index: self.__is_relative_path(index))

		self.findChild(QComboBox, "generationType").currentIndexChanged.connect(lambda index: self.__determine_generation_type(index))

	def generate_json(self):
		try:
			self.__validate()
		except TypeError as e:
			QMessageBox().about(self.parent(), "Error", str(e))

			return

		with open("settings.json", "w", encoding="utf-8") as settings_file:
			json_data = dict()

			for widget_name, _ in SettingsChildWindow.__settings.items():
				json_data[widget_name] = self.__get_value_from_widget(widget_name)

			if self.findChild(QLabel, "prefixes").isVisible():
				json_data["prefixes"] = self.__get_values()

			elif self.findChild(QLabel, "postfixes").isVisible():
				json_data["postfixes"] = self.__get_values()

			json.dump(json_data, settings_file, ensure_ascii=False, indent=4)

	def __init__(self, parent: QWidget):
		super().__init__(parent)

		self.__init()

		bottom_left_corner = parent.geometry().bottomLeft()

		generate_button = QPushButton("Generate", self)

		bottom_left_corner.setY(bottom_left_corner.y() - 23)

		generate_button.move(bottom_left_corner)

		generate_button.clicked.connect(lambda state, x=id: self.generate_json())
