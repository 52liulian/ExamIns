import time
import socket
import logging
import json
import os
import subprocess
from datetime import datetime


class NTPSync:
    """网络校时类
    
    负责从NTP服务器获取标准时间并同步系统时间。
    支持多个NTP服务器配置，自动尝试下一个服务器直到成功。
    """
    
    def __init__(self):
        """初始化网络校时器
        
        创建config目录，加载NTP服务器配置，设置NTP时间戳偏移常量。
        """
        self.logger = logging.getLogger(__name__)
        config_dir = os.path.join(os.path.dirname(__file__), 'config')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        self.ntp_config_file = os.path.join(config_dir, 'ntp_config.json')
        self.NTP_EPOCH = 2208988800
        self.ntp_servers = self.load_ntp_servers()
    
    def load_ntp_servers(self):
        """加载NTP服务器配置
        
        从ntp_config.json文件加载服务器列表，如果文件不存在则使用默认配置。
        
        Returns:
            list: NTP服务器地址列表
        """
        try:
            if os.path.exists(self.ntp_config_file):
                with open(self.ntp_config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info('NTP服务器配置加载成功')
                return config.get('ntp_servers', [
                    "ntp.aliyun.com",
                    "time.windows.com",
                    "time.apple.com"
                ])
            else:
                default_servers = [
                    "ntp.aliyun.com",
                    "time.windows.com",
                    "time.apple.com"
                ]
                self.save_ntp_servers(default_servers)
                self.logger.info('NTP服务器配置文件不存在，使用默认配置')
                return default_servers
        except Exception as e:
            self.logger.error('加载NTP服务器配置失败: %s', e)
            return [
                "ntp.aliyun.com",
                "time.windows.com",
                "time.apple.com"
            ]
    
    def save_ntp_servers(self, servers):
        """保存NTP服务器配置
        
        将服务器列表保存到ntp_config.json文件中。
        
        Args:
            servers: NTP服务器地址列表
        
        Returns:
            bool: 保存成功返回True，失败返回False
        """
        try:
            with open(self.ntp_config_file, 'w', encoding='utf-8') as f:
                json.dump({'ntp_servers': servers}, f, indent=4)
            self.logger.info('NTP服务器配置保存成功')
            return True
        except Exception as e:
            self.logger.error('保存NTP服务器配置失败: %s', e)
            return False
    
    def get_ntp_time(self, server=None):
        """获取NTP服务器时间
        
        如果指定了服务器则尝试连接该服务器，否则按顺序尝试所有配置的服务器。
        
        Args:
            server: NTP服务器地址，默认为None
            
        Returns:
            datetime: 获取到的NTP时间，失败返回None
        """
        if server is None:
            for srv in self.ntp_servers:
                try:
                    return self._get_ntp_time_from_server(srv)
                except Exception as e:
                    self.logger.warning(f"NTP服务器 {srv} 同步失败: {e}")
                    continue
            return None
        else:
            try:
                return self._get_ntp_time_from_server(server)
            except Exception as e:
                self.logger.error(f"NTP服务器 {server} 同步失败: {e}")
                return None
    
    def _get_ntp_time_from_server(self, server):
        """从指定NTP服务器获取时间
        
        发送NTP请求并解析响应，返回datetime对象。
        
        Args:
            server: NTP服务器地址
            
        Returns:
            datetime: 获取到的NTP时间
            
        Raises:
            ValueError: 时间戳超出有效范围时抛出
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        
        try:
            ntp_packet = bytearray(48)
            ntp_packet[0] = 0x1b
            sock.sendto(ntp_packet, (server, 123))
            data, addr = sock.recvfrom(48)
            
            seconds = int.from_bytes(data[40:44], byteorder='big', signed=False)
            fractional = int.from_bytes(data[44:48], byteorder='big', signed=False)
            
            unix_time = seconds - self.NTP_EPOCH
            
            if unix_time < 0 or unix_time > time.time() + 86400 * 365:
                raise ValueError(f"时间戳超出范围: {unix_time}")
            
            ntp_time = datetime.fromtimestamp(unix_time)
            self.logger.info(f"NTP服务器 {server} 同步成功，时间: {ntp_time}")
            return ntp_time
        finally:
            sock.close()
    
    def sync_system_time(self):
        """同步系统时间
        
        获取NTP时间并更新系统时间，需要管理员权限。
        
        Returns:
            bool: 同步成功返回True，失败返回False
        """
        try:
            ntp_time = self.get_ntp_time()
            if ntp_time:
                time_str = ntp_time.strftime("%Y-%m-%d %H:%M:%S")
                cmd = f"powershell -Command \"Set-Date -Date '{time_str}'\""
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    self.logger.info(f"系统时间同步成功: {time_str}")
                    return True
                else:
                    self.logger.warning(f"系统时间同步失败 (权限不足): {result.stderr}")
                    return False
            else:
                self.logger.error("获取NTP时间失败，无法同步系统时间")
                return False
        except Exception as e:
            self.logger.error(f"系统时间同步失败: {e}")
            return False


ntp_sync = NTPSync()