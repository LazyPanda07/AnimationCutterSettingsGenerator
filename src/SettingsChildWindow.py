from PyQt6.QtWidgets import *


def click():
	print("Click")


class SettingsChildWindow(QWidget):
	__WIDTH_STEP = 100

	__largest_width = 0

	__settings = {
		"step": [QTextEdit, "Step in frames between cuts"],
		"animationLength": [QTextEdit, "Length of each animation in frames"],
		"isRelative": [QComboBox, "true", "false"],
		"outPath": [QFileDialog, "Choose out path"],
		"animationType": [QComboBox, "localSpace", "meshSpace", "none"],
		"basePoseType": [QComboBox, "skeletonReferencePose", "animationScaled", "animationFrame", "none"],
		"interpolationType": [QComboBox, "linear", "step"],
		"generationType": [QComboBox, "standard", "prefixes", "postfixes"]
	}

	def __choose_out_path(self, file_dialog: QFileDialog, open_file_dialog: QPushButton):
		if file_dialog.exec():
			open_file_dialog.setToolTip(file_dialog.selectedFiles()[0])

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
			file_dialog = QFileDialog(self)

			file_dialog.setFileMode(QFileDialog.FileMode.Directory)

			file_dialog.setWindowTitle(data[1])

			open_file_dialog = QPushButton(data[1], self)

			open_file_dialog.clicked.connect(lambda state, x=id: self.__choose_out_path(file_dialog, open_file_dialog))

			return open_file_dialog

	def __init_widget(self, label_name: str, widget: QWidget):
		label = self.findChild(QLabel, label_name)
		geometry = label.geometry()

		widget.move(geometry.x() + SettingsChildWindow.__largest_width + SettingsChildWindow.__WIDTH_STEP, geometry.y())

		widget.setFixedHeight(geometry.height())

		label.setObjectName("")

		widget.setObjectName(label_name)

	def __init(self):
		for text, _ in SettingsChildWindow.__settings.items():
			self.__add_label_widget(text)

		for text, data in SettingsChildWindow.__settings.items():
			self.__init_widget(text, self.__create_widget(data))

	def __init__(self, parent: QWidget):
		super().__init__(parent)

		self.__init()

		bottom_left_corner = parent.geometry().bottomLeft()

		generate_button = QPushButton("Generate", self)

		bottom_left_corner.setY(bottom_left_corner.y() - generate_button.size().height())

		generate_button.move(bottom_left_corner)

		generate_button.clicked.connect(click)
