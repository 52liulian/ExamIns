import time
import socket
import logging
import json
import os
from datetime import datetime

class NTPSync:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # 配置文件保存到config文件夹
        config_dir = os.path.join(os.path.dirname(__file__), 'config')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        self.ntp_config_file = os.path.join(config_dir, 'ntp_config.json')
        self.NTP_EPOCH = 2208988800
        self.ntp_servers = self.load_ntp_servers()
    
    def load_ntp_servers(self):
        """加载NTP服务器配置"""
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
                # 使用默认NTP服务器
                default_servers = [
                    "ntp.aliyun.com",
                    "time.windows.com",
                    "time.apple.com"
                ]
                # 保存默认配置
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
        """保存NTP服务器配置"""
        try:
            with open(self.ntp_config_file, 'w', encoding='utf-8') as f:
                json.dump({'ntp_servers': servers}, f, indent=4)
            self.logger.info('NTP服务器配置保存成功')
            return True
        except Exception as e:
            self.logger.error('保存NTP服务器配置失败: %s', e)
            return False
    
    def get_ntp_time(self, server=None):
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
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        
        try:
            ntp_packet = bytearray(48)
            ntp_packet[0] = 0x1b
            sock.sendto(ntp_packet, (server, 123))
            data, addr = sock.recvfrom(48)
            
            # 解析NTP时间戳
            # NTP时间戳是64位，前32位是秒，后32位是 fractional seconds
            seconds = int.from_bytes(data[40:44], byteorder='big', signed=False)
            fractional = int.from_bytes(data[44:48], byteorder='big', signed=False)
            
            # 转换为Unix时间戳
            unix_time = seconds - self.NTP_EPOCH
            
            # 检查时间戳范围
            import time
            if unix_time < 0 or unix_time > time.time() + 86400 * 365:  # 允许最多一年的时间差
                raise ValueError(f"时间戳超出范围: {unix_time}")
            
            ntp_time = datetime.fromtimestamp(unix_time)
            self.logger.info(f"NTP服务器 {server} 同步成功，时间: {ntp_time}")
            return ntp_time
        finally:
            sock.close()
    
    def sync_system_time(self):
        try:
            ntp_time = self.get_ntp_time()
            if ntp_time:
                import subprocess
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