import sys
import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from exam_info import ExamInfo


class GaokaoDialog(QDialog):
    """高考模式选择对话框
    
    提供高考模式下的考试科目选择界面，包含9个科目选项。
    """
    
    def __init__(self, parent=None):
        """初始化高考模式对话框
        
        Args:
            parent: 父窗口对象
        """
        super().__init__(parent)
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.init_ui()

    def init_ui(self):
        """初始化用户界面
        
        创建对话框布局，包含标题、科目选择下拉框和确认/返回按钮。
        """
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
        """处理确定按钮点击事件
        
        获取用户选择的科目，创建考试信息界面并显示。
        
        Returns:
            None
        """
        index = self.combo_box.currentIndex()
        kemu = self.combo_box.currentText()
        
        self.close()
        
        exam_info = ExamInfo(index, kemu, "gk")
        exam_info.init()
        exam_info.exec_()
    
    def on_back(self):
        """处理返回按钮点击事件
        
        返回主选择界面。
        
        Returns:
            None
        """
        self.close()
        from dialog import MainDialog
        main_dialog = MainDialog()
        main_dialog.exec_()
