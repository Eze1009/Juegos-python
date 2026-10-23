from PyQt5.QtWidgets import (QApplication, QWidget,
                             QLabel, QPushButton, QListWidget, 
                             QHBoxLayout, QVBoxLayout, QMainWindow, QMessageBox)

import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QProcess, Qt
from PIL import Image, ImageFilter
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
import sys
from pathlib import Path

game_directory = Path(__file__).resolve().parent
app = QApplication(sys.argv)

App_Juegos = QWidget()
App_Juegos.setWindowTitle('Juegos')
App_Juegos.setFixedSize(900,600)

backround_path = game_directory / "fondo juegos.jpg"
backround = QLabel(App_Juegos)
backround.setPixmap(QPixmap(str(backround_path)))
backround.setGeometry(0, 0, 900, 600)
backround.setScaledContents(True)
backround.lower()
App_Juegos.setStyleSheet("QLabel { color: white; background-color: transparent;}")

title = QLabel("JUEGOS", App_Juegos)
instrucciones = QLabel("Usa las flechas izquierda y derecha para moverte.", App_Juegos)
button_exit = QPushButton("SALIR")

game_process = QProcess(App_Juegos)
game_process.setWorkingDirectory(str(game_directory))
game_process.setProgram(sys.executable)

def start_game(game_file):
    """Inicia Los juegos una sola vez y desactiva temporalmente el boton Jugar."""
    if game_process.state() != QProcess.NotRunning:
        return
    
    game_process.setArguments([str(game_directory / game_file)])
    game_process.start()

def restore_menu():
    """Vuelve a mostrar y activar la ventana del menu."""
    App_Juegos.show()
    App_Juegos.raise_()
    App_Juegos.activateWindow()

def game_finished(exit_code, exit_status):
    """Restaura el menu y avisa si el juego termino por un error."""
    restore_menu()
    if exit_status != QProcess.NormalExit or exit_code != 0:
        details = bytes(game_process.readALLStandardError()).decode(
            "utf-8", errors='replace'
        )
        QMessageBox.critical(
            App_Juegos, "Error en el juego",
            details or f"El juego se cerro inesperadamente (codigo {exit_code})",
        )

def game_error(error):
    """Muestra un mensaje de error si el proceso del juego no pudo iniciarse."""
    if error == QProcess.FailedToStart:
        QMessageBox.critical(
            App_Juegos, "No se pudo abrir el juego", game_process.errorString()
        )


button_juego1 = QPushButton("JUGAR")
button_juego2 = QPushButton("JUGAR")
button_juego3 = QPushButton("JUGAR")

list_juegos_Label_1 = QLabel("Lista de juegos")
list_juegos_Label_2 = QLabel("atrapados")
list_juegos_Label_3 = QLabel("Tirador")
list_juegos_Label_4 = QLabel("Monster Slinger")

imagen_juego1 = QLabel()
imagen_juego1.setPixmap(QPixmap(str(game_directory / "juego atrapados.png")).scaled(200, 100))

imagen_juego2 = QLabel()
imagen_juego2.setPixmap(QPixmap(str(game_directory / "juego tirador.png")).scaled(200, 100))

imagen_juego3 = QLabel()
imagen_juego3.setPixmap(QPixmap(str(game_directory / "juego monster slinger.png")).scaled(200, 100))

layout_juegos_1 = QHBoxLayout()
layout_juegos_2 = QHBoxLayout()
layout_juegos_3 = QHBoxLayout()
layout_juegos_4 = QHBoxLayout()

layout_juegos_1.addWidget(list_juegos_Label_1, alignment = Qt.AlignCenter)
layout_juegos_2.addWidget(list_juegos_Label_2, alignment = Qt.AlignCenter)
layout_juegos_3.addWidget(list_juegos_Label_3, alignment = Qt.AlignCenter)
layout_juegos_4.addWidget(list_juegos_Label_4, alignment = Qt.AlignCenter)
layout_juegos_2.addWidget(imagen_juego1,alignment = Qt.AlignCenter)
layout_juegos_3.addWidget(imagen_juego2,alignment = Qt.AlignCenter)
layout_juegos_4.addWidget(imagen_juego3,alignment = Qt.AlignCenter)
layout_juegos_2.addWidget(button_juego1, alignment = Qt.AlignCenter)
layout_juegos_3.addWidget(button_juego2, alignment = Qt.AlignCenter)
layout_juegos_4.addWidget(button_juego3, alignment = Qt.AlignCenter)
layout_principal = QVBoxLayout()
layout_principal.addWidget(title, alignment=Qt.AlignCenter)
layout_principal.addWidget(instrucciones, alignment=Qt.AlignCenter)
layout_principal.addLayout(layout_juegos_1)
layout_principal.addLayout(layout_juegos_2)
layout_principal.addLayout(layout_juegos_3)
layout_principal.addLayout(layout_juegos_4)
layout_principal.addWidget(button_exit, alignment=Qt.AlignCenter)
App_Juegos.setLayout(layout_principal)

button_juego1.clicked.connect(lambda: start_game("juego atrapados.py"))
button_juego2.clicked.connect(lambda: start_game("juego tirador.py"))
button_juego3.clicked.connect(lambda: start_game("juego monster slinger.py"))

button_exit.clicked.connect(App_Juegos.close)
game_process.started.connect(App_Juegos.hide)
game_process.finished.connect(game_finished)
game_process.errorOccurred.connect(game_error)

if __name__ == '__main__':
    App_Juegos.show()
    sys.exit(app.exec_())


