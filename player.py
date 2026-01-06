import os
import pygame
import logging
from PyQt5.QtCore import QObject, pyqtSignal


class AudioPlayer(QObject):
    over = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.file_path = ""
        self.is_playing = False
        try:
            pygame.mixer.init()
            self.logger.info("初始化音频播放器成功")
        except Exception as e:
            self.logger.error(f"初始化音频播放器失败: {e}", exc_info=True)

    def set_file_path(self, file_path: str):
        self.file_path = file_path
        self.logger.info(f"设置音频文件路径: {file_path}")

    def play_mp3(self):
        if not self.file_path:
            self.logger.error("音频文件路径为空")
            return
        
        if not os.path.exists(self.file_path):
            self.logger.error(f"音频文件不存在 - {self.file_path}")
            return
        
        try:
            self.logger.info(f"开始播放音频: {self.file_path}")
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.play()
            self.is_playing = True
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            self.is_playing = False
            self.logger.info(f"音频播放完成: {self.file_path}")
            self.over.emit()
        except Exception as e:
            self.logger.error(f"播放音频时出错: {e}", exc_info=True)
            self.is_playing = False

    def stop_play(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.logger.info(f"音频播放停止: {self.file_path}")
