# 🔗 InfraLink

Open hardware service access via smart contracts — for agents, users, and devices.

## 🎯 Overview

InfraLink enables decentralized access to hardware devices through smart contracts. Users pay with ERC20 tokens for time-based device access, while device owners can monetize their hardware through blockchain-based payments.

## ✨ Features

- **🔐 Smart Contract Access Control**: Secure device access via Ethereum smart contracts
- **💰 Time-Based Billing**: Pay per second with ERC20 tokens or native ETH
- **📱 Mobile-First Web Interface**: Scan QR codes to connect to devices
- **🎛️ Device Monitoring**: Real-time status dashboard for device owners
- **⚡ Advanced Whitelist System**: Named users with custom fees or free access
- **🔄 Session Management**: Extend, monitor, or terminate sessions
- **📊 Comprehensive Device Info**: Token details, pricing, and device descriptions
- **👥 User Management**: View whitelisted users with names and status
- **💳 Smart Fee Display**: Different rates for regular vs whitelisted users
- **🎯 Enhanced UX**: Clear error messages and intuitive interfaces
- **📇 User Profiles**: Create and manage user profiles with InfraLink Info contract
- **🌐 Native Token Support**: Accept both ERC20 tokens and native ETH payments
- **🔗 Centralized Registry**: Manage device whitelist and user access through Info contract
- **⚠️ Smart Error Handling**: Network detection and helpful error messages

## 🛠️ Tech Stack

### Smart Contracts
- **Solidity** - Device access control and payment logic
- **ERC20** - Token-based payments
- **Ethereum** - Blockchain infrastructure

### Web Application
- **React** + **Vite** - Modern web framework
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Component library
- **RainbowKit** - Wallet connection
- **Wagmi** - Ethereum React hooks
- **Ethers.js** - Ethereum interaction

### Device Monitor
- **Python** - Hardware monitoring script
- **Web3.py** - Ethereum integration
- **Tkinter** - GUI interface

## 🚀 Quick Start

1. **Deploy Contracts**
   ```bash
   # Deploy testtoken.sol (optional)
   # Deploy devicecontract.sol with token address and fees
   ```

2. **Run Web App**
   ```bash
   cd infralink-webapp
   npm install
   npm run dev
   ```

3. **Start Device Monitor**
   ```bash
   pip install -r requirements.txt
   python devicelocal.py
   ```

4. **Generate QR Code**
   - Visit `/device-owner` in web app
   - Enter contract address
   - Generate and print QR code

## 📋 Project Structure

```
InfraLink/
├── devicecontract.sol      # Main device access contract
├── infralink-info.sol      # User profiles and whitelist registry
├── testtoken.sol          # Test ERC20 token
├── devicelocal.py         # Device monitoring script
├── requirements.txt       # Python dependencies
├── SETUP.md              # Detailed setup guide
├── USER_GUIDE.md         # v2.0 user guide
└── infralink-webapp/     # Web application
    ├── src/
    │   ├── components/   # React components
    │   │   ├── UserProfile.tsx      # User profile management
    │   │   ├── WhitelistManager.tsx # Device whitelist management
    │   │   └── ...
    │   ├── pages/        # App pages
    │   │   ├── UserProfilePage.tsx  # User profile page
    │   │   └── ...
    │   ├── hooks/        # Custom hooks
    │   └── lib/          # Utility functions
    └── package.json
```

## 🔧 Core Components

### DeviceAccess Contract
- **activate()**: Pay to activate device for specified duration
- **deactivate()**: End session early
- **getDeviceInfo()**: Get comprehensive device status, user info, and whitelist status
- **getWhitelistInfo()**: Get all whitelisted users with their names
- **setFee()**: Owner can adjust both regular and whitelist pricing
- **setWhitelist()**: Manage user whitelist with custom names
- **setDeviceInfo()**: Update device name and description
- **withdrawFees()**: Withdraw collected payments

### Web Interface
- **Device Scanner**: QR code scanning and manual entry
- **Device Dashboard**: Real-time status and payment interface with whitelist info
- **Tabbed Interface**: Device control, info, and whitelist viewer
- **Smart Fee Display**: Shows user-specific fees (regular vs whitelist)
- **Whitelist Viewer**: Browse all whitelisted users with names
- **QR Generator**: Create QR codes for device owners
- **Wallet Integration**: Connect Web3 wallets with clear error handling

### Device Monitor
- **Contract Monitoring**: Real-time device status with enhanced info
- **GUI Display**: Visual status indicators with whitelist status
- **Device Info Tab**: Shows device name, description, and token details
- **Whitelist Tab**: Browse and refresh whitelisted users
- **Fee Display**: Shows regular and whitelist rates with proper formatting
- **Session Tracking**: Countdown timers and user info

## 🎮 Usage Flow

### For Users
1. Connect Web3 wallet
2. Create your user profile via the Profile page
3. Scan device QR code or enter contract address
4. View device info, pricing, and your whitelist status
5. See personalized fee rate (regular or whitelist)
6. Approve token spending (if using ERC20 tokens)
7. Pay for desired duration (ETH or tokens, or use free access if whitelisted)
8. Device activates for specified time
9. Monitor session and extend if needed
10. View your whitelist information and access to all devices

### For Device Owners
1. Deploy DeviceAccess contract with device info, pricing, and payment method (ERC20 or native ETH)
2. Register device with InfraLink Info contract
3. Set up whitelist with user names and custom fees via the web interface
4. Generate QR code with contract address
5. Place QR code on device
6. Run Python monitor script to track usage
7. Manage fees, whitelist, and device settings through the web interface
8. Collect payments and monitor detailed usage statistics

## 🔐 Security Features

- **Access Control**: Only current session holder can use device
- **Time Limits**: Sessions expire automatically
- **Owner Controls**: Device owner can force deactivation
- **Token Approval**: Explicit approval required for payments
- **Event Logging**: All actions logged on blockchain

## 🧪 Testing

### Local Development
```bash
# Start local blockchain (Ganache/Hardhat)
# Deploy contracts to local network
# Run web app and Python monitor
# Test full user flow
```

### Testnet Deployment
```bash
# Deploy to Sepolia/Goerli testnet
# Get testnet ETH and tokens
# Test with real wallet interactions
# Verify contracts on Etherscan
```

## 📊 Contract Events

- **DeviceActivated**: User starts session (includes whitelist status and amount paid)
- **DeviceDeactivated**: Session ends (includes whitelist status)
- **FeeChanged**: Owner updates pricing (regular and whitelist fees)
- **WhitelistUpdated**: User added/removed from whitelist (includes name)
- **DeviceInfoUpdated**: Device name or description changed

## 🛡️ Error Handling

- **Device Busy**: Another user has active session
- **Insufficient Balance**: Not enough tokens for payment
- **Insufficient Allowance**: Token approval required
- **Invalid Duration**: Must be positive number
- **Whitelist Confusion**: Clear display of user's whitelist status and applicable fees
- **Connection Issues**: Network connectivity problems with helpful messages
- **Contract Errors**: Detailed error messages for debugging

## 🔮 Future Enhancements

- **Streaming Payments**: Real-time payment flows
- **Multi-Device Support**: Single contract for multiple devices
- **Analytics Dashboard**: Usage statistics and revenue tracking
- **Mobile App**: Native iOS/Android applications
- **IoT Integration**: Direct device communication protocols
- **Advanced Whitelist Management**: Bulk operations and CSV import/export
- **Subscription Models**: Monthly/yearly access plans
- **Device Categories**: Organize devices by type and location

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## 📞 Support

- **Documentation**: See SETUP.md for detailed instructions
- **Issues**: Report bugs via GitHub issues
- **Questions**: Check existing issues or start discussions

---

**InfraLink** - Democratizing hardware access through blockchain technology 🚀
