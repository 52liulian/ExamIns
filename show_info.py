import sys
import os
from datetime import timedelta
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon


class ShowInfo(QDialog):
    def __init__(self, sound_data=None, start_time=None, end_time=None, parent=None):
        super().__init__(parent)
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.sound_data = sound_data if sound_data else []
        self.start_time = start_time
        self.end_time = end_time
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("指令列表")
        self.setFixedSize(800, 600)
        
        layout = QVBoxLayout()
        
        title_label = QLabel("考试指令列表")
        title_label.setFont(QFont("微软雅黑", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addSpacing(20)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["序号", "播放时间", "指令内容", "音频文件"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
        
        layout.addSpacing(20)
        
        button_layout = QHBoxLayout()
        self.close_btn = QPushButton("关闭")
        self.close_btn.setFont(QFont("微软雅黑", 12))
        self.close_btn.clicked.connect(self.close)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def set_data(self, sound_data, start_time, end_time):
        self.sound_data = sound_data
        self.start_time = start_time
        self.end_time = end_time

    def show_data(self):
        self.table.setRowCount(len(self.sound_data))
        
        for i, sound in enumerate(self.sound_data):
            item_no = QTableWidgetItem(str(i + 1))
            item_no.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, item_no)
            
            if sound.is_before_exam:
                play_time = self.start_time - timedelta(minutes=sound.play_time)
            else:
                play_time = self.end_time - timedelta(minutes=sound.play_time)
            
            item_time = QTableWidgetItem(play_time.strftime("%H:%M:%S"))
            item_time.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, item_time)
            
            item_content = QTableWidgetItem(sound.play_ins[:50] + "..." if len(sound.play_ins) > 50 else sound.play_ins)
            self.table.setItem(i, 2, item_content)
            
            item_file = QTableWidgetItem(sound.play_file)
            item_file.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 3, item_file)
