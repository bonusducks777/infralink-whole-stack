# 🔗 InfraLink

**Decentralized IoT device access through blockchain payments**

Bridge the gap between Web3 and real-world hardware. Pay with crypto, control actual devices.

## 🎯 What is InfraLink?

InfraLink transforms IoT device access through blockchain technology. Device owners can monetize their hardware by accepting crypto payments for time-based access, while users get seamless device control through Web3 wallets.

**Real devices. Real control. Real blockchain integration.**

## ✨ Features

### 🔐 Smart Contract Access Control
- Device activation through blockchain payments
- Session-based access with automatic expiration
- Owner controls with force deactivation
- Multi-chain compatibility

### 💰 Flexible Payment System
- ERC20 tokens or native cryptocurrency
- Time-based billing (pay per second)
- Whitelisted users with custom rates
- Automatic session management

### 📱 Web3 Interface
- Mobile-first React application
- QR code scanning for device discovery
- Multi-wallet support (MetaMask, WalletConnect, etc.)
- Real-time device status monitoring

### 🎛️ Device Monitor & Control
- Desktop Python GUI for device owners
- Real-time blockchain state monitoring
- Network switching with dropdown selection
- Customizable device payloads

### � Multi-Chain Support
- **Ethereum** (Mainnet, Sepolia)
- **Hedera Testnet** (HBAR native payments)
- **Flow EVM** (Mainnet, Testnet)
- **Zircuit** (Mainnet, Garfield Testnet)
- **Polygon**, **Optimism**, **Arbitrum**, **Base**

### 🔗 Centralized User Registry
- Info contract for unified user management
- Cross-device whitelist sharing
- User profiles with names and metadata
- Single source of truth for permissions

## 🛠️ Architecture

### Smart Contracts
- **Device Contract** - Individual device access control and payments
- **Info Contract** - Centralized user registry and whitelist management
- **Solidity** - EVM-compatible smart contract development
- **Multi-chain deployment** - Same contracts across different networks

### Web Application
- **React 18** + **TypeScript** - Modern frontend development
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** + **shadcn/ui** - Beautiful, responsive design
- **Privy** - Web3 authentication with email/SMS support
- **wagmi** + **viem** - Ethereum React hooks and utilities
- **Tanstack Query** - Smart data fetching and caching

### Device Monitor
- **Python 3.8+** - Cross-platform hardware monitoring
- **Web3.py** - Multi-chain blockchain integration
- **Tkinter** - Native GUI interface
- **Modular payload system** - Customizable device control

### Network Utilities
- **Unified RPC management** - Single interface for all chains
- **Smart fee calculation** - Chain-specific decimal handling
- **Currency formatting** - Native token display (ETH, HBAR, etc.)
- **Network detection** - Automatic chain configuration

## 🚀 Quick Start

### 1. Deploy Smart Contracts
```bash
# Deploy to your preferred network
# Supported: Ethereum, Hedera, Flow EVM, Zircuit

# Deploy Info contract (central registry)
# Deploy Device contract for each device
# Update contract addresses in both webapp and Python monitor
```

### 2. Run Web Application
```bash
cd infralink-webapp
npm install
npm run dev
# Visit http://localhost:5173
```

### 3. Set up Device Monitor
```bash
# Install Python dependencies
pip install web3 tk pygame

# Configure network and contracts in devicelocal.py
python devicelocal.py
```

### 4. Customize Device Control
```bash
# Edit devicepayload.py for your hardware
# Add your enable/disable commands
# Test with: python devicepayload.py test-enable
```

## 🏗️ Project Structure

```
InfraLink/
├── 📄 Smart Contracts
│   ├── devicecontract.sol           # Device access control
│   └── infralink-info.sol           # User registry
├── 🖥️ Device Monitor
│   ├── devicelocal.py               # GUI monitor
│   ├── devicepayload.py             # Hardware control
│   └── network_utils.py             # Multi-chain utilities
├── 🌐 Web Application
│   └── infralink-webapp/
│       ├── src/
│       │   ├── components/
│       │   │   ├── DeviceDashboard.tsx      # Device control interface
│       │   │   ├── DeviceScanner.tsx        # QR code scanning
│       │   │   ├── WalletConnection.tsx     # Web3 authentication
│       │   │   └── ui/                      # Component library
│       │   ├── pages/
│       │   │   ├── Index.tsx                # Main app page
│       │   │   └── NotFound.tsx             # 404 page
│       │   └── hooks/                       # Custom React hooks
│       └── package.json
├── 📚 Documentation
│   ├── HOW_ITS_MADE.md              # Technical deep dive
│   ├── DEVICE_SETUP.md              # Hardware integration guide
│   └── README.md                    # This file
└── 📋 Configuration
    └── project.txt                  # Project overview
```

## 🔧 Core Components

### Device Contract
- **`activate(duration)`** - Pay for device access
- **`deactivate()`** - End session early
- **`getDeviceInfo()`** - Get device status and user info
- **`setFee(regular, whitelist)`** - Update pricing
- **`withdrawFees()`** - Collect payments

### Info Contract
- **`getAllRegisteredUsers()`** - Get registered user list
- **`registerUser(name, metadata)`** - Register new user
- **`updateUserProfile(name, metadata)`** - Update user info
- **`checkUserRegistration(address)`** - Verify user status

### Web Interface
- **Device Scanner** - QR code scanning and manual entry
- **Device Dashboard** - Real-time control and monitoring
- **User Management** - View registered users
- **Wallet Integration** - Multi-chain wallet connection
- **Session Management** - Active session monitoring

### Device Monitor
- **Real-time Status** - Live blockchain state monitoring
- **Network Switching** - Easy chain selection
- **Payload System** - Customizable device control
- **GUI Interface** - Desktop monitoring dashboard

## 🎮 Usage Flow

### For Users
1. **Connect Wallet** - Web3 authentication via Privy
2. **Register Profile** - Create user profile in Info contract
3. **Find Device** - Scan QR code or enter contract address
4. **Pay & Access** - Pay with crypto for device time
5. **Control Device** - Use device for purchased duration

### For Device Owners
1. **Deploy Contracts** - Deploy Device and Info contracts
2. **Set up Monitor** - Configure Python monitoring script
3. **Customize Control** - Edit payload script for hardware
4. **Generate QR Code** - Create access codes for users
5. **Manage Device** - Monitor usage and collect payments

## 🌍 Network Configuration

### Supported Networks
| Network | Chain ID | Native Token | RPC Endpoint |
|---------|----------|--------------|--------------|
| Ethereum Mainnet | 1 | ETH | `https://mainnet.infura.io/v3/...` |
| Ethereum Sepolia | 11155111 | ETH | `https://sepolia.infura.io/v3/...` |
| Hedera Testnet | 296 | HBAR | `https://testnet.hashio.io/api` |
| Flow EVM Mainnet | 747 | FLOW | `https://mainnet.evm.nodes.onflow.org` |
| Flow EVM Testnet | 545 | FLOW | `https://testnet.evm.nodes.onflow.org` |
| Zircuit Mainnet | 48900 | ETH | `https://zircuit1-mainnet.p2pify.com` |
| Zircuit Testnet | 48899 | ETH | `https://zircuit1-testnet.p2pify.com` |

### Network Switching
- **Webapp**: Automatic chain detection with Privy
- **Python Monitor**: Dropdown selection in GUI
- **Unified Config**: Single source for all network settings

## 🔐 Security Features

### Smart Contract Security
- **Access Control** - Only active session holders can use devices
- **Time Limits** - Automatic session expiration
- **Owner Controls** - Force deactivation capabilities
- **Event Logging** - Complete audit trail

### Payment Security
- **Token Approval** - Explicit spending approval required
- **Whitelist Management** - Trusted user access control
- **Fee Validation** - Prevent overpayment attacks
- **Withdrawal Protection** - Owner-only fund access

### Network Security
- **Multi-chain Validation** - Chain-specific transaction validation
- **RPC Redundancy** - Multiple endpoint fallbacks
- **Error Handling** - Comprehensive error reporting
- **Rate Limiting** - Prevent spam attacks

## 🧪 Testing & Development

### Local Development
```bash
# 1. Start local blockchain
npx hardhat node
# or
ganache-cli

# 2. Deploy contracts
# Update contract addresses in both webapp and Python

# 3. Run applications
cd infralink-webapp && npm run dev
python devicelocal.py
```

### Testnet Deployment
```bash
# 1. Get testnet tokens
# - Ethereum Sepolia: https://sepoliafaucet.com
# - Hedera Testnet: https://portal.hedera.com
# - Flow EVM Testnet: https://testnet-faucet.onflow.org

# 2. Deploy contracts
# 3. Update addresses in config files
# 4. Test full user flow
```

### Hardware Integration
```bash
# 1. Edit devicepayload.py
# 2. Add your device control commands
# 3. Test payload execution
python devicepayload.py test-enable
python devicepayload.py test-disable

# 4. Run monitor and test end-to-end
python devicelocal.py
```

## 📊 Contract Events

### Device Contract Events
- **`DeviceActivated`** - User starts session
  - `user` - Session holder address
  - `duration` - Session length in seconds
  - `endsAt` - Session expiration timestamp
  - `isWhitelisted` - User whitelist status
  - `paidAmount` - Payment amount

- **`DeviceDeactivated`** - Session ends
  - `user` - Session holder address
  - `wasWhitelisted` - User whitelist status

- **`FeeChanged`** - Owner updates pricing
  - `regularFee` - New regular user fee
  - `whitelistFee` - New whitelist user fee

### Info Contract Events
- **`UserRegistered`** - New user registration
- **`UserUpdated`** - User profile modification
- **`WhitelistUpdated`** - Whitelist changes

## 🛡️ Error Handling

### Common Issues & Solutions
| Error | Cause | Solution |
|-------|-------|----------|
| Device Busy | Another user has active session | Wait for session to expire |
| Insufficient Balance | Not enough tokens/ETH | Add funds to wallet |
| Insufficient Allowance | Token approval needed | Approve token spending |
| Network Mismatch | Wrong blockchain selected | Switch to correct network |
| Contract Not Found | Invalid contract address | Verify contract deployment |
| RPC Error | Network connectivity issues | Check internet connection |

### Development Debugging
```bash
# Enable debug logging in Python
export DEBUG=true
python devicelocal.py

# Check webapp console for errors
# Open browser DevTools -> Console

# Verify contract deployment
# Check block explorer for contract address
```

## 🔮 Roadmap & Future Features

### Phase 1: Core Platform ✅
- [x] Multi-chain smart contracts
- [x] Web3 authentication
- [x] Device monitoring
- [x] Payment processing
- [x] User registry

### Phase 2: Enhanced Features 🚧
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Subscription models
- [ ] Bulk device management
- [ ] API for third-party integrations

### Phase 3: IoT Ecosystem 🔮
- [ ] Device SDK for easy integration
- [ ] Marketplace for device services
- [ ] Advanced automation and scheduling
- [ ] Machine learning for usage optimization
- [ ] Cross-platform device control

### Phase 4: Enterprise 🚀
- [ ] White-label solutions
- [ ] Enterprise-grade security
- [ ] Regulatory compliance tools
- [ ] Advanced reporting and analytics
- [ ] Custom blockchain deployments

## 🤝 Contributing

### Development Setup
```bash
# Fork and clone repository
git clone https://github.com/yourusername/InfraLink.git
cd InfraLink

# Install dependencies
cd infralink-webapp
npm install

# Python dependencies
pip install -r requirements.txt
```

### Code Style
- **TypeScript**: Follow prettier and eslint rules
- **Python**: Follow PEP 8 standards
- **Solidity**: Follow Solidity style guide
- **Documentation**: Update README and inline comments

### Pull Request Process
1. Create feature branch from `main`
2. Make changes with comprehensive tests
3. Update documentation
4. Submit PR with detailed description
5. Pass code review and CI checks

## 🆘 Support & Community

### Documentation
- **[Technical Deep Dive](HOW_ITS_MADE.md)** - Architecture details
- **[Device Setup Guide](DEVICE_SETUP.md)** - Hardware integration
- **[Project Overview](project.txt)** - High-level summary

### Community
- **GitHub Issues** - Bug reports and feature requests
- **Discussions** - Community Q&A and ideas
- **Discord** - Real-time community chat (coming soon)

### Commercial Support
- **Custom Development** - Tailored solutions
- **Enterprise Deployment** - White-label implementations
- **Consulting Services** - Architecture and integration

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Ethereum Foundation** - For the foundational blockchain technology
- **OpenZeppelin** - For secure smart contract libraries
- **React Team** - For the amazing frontend framework
- **Privy** - For seamless Web3 authentication
- **All Contributors** - For making InfraLink better

---

**InfraLink** - Bridging Web3 and IoT, one device at a time 🌉

*Built with ❤️ for the decentralized future*
