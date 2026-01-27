import os
import json
import logging

class SettingsManager:
    def __init__(self):
        # 配置文件保存到config文件夹
        config_dir = os.path.join(os.path.dirname(__file__), 'config')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        self.config_file = os.path.join(config_dir, 'settings.json')
        self.logger = logging.getLogger(__name__)
        self.config = {}
        self.load_config()

    def load_config(self):
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
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            self.logger.info('配置文件保存成功')
            return True
        except Exception as e:
            self.logger.error('保存配置文件失败: %s', e)
            return False

    def get_auto_ntp_sync(self):
        return self.config.get('auto_ntp_sync', True)

    def set_auto_ntp_sync(self, value):
        self.config['auto_ntp_sync'] = value
        return self.save_config()

settings_manager = SettingsManager()