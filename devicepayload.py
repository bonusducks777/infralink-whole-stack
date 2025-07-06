#!/usr/bin/env python3
"""
InfraLink Device Payload Controller
===================================

This script allows you to trigger device enable/disable actions with customizable payloads.
You can modify the payloads below to execute any commands when a device is activated or deactivated.

Usage:
    python devicepayload.py enable    # Enable device payload
    python devicepayload.py disable   # Disable device payload

The script plays a sound effect and executes custom commands based on device state changes.
"""

import sys
import os
import subprocess
import pygame
import time
from pathlib import Path

# =============================================================================
# CONFIGURATION SECTION - MODIFY THESE TO CUSTOMIZE YOUR PAYLOADS
# =============================================================================

# Sound Configuration
SOUND_FILE = "song.mp3"  # Name of the sound file to play (must be in same directory)
ENABLE_SOUND = True      # Set to False to disable sound effects

# Device Enable Payload Configuration
# These commands will be executed when the device is ENABLED/ACTIVATED
# 
# HOW TO ADD YOUR OWN COMMANDS:
# 1. Each command is a list: ["program", "arg1", "arg2", ...]
# 2. Add your commands to the list below
# 3. Examples of useful payloads:
#    - Send HTTP requests to APIs
#    - Run other Python scripts
#    - Execute system commands
#    - Control hardware (LEDs, relays, etc.)
#    - Send notifications
#    - Log events to files
#
DEVICE_ENABLE_COMMANDS = [
    # Example: Windows notification
    ["powershell", "-Command", "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Device is now ONLINE!', 'InfraLink', 'OK', 'Information')"],
    
    # Example: Print to console
    # ["echo", "Device ENABLED at $(Get-Date)"],
    
    # Example: HTTP API call (requires curl)
    # ["curl", "-X", "POST", "http://your-server.com/api/device/enable"],
    
    # Example: Run another Python script
    # ["python", "your_enable_script.py"],
    
    # Example: Write to log file
    # ["powershell", "-Command", "echo \"Device enabled at $(Get-Date)\" >> device.log"],
    
    # Add your custom enable commands here:
    # ["your_command", "arg1", "arg2"],
]

# Device Disable Payload Configuration  
# These commands will be executed when the device is DISABLED/DEACTIVATED
#
# Same format as enable commands - add your custom disable actions here
DEVICE_DISABLE_COMMANDS = [
    # Example: Windows notification
    ["powershell", "-Command", "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Device is now OFFLINE!', 'InfraLink', 'OK', 'Warning')"],
    
    # Example: Print to console
    # ["echo", "Device DISABLED at $(Get-Date)"],
    
    # Example: HTTP API call (requires curl)
    # ["curl", "-X", "POST", "http://your-server.com/api/device/disable"],
    
    # Example: Run another Python script
    # ["python", "your_disable_script.py"],
    
    # Example: Write to log file
    # ["powershell", "-Command", "echo \"Device disabled at $(Get-Date)\" >> device.log"],
    
    # Add your custom disable commands here:
    # ["your_command", "arg1", "arg2"],
]

# Advanced Configuration
COMMAND_TIMEOUT = 30     # Maximum time to wait for each command (seconds)
LOG_COMMANDS = True      # Set to True to log command execution
CONTINUE_ON_ERROR = True # Set to True to continue executing commands even if one fails

# =============================================================================
# END CONFIGURATION SECTION
# =============================================================================

class DevicePayloadController:
    """
    Controls device payloads and sound effects for InfraLink device state changes.
    """
    
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.sound_enabled = ENABLE_SOUND
        self.init_sound_system()
        
    def init_sound_system(self):
        """Initialize pygame mixer for sound effects."""
        if not self.sound_enabled:
            print("Sound effects disabled in configuration")
            return
            
        try:
            pygame.mixer.init()
            self.sound_initialized = True
            print("Sound system initialized successfully")
        except pygame.error as e:
            print(f"Warning: Could not initialize sound system: {e}")
            self.sound_initialized = False
            
    def play_sound(self):
        """Play the configured sound effect."""
        if not self.sound_enabled or not self.sound_initialized:
            return
            
        sound_path = self.script_dir / SOUND_FILE
        
        if not sound_path.exists():
            print(f"Warning: Sound file '{SOUND_FILE}' not found at {sound_path}")
            return
            
        try:
            pygame.mixer.music.load(str(sound_path))
            pygame.mixer.music.play()
            print(f"Playing sound effect: {SOUND_FILE}")
            
            # Wait for sound to finish playing (optional)
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except pygame.error as e:
            print(f"Error playing sound: {e}")
        except Exception as e:
            print(f"Unexpected error playing sound: {e}")
            
    def execute_command(self, command):
        """
        Execute a single command with error handling and logging.
        
        Args:
            command (list): Command and arguments to execute
            
        Returns:
            bool: True if command succeeded, False otherwise
        """
        if LOG_COMMANDS:
            print(f"Executing command: {' '.join(command)}")
            
        try:
            result = subprocess.run(
                command,
                timeout=COMMAND_TIMEOUT,
                capture_output=True,
                text=True,
                check=True
            )
            
            if LOG_COMMANDS and result.stdout:
                print(f"Command output: {result.stdout.strip()}")
                
            return True
            
        except subprocess.TimeoutExpired:
            print(f"Command timed out after {COMMAND_TIMEOUT} seconds: {' '.join(command)}")
            return False
            
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}: {' '.join(command)}")
            if e.stderr:
                print(f"Error output: {e.stderr.strip()}")
            return False
            
        except FileNotFoundError:
            print(f"Command not found: {command[0]}")
            return False
            
        except Exception as e:
            print(f"Unexpected error executing command: {e}")
            return False
            
    def execute_command_list(self, commands, action_name):
        """
        Execute a list of commands for a specific action.
        
        Args:
            commands (list): List of commands to execute
            action_name (str): Name of the action for logging
        """
        if not commands:
            print(f"No commands configured for {action_name}")
            return
            
        print(f"\nExecuting {action_name} payload ({len(commands)} commands):")
        print("=" * 50)
        
        success_count = 0
        
        for i, command in enumerate(commands, 1):
            print(f"\n[{i}/{len(commands)}] Processing command...")
            
            if self.execute_command(command):
                success_count += 1
                print(f"✓ Command {i} completed successfully")
            else:
                print(f"✗ Command {i} failed")
                if not CONTINUE_ON_ERROR:
                    print("Stopping execution due to error (CONTINUE_ON_ERROR=False)")
                    break
                    
        print(f"\n{action_name} payload completed: {success_count}/{len(commands)} commands succeeded")
        
    def device_enable(self):
        """Execute device enable payload."""
        print("🟢 DEVICE ENABLE triggered")
        
        # Play sound effect
        self.play_sound()
        
        # Execute enable commands
        self.execute_command_list(DEVICE_ENABLE_COMMANDS, "DEVICE ENABLE")
        
    def device_disable(self):
        """Execute device disable payload."""
        print("🔴 DEVICE DISABLE triggered")
        
        # Play sound effect
        self.play_sound()
        
        # Execute disable commands
        self.execute_command_list(DEVICE_DISABLE_COMMANDS, "DEVICE DISABLE")
        
    def cleanup(self):
        """Clean up resources."""
        if self.sound_initialized:
            try:
                pygame.mixer.quit()
            except:
                pass

def print_usage():
    """Print usage information."""
    print("InfraLink Device Payload Controller")
    print("==================================")
    print()
    print("Usage:")
    print("  python devicepayload.py enable     # Trigger device enable payload")
    print("  python devicepayload.py disable    # Trigger device disable payload")
    print("  python devicepayload.py --help     # Show this help message")
    print()
    print("Configuration:")
    print(f"  Sound file: {SOUND_FILE}")
    print(f"  Sound enabled: {ENABLE_SOUND}")
    print(f"  Enable commands: {len(DEVICE_ENABLE_COMMANDS)} configured")
    print(f"  Disable commands: {len(DEVICE_DISABLE_COMMANDS)} configured")
    print()
    print("To customize payloads, edit the DEVICE_ENABLE_COMMANDS and")
    print("DEVICE_DISABLE_COMMANDS lists at the top of this script.")

def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)
        
    action = sys.argv[1].lower()
    
    if action in ['--help', '-h', 'help']:
        print_usage()
        sys.exit(0)
        
    if action not in ['enable', 'disable']:
        print(f"Error: Unknown action '{action}'")
        print_usage()
        sys.exit(1)
        
    controller = DevicePayloadController()
    
    try:
        if action == 'enable':
            controller.device_enable()
        elif action == 'disable':
            controller.device_disable()
            
        print(f"\n✓ {action.title()} payload execution completed")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
    finally:
        controller.cleanup()

if __name__ == "__main__":
    main()
