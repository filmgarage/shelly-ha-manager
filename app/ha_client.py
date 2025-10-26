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
            # Step 1: Get all states (entities)
            logger.info("Step 1: Fetching all entities from HA...")
            response = requests.get(
                f'{self.ha_url}/api/states',
                headers=self.headers,
                timeout=10
            )
            
            logger.info(f"Response status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"Failed to get entities: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return []
            
            entities = response.json()
            logger.info(f"✓ Found {len(entities)} total entities")
            
            # Step 2: Find Shelly entities
            shelly_entities = []
            for entity in entities:
                attributes = entity.get('attributes', {})
                
                # Check for Shelly integration
                # Entities from Shelly integration have specific attributes
                friendly_name = attributes.get('friendly_name', '')
                device_class = attributes.get('device_class', '')
                
                # Check if entity_id contains 'shelly' or if it's from Shelly integration
                entity_id = entity.get('entity_id', '')
                
                if 'shelly' in entity_id.lower() or 'shelly' in friendly_name.lower():
                    shelly_entities.append(entity)
            
            logger.info(f"✓ Found {len(shelly_entities)} Shelly entities")
            
            if shelly_entities:
                logger.info("Sample Shelly entity:")
                sample = shelly_entities[0]
                logger.info(f"  - entity_id: {sample.get('entity_id')}")
                logger.info(f"  - friendly_name: {sample.get('attributes', {}).get('friendly_name')}")
            
            # Step 3: Get unique devices from entities
            devices_map = {}
            
            for entity in shelly_entities:
                attributes = entity.get('attributes', {})
                
                # Try to get device info from entity attributes
                # Many HA integrations store device info in entity attributes
                device_name = attributes.get('friendly_name', 'Unknown Device')
                
                # Extract IP from entity_id or attributes
                entity_id = entity.get('entity_id', '')
                
                # Try to find IP in entity_id (e.g., switch.shellyplus1_aabbccddee)
                # Or look in attributes
                device_id = None
                ip_address = None
                
                # Some Shelly entities have IP in their unique_id or entity_id
                if 'shelly' in entity_id:
                    # Extract device identifier from entity_id
                    parts = entity_id.split('.')
                    if len(parts) > 1:
                        device_part = parts[1]
                        # Extract the unique part (like shellyplus1_aabbccddee)
                        device_id = device_part
                
                # Try to find the device in device registry
                if device_id and device_id not in devices_map:
                    device_info = self.get_device_by_entity_attributes(entity)
                    if device_info:
                        devices_map[device_id] = device_info
            
            logger.info(f"✓ Found {len(devices_map)} unique Shelly devices")
            logger.info("=" * 60)
            
            return list(devices_map.values())
            
        except Exception as e:
            logger.error(f"❌ Error getting Shelly devices: {e}", exc_info=True)
            logger.info("=" * 60)
            return []
    
    def get_device_by_entity_attributes(self, entity):
        """Try to extract device info from entity attributes"""
        try:
            attributes = entity.get('attributes', {})
            entity_id = entity.get('entity_id', '')
            
            # Get device name
            device_name = attributes.get('friendly_name', 'Unknown')
            
            # Try to extract IP - this varies by integration
            # Some options:
            # 1. Check for 'host' in attributes
            # 2. Check for 'ip_address' in attributes  
            # 3. Use the entity registry to find the device
            
            # For now, we'll need to query the device registry
            # via the config/device_registry API
            
            return {
                'name': device_name,
                'entity_id': entity_id,
                'ip': None,  # Will be populated if we can find it
                'model': 'Unknown',
                'manufacturer': 'Shelly',
                'sw_version': '',
                'mac': None,
                'id': entity_id
            }
            
        except Exception as e:
            logger.error(f"Error extracting device info from entity: {e}")
            return None
    
    def get_all_devices(self):
        """Get all devices from HA device registry"""
        logger.info("Fetching device registry from HA...")
        
        try:
            # Try the websocket API approach via REST
            response = requests.get(
                f'{self.ha_url}/api/config/device_registry/list',
                headers=self.headers,
                timeout=10
            )
            
            logger.info(f"Device registry response: {response.status_code}")
            
            if response.status_code == 200:
                devices = response.json()
                logger.info(f"✓ Found {len(devices)} devices in registry")
                
                # Filter for Shelly devices
                shelly_devices = []
                for device in devices:
                    manufacturer = device.get('manufacturer', '').lower()
                    model = device.get('model', '').lower()
                    name = device.get('name', '').lower()
                    
                    if 'shelly' in manufacturer or 'shelly' in model or 'shelly' in name:
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
                            ip_address = self.get_ip_from_config_entry(entry_id)
                        
                        shelly_devices.append({
                            'id': device.get('id'),
                            'name': device.get('name', 'Unknown'),
                            'model': device.get('model', 'Unknown'),
                            'manufacturer': device.get('manufacturer', 'Shelly'),
                            'sw_version': device.get('sw_version', ''),
                            'ip': ip_address,
                            'mac': mac_address
                        })
                
                logger.info(f"✓ Found {len(shelly_devices)} Shelly devices")
                return shelly_devices
            else:
                logger.warning(f"Could not access device registry: {response.status_code}")
                return []
            
        except Exception as e:
            logger.error(f"Error getting device registry: {e}", exc_info=True)
            return []
    
    def get_ip_from_config_entry(self, entry_id):
        """Get IP address from a config entry"""
        try:
            # This endpoint might not work - depends on HA version
            response = requests.get(
                f'{self.ha_url}/api/config/config_entries/entry/{entry_id}',
                headers=self.headers,
                timeout=5
            )
            
            if response.status_code == 200:
                entry = response.json()
                data = entry.get('data', {})
                return data.get('host') or data.get('ip_address')
            
        except Exception as e:
            logger.debug(f"Could not get IP from config entry: {e}")
        
        return None
    
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
