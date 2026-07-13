import sys
import os
import logging
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QIcon

from dialog import MainDialog
from settings import settings_manager
from ntp_sync import ntp_sync


def setup_logging():
    """配置日志系统
    
    创建logs目录并配置日志格式，日志同时输出到文件和控制台。
    日志文件名格式为 YYYY-MM-DD.log。
    """
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """主程序入口函数
    
    执行流程：
    1. 初始化日志系统
    2. 根据配置执行自动网络校时
    3. 创建Qt应用实例
    4. 设置应用图标和字体
    5. 显示主对话框并启动事件循环
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("考试指令播放系统启动")
    
    if settings_manager.get_auto_ntp_sync():
        logger.info("开始自动网络校时")
        success = ntp_sync.sync_system_time()
        if success:
            logger.info("网络校时成功")
        else:
            logger.warning("网络校时失败，可能需要管理员权限")
    else:
        logger.info("自动网络校时已禁用")
    
    app = QApplication(sys.argv)
    
    icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    else:
        logger.warning(f"图标文件不存在: {icon_path}")
    
    font = QFont("微软雅黑", 10)
    app.setFont(font)
    
    try:
        main_dialog = MainDialog()
        main_dialog.show()
        logger.info("显示主对话框")
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"应用运行出错: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
