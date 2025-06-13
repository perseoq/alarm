import os
import sys
from datetime import datetime, timedelta
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                              QLabel, QPushButton, QSpinBox, QComboBox, QWidget)
from PySide6.QtCore import QTimer, QTime, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput


class AlarmClock(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Alarma")
        self.setFixedSize(400, 250)
        
        # Configuración del reproductor de audio
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        # Variables
        self.alarm_time = None
        self.alarm_active = False
        
        # Widgets
        self.current_time_label = QLabel("Hora actual: ")
        self.alarm_time_label = QLabel("Hora de la alarma: --:--")
        self.minutes_input = QSpinBox()
        self.minutes_input.setRange(1, 1440)  # De 1 minuto a 24 horas
        self.minutes_input.setValue(10)
        
        self.sound_selector = QComboBox()
        self.load_sounds()
        
        self.set_alarm_button = QPushButton("Activar Alarma")
        self.set_alarm_button.clicked.connect(self.toggle_alarm)
        self.stop_button = QPushButton("Detener Alarma")
        self.stop_button.clicked.connect(self.stop_alarm)
        self.stop_button.setEnabled(False)
        
        # Diseño
        main_layout = QVBoxLayout()
        
        # Hora actual
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Hora actual:"))
        time_layout.addWidget(self.current_time_label)
        main_layout.addLayout(time_layout)
        
        # Configuración de alarma
        config_layout = QHBoxLayout()
        config_layout.addWidget(QLabel("Minutos programados:"))
        config_layout.addWidget(self.minutes_input)
        main_layout.addLayout(config_layout)
        
        # Selección de sonido
        sound_layout = QHBoxLayout()
        sound_layout.addWidget(QLabel("Sonido de alarma:"))
        sound_layout.addWidget(self.sound_selector)
        main_layout.addLayout(sound_layout)
        
        # Hora de alarma
        alarm_time_layout = QHBoxLayout()
        alarm_time_layout.addWidget(QLabel("Hora en la que suena la alarma:"))
        alarm_time_layout.addWidget(self.alarm_time_label)
        main_layout.addLayout(alarm_time_layout)
        
        # Botones
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.set_alarm_button)
        button_layout.addWidget(self.stop_button)
        main_layout.addLayout(button_layout)
        
        # Configurar widget central
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Temporizador para actualizar la hora
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Actualizar cada segundo
        
        # Temporizador para verificar la alarma
        self.alarm_check_timer = QTimer()
        self.alarm_check_timer.timeout.connect(self.check_alarm)
        
        self.update_time()
    
    def load_sounds(self):
        """Carga los archivos MP3 de la carpeta sounds/"""
        sounds_dir = "sounds"
        if not os.path.exists(sounds_dir):
            os.makedirs(sounds_dir)
            print(f"Se creó la carpeta {sounds_dir}. Por favor, añade archivos MP3.")
        
        self.sound_selector.clear()
        self.sound_selector.addItem("-- Seleccionar --", None)
        
        for file in os.listdir(sounds_dir):
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(sounds_dir, file)
                self.sound_selector.addItem(file, file_path)
    
    def update_time(self):
        """Actualiza la hora actual en la interfaz"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.current_time_label.setText(current_time)
        
        # Si hay una alarma activa, actualiza el tiempo restante
        if self.alarm_active and self.alarm_time:
            remaining = self.alarm_time - datetime.now()
            if remaining.total_seconds() > 0:
                mins, secs = divmod(int(remaining.total_seconds()), 60)
                self.alarm_time_label.setText(f"{mins:02d}:{secs:02d} restantes")
            else:
                self.alarm_time_label.setText("¡ALARMA!")
    
    def toggle_alarm(self):
        """Activa o desactiva la alarma"""
        if self.alarm_active:
            self.cancel_alarm()
        else:
            self.set_alarm()
    
    def set_alarm(self):
        """Configura la alarma para que suene en los minutos especificados"""
        minutes = self.minutes_input.value()
        sound_path = self.sound_selector.currentData()
        
        if not sound_path:
            print("Por favor, selecciona un sonido de alarma")
            return
        
        self.alarm_time = datetime.now() + timedelta(minutes=minutes)
        self.alarm_active = True
        self.alarm_check_timer.start(1000)  # Verificar cada segundo
        
        self.set_alarm_button.setText("Cancelar Alarma")
        self.stop_button.setEnabled(False)
        self.minutes_input.setEnabled(False)
        self.sound_selector.setEnabled(False)
        
        alarm_time_str = self.alarm_time.strftime("%H:%M:%S")
        self.alarm_time_label.setText(alarm_time_str)
        print(f"Alarma programada para las {alarm_time_str}")
    
    def cancel_alarm(self):
        """Cancela la alarma programada"""
        self.alarm_active = False
        self.alarm_check_timer.stop()
        
        self.set_alarm_button.setText("Activar Alarma")
        self.minutes_input.setEnabled(True)
        self.sound_selector.setEnabled(True)
        self.alarm_time_label.setText("--:--")
        
        print("Alarma cancelada")
    
    def check_alarm(self):
        """Verifica si es hora de que suene la alarma"""
        if self.alarm_active and datetime.now() >= self.alarm_time:
            self.trigger_alarm()
    
    def trigger_alarm(self):
        """Reproduce el sonido de alarma"""
        sound_path = self.sound_selector.currentData()
        if sound_path:
            self.player.setSource(QUrl.fromLocalFile(sound_path))
            self.player.play()
            self.alarm_active = False
            self.set_alarm_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.alarm_time_label.setText("¡ALARMA!")
            print("¡ALARMA!")
    
    def stop_alarm(self):
        """Detiene el sonido de la alarma"""
        self.player.stop()
        self.stop_button.setEnabled(False)
        self.alarm_time_label.setText("--:--")
        print("Alarma detenida")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AlarmClock()
    window.show()
    sys.exit(app.exec())