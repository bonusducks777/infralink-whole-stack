import time
import tkinter as tk
from tkinter import ttk, messagebox
from web3 import Web3
import json

# === CONFIG ===
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_PROJECT_ID"  # Replace with your node
DEVICE_CONTRACT_ADDRESS = "0xYourDeviceContractAddress"  # Will be updated when contract is deployed

# Enhanced Contract ABI with whitelist support
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
        "inputs": [
            {"internalType": "uint256", "name": "secondsToActivate", "type": "uint256"}
        ],
        "name": "activate",
        "outputs": [],
        "stateMutability": "nonpayable",
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
            {"internalType": "uint8", "name": "_tokenDecimals", "type": "uint8"},
            {"internalType": "string", "name": "_deviceName", "type": "string"},
            {"internalType": "string", "name": "_deviceDescription", "type": "string"},
            {"internalType": "bool", "name": "_lastUserWasWhitelisted", "type": "bool"},
            {"internalType": "string", "name": "_whitelistName", "type": "string"},
            {"internalType": "bool", "name": "_useNativeToken", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getWhitelistInfo",
        "outputs": [
            {"internalType": "address[]", "name": "addresses", "type": "address[]"},
            {"internalType": "string[]", "name": "names", "type": "string[]"},
            {"internalType": "uint256", "name": "count", "type": "uint256"}
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
        "name": "sessionEndsAt",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
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
        "name": "deviceName",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "deviceDescription",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "tokenName",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "tokenSymbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "feePerSecond",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "whitelistFeePerSecond",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

class DeviceMonitor:
    def __init__(self):
        self.w3 = None
        self.contract = None
        self.root = tk.Tk()
        self.setup_ui()
        self.last_error = None
        self.update_interval = 10000  # 10 seconds for demo, 60000 for production
        self.device_info = {}
        self.whitelist_info = {}
        
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
        
        # Whitelist tab
        whitelist_frame = ttk.Frame(notebook, padding="10")
        notebook.add(whitelist_frame, text="Whitelist Info")
        self.setup_whitelist_tab(whitelist_frame)
        
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
        # Whitelist summary
        summary_frame = ttk.LabelFrame(parent, text="Whitelist Summary", padding="10")
        summary_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.whitelist_count_label = ttk.Label(summary_frame, text="Total Whitelisted Users: 0")
        self.whitelist_count_label.pack(pady=5)
        
        # Whitelist details
        details_frame = ttk.LabelFrame(parent, text="Whitelisted Users", padding="10")
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
        ttk.Button(details_frame, text="Refresh Whitelist", command=self.refresh_whitelist).grid(row=1, column=0, pady=10)
        
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
                
            # Initialize contract
            self.contract = self.w3.eth.contract(address=contract_address, abi=CONTRACT_ABI)
            
            # Test contract call
            owner = self.contract.functions.owner().call()
            
            self.status_bar.config(text=f"Connected to contract. Owner: {owner[:10]}...")
            self.connect_btn.config(state='disabled')
            self.start_monitoring()
            
        except Exception as e:
            self.status_bar.config(text=f"Connection failed: {str(e)}")
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            
    def start_monitoring(self):
        self.update_status()
        
    def update_status(self):
        try:
            if not self.contract:
                return
                
            # Get device info with zero address to get general info
            zero_address = "0x0000000000000000000000000000000000000000"
            device_info = self.contract.functions.getDeviceInfo(zero_address).call()
            
            # Parse the enhanced device info response
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
            device_name = device_info[10]
            device_description = device_info[11]
            last_user_was_whitelisted = device_info[12]
            whitelist_name = device_info[13]
            use_native_token = device_info[14]
            
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
            whitelist_fee = self.contract.functions.whitelistFeePerSecond().call()
            
            current_time = int(time.time())
            
            # Update device info labels
            self.device_name_label.config(text=f"Device: {device_name}")
            self.device_desc_label.config(text=f"Description: {device_description}")
            
            if use_native_token:
                self.token_info_label.config(text=f"Payment Token: Native Token (ETH)")
            else:
                self.token_info_label.config(text=f"Payment Token: {token_name} ({token_symbol})")
            
            # Update fee info
            regular_fee_formatted = self.format_token_amount(regular_fee, token_decimals)
            whitelist_fee_formatted = self.format_token_amount(whitelist_fee, token_decimals)
            
            token_display = "ETH" if use_native_token else token_symbol
            
            self.regular_fee_label.config(text=f"Regular Fee: {regular_fee_formatted} {token_display}/sec")
            
            if whitelist_fee == 0:
                self.whitelist_fee_label.config(text=f"Whitelist Fee: FREE")
            else:
                self.whitelist_fee_label.config(text=f"Whitelist Fee: {whitelist_fee_formatted} {token_display}/sec")
            
            # Update UI
            if is_active and session_ends_at > current_time:
                self.status_label.config(text="� ONLINE", foreground="green")
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
                    self.fee_label.config(text=f"Current user's rate: {current_fee_formatted} {token_symbol}/sec")
                else:
                    self.fee_label.config(text=f"Current user's rate: {regular_fee_formatted} {token_symbol}/sec")
                
            else:
                self.status_label.config(text="🔒 OFFLINE", foreground="red")
                self.user_label.config(text="No active user")
                self.whitelist_status_label.config(text="")
                self.time_label.config(text="Time remaining: --")
                self.progress['value'] = 0
                self.fee_label.config(text=f"Regular rate: {regular_fee_formatted} {token_symbol}/sec")
                
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
        """Format token amount with proper decimal places"""
        if amount == 0:
            return "0"
        
        # Convert to decimal with proper precision
        decimal_amount = amount / (10 ** decimals)
        
        # Format with appropriate decimal places
        if decimal_amount >= 1:
            return f"{decimal_amount:.6f}"
        else:
            return f"{decimal_amount:.8f}"
    
    def refresh_whitelist(self):
        """Refresh the whitelist information"""
        try:
            if not self.contract:
                messagebox.showerror("Error", "Please connect to contract first")
                return
                
            # Get whitelist info
            whitelist_info = self.contract.functions.getWhitelistInfo().call()
            addresses = whitelist_info[0]
            names = whitelist_info[1]
            count = whitelist_info[2]
            
            # Update whitelist count
            self.whitelist_count_label.config(text=f"Total Whitelisted Users: {count}")
            
            # Clear existing items
            for item in self.whitelist_tree.get_children():
                self.whitelist_tree.delete(item)
                
            # Add whitelist entries
            for i, address in enumerate(addresses):
                name = names[i] if i < len(names) else "Unknown"
                self.whitelist_tree.insert('', tk.END, values=(address, name))
                
            # Store whitelist info
            self.whitelist_info = {
                'addresses': addresses,
                'names': names,
                'count': count
            }
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh whitelist: {str(e)}")
            print(f"Whitelist refresh error: {e}")
    
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
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    monitor = DeviceMonitor()
    monitor.run()
