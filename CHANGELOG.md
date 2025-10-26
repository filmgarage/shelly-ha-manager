# Changelog

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
