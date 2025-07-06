import time
import tkinter as tk
from tkinter import ttk, messagebox
from web3 import Web3
import json
import subprocess
import os
from network_utils import get_network_info, format_native_amount, get_currency_symbol

# === CONFIG ===
# Supported Networks:
# - Ethereum Mainnet: "https://mainnet.infura.io/v3/YOUR_PROJECT_ID"
# - Ethereum Sepolia: "https://sepolia.infura.io/v3/YOUR_PROJECT_ID"  
# - Hedera Testnet: "https://testnet.hashio.io/api"
# - Local development: "http://127.0.0.1:8545"
INFURA_URL = "https://testnet.hashio.io/api"  # Hedera testnet by default
DEVICE_CONTRACT_ADDRESS = "0xaff84326fc701dfb3c5881b2749dba27e9a98978"  # Updated contract address
INFO_CONTRACT_ADDRESS = "0x7aee0cbbcd0e5257931f7dc87f0345c1bb2aab39"  # Info contract for whitelist logic

# Device Contract ABI - Updated to match actual deployed contract
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "_token", "type": "address"},
            {"internalType": "uint256", "name": "_feePerSecond", "type": "uint256"},
            {"internalType": "uint256", "name": "_whitelistFeePerSecond", "type": "uint256"},
            {"internalType": "string", "name": "_deviceName", "type": "string"},
            {"internalType": "string", "name": "_deviceDescription", "type": "string"}
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "duration", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "endsAt", "type": "uint256"},
            {"indexed": False, "internalType": "bool", "name": "isWhitelisted", "type": "bool"},
            {"indexed": False, "internalType": "uint256", "name": "paidAmount", "type": "uint256"}
        ],
        "name": "DeviceActivated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
            {"indexed": False, "internalType": "bool", "name": "wasWhitelisted", "type": "bool"}
        ],
        "name": "DeviceDeactivated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "string", "name": "name", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "description", "type": "string"}
        ],
        "name": "DeviceInfoUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "newFee", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "newWhitelistFee", "type": "uint256"}
        ],
        "name": "FeeChanged",
        "type": "event"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "secondsToActivate", "type": "uint256"}
        ],
        "name": "activate",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "deactivate",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "deviceDescription",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "deviceName",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "feePerSecond",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "forceDeactivate",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getDeviceDetails",
        "outputs": [
            {"internalType": "string", "name": "_deviceName", "type": "string"},
            {"internalType": "string", "name": "_deviceDescription", "type": "string"},
            {"internalType": "bool", "name": "_useNativeToken", "type": "bool"},
            {"internalType": "bool", "name": "_lastUserWasWhitelisted", "type": "bool"},
            {"internalType": "uint256", "name": "_whitelistFeePerSecond", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"}
        ],
        "name": "getDeviceInfo",
        "outputs": [
            {"internalType": "uint256", "name": "_feePerSecond", "type": "uint256"},
            {"internalType": "bool", "name": "_isActive", "type": "bool"},
            {"internalType": "address", "name": "_lastActivatedBy", "type": "address"},
            {"internalType": "uint256", "name": "_sessionEndsAt", "type": "uint256"},
            {"internalType": "address", "name": "_token", "type": "address"},
            {"internalType": "bool", "name": "_isWhitelisted", "type": "bool"},
            {"internalType": "uint256", "name": "_timeRemaining", "type": "uint256"},
            {"internalType": "string", "name": "_tokenName", "type": "string"},
            {"internalType": "string", "name": "_tokenSymbol", "type": "string"},
            {"internalType": "uint8", "name": "_tokenDecimals", "type": "uint8"}
        ],
        "stateMutability": "view",
        "type": "function"
    },


    {
        "inputs": [],
        "name": "isActive",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "lastActivatedBy",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "lastUserWasWhitelisted",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {"internalType": "address", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "sessionEndsAt",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_name", "type": "string"},
            {"internalType": "string", "name": "_description", "type": "string"}
        ],
        "name": "setDeviceInfo",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_fee", "type": "uint256"},
            {"internalType": "uint256", "name": "_whitelistFee", "type": "uint256"}
        ],
        "name": "setFee",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_token", "type": "address"}
        ],
        "name": "setToken",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },


    {
        "inputs": [],
        "name": "token",
        "outputs": [
            {"internalType": "address", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "tokenDecimals",
        "outputs": [
            {"internalType": "uint8", "name": "", "type": "uint8"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "tokenName",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "tokenSymbol",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "newOwner", "type": "address"}
        ],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "useNativeToken",
        "outputs": [
            {"internalType": "bool", "name": "", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },



    {
        "inputs": [],
        "name": "whitelistFeePerSecond",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },

    {
        "inputs": [],
        "name": "withdrawFees",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Info Contract ABI for whitelist functionality - Updated to match actual deployed contract
INFO_CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"},
            {"internalType": "address", "name": "deviceContract", "type": "address"}
        ],
        "name": "getWhitelistInfo",
        "outputs": [
            {"internalType": "string", "name": "whitelistName", "type": "string"},
            {"internalType": "uint256", "name": "feePerSecond", "type": "uint256"},
            {"internalType": "bool", "name": "isFree", "type": "bool"},
            {"internalType": "uint256", "name": "addedAt", "type": "uint256"},
            {"internalType": "address", "name": "addedBy", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"},
            {"internalType": "address", "name": "deviceContract", "type": "address"}
        ],
        "name": "isUserWhitelisted",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "getUserWhitelists",
        "outputs": [
            {"internalType": "address[]", "name": "deviceContracts", "type": "address[]"},
            {"internalType": "string[]", "name": "deviceNames", "type": "string[]"},
            {"internalType": "string[]", "name": "whitelistNames", "type": "string[]"},
            {"internalType": "uint256[]", "name": "feePerSeconds", "type": "uint256[]"},
            {"internalType": "bool[]", "name": "isFreeAccess", "type": "bool[]"},
            {"internalType": "uint256[]", "name": "addedAts", "type": "uint256[]"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "getUserProfile",
        "outputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "bio", "type": "string"},
            {"internalType": "string", "name": "email", "type": "string"},
            {"internalType": "string", "name": "avatar", "type": "string"},
            {"internalType": "bool", "name": "exists", "type": "bool"},
            {"internalType": "uint256", "name": "createdAt", "type": "uint256"},
            {"internalType": "uint256", "name": "updatedAt", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getAllRegisteredUsers",
        "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getAllRegisteredDevices",
        "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
        "stateMutability": "view",
        "type": "function"
    }
]

class DeviceMonitor:
    def __init__(self):
        self.w3 = None
        self.contract = None
        self.info_contract = None  # Info contract for whitelist logic
        self.root = tk.Tk()
        self.setup_ui()
        self.last_error = None
        self.update_interval = 10000  # 10 seconds for demo, 60000 for production
        self.device_info = {}
        self.whitelist_info = {}
        self.last_device_state = None  # Track device state changes
        
    def setup_ui(self):
        self.root.title("InfraLink Device Monitor")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Main frame with notebook
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status tab
        status_frame = ttk.Frame(notebook, padding="10")
        notebook.add(status_frame, text="Device Status")
        self.setup_status_tab(status_frame)
        
        # Users tab
        users_frame = ttk.Frame(notebook, padding="10")
        notebook.add(users_frame, text="Registered Users")
        self.setup_whitelist_tab(users_frame)
        
        # Configuration tab remains at bottom
        config_frame = ttk.Frame(notebook, padding="10")
        notebook.add(config_frame, text="Configuration")
        self.setup_config_tab(config_frame)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
    def setup_status_tab(self, parent):
        # Device Info Frame
        info_frame = ttk.LabelFrame(parent, text="Device Information", padding="10")
        info_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.device_name_label = ttk.Label(info_frame, text="Device: Loading...", font=("Arial", 12, "bold"))
        self.device_name_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.device_desc_label = ttk.Label(info_frame, text="Description: Loading...")
        self.device_desc_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.token_info_label = ttk.Label(info_frame, text="Payment Token: Loading...")
        self.token_info_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # Device Status Frame
        status_frame = ttk.LabelFrame(parent, text="Current Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status indicators
        self.status_label = ttk.Label(status_frame, text="🔒 OFFLINE", 
                                     font=("Arial", 16, "bold"))
        self.status_label.grid(row=0, column=0, pady=5)
        
        self.user_label = ttk.Label(status_frame, text="No active user")
        self.user_label.grid(row=1, column=0, pady=2)
        
        self.whitelist_status_label = ttk.Label(status_frame, text="")
        self.whitelist_status_label.grid(row=2, column=0, pady=2)
        
        self.time_label = ttk.Label(status_frame, text="Time remaining: --")
        self.time_label.grid(row=3, column=0, pady=2)
        
        self.fee_label = ttk.Label(status_frame, text="Fee per second: --")
        self.fee_label.grid(row=4, column=0, pady=2)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, length=400, mode='determinate')
        self.progress.grid(row=5, column=0, pady=10)
        
        # Pricing Frame
        pricing_frame = ttk.LabelFrame(parent, text="Pricing Information", padding="10")
        pricing_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.regular_fee_label = ttk.Label(pricing_frame, text="Regular Fee: --")
        self.regular_fee_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.whitelist_fee_label = ttk.Label(pricing_frame, text="Whitelist Fee: --")
        self.whitelist_fee_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
    def setup_whitelist_tab(self, parent):
        # Users summary
        summary_frame = ttk.LabelFrame(parent, text="Registered Users Summary", padding="10")
        summary_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.whitelist_count_label = ttk.Label(summary_frame, text="Total Registered Users: 0")
        self.whitelist_count_label.pack(pady=5)
        
        # Users details
        details_frame = ttk.LabelFrame(parent, text="Registered Users", padding="10")
        details_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create treeview for whitelist
        columns = ('Address', 'Name')
        self.whitelist_tree = ttk.Treeview(details_frame, columns=columns, show='headings', height=10)
        
        # Define headings
        self.whitelist_tree.heading('Address', text='Address')
        self.whitelist_tree.heading('Name', text='Name')
        
        # Define column widths
        self.whitelist_tree.column('Address', width=300)
        self.whitelist_tree.column('Name', width=200)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.whitelist_tree.yview)
        self.whitelist_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.whitelist_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights for whitelist tab
        parent.rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
        details_frame.columnconfigure(0, weight=1)
        
        # Refresh button
        ttk.Button(details_frame, text="Refresh Users", command=self.refresh_whitelist).grid(row=1, column=0, pady=10)
        
    def setup_config_tab(self, parent):
        # Connection Frame
        conn_frame = ttk.LabelFrame(parent, text="Connection", padding="10")
        conn_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Contract address entry
        ttk.Label(conn_frame, text="Contract Address:").grid(row=0, column=0, sticky=tk.W)
        self.address_entry = ttk.Entry(conn_frame, width=60)
        self.address_entry.grid(row=0, column=1, padx=5)
        self.address_entry.insert(0, DEVICE_CONTRACT_ADDRESS)
        
        # RPC URL entry
        ttk.Label(conn_frame, text="RPC URL:").grid(row=1, column=0, sticky=tk.W)
        self.rpc_entry = ttk.Entry(conn_frame, width=60)
        self.rpc_entry.grid(row=1, column=1, padx=5)
        self.rpc_entry.insert(0, INFURA_URL)
        
        # Connect button
        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.connect_to_contract)
        self.connect_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Status bar
        self.status_bar = ttk.Label(conn_frame, text="Ready to connect", relief=tk.SUNKEN)
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Control Frame
        control_frame = ttk.LabelFrame(parent, text="Monitoring Controls", padding="10")
        control_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.start_btn = ttk.Button(control_frame, text="Start Monitoring", command=self.start_monitoring)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="Stop Monitoring", command=self.stop_monitoring)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # Auto-refresh interval
        ttk.Label(control_frame, text="Update Interval (seconds):").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.interval_var = tk.StringVar(value="10")
        interval_entry = ttk.Entry(control_frame, textvariable=self.interval_var, width=10)
        interval_entry.grid(row=1, column=1, padx=5, pady=(10, 0))
        
        # Configure grid weights
        conn_frame.columnconfigure(1, weight=1)
        
    def call_device_payload(self, action, user_address=None, is_whitelisted=False):
        """Call the devicepayload.py script for device control"""
        try:
            script_path = os.path.join(os.path.dirname(__file__), "devicepayload.py")
            if not os.path.exists(script_path):
                print(f"Warning: devicepayload.py not found at {script_path}")
                return False
                
            cmd = ["python", script_path, action]
            if user_address:
                cmd.append(user_address)
                cmd.append(str(is_whitelisted).lower())
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"Device payload {action} executed successfully")
                if result.stdout:
                    print(f"Output: {result.stdout.strip()}")
                return True
            else:
                print(f"Device payload {action} failed")
                if result.stderr:
                    print(f"Error: {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"Device payload {action} timed out")
            return False
        except Exception as e:
            print(f"Error calling device payload {action}: {e}")
            return False
        
    def connect_to_contract(self):
        try:
            rpc_url = self.rpc_entry.get().strip()
            contract_address = self.address_entry.get().strip()
            
            if not rpc_url or not contract_address:
                messagebox.showerror("Error", "Please enter both RPC URL and contract address")
                return
                
            # Initialize Web3
            self.w3 = Web3(Web3.HTTPProvider(rpc_url))
            
            if not self.w3.is_connected():
                raise Exception("Failed to connect to RPC node")
            
            # Convert address to checksummed format if needed
            if contract_address.startswith('0x') and len(contract_address) == 42:
                contract_address = self.w3.to_checksum_address(contract_address.lower())
                
            # Initialize contract
            self.contract = self.w3.eth.contract(address=contract_address, abi=CONTRACT_ABI)
            
            # Test device contract call
            owner = self.contract.functions.owner().call()
            
            # Try to initialize Info contract for whitelist functionality
            try:
                info_contract_address = self.w3.to_checksum_address(INFO_CONTRACT_ADDRESS.lower())
                self.info_contract = self.w3.eth.contract(address=info_contract_address, abi=INFO_CONTRACT_ABI)
                
                # Test Info contract call - try to get owner or check if contract exists
                try:
                    # Try to call a simple function to see if contract exists
                    code = self.w3.eth.get_code(info_contract_address)
                    if code == '0x':
                        raise Exception("Info contract not deployed at this address")
                    print("Info contract found and connected successfully")
                except Exception as test_error:
                    raise Exception(f"Info contract test failed: {test_error}")
                
            except Exception as info_error:
                print(f"Info contract connection failed: {info_error}")
                print("Info contract unavailable - whitelist functionality will be disabled")
                self.info_contract = None
                
            self.status_bar.config(text=f"Connected to contract. Owner: {owner[:10]}...")
            if self.info_contract:
                self.status_bar.config(text=f"Connected to contracts. Owner: {owner[:10]}...")
            else:
                self.status_bar.config(text=f"Connected to device contract (Info contract unavailable). Owner: {owner[:10]}...")
                
            self.connect_btn.config(state='disabled')
            self.start_monitoring()
            
        except Exception as e:
            self.status_bar.config(text=f"Connection failed: {str(e)}")
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            print(f"Connection error: {e}")
            
    def start_monitoring(self):
        self.update_status()
        
    def update_status(self):
        try:
            if not self.contract:
                return
                
            # Get device info with zero address to get general info
            zero_address = "0x0000000000000000000000000000000000000000"
            device_info = self.contract.functions.getDeviceInfo(zero_address).call()
            
            # Parse the device info response (10 values from getDeviceInfo)
            fee_per_second = device_info[0]
            is_active = device_info[1]
            last_activated_by = device_info[2]
            session_ends_at = device_info[3]
            token_address = device_info[4]
            is_whitelisted = device_info[5]
            time_remaining = device_info[6]
            token_name = device_info[7]
            token_symbol = device_info[8]
            token_decimals = device_info[9]
            
            # Get additional device details separately
            device_details = self.contract.functions.getDeviceDetails().call()
            device_name = device_details[0]
            device_description = device_details[1]
            use_native_token = device_details[2]
            last_user_was_whitelisted = device_details[3]
            whitelist_fee_per_second = device_details[4]
            
            # Store device info for other uses
            self.device_info = {
                'device_name': device_name,
                'device_description': device_description,
                'token_name': token_name,
                'token_symbol': token_symbol,
                'token_decimals': token_decimals,
                'token_address': token_address,
                'fee_per_second': fee_per_second,
                'last_user_was_whitelisted': last_user_was_whitelisted,
                'use_native_token': use_native_token
            }
            
            # Get regular and whitelist fees
            regular_fee = self.contract.functions.feePerSecond().call()
            whitelist_fee = whitelist_fee_per_second  # Use the value from getDeviceDetails
            
            current_time = int(time.time())
            
            # Update device info labels
            self.device_name_label.config(text=f"Device: {device_name}")
            self.device_desc_label.config(text=f"Description: {device_description}")
            
            if use_native_token:
                # Get network-aware native token name
                try:
                    chain_id = self.w3.eth.chain_id
                    network_info = get_network_info(chain_id)
                    native_currency = network_info['currency']
                    self.token_info_label.config(text=f"Payment Token: Native Token ({native_currency})")
                except:
                    self.token_info_label.config(text=f"Payment Token: Native Token ({token_symbol})")
            else:
                self.token_info_label.config(text=f"Payment Token: {token_name} ({token_symbol})")
            
            # Update fee info
            regular_fee_formatted = self.format_token_amount(regular_fee, token_decimals)
            whitelist_fee_formatted = self.format_token_amount(whitelist_fee, token_decimals)
            
            # Get network-aware currency symbol
            try:
                chain_id = self.w3.eth.chain_id
                token_display = get_currency_symbol(chain_id, token_symbol if use_native_token else token_symbol)
            except:
                token_display = "HBAR" if use_native_token else token_symbol
            
            self.regular_fee_label.config(text=f"Regular Fee: {regular_fee_formatted} {token_display}/sec")
            
            if whitelist_fee == 0:
                self.whitelist_fee_label.config(text=f"Whitelist Fee: FREE")
            else:
                self.whitelist_fee_label.config(text=f"Whitelist Fee: {whitelist_fee_formatted} {token_display}/sec")
            
            # Update UI and detect state changes
            current_state = {
                'is_active': is_active and session_ends_at > current_time,
                'user_address': last_activated_by,
                'is_whitelisted': last_user_was_whitelisted
            }
            
            # Check for state changes and trigger payload actions
            if self.last_device_state is not None:
                # Device enabled (inactive -> active)
                if not self.last_device_state['is_active'] and current_state['is_active']:
                    print(f"Device state change: ENABLED by {current_state['user_address']}")
                    self.call_device_payload('enable', current_state['user_address'], current_state['is_whitelisted'])
                
                # Device disabled (active -> inactive)
                elif self.last_device_state['is_active'] and not current_state['is_active']:
                    print(f"Device state change: DISABLED (user {self.last_device_state['user_address']})")
                    self.call_device_payload('disable', self.last_device_state['user_address'], self.last_device_state['is_whitelisted'])
            
            # Store current state for next comparison
            self.last_device_state = current_state
                
            # Update UI
            if current_state['is_active']:
                self.status_label.config(text="🟢 ONLINE", foreground="green")
                self.user_label.config(text=f"Active user: {last_activated_by[:10]}...")
                
                # Show whitelist status of current user
                if last_user_was_whitelisted:
                    self.whitelist_status_label.config(text="✅ Current user is whitelisted", foreground="green")
                else:
                    self.whitelist_status_label.config(text="Regular user (not whitelisted)", foreground="blue")
                
                remaining_seconds = max(0, session_ends_at - current_time)
                remaining_minutes = remaining_seconds // 60
                remaining_secs = remaining_seconds % 60
                
                self.time_label.config(text=f"Time remaining: {remaining_minutes}m {remaining_secs}s")
                
                # Update progress bar (calculate based on time remaining vs total duration)
                if time_remaining > 0:
                    elapsed = time_remaining - remaining_seconds
                    progress_value = (elapsed / time_remaining) * 100
                    self.progress['value'] = min(max(progress_value, 0), 100)
                else:
                    self.progress['value'] = 100
                
                # Update fee label with current user's rate
                if last_user_was_whitelisted:
                    current_fee_formatted = whitelist_fee_formatted if whitelist_fee > 0 else "FREE"
                    self.fee_label.config(text=f"Current user's rate: {current_fee_formatted} {token_display}/sec")
                else:
                    self.fee_label.config(text=f"Current user's rate: {regular_fee_formatted} {token_display}/sec")
                
            else:
                self.status_label.config(text="🔒 OFFLINE", foreground="red")
                self.user_label.config(text="No active user")
                self.whitelist_status_label.config(text="")
                self.time_label.config(text="Time remaining: --")
                self.progress['value'] = 0
                self.fee_label.config(text=f"Regular rate: {regular_fee_formatted} {token_display}/sec")
                
            self.status_bar.config(text=f"Last updated: {time.strftime('%H:%M:%S')}")
            self.last_error = None
            
        except Exception as e:
            error_msg = f"Error updating status: {str(e)}"
            self.status_bar.config(text=error_msg)
            if self.last_error != str(e):
                print(f"Error: {e}")
                self.last_error = str(e)
            
        # Schedule next update
        self.root.after(self.update_interval, self.update_status)
        
    def format_token_amount(self, amount, decimals):
        """Format token amount with proper decimal places using network-aware formatting"""
        if amount == 0:
            return "0"
        
        # Use network utilities if we have chain info
        if hasattr(self, 'w3') and self.w3 and self.w3.is_connected():
            try:
                chain_id = self.w3.eth.chain_id
                return format_native_amount(amount, chain_id, decimals)
            except:
                pass  # Fall back to manual formatting
        
        # Fallback to manual formatting
        decimal_amount = amount / (10 ** decimals)
        
        # Format with appropriate decimal places
        if decimal_amount >= 1:
            return f"{decimal_amount:.6f}"
        else:
            return f"{decimal_amount:.8f}"
    
    def refresh_whitelist(self):
        """Refresh the whitelist information using Info contract only"""
        try:
            if not self.info_contract:
                messagebox.showerror("Error", "Info contract not available")
                return
                
            print("Attempting to query Info contract...")
            # Get all registered users from Info contract
            all_users = self.info_contract.functions.getAllRegisteredUsers().call()
            print(f"Info contract returned {len(all_users)} registered users")
            
            # Update whitelist count
            self.whitelist_count_label.config(text=f"Total Registered Users: {len(all_users)}")
            
            # Clear existing items
            for item in self.whitelist_tree.get_children():
                self.whitelist_tree.delete(item)
            
            # Add user entries
            for address in all_users:
                self.whitelist_tree.insert('', tk.END, values=(address, "Registered User"))
            
            # Store basic info
            self.whitelist_info = {
                'addresses': all_users,
                'names': ["Registered User"] * len(all_users),
                'count': len(all_users)
            }
            print("Info contract query successful")
                
        except Exception as e:
            print(f"Info contract whitelist query failed: {e}")
            messagebox.showerror("Error", f"Failed to refresh whitelist: {str(e)}")
            # Show empty whitelist on failure
            self.whitelist_count_label.config(text="Total Registered Users: 0 (Unable to fetch)")
            for item in self.whitelist_tree.get_children():
                self.whitelist_tree.delete(item)
            self.whitelist_info = {'addresses': [], 'names': [], 'count': 0}
    
    def stop_monitoring(self):
        """Stop the monitoring updates"""
        # This would stop the after() calls if we had a way to cancel them
        # For now, just disable the connect button
        self.connect_btn.config(state='normal')
        self.status_bar.config(text="Monitoring stopped")
        
    def get_update_interval(self):
        """Get the update interval from the UI"""
        try:
            return int(self.interval_var.get()) * 1000  # Convert to milliseconds
        except ValueError:
            return 10000  # Default 10 seconds
    
    def start_monitoring(self):
        """Start monitoring and update the interval"""
        self.update_interval = self.get_update_interval()
        self.update_status()
        self.refresh_whitelist()  # Also refresh whitelist when starting
        
    def on_closing(self):
        """Handle app closing"""
        self.root.destroy()
        
    def run(self):
        # Set up proper window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    monitor = DeviceMonitor()
    monitor.run()
