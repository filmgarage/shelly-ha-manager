"""
Shelly Gen1 HTTP API Client
"""
import requests
import logging

logger = logging.getLogger(__name__)


class ShellyGen1Client:
    """Client for Shelly Gen1 devices (HTTP API)"""
    
    def __init__(self, ip, password=None, timeout=5):
        self.ip = ip
        self.password = password
        self.timeout = timeout
        self.base_url = f"http://{ip}"
    
    def get_auth(self):
        """Get authentication tuple if password is set"""
        if self.password:
            return ('admin', self.password)
        return None
    
    def get_device_info(self):
        """Get device information"""
        try:
            response = requests.get(
                f"{self.base_url}/shelly",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'type': data.get('type'),
                    'mac': data.get('mac'),
                    'auth': data.get('auth', False),
                    'fw': data.get('fw'),
                    'generation': 1
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting Gen1 device info from {self.ip}: {e}")
            return None
    
    def get_settings(self):
        """Get device settings"""
        try:
            response = requests.get(
                f"{self.base_url}/settings",
                auth=self.get_auth(),
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                return {'error': 'Authentication required'}
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting Gen1 settings from {self.ip}: {e}")
            return None
    
    def get_status(self):
        """Get device status"""
        try:
            response = requests.get(
                f"{self.base_url}/status",
                auth=self.get_auth(),
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting Gen1 status from {self.ip}: {e}")
            return None
    
    def set_auth(self, enable, password):
        """Enable or disable authentication"""
        try:
            params = {
                'enabled': 1 if enable else 0,
                'username': 'admin',
                'password': password if enable else ''
            }
            
            response = requests.get(
                f"{self.base_url}/settings/login",
                params=params,
                auth=self.get_auth(),
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {'success': True, 'response': response.json()}
            
            return {'success': False, 'error': f'Status {response.status_code}'}
            
        except Exception as e:
            logger.error(f"Error setting Gen1 auth on {self.ip}: {e}")
            return {'success': False, 'error': str(e)}
    
    def reboot(self):
        """Reboot device"""
        try:
            response = requests.get(
                f"{self.base_url}/reboot",
                auth=self.get_auth(),
                timeout=self.timeout
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Error rebooting Gen1 device {self.ip}: {e}")
            return False
    
    def update_firmware(self):
        """Trigger firmware update"""
        try:
            response = requests.get(
                f"{self.base_url}/ota?update=true",
                auth=self.get_auth(),
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {'success': True, 'response': response.json()}
            
            return {'success': False, 'error': f'Status {response.status_code}'}
            
        except Exception as e:
            logger.error(f"Error updating Gen1 firmware on {self.ip}: {e}")
            return {'success': False, 'error': str(e)}
