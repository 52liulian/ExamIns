import sys
import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton, QCheckBox, QDesktopWidget
from PyQt5.QtGui import QFont, QIcon

from settings import settings_manager, VERSION


class MainDialog(QDialog):
    """主选择对话框
    
    提供考试模式选择界面，包含高考模式和普通模式两个选项，
    以及网络校时设置复选框。
    """
    
    def __init__(self, parent=None):
        """初始化主对话框
        
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
        
        创建对话框布局，包含模式选择单选按钮、网络校时复选框和进入考试按钮。
        """
        self.setWindowTitle(f"考试指令播放系统 v{VERSION}")
        self.setFixedSize(300, 150)
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        layout = QVBoxLayout()
        
        layout.addSpacing(60)
        
        radio_layout = QHBoxLayout()
        radio_layout.addStretch()
        self.gaokao_radio = QRadioButton("高考模式")
        self.gaokao_radio.setFont(QFont("微软雅黑", 12))
        self.gaokao_radio.setChecked(True)
        radio_layout.addWidget(self.gaokao_radio)
        radio_layout.addSpacing(40)
        self.putong_radio = QRadioButton("普通模式")
        self.putong_radio.setFont(QFont("微软雅黑", 12))
        radio_layout.addWidget(self.putong_radio)
        radio_layout.addStretch()
        layout.addLayout(radio_layout)
        
        layout.addSpacing(20)
        
        ntp_layout = QHBoxLayout()
        ntp_layout.addStretch()
        self.ntp_checkbox = QCheckBox("启动时自动网络校时")
        self.ntp_checkbox.setFont(QFont("微软雅黑", 10))
        self.ntp_checkbox.setChecked(settings_manager.get_auto_ntp_sync())
        self.ntp_checkbox.stateChanged.connect(self.on_ntp_checkbox_changed)
        ntp_layout.addWidget(self.ntp_checkbox)
        ntp_layout.addStretch()
        layout.addLayout(ntp_layout)
        
        layout.addSpacing(40)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.start_btn = QPushButton("进入考试")
        self.start_btn.setFont(QFont("微软雅黑", 12))
        self.start_btn.setMinimumWidth(120)
        self.start_btn.setMinimumHeight(40)
        self.start_btn.clicked.connect(self.on_start_exam)
        button_layout.addWidget(self.start_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        layout.addSpacing(20)
        
        self.setLayout(layout)

    def on_ntp_checkbox_changed(self, state):
        """处理自动网络校时复选框状态变化
        
        Args:
            state: 复选框状态，2表示选中，0表示未选中
        """
        auto_sync = state == 2
        settings_manager.set_auto_ntp_sync(auto_sync)
    
    def on_start_exam(self):
        """处理进入考试按钮点击事件
        
        根据用户选择的模式，打开对应的模式选择界面。
        """
        self.close()
        
        if self.gaokao_radio.isChecked():
            from gaokao import GaokaoDialog
            gaokao_dialog = GaokaoDialog()
            gaokao_dialog.exec_()
        elif self.putong_radio.isChecked():
            from putong import PutongDialog
            putong_dialog = PutongDialog()
            putong_dialog.exec_()
