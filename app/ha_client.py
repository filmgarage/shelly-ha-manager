"""
Home Assistant API client to fetch Shelly devices
"""
import os
import requests
import logging

logger = logging.getLogger(__name__)


class HomeAssistantClient:
    """Client to interact with Home Assistant Supervisor API"""
    
    def __init__(self):
        self.supervisor_token = os.environ.get('SUPERVISOR_TOKEN', '')
        self.ha_url = 'http://supervisor/core'
        self.headers = {
            'Authorization': f'Bearer {self.supervisor_token}',
            'Content-Type': 'application/json'
        }
    
    def get_shelly_devices(self):
        """Get all Shelly devices from Home Assistant"""
        try:
            # Get all entities
            response = requests.get(
                f'{self.ha_url}/api/states',
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to get entities: {response.status_code}")
                return []
            
            entities = response.json()
            shelly_devices = {}
            
            # Find all entities from Shelly integration
            for entity in entities:
                entity_id = entity.get('entity_id', '')
                attributes = entity.get('attributes', {})
                
                # Check if it's a Shelly device
                integration = attributes.get('integration', '')
                device_id = attributes.get('device_id', '')
                
                if integration == 'shelly' and device_id:
                    if device_id not in shelly_devices:
                        # Get device info
                        device_info = self.get_device_info(device_id)
                        if device_info:
                            shelly_devices[device_id] = device_info
            
            return list(shelly_devices.values())
            
        except Exception as e:
            logger.error(f"Error getting Shelly devices: {e}")
            return []
    
    def get_device_info(self, device_id):
        """Get detailed device information"""
        try:
            response = requests.get(
                f'{self.ha_url}/api/config/device_registry/list',
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code != 200:
                return None
            
            devices = response.json()
            
            for device in devices:
                if device.get('id') == device_id:
                    # Extract IP from connections
                    connections = device.get('connections', [])
                    ip_address = None
                    mac_address = None
                    
                    for conn_type, conn_value in connections:
                        if conn_type == 'mac':
                            mac_address = conn_value
                    
                    # Try to get IP from config entries
                    config_entries = device.get('config_entries', [])
                    if config_entries:
                        entry_id = config_entries[0]
                        ip_address = self.get_device_ip_from_config(entry_id)
                    
                    return {
                        'id': device_id,
                        'name': device.get('name', 'Unknown'),
                        'model': device.get('model', 'Unknown'),
                        'manufacturer': device.get('manufacturer', ''),
                        'sw_version': device.get('sw_version', ''),
                        'ip': ip_address,
                        'mac': mac_address,
                        'identifiers': device.get('identifiers', [])
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting device info for {device_id}: {e}")
            return None
    
    def get_device_ip_from_config(self, entry_id):
        """Get device IP from config entry"""
        try:
            response = requests.get(
                f'{self.ha_url}/api/config/config_entries/entry/{entry_id}',
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                entry = response.json()
                data = entry.get('data', {})
                return data.get('host') or data.get('ip')
            
            return None
            
        except Exception as e:
            logger.debug(f"Could not get IP from config entry: {e}")
            return None
