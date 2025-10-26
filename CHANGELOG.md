# Changelog

## [0.0.5] - 2025-10-27

### 🚀 Major Change: WebSocket API Implementation

**The Problem**: In v0.0.4, 19 out of 104 devices had no IP addresses because the REST API endpoints for device registry didn't exist or weren't accessible.

**The Solution**: Switched to **WebSocket API** - the official and proper way to access Home Assistant's device registry and config entries!

### What's New
- ✅ **WebSocket Client** - New `ha_websocket.py` module for HA WebSocket API
- ✅ **Complete IP Discovery** - All Shelly devices now get their IP addresses
- ✅ **Device Registry Access** - Proper access via `config/device_registry/list`
- ✅ **Config Entries Access** - Proper access via `config_entries/list`
- ✅ **Reliable Connection** - Uses the same API that Home Assistant itself uses

### How It Works Now
```
1. Connect to ws://supervisor/core/websocket
2. Authenticate with SUPERVISOR_TOKEN
3. Request device_registry/list → Get all devices
4. Request config_entries/list → Get all config entries
5. Match Shelly devices with their config entries
6. Extract IP from entry.data.host
7. Return complete device info with IPs!
```

### Technical Details
- Added `websocket-client==1.6.4` dependency
- Completely rewrote `ha_client.py` to use WebSocket
- Removed unreliable REST API fallbacks
- Better logging showing WebSocket connection status

### Expected Result
- **Before**: `discovered_with_ip: 85, discovered_without_ip: 19`
- **After**: `discovered_with_ip: 104, discovered_without_ip: 0` 🎉

**Note**: After updating, you MUST rebuild the add-on (not just restart) to install the new `websocket-client` dependency!

## [0.0.3] - 2025-10-26

### Fixed
- 🎯 **IP Address Discovery** - Now properly retrieves IP addresses via config entries
- 📊 **Config Entries API** - Added /api/config/config_entries/list support
- 🔗 **Device Matching** - Match devices with their config entries to get IP
- 📝 **Better Logging** - Shows which devices have/don't have IP addresses

### How it works now
1. Fetch all config entries from HA
2. Filter for Shelly entries (domain: 'shelly')
3. Fetch device registry
4. Match each device with its config entry
5. Extract IP from config entry data (host field)
6. Enrich device info with live Shelly API data

This should fix the "No IP address" issue!

## [0.0.2] - 2025-10-26

### Fixed
- 🔧 **HA API Connection** - Improved Home Assistant API integration
- 📊 **Better Logging** - Extensive debug logging for troubleshooting
- 🔍 **Debug Endpoint** - Added `/api/debug` to test HA API connectivity

## [0.0.1] - 2025-10-26

### 🎉 Initial Release
- Gen1 + Gen2+ support
- Home Assistant integration
- Beautiful UI
