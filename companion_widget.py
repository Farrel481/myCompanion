import random

from pathlib import Path
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QWidget

class Companion(QWidget):
    BLOB_X = 10
    BLOB_Y = 0

    def __init__(self):
        super().__init__()
        self.drag_offset = None
        self.is_carried = False
        self.bob_step = 0 
        self.default_position_set = False

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(180, 180)
        self.setCursor(Qt.OpenHandCursor)

        sprite_folder = Path(__file__).parent/"assets"/"sprites"
        idle_1 = QPixmap(str(sprite_folder/"slime_idle_1.png"))
        idle_2 = QPixmap(str(sprite_folder/"slime_idle_2.png"))
        
        if idle_1.isNull() or idle_2.isNull():
            raise FileNotFoundError("File on assets folder can't be read. Check.")
        
        self.idle_frames = [
            idle_1.scaled(160, 160, Qt.KeepAspectRatio, Qt.FastTransformation),
            idle_2.scaled(160, 160, Qt.KeepAspectRatio, Qt.FastTransformation),
        ]
        self.idle_frame_index = 0

        self.blob = QLabel(parent = self)
        self.blob.setPixmap(self.idle_frames[self.idle_frame_index])
        self.blob.setFixedSize(160, 160)
        self.blob.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.blob.move(self.BLOB_X, self.BLOB_Y)

        self.hint = QLabel(parent=self)
        self.hint.setStyleSheet("""color: white; font-size: 12px;""")
        self.hint.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.hint.hide()

        self.idle_timer = QTimer(self)
        self.idle_timer.setSingleShot(True)
        self.idle_timer.timeout.connect(self.animate_idle)

        self.carry_timer = QTimer(self)
        self.carry_timer.setInterval(100)
        self.carry_timer.timeout.connect(self.animate_carried)

    def default_place(self):
        current_screen = self.screen()
        if current_screen is None:
            return
        screen_area = current_screen.availableGeometry()

        x_position = (screen_area.right() - self.width() - 15)
        y_position = (screen_area.bottom() - self.height() + 1)

        self.move(x_position, y_position)

    def schedule_blink(self):
        if self.is_carried:
            return
        if self.idle_frame_index == 0:
            delay=random.randint(3200, 11200)
        else:
            delay= 180
        
        self.idle_timer.start(delay)
    
    def animate_idle(self):
        if self.is_carried:
            return
        self.idle_frame_index = (self.idle_frame_index+ 1) %len (self.idle_frames)

        self.blob.setPixmap(self.idle_frames[self.idle_frame_index])

        self.schedule_blink()

    def center_hint(self):
        self.hint.adjustSize()

        x_position =(self.width() - self.hint.width()) // 2

        self.hint.move(x_position, 145)

    def set_carried(self, carried):
        self.is_carried = carried

        if carried:
            self.idle_timer.stop()
            self.hint.setText("Hey! Whachu doin?")
            self.center_hint()
            self.hint.show()
            self.carry_timer.start()

        else:
            self.carry_timer.stop()
            self.blob.move(self.BLOB_X, self.BLOB_Y)
            self.hint.hide()
            self.schedule_blink()

    def animate_carried(self):
        if not self.is_carried:
            return
            
        self.bob_step = (self.bob_step + 1)%2

        if self.bob_step == 0:
            self.blob.move(self.BLOB_X, 0)
        else:
            self.blob.move(self.BLOB_X, 7)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_offset = (event.globalPosition().toPoint() - self.frameGeometry().topLeft())

            self.setCursor(Qt.ClosedHandCursor)
            self.set_carried(True)
    
    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton and self.drag_offset is not None):
            new_position = (event.globalPosition().toPoint() - self.drag_offset)

            self.move(new_position)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_offset = None
            self.setCursor(Qt.OpenHandCursor)
            self.set_carried(False)

    def showEvent(self, event):
        super().showEvent(event)
        if not self.default_position_set:
            self.default_place()
            self.default_position_set = True

        self.schedule_blink()
        

