import sys
import os
import logging
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QIcon

from data import SoundData, Sound
from player import AudioPlayer


class ExamInfo(QDialog):
    def __init__(self, index=0, kemu="", exam_type="", parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            self.logger.info(f"加载窗口图标: {icon_path}")
        else:
            self.logger.warning(f"窗口图标不存在: {icon_path}")
        
        self.index = index
        self.kemu = kemu
        self.exam_type = exam_type
        self.start_time = None
        self.end_time = None
        self.current_index = 0
        self.sound_data = []
        self.play_time_list = []
        
        self.logger.info(f"初始化考试信息 - 类型: {exam_type}, 科目: {kemu}, 索引: {index}")
        
        self.player = AudioPlayer()
        self.player.over.connect(self.next_ins)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_time)
        
        self.init_ui()
        self.init_exam_times()

    def init_ui(self):
        self.setWindowTitle("考试信息")
        self.setFixedSize(600, 400)
        
        layout = QVBoxLayout()
        
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel("科目:"))
        self.kemu_label = QLabel()
        self.kemu_label.setFont(QFont("微软雅黑", 12, QFont.Bold))
        info_layout.addWidget(self.kemu_label)
        info_layout.addStretch()
        
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("开始时间:"))
        self.start_time_label = QLabel()
        time_layout.addWidget(self.start_time_label)
        time_layout.addWidget(QLabel("结束时间:"))
        self.end_time_label = QLabel()
        time_layout.addWidget(self.end_time_label)
        
        system_layout = QHBoxLayout()
        system_layout.addWidget(QLabel("系统时间:"))
        self.system_time_label = QLabel()
        self.system_time_label.setFont(QFont("微软雅黑", 14, QFont.Bold))
        system_layout.addWidget(self.system_time_label)
        system_layout.addStretch()
        
        ins_layout = QVBoxLayout()
        ins_layout.addWidget(QLabel("当前/下条指令:"))
        self.ins_label = QLabel()
        self.ins_label.setFont(QFont("微软雅黑", 11))
        ins_layout.addWidget(self.ins_label)
        
        content_layout = QVBoxLayout()
        content_layout.addWidget(QLabel("指令内容:"))
        self.ins_content_label = QLabel()
        self.ins_content_label.setWordWrap(True)
        self.ins_content_label.setFont(QFont("微软雅黑", 10))
        content_layout.addWidget(self.ins_content_label)
        
        button_layout = QHBoxLayout()
        self.ins_list_btn = QPushButton("查看指令列表")
        self.ins_list_btn.clicked.connect(self.show_ins_list)
        self.stop_btn = QPushButton("停止")
        self.stop_btn.clicked.connect(self.stop_exam)
        button_layout.addWidget(self.ins_list_btn)
        button_layout.addWidget(self.stop_btn)
        
        layout.addLayout(info_layout)
        layout.addLayout(time_layout)
        layout.addLayout(system_layout)
        layout.addLayout(ins_layout)
        layout.addLayout(content_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def init_exam_times(self):
        self.logger.info("初始化考试时间配置")
        if self.exam_type == "gk":
            self.logger.info("高考模式时间配置")
            if self.index == 0 or self.index == 2:
                self.start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
                self.end_time = datetime.now().replace(hour=11, minute=30, second=0, microsecond=0)
                self.logger.info(f"设置考试时间: 开始={self.start_time.strftime('%H:%M:%S')}, 结束={self.end_time.strftime('%H:%M:%S')}")
            elif self.index == 1 or self.index == 3:
                self.start_time = datetime.now().replace(hour=15, minute=0, second=0, microsecond=0)
                self.end_time = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
                self.logger.info(f"设置考试时间: 开始={self.start_time.strftime('%H:%M:%S')}, 结束={self.end_time.strftime('%H:%M:%S')}")
        
        if self.start_time and self.end_time:
            self.kemu_label.setText(self.kemu)
            self.start_time_label.setText(self.start_time.strftime("%H:%M:%S"))
            self.end_time_label.setText(self.end_time.strftime("%H:%M:%S"))
            self.logger.info("考试时间显示已更新")
        self.update_system_time()

    def set_start_time(self, start_time):
        self.start_time = start_time
        self.logger.info(f"设置考试开始时间: {start_time.strftime('%H:%M:%S')}")

    def set_end_time(self, end_time):
        self.end_time = end_time
        self.logger.info(f"设置考试结束时间: {end_time.strftime('%H:%M:%S')}")

    def init(self):
        self.logger.info("初始化考试信息界面")
        if self.start_time and self.end_time:
            self.kemu_label.setText(self.kemu)
            self.start_time_label.setText(self.start_time.strftime("%H:%M:%S"))
            self.end_time_label.setText(self.end_time.strftime("%H:%M:%S"))
            self.logger.info("考试信息显示已更新")
        
        try:
            self.init_ins()
            self.init_info()
            if self.play_time_list:
                self.timer.start(10)
                self.logger.info("考试计时器已启动")
        except Exception as e:
            self.logger.error(f"初始化考试信息失败: {e}", exc_info=True)
            QMessageBox.critical(self, "错误", f"初始化考试信息失败: {str(e)}")

    def init_info(self):
        self.update_system_time()

    def init_ins(self):
        self.logger.info("初始化考试指令列表")
        try:
            ins_data = SoundData(self.exam_type)
            ins_data.set_sound()
            self.sound_data = ins_data.get_sound()
            self.logger.info(f"加载了 {len(self.sound_data)} 条考试指令")
            
            # 外语科目时使用p5w.mp3
            if (self.exam_type == "gk" and self.index == 3) or (self.exam_type == "pt" and self.index == 3):  # index 3 对应外语科目
                for i, sound in enumerate(self.sound_data):
                    if sound.play_file == "p5.mp3":
                        self.sound_data[i] = Sound(
                            play_time=sound.play_time,
                            play_ins=sound.play_ins,
                            play_file="p5w.mp3",
                            is_before_exam=sound.is_before_exam
                        )
                        self.logger.info(f"外语科目：将指令 {i} 的音频文件从 {sound.play_file} 改为 p5w.mp3")
                        break
            
            self.play_time_list = []
            for sound in self.sound_data:
                if sound.is_before_exam:
                    play_time = self.start_time - timedelta(minutes=sound.play_time)
                else:
                    play_time = self.end_time - timedelta(minutes=sound.play_time)
                self.play_time_list.append(play_time)
                self.logger.info(f"指令 '{sound.play_ins}' 播放时间: {play_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            current_time = datetime.now()
            if current_time > self.play_time_list[-1]:
                self.ins_label.setText("播放时间：到播放队列尾！")
                self.logger.info("当前时间已超过最后一条指令的播放时间")
                return
            
            if current_time < self.play_time_list[0]:
                self.ins_label.setText(f"即将播放指令时间：{self.play_time_list[0].strftime('%H:%M:%S')}")
                self.ins_content_label.setText(self.sound_data[0].play_ins)
                self.logger.info(f"下条指令时间: {self.play_time_list[0].strftime('%H:%M:%S')}")
                return
            
            for i, play_time in enumerate(self.play_time_list):
                if current_time > play_time:
                    continue
                else:
                    self.current_index = i
                    break
            
            self.ins_label.setText(f"下条指令播放时间：{self.play_time_list[self.current_index].strftime('%H:%M:%S')}")
            self.ins_content_label.setText(self.sound_data[self.current_index].play_ins)
            self.logger.info(f"当前指令索引: {self.current_index}, 下条指令时间: {self.play_time_list[self.current_index].strftime('%H:%M:%S')}")
        except Exception as e:
            self.logger.error(f"初始化考试指令失败: {e}", exc_info=True)
            QMessageBox.critical(self, "错误", f"初始化考试指令失败: {str(e)}")

    def update_system_time(self):
        current_time = datetime.now()
        self.system_time_label.setText(current_time.strftime("%H:%M:%S"))

    def check_time(self):
        current_time = datetime.now()
        self.update_system_time()
        
        if current_time.second == 0:
            for i, play_time in enumerate(self.play_time_list):
                if current_time.hour == play_time.hour and current_time.minute == play_time.minute and current_time.second == play_time.second:
                    self.logger.info(f"时间到，开始播放指令 {i}")
                    self.play_ins(i)
                    break

    def play_ins(self, index):
        if index < 0 or index >= len(self.sound_data):
            self.logger.error(f"无效的指令索引: {index}")
            return
        
        self.current_index = index
        sound = self.sound_data[index]
        
        self.ins_label.setText(f"播放时间：{self.play_time_list[index].strftime('%H:%M:%S')}")
        self.ins_content_label.setText(sound.play_ins)
        
        self.logger.info(f"开始播放指令 {index}: {sound.play_ins}")
        self.play_mp3(f"Mp3/{sound.play_file}")

    def play_mp3(self, file_path):
        if not file_path:
            self.logger.error("音频文件路径为空")
            QMessageBox.critical(self, "错误", "音频文件错误！")
            return
        
        abs_path = os.path.join(os.path.dirname(__file__), file_path)
        if not os.path.exists(abs_path):
            self.logger.error(f"音频文件不存在: {abs_path}")
            QMessageBox.critical(self, "错误", f"音频文件不存在: {file_path}！")
            return
        
        self.logger.info(f"准备播放音频文件: {abs_path}")
        self.player.set_file_path(abs_path)
        self.player.play_mp3()

    def next_ins(self):
        if self.current_index + 1 == len(self.play_time_list):
            self.ins_label.setText("指令播放结束！")
            self.ins_content_label.setText("")
            self.logger.info("所有指令播放完成")
        else:
            self.ins_label.setText(f"下条指令播放时间：{self.play_time_list[self.current_index + 1].strftime('%H:%M:%S')}")
            self.ins_content_label.setText(self.sound_data[self.current_index + 1].play_ins)
            self.logger.info(f"准备播放下一条指令: {self.current_index + 1}")

    def show_ins_list(self):
        self.logger.info("显示指令列表")
        try:
            from show_info import ShowInfo
            show_info = ShowInfo(self.sound_data, self.start_time, self.end_time)
            show_info.show_data()
            show_info.exec_()
        except Exception as e:
            self.logger.error(f"显示指令列表失败: {e}", exc_info=True)

    def stop_exam(self):
        self.logger.info("停止考试")
        self.player.stop_play()
        self.timer.stop()
        self.close()
        
        if self.exam_type == "gk":
            self.logger.info("返回高考模式选择界面")
            from gaokao import GaokaoDialog
            gaokao_dialog = GaokaoDialog()
            gaokao_dialog.exec_()
        elif self.exam_type == "pt":
            self.logger.info("返回普通模式选择界面")
            from putong import PutongDialog
            putong_dialog = PutongDialog()
            putong_dialog.exec_()

    def closeEvent(self, event):
        self.logger.info("关闭考试信息窗口")
        self.player.stop_play()
        self.timer.stop()
        event.accept()
