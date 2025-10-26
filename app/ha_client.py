"""
Home Assistant API client to fetch Shelly devices
"""
import os
import requests
import logging
import re

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
        """Get all Shelly devices from Home Assistant via entity states"""
        logger.info("=" * 60)
        logger.info("FETCHING SHELLY DEVICES FROM HOME ASSISTANT")
        logger.info("=" * 60)
        
        try:
            # Get all entity states
            logger.info("Fetching entity states from HA...")
            response = requests.get(
                f'{self.ha_url}/api/states',
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to get states: {response.status_code}")
                return []
            
            entities = response.json()
            logger.info(f"✓ Found {len(entities)} total entities")
            
            # Find all Shelly entities and extract device info
            devices_map = {}
            
            for entity in entities:
                entity_id = entity.get('entity_id', '')
                attributes = entity.get('attributes', {})
                
                # Check if this is a Shelly entity
                if not ('shelly' in entity_id.lower() or 
                       'shelly' in attributes.get('friendly_name', '').lower()):
                    continue
                
                # Try to extract device identifier and IP
                device_id = None
                device_name = attributes.get('friendly_name', 'Unknown')
                ip_address = None
                
                # Method 1: Check if entity has device_info with host
                if 'device_info' in attributes:
                    device_info = attributes['device_info']
                    if isinstance(device_info, dict):
                        ip_address = device_info.get('host') or device_info.get('hostname')
                
                # Method 2: Try to extract IP from entity_id
                # Example: switch.shellyplus1_192_168_1_100
                if not ip_address:
                    # Look for IP pattern in entity_id
                    ip_match = re.search(r'(\d+)_(\d+)_(\d+)_(\d+)', entity_id)
                    if ip_match:
                        ip_address = '.'.join(ip_match.groups())
                
                # Method 3: Check attributes for common IP fields
                if not ip_address:
                    for field in ['host', 'ip_address', 'hostname', 'ip']:
                        if field in attributes:
                            ip_address = attributes[field]
                            break
                
                # Method 4: Check state attributes recursively
                if not ip_address and isinstance(attributes, dict):
                    for key, value in attributes.items():
                        if isinstance(value, dict):
                            for subkey in ['host', 'ip_address', 'hostname', 'ip']:
                                if subkey in value:
                                    ip_address = value[subkey]
                                    break
                        if ip_address:
                            break
                
                # Extract device ID from entity_id
                # Example: switch.shellyplus1_aabbccdd -> shellyplus1_aabbccdd
                if '.' in entity_id:
                    device_id = entity_id.split('.', 1)[1]
                    # Remove IP suffix if present
                    device_id = re.sub(r'_\d+_\d+_\d+_\d+$', '', device_id)
                
                # Group entities by device
                if device_id and device_id not in devices_map:
                    devices_map[device_id] = {
                        'id': device_id,
                        'name': device_name,
                        'ip': ip_address,
                        'entities': [entity_id],
                        'model': 'Unknown',
                        'manufacturer': 'Shelly',
                        'sw_version': '',
                        'mac': None
                    }
                    
                    if ip_address:
                        logger.info(f"✓ Found device: {device_name} at {ip_address}")
                    else:
                        logger.warning(f"⚠ Found device: {device_name} but no IP address")
                elif device_id:
                    # Update existing device
                    existing = devices_map[device_id]
                    if not existing['ip'] and ip_address:
                        existing['ip'] = ip_address
                        logger.info(f"✓ Found IP for {device_name}: {ip_address}")
                    existing['entities'].append(entity_id)
            
            shelly_devices = list(devices_map.values())
            
            logger.info(f"✓ Found {len(shelly_devices)} unique Shelly devices")
            logger.info(f"  - With IP: {sum(1 for d in shelly_devices if d.get('ip'))}")
            logger.info(f"  - Without IP: {sum(1 for d in shelly_devices if not d.get('ip'))}")
            
            # For devices without IP, try to get it from the device name
            for device in shelly_devices:
                if not device.get('ip'):
                    # Try to extract from device name if it contains IP
                    name = device.get('name', '')
                    ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', name)
                    if ip_match:
                        device['ip'] = ip_match.group(1)
                        logger.info(f"✓ Extracted IP from name for {name}: {device['ip']}")
            
            logger.info("=" * 60)
            return shelly_devices
            
        except Exception as e:
            logger.error(f"❌ Error getting Shelly devices: {e}", exc_info=True)
            logger.info("=" * 60)
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
