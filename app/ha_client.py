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
        
        logger.info(f"HA Client initialized. Token present: {bool(self.supervisor_token)}")
    
    def get_shelly_devices(self):
        """Get all Shelly devices from Home Assistant"""
        logger.info("=" * 60)
        logger.info("FETCHING SHELLY DEVICES FROM HOME ASSISTANT")
        logger.info("=" * 60)
        
        try:
            # Get all config entries first
            logger.info("Step 1: Fetching config entries...")
            config_entries = self.get_config_entries()
            logger.info(f"✓ Found {len(config_entries)} config entries")
            
            # Filter for Shelly entries
            shelly_entries = [e for e in config_entries if e.get('domain') == 'shelly']
            logger.info(f"✓ Found {len(shelly_entries)} Shelly config entries")
            
            # Get device registry
            logger.info("Step 2: Fetching device registry...")
            devices = self.get_device_registry()
            logger.info(f"✓ Found {len(devices)} devices in registry")
            
            # Match Shelly devices with their config entries
            shelly_devices = []
            
            for device in devices:
                manufacturer = device.get('manufacturer', '').lower()
                model = device.get('model', '').lower()
                name = device.get('name', '').lower()
                
                if 'shelly' in manufacturer or 'shelly' in model or 'shelly' in name:
                    # Get config entry for this device
                    config_entry_ids = device.get('config_entries', [])
                    
                    ip_address = None
                    mac_address = None
                    
                    # Extract MAC from connections
                    connections = device.get('connections', [])
                    for conn_type, conn_value in connections:
                        if conn_type == 'mac':
                            mac_address = conn_value
                    
                    # Try to get IP from config entries
                    for entry_id in config_entry_ids:
                        # Find matching config entry
                        matching_entry = next((e for e in shelly_entries if e.get('entry_id') == entry_id), None)
                        if matching_entry:
                            # Extract IP from config entry data
                            entry_data = matching_entry.get('data', {})
                            ip_address = entry_data.get('host') or entry_data.get('ip_address')
                            
                            if ip_address:
                                logger.info(f"✓ Found IP for {device.get('name')}: {ip_address}")
                                break
                    
                    if not ip_address:
                        logger.warning(f"⚠ No IP found for {device.get('name')} (MAC: {mac_address})")
                    
                    shelly_devices.append({
                        'id': device.get('id'),
                        'name': device.get('name', 'Unknown'),
                        'model': device.get('model', 'Unknown'),
                        'manufacturer': device.get('manufacturer', 'Shelly'),
                        'sw_version': device.get('sw_version', ''),
                        'ip': ip_address,
                        'mac': mac_address,
                        'identifiers': device.get('identifiers', [])
                    })
            
            logger.info(f"✓ Returning {len(shelly_devices)} Shelly devices")
            logger.info(f"  - With IP: {sum(1 for d in shelly_devices if d.get('ip'))}")
            logger.info(f"  - Without IP: {sum(1 for d in shelly_devices if not d.get('ip'))}")
            logger.info("=" * 60)
            
            return shelly_devices
            
        except Exception as e:
            logger.error(f"❌ Error getting Shelly devices: {e}", exc_info=True)
            logger.info("=" * 60)
            return []
    
    def get_config_entries(self):
        """Get all config entries from Home Assistant"""
        try:
            response = requests.get(
                f'{self.ha_url}/api/config/config_entries/list',
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Could not get config entries: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting config entries: {e}")
            return []
    
    def get_device_registry(self):
        """Get device registry from Home Assistant"""
        try:
            response = requests.get(
                f'{self.ha_url}/api/config/device_registry/list',
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Could not get device registry: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting device registry: {e}")
            return []
    
    def test_connection(self):
        """Test if we can connect to HA API"""
        logger.info("Testing HA API connection...")
        
        try:
            response = requests.get(
                f'{self.ha_url}/api/',
                headers=self.headers,
                timeout=5
            )
            
            logger.info(f"API test response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✓ Connected to HA API")
                logger.info(f"  - Message: {data.get('message')}")
                return True
            else:
                logger.error(f"❌ API connection failed: {response.status_code}")
                return False
            
        except Exception as e:
            logger.error(f"❌ API connection error: {e}")
            return False
