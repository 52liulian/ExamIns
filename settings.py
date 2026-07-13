import os
import json
import logging

VERSION = "1.0.1"


class SettingsManager:
    """配置管理器类
    
    负责加载、保存和管理应用程序配置，配置文件存储在config/settings.json中。
    """
    
    def __init__(self):
        """初始化配置管理器
        
        创建config目录并加载配置文件，如果配置文件不存在则使用默认配置。
        """
        config_dir = os.path.join(os.path.dirname(__file__), 'config')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        self.config_file = os.path.join(config_dir, 'settings.json')
        self.logger = logging.getLogger(__name__)
        self.config = {}
        self.load_config()

    def load_config(self):
        """加载配置文件
        
        从settings.json文件加载配置，如果文件不存在或加载失败则使用默认配置。
        
        Returns:
            None
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                self.logger.info('配置文件加载成功')
            else:
                self.config = {'auto_ntp_sync': True}
                self.logger.info('配置文件不存在，使用默认配置')
        except Exception as e:
            self.logger.error('加载配置文件失败: %s', e)
            self.config = {'auto_ntp_sync': True}

    def save_config(self):
        """保存配置文件
        
        将当前配置保存到settings.json文件中。
        
        Returns:
            bool: 保存成功返回True，失败返回False
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            self.logger.info('配置文件保存成功')
            return True
        except Exception as e:
            self.logger.error('保存配置文件失败: %s', e)
            return False

    def get_auto_ntp_sync(self):
        """获取自动网络校时配置
        
        Returns:
            bool: True表示启用自动网络校时，False表示禁用
        """
        return self.config.get('auto_ntp_sync', True)

    def set_auto_ntp_sync(self, value):
        """设置自动网络校时配置
        
        Args:
            value: True表示启用自动网络校时，False表示禁用
        
        Returns:
            bool: 保存成功返回True，失败返回False
        """
        self.config['auto_ntp_sync'] = value
        return self.save_config()

settings_manager = SettingsManager()