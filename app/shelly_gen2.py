"""
Shelly Gen2+ RPC API Client
"""
import requests
import logging
import uuid

logger = logging.getLogger(__name__)


class ShellyGen2Client:
    """Client for Shelly Gen2+ devices (RPC API)"""
    
    def __init__(self, ip, password=None, timeout=5):
        self.ip = ip
        self.password = password
        self.timeout = timeout
        self.base_url = f"http://{ip}/rpc"
    
    def make_rpc_call(self, method, params=None):
        """Make an RPC call to the device"""
        try:
            payload = {
                'id': str(uuid.uuid4()),
                'method': method
            }
            
            if params:
                payload['params'] = params
            
            # Add password if available and needed
            if self.password and params is None:
                payload['params'] = {'password': self.password}
            elif self.password and params:
                payload['params']['password'] = self.password
            
            response = requests.post(
                self.base_url,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'result' in result:
                    return result['result']
                elif 'error' in result:
                    logger.error(f"RPC error: {result['error']}")
                    return None
            
            return None
            
        except Exception as e:
            logger.error(f"Error making RPC call to {self.ip}: {e}")
            return None
    
    def get_device_info(self):
        """Get device information"""
        try:
            data = self.make_rpc_call('Shelly.GetDeviceInfo')
            
            if data:
                return {
                    'type': data.get('model'),
                    'mac': data.get('mac'),
                    'auth': data.get('auth_en', False),
                    'fw': data.get('fw_id', data.get('ver')),
                    'generation': 2,
                    'name': data.get('name', f"Shelly {data.get('model')}")
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting Gen2 device info from {self.ip}: {e}")
            return None
    
    def get_config(self):
        """Get device configuration"""
        try:
            return self.make_rpc_call('Shelly.GetConfig')
        except Exception as e:
            logger.error(f"Error getting Gen2 config from {self.ip}: {e}")
            return None
    
    def get_status(self):
        """Get device status"""
        try:
            return self.make_rpc_call('Shelly.GetStatus')
        except Exception as e:
            logger.error(f"Error getting Gen2 status from {self.ip}: {e}")
            return None
    
    def set_auth(self, enable, password):
        """Enable or disable authentication"""
        try:
            params = {
                'config': {
                    'auth': {
                        'enable': enable,
                        'user': 'admin',
                        'pass': password if enable else ''
                    }
                }
            }
            
            # If auth is currently enabled, include password in request
            if self.password:
                params['password'] = self.password
            
            result = self.make_rpc_call('Sys.SetConfig', params)
            
            if result is not None:
                return {'success': True, 'response': result}
            
            return {'success': False, 'error': 'RPC call failed'}
            
        except Exception as e:
            logger.error(f"Error setting Gen2 auth on {self.ip}: {e}")
            return {'success': False, 'error': str(e)}
    
    def reboot(self):
        """Reboot device"""
        try:
            result = self.make_rpc_call('Shelly.Reboot')
            return result is not None
        except Exception as e:
            logger.error(f"Error rebooting Gen2 device {self.ip}: {e}")
            return False
    
    def update_firmware(self, stage='stable'):
        """Trigger firmware update"""
        try:
            params = {'stage': stage}
            result = self.make_rpc_call('Shelly.Update', params)
            
            if result is not None:
                return {'success': True, 'response': result}
            
            return {'success': False, 'error': 'RPC call failed'}
            
        except Exception as e:
            logger.error(f"Error updating Gen2 firmware on {self.ip}: {e}")
            return {'success': False, 'error': str(e)}
