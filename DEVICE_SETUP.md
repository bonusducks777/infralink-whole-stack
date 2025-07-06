# InfraLink Device Control Setup

## Quick Start

1. **Configure your device commands** in `devicepayload.py`:
   ```python
   ENABLE_COMMANDS = [
       "python your_enable_script.py",  # Your custom enable command
       "curl -X POST http://device-ip/api/enable",  # HTTP API call
   ]
   
   DISABLE_COMMANDS = [
       "python your_disable_script.py",  # Your custom disable command  
       "curl -X POST http://device-ip/api/disable",  # HTTP API call
   ]
   ```

2. **Add a sound file** (optional):
   - Place `song.mp3` in the same directory as `devicepayload.py`
   - Or modify `SOUND_FILE` variable to point to your audio file

3. **Test your setup**:
   ```bash
   python devicepayload.py test-enable
   python devicepayload.py test-disable
   ```

4. **Run the device monitor**:
   ```bash
   python devicelocal.py
   ```

## How It Works

- `devicelocal.py` - GUI monitor that watches blockchain state
- `devicepayload.py` - Executes actual device control commands
- When device state changes (enabled/disabled), the monitor calls the payload script
- Payload script plays sound and runs your custom commands

## Customization Examples

### GPIO Control (Raspberry Pi)
```python
ENABLE_COMMANDS = ["gpio write 18 1"]  # Turn on GPIO pin 18
DISABLE_COMMANDS = ["gpio write 18 0"]  # Turn off GPIO pin 18
```

### HTTP API Control
```python
ENABLE_COMMANDS = ["curl -X POST http://192.168.1.100/api/turn_on"]
DISABLE_COMMANDS = ["curl -X POST http://192.168.1.100/api/turn_off"]
```

### Serial Communication
```python
ENABLE_COMMANDS = ["echo 'ON' > /dev/ttyUSB0"]
DISABLE_COMMANDS = ["echo 'OFF' > /dev/ttyUSB0"]
```

### Multiple Commands
```python
ENABLE_COMMANDS = [
    "python setup_device.py",
    "systemctl start my-service",
    "logger 'Device enabled by blockchain'"
]
```

Ready to control real devices with Web3 payments! 🚀
