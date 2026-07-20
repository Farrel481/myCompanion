from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QLabel, QWidget

class Companion(QWidget):
    def __init__(self):
        super().__init__()
        self.drag_offset = None
        self.is_carried = False
        self.bob_step = 0

        self.walk_speed = 3
        self.walk_direction = 1
        self.walk_timer = QTimer(self)
        self.walk_timer.setInterval(30)
        self.walk_timer.timeout.connect(self.walk_one_step)
        self.walk_timer.start()

        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint 
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(180, 180)
        self.setCursor(Qt.OpenHandCursor)
        
        self.blob = QLabel("o", parent=self)
        self.blob.setStyleSheet("""color: #8B5CF6; font-size: 130px;""")
        self.blob.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.blob.adjustSize()
        self.blob.move(24, 8)

        self.hint = QLabel("Drag me!", parent=self)
        self.hint.setStyleSheet("""color: white; font-size: 12px;""")
        self.hint.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.center_hint()
        
        self.animation_timer = QTimer(self)
        self.animation_timer.setInterval(100)
        self.animation_timer.timeout.connect(self.animate_carried)

    def walk_one_step(self):
        if self.is_carried:
            return
        
        current_screen = self.screen()
        if current_screen is None:
            return
        
        screen_area = current_screen.availableGeometry()
        next_x = self.x() + self.walk_speed * self.walk_direction
        left_limit = screen_area.left()
        right_limit = screen_area.right() - self.width()

        if next_x <= left_limit or next_x >= right_limit:
            self.walk_direction *= -1
            next_x = self.x() + self.walk_speed * self.walk_direction

        self.move(next_x, self.y())

    def land_on_ground(self):
        current_screen = self.screen()
        if current_screen is None:
            return
        
        screen_area = current_screen.availableGeometry()
        ground_y = screen_area.bottom() - self.height() + 1
        self.move(self.x(), ground_y)

    def showEvent(self, event):
        super().showEvent(event)
        self.land_on_ground()

    def center_hint(self):
        self.hint.adjustSize()
        x_position = (self.width() - self.hint.width()) // 2
        self.hint.move(x_position, 145)

    def set_carried(self, carried):
        self.is_carried = carried
        if carried:
            self.hint.setText("Hey whachu doin!")
            self.animation_timer.start()
        else:
            self.hint.setText("Drag me!")
            self.animation_timer.stop()
            self.blob.move(24, 8)

        self.center_hint()

    def animate_carried(self):
        if not self.is_carried:
            return
        self.bob_step = (self.bob_step + 1) % 2
        if self.bob_step == 0:
            self.blob.move(24, 3)
        else:
            self.blob.move(24, 8)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_offset = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )

            self.setCursor(Qt.ClosedHandCursor)
            self.set_carried(True)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drag_offset is not None:
            new_position = event.globalPosition().toPoint() - self.drag_offset
            self.move(new_position)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_offset = None
            self.setCursor(Qt.OpenHandCursor)
            self.set_carried(False)

        self.land_on_ground()
