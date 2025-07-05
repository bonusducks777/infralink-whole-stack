# InfraLink v2.0 Deployment & Setup Guide

## 📋 Prerequisites

1. **Node.js** (v18 or higher)
2. **Python** (v3.8 or higher)
3. **Web3 Wallet** (MetaMask, WalletConnect compatible)
4. **Ethereum Node Access** (Infura, Alchemy, or local node)
5. **Solidity Compiler** (for contract deployment)

## 🚀 Quick Start

### 1. Deploy Smart Contracts

#### Deploy InfraLink Info Contract (New in v2.0)
```solidity
// Deploy infralink-info.sol first - this is the central registry
// No constructor parameters needed
// This contract will be permanent and handle all user profiles and device whitelist
```

#### Deploy Test Token (Optional)
```solidity
// Deploy testtoken.sol if you need a test ERC20 token
// Constructor parameters: name, symbol, decimals
// Example: "InfraLink Token", "ILT", 18
```

#### Deploy Device Contract
```solidity
// Deploy devicecontract.sol with these parameters:
// - _token: Address of your ERC20 token (set to zero address for native ETH)
// - _feePerSecond: Fee in token units per second for regular users (e.g., 1000000000000000 for 0.001 tokens)
// - _whitelistFeePerSecond: Fee in token units per second for whitelisted users (0 for free access)
// - _deviceName: Human-readable name for your device (e.g., "3D Printer Lab A")
// - _deviceDescription: Description of the device (e.g., "High-resolution 3D printer for prototyping")
// - _useNativeToken: true for ETH payments, false for ERC20 tokens
```

### 2. Set Up Web Application

```bash
cd infralink-webapp
npm install

# Update contract addresses in:
# - src/components/UserProfile.tsx
# - src/components/WhitelistManager.tsx
# Set INFRALINK_INFO_ADDRESS to your deployed Info contract

npm run dev
```

The app will be available at `http://localhost:5173`

### 3. Configure Device Monitor

```bash
# Install Python dependencies
pip install -r requirements.txt

# Edit devicelocal.py and update:
# - INFURA_URL: Your Ethereum node URL
# - DEVICE_CONTRACT_ADDRESS: Your deployed contract address

# Run the monitor
python devicelocal.py
```

## 🔧 Configuration

### Contract Owner Tasks

1. **Register Device with Info Contract**
   ```solidity
   // In infralink-info.sol
   registerDevice(address deviceContract, string deviceName, string deviceDescription)
   ```

2. **Set Fees**
   ```solidity
   setFee(uint256 _regularFee, uint256 _whitelistFee) // Set both fees at once
   setWhitelistFee(uint256 _fee) // Set whitelist fee only (0 for free access)
   ```

3. **Manage Whitelist (Enhanced in v2.0)**
   ```solidity
   // Via device contract (legacy)
   setWhitelist(address user, bool status, string name) // Add/remove user with custom name
   
   // Via InfraLink Info contract (recommended)
   addDeviceWhitelist(address deviceContract, address user, string name, uint256 fee, bool isFree)
   removeDeviceWhitelist(address deviceContract, address user)
   ```

4. **Update Device Information**
   ```solidity
   setDeviceInfo(string name, string description) // Update device details
   ```

5. **Withdraw Fees (Enhanced for Native Tokens)**
   ```solidity
   withdrawFees() // Withdraw collected fees (ETH or ERC20) to owner
   ```

6. **View Information (Enhanced)**
   ```solidity
   getDeviceInfo(address user) // Get comprehensive device and user info (including native token support)
   getWhitelistInfo() // Get all whitelisted users and their names
   ```

### User Profile Management (New in v2.0)

1. **Create/Update Profile**
   ```solidity
   // In infralink-info.sol
   setUserProfile(string name, string bio, string email, string avatar)
   ```

2. **View Profile and Device Access**
   ```solidity
   getUserProfile(address user) // Get user profile information
   getAllUserDevices(address user) // Get all devices user has whitelist access to
   ```

### Device Setup

1. **Generate QR Code**
   - Go to `/device-owner` in the web app
   - Use the QR Generator tab
   - Enter your contract address
   - Generate and print QR code
   - Place on your device

2. **Manage Whitelist**
   - Use the Whitelist Manager tab in Device Owner tools
   - Enter your device contract address
   - Add/remove users with custom names and fees
   - View user profiles when managing access

3. **Configure Monitor**
   - Update `devicelocal.py` with your contract address
   - Run the Python script on your device hardware
   - Monitor will show device status, payment type, and countdown

## 💰 Native Token Support (New in v2.0)

### Using Native ETH Instead of ERC20

1. **Deploy Device Contract with Native Token Support**
   ```solidity
   // Set _useNativeToken to true in constructor
   // Set _token to zero address (0x0000000000000000000000000000000000000000)
   // Set fees in wei (1 ETH = 1e18 wei)
   ```

2. **User Experience with Native Tokens**
   - No token approval required
   - Direct ETH payment to contract
   - Fees shown in ETH instead of token units
   - Automatic balance checking for ETH

3. **Device Owner Benefits**
   - Simpler user experience (no token approval step)
   - Direct ETH collection
   - Lower gas costs for users
   - Broader user accessibility
   - Monitor will show device status and countdown

## 📱 User Flow

1. **Connect Wallet**
   - Users open the web app
   - Connect their Web3 wallet

2. **Find Device**
   - Scan QR code OR enter contract address manually
   - App fetches device information from contract

3. **Activate Device**
   - Choose duration (minutes)
   - Approve ERC20 token spending
   - Pay for device activation
   - Device becomes active for specified duration

4. **Monitor Session**
   - View remaining time
   - Extend session if needed
   - Deactivate early if desired

## 🔐 Security Notes

- **Contract Owner**: Has full control over fees and whitelist
- **Device Access**: Only current session holder can use device
- **Token Approval**: Users must approve token spending before activation
- **Session Management**: Sessions expire automatically or can be ended manually

## 🧪 Testing

### Local Testing Setup

1. **Use Ganache or Hardhat** for local blockchain
2. **Deploy contracts** to local network
3. **Fund test accounts** with test tokens
4. **Test full flow** from QR scan to device activation

### Testnet Deployment

1. **Deploy to Sepolia/Goerli** testnet
2. **Get testnet ETH** from faucets
3. **Test with real wallet** interactions
4. **Verify contract** on Etherscan

## 📊 Monitoring & Analytics

### Device Monitor Features
- **Real-time session status** with device name and description
- **Token information display** showing payment token details
- **User whitelist status** showing if current user is whitelisted
- **Fee rate display** showing regular and whitelist rates
- **Whitelist viewer** showing all whitelisted users with their names
- **Progress tracking** with accurate countdown timer
- **Connection status** and error handling
- **Automatic updates** with configurable intervals

### Contract Events
- `DeviceActivated`: When device is activated (includes whitelist status and amount paid)
- `DeviceDeactivated`: When device is deactivated (includes whitelist status)
- `FeeChanged`: When fees are updated (both regular and whitelist fees)
- `WhitelistUpdated`: When whitelist is modified (includes user name)
- `DeviceInfoUpdated`: When device information is updated

## 🛠️ Troubleshooting

### Common Issues

1. **"Device is busy"**
   - Another user has an active session
   - Wait for session to expire or subscribe to notifications

2. **"Insufficient allowance"**
   - Approve token spending first
   - Check token balance and allowance amount

3. **"Insufficient balance"**
   - User doesn't have enough tokens
   - Show current balance vs required payment

4. **"Not whitelisted" or fee confusion**
   - User sees different fee rates based on whitelist status
   - Clear display of regular vs whitelist fees
   - Whitelist status clearly shown in UI

5. **"Connection failed"**
   - Check RPC URL in Python script
   - Verify contract address is correct
   - Ensure network connectivity

6. **Python script errors**
   - Install dependencies: `pip install web3`
   - Check contract ABI matches deployed contract
   - Verify network connection and RPC endpoint

7. **Whitelist issues**
   - Only contract owner can modify whitelist
   - Whitelist names are optional but recommended
   - Free access requires whitelist fee to be set to 0

### Debug Tips

- Check browser console for errors
- Verify contract addresses are correct
- Ensure sufficient token balance
- Check network connectivity
- Monitor contract events on block explorer

## 🔄 Maintenance

### Regular Tasks

1. **Monitor device uptime**
2. **Check fee collection**
3. **Update whitelist as needed**
4. **Backup contract data**
5. **Monitor for software updates**

### Upgrades

- Contract upgrades require redeployment
- Update QR codes if contract address changes
- Notify users of any changes
- Test thoroughly before production use

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review contract code and comments
3. Test on local/testnet environment
4. Check network status and connectivity
