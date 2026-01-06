import sys
import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton
from PyQt5.QtGui import QFont, QIcon


class MainDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("考试指令播放系统")
        self.setFixedSize(380, 200)
        
        layout = QVBoxLayout()
        
        layout.addSpacing(60)
        
        radio_layout = QHBoxLayout()
        self.gaokao_radio = QRadioButton("高考模式")
        self.gaokao_radio.setFont(QFont("微软雅黑", 12))
        self.gaokao_radio.setChecked(True)
        radio_layout.addWidget(self.gaokao_radio)
        radio_layout.addStretch()
        self.putong_radio = QRadioButton("普通模式")
        self.putong_radio.setFont(QFont("微软雅黑", 12))
        radio_layout.addWidget(self.putong_radio)
        radio_layout.addStretch()
        layout.addLayout(radio_layout)
        
        layout.addSpacing(60)
        
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("进入考试")
        self.start_btn.setFont(QFont("微软雅黑", 12))
        self.start_btn.clicked.connect(self.on_start_exam)
        button_layout.addStretch()
        button_layout.addWidget(self.start_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def on_start_exam(self):
        self.close()
        
        if self.gaokao_radio.isChecked():
            from gaokao import GaokaoDialog
            gaokao_dialog = GaokaoDialog()
            gaokao_dialog.exec_()
        elif self.putong_radio.isChecked():
            from putong import PutongDialog
            putong_dialog = PutongDialog()
            putong_dialog.exec_()
