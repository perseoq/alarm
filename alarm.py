import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox, QSpinBox,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import QTimer, QTime, Qt
from PySide6.QtGui import QFontDatabase, QFont
import pygame


class AlarmClock(QWidget):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()

        self.setWindowTitle("Alarma")
        self.setFixedSize(510, 370)
        self.setStyleSheet("background-color: #95AD81;")

        self.alarm_time = None
        self.is_alarm_active = False
        self.init_ui()
        self.start_timer()

    
  

    def init_ui(self):
        def get_resource_path(relative_path):
            """Retorna la ruta al archivo ya sea en modo desarrollo o empaquetado con PyInstaller."""
            base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
            return os.path.join(base_path, relative_path)  
        # ======= RELOJ: HORA ACTUAL =======
        lbl_actual = QLabel("HORA ACTUAL")
        lbl_actual.setStyleSheet("font-weight: bold;")
        fuente1 = get_resource_path("fonts/font.ttf")
        fuente2 = get_resource_path("fonts/ubuntu.ttf")
        font_id = QFontDatabase.addApplicationFont(fuente1)
        ubuntu_id = QFontDatabase.addApplicationFont(fuente2)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QFont(font_family, 70, QFont.Bold)
        elif ubuntu_id != -1:
            ubuntu_family = QFontDatabase.applicationFontFamilies(ubuntu_id)[0]
            custom_font = QFont(ubuntu_family, 70, QFont.Bold)
        else:
            custom_font = QFont("Arial", 70, QFont.Bold)

        self.current_display = QLabel("07:20")
        self.current_display.setAlignment(Qt.AlignCenter)
        self.current_display.setFont(custom_font)
        self.current_display.setFixedSize(280, 100)
        self.current_display.setStyleSheet(
            "background-color: #2e2e2e; color: white; padding: 10px;"
        )

        # ======= RELOJ: HORA ALARMA =======
        lbl_alarma = QLabel("HORA ALARMA")
        lbl_alarma.setStyleSheet("font-weight: bold;")
        self.alarm_display = QLabel("07:22")
        self.alarm_display.setAlignment(Qt.AlignCenter)
        self.current_display.setFont(custom_font)
        self.alarm_display.setFont(custom_font)        
        self.alarm_display.setFixedSize(280, 100)
        self.alarm_display.setStyleSheet(
            "background-color: #2e2e2e; color: white; padding: 10px;"
        )

        # Izquierda (relojes)
        left = QVBoxLayout()
 
        left.addWidget(lbl_actual)
        left.setSpacing(3)
        left.addWidget(self.current_display)

        left.addWidget(lbl_alarma)
        left.addWidget(self.alarm_display)

        # ======= DERECHA: Controles =======
        lbl_minutos = QLabel("MINUTOS")
        self.spin_minutos = QSpinBox()
        self.spin_minutos.setRange(1, 120)
        self.spin_minutos.setFixedSize(180, 30)

        lbl_sonido = QLabel("SONIDO")
        self.sound_combo = QComboBox()
        self.sound_combo.setFixedSize(180, 30)
        self.load_sounds()

        self.btn_activar = QPushButton("ACTIVAR ALARMA")
        self.btn_activar.setFixedSize(180, 40)
        self.btn_activar.setStyleSheet("background-color: #198CA6; color: white;")
        self.btn_activar.clicked.connect(self.activar_alarma)

        self.btn_cancelar = QPushButton("CANCELAR ALARMA")
        self.btn_cancelar.setFixedSize(180, 40)
        self.btn_cancelar.setStyleSheet("background-color: #5BD75B; color: white;")
        self.btn_cancelar.clicked.connect(self.cancelar_alarma)
        self.btn_cancelar.hide()

        self.btn_detener = QPushButton("DETENER ALARMA")
        self.btn_detener.setFixedSize(180, 40)
        self.btn_detener.setStyleSheet("background-color: #CB4E19; color: white;")
        self.btn_detener.clicked.connect(self.detener_alarma)

        right = QVBoxLayout()
        right.addSpacing(50)
        right.addWidget(lbl_minutos)
        right.addWidget(self.spin_minutos)
        right.setSpacing(10)
        right.addWidget(lbl_sonido)
        right.addWidget(self.sound_combo)
        right.addSpacing(600)
        right.addWidget(self.btn_activar)
        right.addWidget(self.btn_cancelar)
        right.addSpacing(10)
        right.addWidget(self.btn_detener)
        right.addStretch()

        # Layout principal
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(30)
        layout.addLayout(left)
        layout.addLayout(right)

        self.setLayout(layout)

    def load_sounds(self):

        def get_resource_path(relative_path):
            base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
            return os.path.join(base_path, relative_path)

        self.sound_combo.clear()
        
        sounds_dir = get_resource_path("sounds")

        if not os.path.exists(sounds_dir):
            os.makedirs(sounds_dir)  # Sólo útil fuera de PyInstaller

        for file in os.listdir(sounds_dir):
            if file.endswith(".mp3"):
                self.sound_combo.addItem(file)

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        now = QTime.currentTime()
        self.current_display.setText(now.toString("HH:mm"))
        if self.is_alarm_active and self.alarm_time == now.toString("HH:mm"):
            self.activar_alerta()

    def activar_alarma(self):
        now = QTime.currentTime()
        mins = self.spin_minutos.value()
        alarma = now.addSecs(mins * 60)
        self.alarm_time = alarma.toString("HH:mm")
        self.alarm_display.setText(self.alarm_time)
        self.is_alarm_active = True
        self.btn_activar.hide()
        self.btn_cancelar.show()

    def cancelar_alarma(self):
        self.is_alarm_active = False
        self.alarm_display.setText("--:--")
        self.btn_cancelar.hide()
        self.btn_activar.show()

    def activar_alerta(self):
        self.is_alarm_active = False
        self.alarm_display.setText("ALARM!")
        self.reproducir_sonido()
        self.btn_cancelar.show()
        self.btn_activar.hide()

    def detener_alarma(self):
        pygame.mixer.music.stop()
        self.alarm_display.setText("--:--")
        self.btn_cancelar.hide()
        self.btn_activar.show()

    def reproducir_sonido(self):
        def get_resource_path(relative_path):
            base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
            return os.path.join(base_path, relative_path)
        file_name = self.sound_combo.currentText()
        sound_path = get_resource_path(f"sounds/{file_name}")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(loops=-1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AlarmClock()
    ventana.show()
    sys.exit(app.exec())
