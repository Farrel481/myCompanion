import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QWidget

app = QApplication(sys.argv)

window = QWidget()

window.setWindowFlags(
    Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
)
window.setAttribute(Qt.WA_TranslucentBackground)
window.setFixedSize(180, 180)

blob = QLabel("●", parent=window)
blob.setStyleSheet("""
    color: #8B5CF6;
    font-size: 130px;
""")

blob.adjustSize()
blob.move(24, 8)

hint = QLabel("prototype", parent=window)
hint.setStyleSheet("""
    color: white;
    font-size: 12px;
""")

hint.adjustSize()
hint.move(37, 65)

window.show()
sys.exit(app.exec())