import sys
import os
import logging
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QIcon

from dialog import MainDialog

# 配置日志
def setup_logging():
    # 创建logs文件夹
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 日志文件名格式：YYYY-MM-DD.log
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    # 初始化日志
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("考试指令播放系统启动")
    
    app = QApplication(sys.argv)
    
    icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        logger.info(f"加载图标成功: {icon_path}")
    else:
        logger.warning(f"图标文件不存在: {icon_path}")
    
    font = QFont("微软雅黑", 10)
    app.setFont(font)
    logger.info("设置应用字体为微软雅黑 10")
    
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
