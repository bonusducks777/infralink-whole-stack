"""
InfraLink Device Payload Controller
Handles device enable/disable actions with customizable commands and sound effects.
This script is called by devicelocal.py when device state changes occur.
"""

import os
import sys
import subprocess
import time
import pygame
from pathlib import Path

# === CONFIGURATION ===
# Sound settings
SOUND_ENABLED = True
SOUND_FILE = "song.mp3"  # Place your sound file in the same directory
SOUND_VOLUME = 0.7  # Volume level (0.0 to 1.0)

# Custom commands for device enable/disable
# Modify these to control your specific device/hardware
ENABLE_COMMANDS = [
    # Example commands - replace with your actual device control commands
    # "gpio write 18 1",  # Turn on GPIO pin 18
    # "curl -X POST http://192.168.1.100/api/enable",  # HTTP API call
    # "python turn_on_led.py",  # Run custom Python script
    # "echo 'Device enabled' > /dev/ttyUSB0",  # Send serial command
]

DISABLE_COMMANDS = [
    # Example commands - replace with your actual device control commands
    # "gpio write 18 0",  # Turn off GPIO pin 18
    # "curl -X POST http://192.168.1.100/api/disable",  # HTTP API call
    # "python turn_off_led.py",  # Run custom Python script
    # "echo 'Device disabled' > /dev/ttyUSB0",  # Send serial command
]

# === SOUND SYSTEM ===
def initialize_sound():
    """Initialize pygame mixer for sound playback"""
    try:
        pygame.mixer.init()
        pygame.mixer.music.set_volume(SOUND_VOLUME)
        return True
    except Exception as e:
        print(f"Sound initialization failed: {e}")
        return False

def play_sound(sound_file=None):
    """Play sound effect when device is enabled"""
    if not SOUND_ENABLED:
        return
    
    try:
        if sound_file is None:
            sound_file = SOUND_FILE
            
        if not os.path.exists(sound_file):
            print(f"Sound file not found: {sound_file}")
            return
            
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        print(f"Playing sound: {sound_file}")
        
    except Exception as e:
        print(f"Error playing sound: {e}")

def stop_sound():
    """Stop any currently playing sound"""
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"Error stopping sound: {e}")

# === COMMAND EXECUTION ===
def run_command(command, timeout=30):
    """Execute a system command with timeout"""
    try:
        print(f"Executing: {command}")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            print(f"Command succeeded: {command}")
            if result.stdout:
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"Command failed: {command}")
            print(f"Error: {result.stderr.strip()}")
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"Command timed out: {command}")
        return False
    except Exception as e:
        print(f"Error executing command '{command}': {e}")
        return False

def run_commands(commands, description=""):
    """Execute a list of commands"""
    if not commands:
        print(f"No {description} commands configured")
        return True
        
    print(f"Running {description} commands...")
    success_count = 0
    
    for cmd in commands:
        if run_command(cmd):
            success_count += 1
        else:
            print(f"Failed to execute {description} command: {cmd}")
    
    print(f"Completed {success_count}/{len(commands)} {description} commands")
    return success_count == len(commands)

# === DEVICE CONTROL FUNCTIONS ===
def on_device_enable(user_address=None, is_whitelisted=False):
    """
    Called when device is enabled/activated
    
    Args:
        user_address (str): Address of the user who activated the device
        is_whitelisted (bool): Whether the user is whitelisted
    """
    print("=" * 50)
    print("🟢 DEVICE ENABLE EVENT")
    print(f"User: {user_address}")
    print(f"Whitelisted: {is_whitelisted}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Play sound effect
    if SOUND_ENABLED:
        play_sound()
    
    # Execute enable commands
    success = run_commands(ENABLE_COMMANDS, "enable")
    
    if success:
        print("✅ Device successfully enabled")
    else:
        print("❌ Some enable commands failed")
    
    return success

def on_device_disable(user_address=None, was_whitelisted=False):
    """
    Called when device is disabled/deactivated
    
    Args:
        user_address (str): Address of the user whose session ended
        was_whitelisted (bool): Whether the user was whitelisted
    """
    print("=" * 50)
    print("🔴 DEVICE DISABLE EVENT")
    print(f"User: {user_address}")
    print(f"Was Whitelisted: {was_whitelisted}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Stop any playing sound
    stop_sound()
    
    # Execute disable commands
    success = run_commands(DISABLE_COMMANDS, "disable")
    
    if success:
        print("✅ Device successfully disabled")
    else:
        print("❌ Some disable commands failed")
    
    return success

# === TESTING FUNCTIONS ===
def test_enable():
    """Test the enable functionality"""
    print("Testing device enable...")
    return on_device_enable("0x1234567890abcdef", True)

def test_disable():
    """Test the disable functionality"""
    print("Testing device disable...")
    return on_device_disable("0x1234567890abcdef", True)

def test_sound():
    """Test the sound system"""
    print("Testing sound system...")
    if initialize_sound():
        play_sound()
        time.sleep(2)
        stop_sound()
        print("Sound test completed")
    else:
        print("Sound test failed - could not initialize sound system")

# === MAIN EXECUTION ===
def main():
    """Main function for testing or direct execution"""
    if len(sys.argv) < 2:
        print("InfraLink Device Payload Controller")
        print("Usage: python devicepayload.py <command> [args]")
        print("Commands:")
        print("  enable [user_address] [is_whitelisted]")
        print("  disable [user_address] [was_whitelisted]")
        print("  test-enable")
        print("  test-disable")
        print("  test-sound")
        return
    
    command = sys.argv[1].lower()
    
    # Initialize sound system
    if SOUND_ENABLED:
        initialize_sound()
    
    if command == "enable":
        user_address = sys.argv[2] if len(sys.argv) > 2 else None
        is_whitelisted = sys.argv[3].lower() == "true" if len(sys.argv) > 3 else False
        on_device_enable(user_address, is_whitelisted)
        
    elif command == "disable":
        user_address = sys.argv[2] if len(sys.argv) > 2 else None
        was_whitelisted = sys.argv[3].lower() == "true" if len(sys.argv) > 3 else False
        on_device_disable(user_address, was_whitelisted)
        
    elif command == "test-enable":
        test_enable()
        
    elif command == "test-disable":
        test_disable()
        
    elif command == "test-sound":
        test_sound()
        
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
