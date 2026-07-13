import os
import pygame
import logging
from PyQt5.QtCore import QObject, pyqtSignal


class AudioPlayer(QObject):
    """音频播放器类
    
    使用pygame实现音频文件的播放功能，支持播放状态跟踪和播放完成信号。
    
    Signals:
        over: 音频播放完成时发出的信号
    """
    
    over = pyqtSignal()

    def __init__(self):
        """初始化音频播放器
        
        初始化pygame音频系统，并设置播放状态。
        """
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
        """设置要播放的音频文件路径
        
        Args:
            file_path: 音频文件的绝对路径
        """
        self.file_path = file_path
        self.logger.info(f"设置音频文件路径: {file_path}")

    def play_mp3(self):
        """播放音频文件
        
        检查文件路径和文件存在性，然后播放音频。
        播放完成后发出over信号。
        
        Returns:
            None
        """
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
        """停止当前正在播放的音频
        
        如果音频正在播放，则停止播放并更新播放状态。
        
        Returns:
            None
        """
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.logger.info(f"音频播放停止: {self.file_path}")
