from PySide6 import QtCore, QtWidgets, QtGui
import asyncio
from googletrans import Translator
from qasync import QEventLoop, asyncSlot

class Root(QtWidgets.QWidget):
    def __init__(self, loop=None):
        super().__init__()

        exit_shortcut = QtGui.QKeySequence(QtCore.Qt.Key_Escape)
        self.exit_shortcut = QtGui.QShortcut(exit_shortcut, self)
        self.exit_shortcut.activated.connect(self.close)

        translate_shortcut = QtGui.QKeySequence(QtCore.Qt.Key_Return)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Translator")
        self.resize(400, 100)

        # Input filed
        self.line_edit = QtWidgets.QLineEdit(parent=self)
        self.line_edit.setFont(QtGui.QFont("Mono", 16))

        # Button for translate function
        self.translate_button = QtWidgets.QPushButton("Translate")
        self.translate_button.clicked.connect(self.translate_text)
        self.translate_button.setShortcut(translate_shortcut)
        self.translate_button.setFont(QtGui.QFont("Mono", 0))

        # Layout
        self.layout = QtWidgets.QVBoxLayout(self)
        
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.translate_button)

        self.loop = loop or asyncio.get_event_loop()
         

    @asyncSlot()
    async def translate_text(self):
        # Making translate button dissapear 
        self.layout.removeWidget(self.translate_button)
        self.translate_button.deleteLater()
        self.translate_button = None

        # Translating
        async with Translator() as translator:
            lang_list = ["ru", "en"]
            lang = await translator.detect(self.line_edit.text())

            is_en = lang.lang == "en"
            src = lang_list[is_en]
            dest = lang_list[not is_en]

            result = await translator.translate(self.line_edit.text(), src=src, dest=dest)

            self.new_label = QtWidgets.QLabel(result.text)
            self.new_label.setFont(QtGui.QFont("Mono", 16))
            self.new_label.setFrameShape(QtWidgets.QFrame.Panel)
            self.new_label.setFrameShadow(QtWidgets.QFrame.Plain)
            self.new_label.setLineWidth(1)

            self.layout.addWidget(self.new_label)
        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    root = Root()
    root.show()

    with loop:
        loop.run_forever()