# Shelly HA Manager

Manage your Shelly devices directly from Home Assistant - supports both Gen1 and Gen2+ devices!

## ✨ Features

- 📡 **No Network Scanning** - Gets devices directly from Home Assistant
- 🔄 **Gen1 + Gen2+ Support** - Works with all Shelly generations
- 🔐 **Authentication Management** - Enable/disable password protection
- 🔄 **Firmware Updates** - Update devices to latest firmware
- 🔄 **Device Reboots** - Restart devices remotely
- 🎨 **Clean UI** - Beautiful, user-friendly interface
- 🚀 **Ingress Support** - Works seamlessly with Home Assistant

## 🎯 How It Works

Instead of scanning your entire network, this add-on:
1. Queries Home Assistant for all Shelly devices
2. Gets their IP addresses from the Shelly integration
3. Connects directly to each device (Gen1 HTTP or Gen2+ RPC)
4. Displays them in a unified interface

**Benefits:**
- ✅ Faster - no network scanning needed
- ✅ More reliable - only manages devices HA knows about
- ✅ Unified view of all your Shelly devices
- ✅ Works with Gen1 AND Gen2+

## 📦 Installation

1. Add this repository to your Home Assistant add-on store:
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Click **⋮** (three dots) → **Repositories**
   - Add: `https://github.com/filmgarage/ha-addon-shelly-manager`

2. Install the **Shelly HA Manager** add-on

3. Configure your admin password (optional but recommended)

4. Start the add-on

5. Open via the sidebar!

## ⚙️ Configuration

### `admin_password` (optional)

The admin password for your Shelly devices. Required for:
- Enabling/disabling authentication
- Accessing protected devices
- Triggering firmware updates on protected devices

**Example:**
```yaml
admin_password: "your_secure_password"
```

**Note:** Gen1 uses username `admin` with this password. Gen2+ only uses the password.

## 🚀 Usage

1. **Open the add-on** from the Home Assistant sidebar
2. **Click "Scan Devices"** - fetches your Shelly devices from HA
3. **View your devices** with:
   - Device name
   - Model (type)
   - Generation (Gen1 or Gen2+)
   - IP address
   - MAC address
   - Firmware version
   - Authentication status

4. **Manage devices:**
   - 🔐 Toggle authentication on/off
   - 🔄 Update firmware
   - 🔄 Reboot device

## 🔧 Requirements

- Home Assistant with Shelly integration configured
- Your Shelly devices must be added to Home Assistant
- Network access between HA and your Shelly devices

## 🐛 Troubleshooting

### No devices shown?

- Make sure your Shelly devices are added to Home Assistant
- Check that the Shelly integration is configured correctly
- Verify devices are online and reachable

### Can't toggle authentication?

- Ensure admin password is configured in add-on settings
- Check that the password matches what's on the device
- Look at the add-on logs for detailed error messages

### Firmware update fails?

- Ensure device has internet access
- Check that authentication password is correct (if device is protected)
- Verify device has enough free memory

## 📊 Supported Devices

**Gen1 (HTTP API):**
- Shelly 1, 1PM, 1L
- Shelly 2.5
- Shelly Plug, Plug S
- Shelly RGBW2
- Shelly Dimmer, Dimmer 2
- Shelly EM
- All other Gen1 models

**Gen2+ (RPC API):**
- Shelly Plus 1, 1PM
- Shelly Plus 2PM
- Shelly Plus Plug S
- Shelly Pro series
- All other Gen2+ models

## 🔒 Security

- All communication happens locally
- No cloud connectivity required
- Passwords are only stored in add-on configuration
- Authentication details never logged

## 📝 License

MIT License - see LICENSE file

## 🙏 Credits

Built with ❤️ for the Home Assistant community
