import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTimeEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QFont, QIcon

from exam_info import ExamInfo


class PutongDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.start_time = None
        self.end_time = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("普通模式")
        self.setFixedSize(450, 300)
        
        layout = QVBoxLayout()
        
        title_label = QLabel("考试指令播放系统")
        title_label.setFont(QFont("微软雅黑", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addSpacing(30) #  添加30像素的间距
        
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(QLabel("请选择考试科目："))
        self.combo_box = QComboBox()
        self.combo_box.setFont(QFont("微软雅黑", 12))
        self.combo_box.addItem("语文")
        self.combo_box.addItem("数学")
        self.combo_box.addItem("思想政治")
        self.combo_box.addItem("外语")
        self.combo_box.addItem("物理/历史")
        self.combo_box.addItem("信息/通用技术")
        self.combo_box.addItem("化学/地理")
        self.combo_box.addItem("地理")
        self.combo_box.addItem("生物")
        self.combo_box.addItem("物理")
        self.combo_box.addItem("历史")
        self.combo_box.addItem("信息技术")
        self.combo_box.addItem("通用技术")
        self.combo_box.addItem("其他")
        self.combo_box.currentIndexChanged.connect(self.on_combo_changed)
        combo_layout.addWidget(self.combo_box)
        combo_layout.addStretch()
        layout.addLayout(combo_layout)
        
        layout.addSpacing(20)
        
        start_time_layout = QHBoxLayout()
        start_time_layout.addWidget(QLabel("考试开始时间："))
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat("HH:mm:ss")
        self.start_time_edit.setFont(QFont("微软雅黑", 12))
        start_time_layout.addWidget(self.start_time_edit)
        start_time_layout.addStretch()
        layout.addLayout(start_time_layout)
        
        layout.addSpacing(10)
        
        end_time_layout = QHBoxLayout()
        end_time_layout.addWidget(QLabel("考试结束时间："))
        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setDisplayFormat("HH:mm:ss")
        self.end_time_edit.setFont(QFont("微软雅黑", 12))
        end_time_layout.addWidget(self.end_time_edit)
        end_time_layout.addStretch()
        layout.addLayout(end_time_layout)
        
        layout.addSpacing(30)
        
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("确定")
        self.ok_btn.setFont(QFont("微软雅黑", 12))
        self.ok_btn.clicked.connect(self.on_ok)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        self.on_combo_changed(0)

    def on_combo_changed(self, index):
        if index == 0:
            self.start_time_edit.setTime(QTime(8, 0, 0))
            self.end_time_edit.setTime(QTime(10, 30, 0))
        elif index == 1:
            self.start_time_edit.setTime(QTime(8, 0, 0))
            self.end_time_edit.setTime(QTime(10, 0, 0))
        elif index == 2:
            self.start_time_edit.setTime(QTime(10, 20, 0))
            self.end_time_edit.setTime(QTime(11, 50, 0))
        elif index == 3:
            self.start_time_edit.setTime(QTime(8, 0, 0))
            self.end_time_edit.setTime(QTime(10, 0, 0))
        elif index == 4:
            self.start_time_edit.setTime(QTime(14, 0, 0))
            self.end_time_edit.setTime(QTime(15, 30, 0))
        elif index == 5:
            self.start_time_edit.setTime(QTime(15, 50, 0))
            self.end_time_edit.setTime(QTime(16, 50, 0))
        elif index == 6:
            self.start_time_edit.setTime(QTime(14, 0, 0))
            self.end_time_edit.setTime(QTime(15, 30, 0))
        elif index == 7:
            self.start_time_edit.setTime(QTime(15, 50, 0))
            self.end_time_edit.setTime(QTime(17, 20, 0))
        elif index == 8:
            self.start_time_edit.setTime(QTime(14, 0, 0))
            self.end_time_edit.setTime(QTime(15, 30, 0))
        elif index == 9:
            self.start_time_edit.setTime(QTime(14, 0, 0))
            self.end_time_edit.setTime(QTime(15, 30, 0))
        elif index == 10:
            self.start_time_edit.setTime(QTime(14, 0, 0))
            self.end_time_edit.setTime(QTime(15, 30, 0))
        elif index == 11:
            self.start_time_edit.setTime(QTime(15, 50, 0))
            self.end_time_edit.setTime(QTime(16, 50, 0))
        elif index == 12:
            self.start_time_edit.setTime(QTime(15, 50, 0))
            self.end_time_edit.setTime(QTime(16, 50, 0))
        elif index == 13:
            self.start_time_edit.setTime(QTime(0, 0, 0))
            self.end_time_edit.setTime(QTime(0, 0, 0))

    def on_ok(self):
        index = self.combo_box.currentIndex()
        kemu = self.combo_box.currentText()
        
        start_time = self.start_time_edit.time()
        end_time = self.end_time_edit.time()
        
        if start_time >= end_time:
            QMessageBox.warning(self, "错误", "考试时间配置错误，请重新配置！")
            return
        
        if (end_time.hour() - start_time.hour()) < 1:
            QMessageBox.warning(self, "错误", "考试时间间隔太短，不符合考试要求！")
            return
        
        self.close()
        
        exam_info = ExamInfo(index, kemu, "pt")
        exam_info.set_start_time(datetime.now().replace(
            hour=start_time.hour(),
            minute=start_time.minute(),
            second=start_time.second(),
            microsecond=0
        ))
        exam_info.set_end_time(datetime.now().replace(
            hour=end_time.hour(),
            minute=end_time.minute(),
            second=end_time.second(),
            microsecond=0
        ))
        exam_info.init()
        exam_info.exec_()
