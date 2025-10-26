# Changelog

## [1.0.0] - 2025-10-26

### 🎉 Initial Release

#### Features
- ✨ **Home Assistant Integration** - Fetches Shelly devices directly from HA (no network scanning!)
- 🔄 **Gen1 Support** - Full support for Shelly Gen1 devices (HTTP API)
- 🔄 **Gen2+ Support** - Full support for Shelly Gen2+ devices (RPC API)
- 🔐 **Authentication Management** - Enable/disable password protection on devices
- 📦 **Firmware Updates** - Trigger firmware updates to latest stable version
- 🔄 **Device Reboots** - Remotely reboot devices
- 🎨 **Clean UI** - User-friendly interface with device overview
- 🐛 **Extensive Logging** - Detailed debug logs for troubleshooting
- 🚀 **Ingress Support** - Seamless integration with Home Assistant UI

#### Supported Operations
- View all Shelly devices from Home Assistant
- See device details (name, model, generation, IP, MAC, firmware)
- Check authentication status
- Toggle authentication on/off
- Update firmware
- Reboot devices

#### Technical
- Flask-based backend
- Modular client architecture (separate Gen1/Gen2 clients)
- Home Assistant Supervisor API integration
- Proper error handling and logging
- Simple, maintainable codebase
