#!/usr/bin/env python3
"""
InfraLink Demo Script
This script demonstrates the complete InfraLink workflow for testing purposes.
"""

import json
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from web3 import Web3
from datetime import datetime

class InfraLinkDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("InfraLink Demo")
        self.root.geometry("800x600")
        
        # Demo configuration
        self.demo_config = {
            "rpc_url": "http://localhost:8545",  # Default Ganache/Hardhat
            "contract_address": "0x0000000000000000000000000000000000000000",
            "token_address": "0x0000000000000000000000000000000000000000",
            "private_key": "0x0000000000000000000000000000000000000000000000000000000000000000",
            "fee_per_second": 1000000000000000  # 0.001 tokens per second
        }
        
        self.w3 = None
        self.contract = None
        self.token_contract = None
        self.account = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configuration tab
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="Configuration")
        self.setup_config_tab(config_frame)
        
        # Contract deployment tab
        deploy_frame = ttk.Frame(notebook)
        notebook.add(deploy_frame, text="Contract Deployment")
        self.setup_deploy_tab(deploy_frame)
        
        # Device monitor tab
        monitor_frame = ttk.Frame(notebook)
        notebook.add(monitor_frame, text="Device Monitor")
        self.setup_monitor_tab(monitor_frame)
        
        # User simulation tab
        user_frame = ttk.Frame(notebook)
        notebook.add(user_frame, text="User Simulation")
        self.setup_user_tab(user_frame)
        
        # Logs tab
        logs_frame = ttk.Frame(notebook)
        notebook.add(logs_frame, text="Logs")
        self.setup_logs_tab(logs_frame)
        
    def setup_config_tab(self, parent):
        # Configuration form
        config_frame = ttk.LabelFrame(parent, text="Network Configuration", padding="10")
        config_frame.pack(fill='x', pady=5)
        
        # RPC URL
        ttk.Label(config_frame, text="RPC URL:").grid(row=0, column=0, sticky='w', pady=2)
        self.rpc_entry = ttk.Entry(config_frame, width=60)
        self.rpc_entry.grid(row=0, column=1, padx=5)
        self.rpc_entry.insert(0, self.demo_config["rpc_url"])
        
        # Contract addresses
        ttk.Label(config_frame, text="Device Contract:").grid(row=1, column=0, sticky='w', pady=2)
        self.contract_entry = ttk.Entry(config_frame, width=60)
        self.contract_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(config_frame, text="Token Contract:").grid(row=2, column=0, sticky='w', pady=2)
        self.token_entry = ttk.Entry(config_frame, width=60)
        self.token_entry.grid(row=2, column=1, padx=5)
        
        # Private key
        ttk.Label(config_frame, text="Private Key:").grid(row=3, column=0, sticky='w', pady=2)
        self.key_entry = ttk.Entry(config_frame, width=60, show="*")
        self.key_entry.grid(row=3, column=1, padx=5)
        
        # Connect button
        ttk.Button(config_frame, text="Connect", command=self.connect_blockchain).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Status
        self.status_label = ttk.Label(config_frame, text="Not connected", foreground="red")
        self.status_label.grid(row=5, column=0, columnspan=2)
        
    def setup_deploy_tab(self, parent):
        # Deployment instructions
        deploy_frame = ttk.LabelFrame(parent, text="Contract Deployment", padding="10")
        deploy_frame.pack(fill='both', expand=True, pady=5)
        
        instructions = """
        1. Deploy TestToken contract:
           - Name: "InfraLink Test Token"
           - Symbol: "ILT"
           - Decimals: 18
        
        2. Deploy DeviceAccess contract:
           - Token address: [TestToken address]
           - Fee per second: 1000000000000000 (0.001 tokens)
           - Whitelist fee: 500000000000000 (0.0005 tokens)
        
        3. Mint test tokens to your account
        
        4. Update configuration with deployed addresses
        """
        
        instructions_text = tk.Text(deploy_frame, height=10, wrap='word')
        instructions_text.pack(fill='both', expand=True)
        instructions_text.insert('1.0', instructions)
        instructions_text.config(state='disabled')
        
        # Quick deployment buttons (for local testing)
        button_frame = ttk.Frame(deploy_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Deploy Test Token", command=self.deploy_test_token).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Deploy Device Contract", command=self.deploy_device_contract).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Mint Test Tokens", command=self.mint_test_tokens).pack(side='left', padx=5)
        
    def setup_monitor_tab(self, parent):
        # Device status display
        status_frame = ttk.LabelFrame(parent, text="Device Status", padding="10")
        status_frame.pack(fill='x', pady=5)
        
        # Status indicators
        self.device_status = ttk.Label(status_frame, text="🔒 OFFLINE", font=("Arial", 14, "bold"))
        self.device_status.pack(pady=5)
        
        self.user_info = ttk.Label(status_frame, text="No active user")
        self.user_info.pack(pady=2)
        
        self.time_info = ttk.Label(status_frame, text="Time remaining: --")
        self.time_info.pack(pady=2)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, length=400, mode='determinate')
        self.progress.pack(pady=10)
        
        # Control buttons
        control_frame = ttk.Frame(status_frame)
        control_frame.pack(fill='x', pady=5)
        
        ttk.Button(control_frame, text="Start Monitoring", command=self.start_monitoring).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Stop Monitoring", command=self.stop_monitoring).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Force Deactivate", command=self.force_deactivate).pack(side='left', padx=5)
        
        self.monitoring = False
        
    def setup_user_tab(self, parent):
        # User simulation
        user_frame = ttk.LabelFrame(parent, text="User Simulation", padding="10")
        user_frame.pack(fill='x', pady=5)
        
        # Duration input
        ttk.Label(user_frame, text="Duration (seconds):").grid(row=0, column=0, sticky='w', pady=2)
        self.duration_entry = ttk.Entry(user_frame, width=10)
        self.duration_entry.grid(row=0, column=1, padx=5)
        self.duration_entry.insert(0, "300")  # 5 minutes
        
        # Action buttons
        button_frame = ttk.Frame(user_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Activate Device", command=self.activate_device).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Deactivate Device", command=self.deactivate_device).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Check Balance", command=self.check_balance).pack(side='left', padx=5)
        
        # Device info display
        info_frame = ttk.LabelFrame(user_frame, text="Device Information", padding="10")
        info_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)
        
        self.device_info_text = tk.Text(info_frame, height=8, wrap='word')
        self.device_info_text.pack(fill='both', expand=True)
        
    def setup_logs_tab(self, parent):
        # Logs display
        logs_frame = ttk.LabelFrame(parent, text="Event Logs", padding="10")
        logs_frame.pack(fill='both', expand=True, pady=5)
        
        self.logs_text = scrolledtext.ScrolledText(logs_frame, wrap='word')
        self.logs_text.pack(fill='both', expand=True)
        
        # Clear logs button
        ttk.Button(logs_frame, text="Clear Logs", command=self.clear_logs).pack(pady=5)
        
    def log_message(self, message):
        """Add a timestamped message to the logs"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.logs_text.insert('end', log_entry)
        self.logs_text.see('end')
        
    def clear_logs(self):
        """Clear all log messages"""
        self.logs_text.delete('1.0', 'end')
        
    def connect_blockchain(self):
        """Connect to blockchain and initialize contracts"""
        try:
            rpc_url = self.rpc_entry.get()
            contract_addr = self.contract_entry.get()
            token_addr = self.token_entry.get()
            private_key = self.key_entry.get()
            
            # Initialize Web3
            self.w3 = Web3(Web3.HTTPProvider(rpc_url))
            
            if not self.w3.is_connected():
                raise Exception("Failed to connect to blockchain")
            
            # Initialize account
            if private_key:
                self.account = self.w3.eth.account.from_key(private_key)
                self.log_message(f"Connected account: {self.account.address}")
            
            # Initialize contracts if addresses provided
            if contract_addr and contract_addr != "0x0000000000000000000000000000000000000000":
                # Use simplified ABI for demo
                device_abi = [
                    {"inputs": [], "name": "isActive", "outputs": [{"type": "bool"}], "stateMutability": "view", "type": "function"},
                    {"inputs": [], "name": "sessionEndsAt", "outputs": [{"type": "uint256"}], "stateMutability": "view", "type": "function"},
                    {"inputs": [], "name": "lastActivatedBy", "outputs": [{"type": "address"}], "stateMutability": "view", "type": "function"},
                    {"inputs": [{"type": "uint256"}], "name": "activate", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
                    {"inputs": [], "name": "deactivate", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
                ]
                self.contract = self.w3.eth.contract(address=contract_addr, abi=device_abi)
                self.log_message(f"Device contract initialized: {contract_addr}")
            
            self.status_label.config(text="Connected", foreground="green")
            self.log_message("Blockchain connection established")
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", foreground="red")
            self.log_message(f"Connection failed: {str(e)}")
            
    def deploy_test_token(self):
        """Deploy test token contract (placeholder)"""
        self.log_message("Test token deployment would happen here")
        messagebox.showinfo("Deploy Token", "This would deploy a test ERC20 token contract")
        
    def deploy_device_contract(self):
        """Deploy device contract (placeholder)"""
        self.log_message("Device contract deployment would happen here")
        messagebox.showinfo("Deploy Device", "This would deploy the DeviceAccess contract")
        
    def mint_test_tokens(self):
        """Mint test tokens (placeholder)"""
        self.log_message("Token minting would happen here")
        messagebox.showinfo("Mint Tokens", "This would mint test tokens to your account")
        
    def start_monitoring(self):
        """Start device monitoring"""
        if not self.contract:
            messagebox.showerror("Error", "Please connect to a device contract first")
            return
            
        self.monitoring = True
        self.log_message("Started device monitoring")
        self.monitor_device()
        
    def stop_monitoring(self):
        """Stop device monitoring"""
        self.monitoring = False
        self.log_message("Stopped device monitoring")
        
    def monitor_device(self):
        """Monitor device status"""
        if not self.monitoring or not self.contract:
            return
            
        try:
            # Get device status
            is_active = self.contract.functions.isActive().call()
            session_ends_at = self.contract.functions.sessionEndsAt().call()
            last_activated_by = self.contract.functions.lastActivatedBy().call()
            
            current_time = int(time.time())
            time_remaining = max(0, session_ends_at - current_time)
            
            # Update UI
            if is_active and time_remaining > 0:
                self.device_status.config(text="🔓 ONLINE", foreground="green")
                self.user_info.config(text=f"Active user: {last_activated_by[:10]}...")
                self.time_info.config(text=f"Time remaining: {time_remaining}s")
                
                # Update progress bar
                if session_ends_at > current_time:
                    progress = ((session_ends_at - current_time) / 3600) * 100  # Assuming 1 hour max
                    self.progress['value'] = min(progress, 100)
            else:
                self.device_status.config(text="🔒 OFFLINE", foreground="red")
                self.user_info.config(text="No active user")
                self.time_info.config(text="Time remaining: --")
                self.progress['value'] = 0
                
        except Exception as e:
            self.log_message(f"Monitoring error: {str(e)}")
            
        # Schedule next check
        if self.monitoring:
            self.root.after(5000, self.monitor_device)  # Check every 5 seconds
            
    def activate_device(self):
        """Simulate device activation"""
        if not self.contract or not self.account:
            messagebox.showerror("Error", "Please connect to blockchain and contract first")
            return
            
        try:
            duration = int(self.duration_entry.get())
            
            # Build transaction
            txn = self.contract.functions.activate(duration).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign and send transaction
            signed_txn = self.account.sign_transaction(txn)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            self.log_message(f"Device activation transaction sent: {tx_hash.hex()}")
            
            # Wait for confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                self.log_message(f"Device activated successfully for {duration} seconds")
                messagebox.showinfo("Success", f"Device activated for {duration} seconds")
            else:
                self.log_message("Device activation failed")
                messagebox.showerror("Error", "Device activation failed")
                
        except Exception as e:
            self.log_message(f"Activation error: {str(e)}")
            messagebox.showerror("Error", f"Activation failed: {str(e)}")
            
    def deactivate_device(self):
        """Simulate device deactivation"""
        if not self.contract or not self.account:
            messagebox.showerror("Error", "Please connect to blockchain and contract first")
            return
            
        try:
            # Build transaction
            txn = self.contract.functions.deactivate().build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign and send transaction
            signed_txn = self.account.sign_transaction(txn)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            self.log_message(f"Device deactivation transaction sent: {tx_hash.hex()}")
            
            # Wait for confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                self.log_message("Device deactivated successfully")
                messagebox.showinfo("Success", "Device deactivated")
            else:
                self.log_message("Device deactivation failed")
                messagebox.showerror("Error", "Device deactivation failed")
                
        except Exception as e:
            self.log_message(f"Deactivation error: {str(e)}")
            messagebox.showerror("Error", f"Deactivation failed: {str(e)}")
            
    def force_deactivate(self):
        """Force deactivate device (owner only)"""
        if not self.contract or not self.account:
            messagebox.showerror("Error", "Please connect to blockchain and contract first")
            return
            
        if messagebox.askyesno("Confirm", "Force deactivate device? This can only be done by the contract owner."):
            self.log_message("Force deactivation would happen here (owner only)")
            
    def check_balance(self):
        """Check account balance"""
        if not self.w3 or not self.account:
            messagebox.showerror("Error", "Please connect to blockchain first")
            return
            
        try:
            balance = self.w3.eth.get_balance(self.account.address)
            balance_eth = self.w3.from_wei(balance, 'ether')
            
            self.log_message(f"Account balance: {balance_eth} ETH")
            messagebox.showinfo("Balance", f"Account balance: {balance_eth} ETH")
            
        except Exception as e:
            self.log_message(f"Balance check error: {str(e)}")
            messagebox.showerror("Error", f"Balance check failed: {str(e)}")
            
    def run(self):
        """Start the demo application"""
        self.log_message("InfraLink Demo started")
        self.root.mainloop()

if __name__ == "__main__":
    demo = InfraLinkDemo()
    demo.run()
