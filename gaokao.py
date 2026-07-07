import sys
import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from exam_info import ExamInfo


class GaokaoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("高考模式")
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        
        title_label = QLabel("考试指令播放系统")
        title_label.setFont(QFont("微软雅黑", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addSpacing(50)
        
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(QLabel("请选择考试科目："))
        self.combo_box = QComboBox()
        self.combo_box.setFont(QFont("微软雅黑", 12))
        self.combo_box.addItem("语文")
        self.combo_box.addItem("数学")
        self.combo_box.addItem("外语")
        self.combo_box.addItem("物理")
        self.combo_box.addItem("历史")
        self.combo_box.addItem("化学")
        self.combo_box.addItem("生物")
        self.combo_box.addItem("地理")
        self.combo_box.addItem("政治")
        combo_layout.addWidget(self.combo_box)
        combo_layout.addStretch()
        layout.addLayout(combo_layout)
        
        layout.addSpacing(50)
        
        button_layout = QHBoxLayout()
        self.back_btn = QPushButton("返回")
        self.back_btn.setFont(QFont("微软雅黑", 12))
        self.back_btn.setMinimumHeight(40)
        self.back_btn.clicked.connect(self.on_back)
        self.ok_btn = QPushButton("确定")
        self.ok_btn.setFont(QFont("微软雅黑", 12))
        self.ok_btn.setMinimumHeight(40)
        self.ok_btn.clicked.connect(self.on_ok)
        button_layout.addStretch()
        button_layout.addWidget(self.back_btn)
        button_layout.addSpacing(20)
        button_layout.addWidget(self.ok_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def on_ok(self):
        index = self.combo_box.currentIndex()
        kemu = self.combo_box.currentText()
        
        self.close()
        
        exam_info = ExamInfo(index, kemu, "gk")
        exam_info.init()
        exam_info.exec_()
    
    def on_back(self):
        self.close()
        from dialog import MainDialog
        main_dialog = MainDialog()
        main_dialog.exec_()
