import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget, QApplication

class Companion(QWidget):
    def __init__(self):
        super().__init__()
        self.drag_offset = None
        self.setWindowFlags
        (
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint 
        )
        self.setAttribute
        (
            Qt.WA_TranslucentBackground
        )
        self.setFixedSize(180, 180)
        self.setCursor(Qt.OpenHandCursor)
        
        blob = QLabel("●", parent=self)
        blob.setStyleSheet("""
            color: #8B5CF6;
            font-size: 130px;
        """)
        blob.setAttribute(Qt.WA_TranslucentForMouseEvents)
        blob.adjustSize()
        blob.move(24, 8)

        hint = QLabel("Drag me!", parent=self)
        hint.setStyleSheet("""
            color: white;
            font-size: 12px;
        """)
        hint.setAttribute(Qt.WA_TranslucentForMouseEvents)
        hint.adjustSize()
        hint.move(58, 145)

    def mousePressEvent(self, event):
        if event.button() & Qt.leftButton and self.drag_offset is not None:
            new_position = (
                event.globalPosition().toPoint() - self.drag_offset
            )
            self.move(new_position)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.leftButton:
            self.drag_offset = None
            self.setCursor(Qt.openHandCursor)

app = QApplication(sys.argv)

companion = Companion()

companion.show()

sys.exit(app.exec())
