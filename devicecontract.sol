// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);
    function name() external view returns (string memory);
    function symbol() external view returns (string memory);
    function decimals() external view returns (uint8);
}

contract DeviceAccess {
    address public owner;
    address public token; // If address(0), uses native token (ETH)
    string public tokenName;
    string public tokenSymbol;
    uint8 public tokenDecimals;
    uint256 public feePerSecond;
    uint256 public whitelistFeePerSecond;
    string public deviceName;
    string public deviceDescription;
    bool public useNativeToken; // True if using ETH, false if using ERC20
    
    address public lastActivatedBy;
    uint256 public sessionEndsAt;
    bool public isActive;
    bool public lastUserWasWhitelisted;

    mapping(address => bool) public whitelist;
    mapping(address => string) public whitelistNames;
    address[] public whitelistAddresses;
    uint256 public whitelistCount;

    event DeviceActivated(address indexed user, uint256 duration, uint256 endsAt, bool isWhitelisted, uint256 paidAmount);
    event DeviceDeactivated(address indexed user, bool wasWhitelisted);
    event FeeChanged(uint256 newFee, uint256 newWhitelistFee);
    event WhitelistUpdated(address indexed user, bool status, string name);
    event DeviceInfoUpdated(string name, string description);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor(
        address _token, 
        uint256 _feePerSecond, 
        uint256 _whitelistFeePerSecond,
        string memory _deviceName,
        string memory _deviceDescription
    ) {
        owner = msg.sender;
        token = _token;
        feePerSecond = _feePerSecond;
        whitelistFeePerSecond = _whitelistFeePerSecond;
        deviceName = _deviceName;
        deviceDescription = _deviceDescription;
        
        // Check if using native token
        useNativeToken = (_token == address(0));
        
        if (useNativeToken) {
            // Detect network and set appropriate native token info
            if (block.chainid == 296) {
                // Hedera testnet
                tokenName = "HBAR";
                tokenSymbol = "HBAR";
                tokenDecimals = 8; // HBAR has 8 decimal places (tinybars)
            } else if (block.chainid == 295) {
                // Hedera mainnet
                tokenName = "HBAR";
                tokenSymbol = "HBAR";
                tokenDecimals = 8;
            } else {
                // Ethereum or other EVM networks
                tokenName = "Ether";
                tokenSymbol = "ETH";
                tokenDecimals = 18;
            }
        } else {
            // Get token information
            try IERC20(token).name() returns (string memory name) {
                tokenName = name;
            } catch {
                tokenName = "Unknown Token";
            }
            
            try IERC20(token).symbol() returns (string memory symbol) {
                tokenSymbol = symbol;
            } catch {
                tokenSymbol = "UNK";
            }
            
            try IERC20(token).decimals() returns (uint8 decimals) {
                tokenDecimals = decimals;
            } catch {
                tokenDecimals = 18;
            }
        }
    }

    function activate(uint256 secondsToActivate) external payable {
        require(secondsToActivate > 0, "Invalid time");
        require(!isActive || block.timestamp >= sessionEndsAt, "Device is busy");

        bool userIsWhitelisted = whitelist[msg.sender];
        uint256 cost = userIsWhitelisted ? whitelistFeePerSecond * secondsToActivate : feePerSecond * secondsToActivate;
        
        if (cost > 0) {
            if (useNativeToken) {
                string memory currencyName = tokenSymbol;
                require(msg.value >= cost, string(abi.encodePacked("Insufficient ", currencyName, " sent")));
                
                // Refund excess native token
                if (msg.value > cost) {
                    payable(msg.sender).transfer(msg.value - cost);
                }
            } else {
                require(msg.value == 0, "Native token sent but ERC20 token required");
                require(IERC20(token).allowance(msg.sender, address(this)) >= cost, "Insufficient allowance");
                require(IERC20(token).balanceOf(msg.sender) >= cost, "Insufficient balance");
                IERC20(token).transferFrom(msg.sender, address(this), cost);
            }
        } else {
            require(msg.value == 0, "Native token sent but access is free");
        }

        lastActivatedBy = msg.sender;
        sessionEndsAt = block.timestamp + secondsToActivate;
        isActive = true;
        lastUserWasWhitelisted = userIsWhitelisted;

        emit DeviceActivated(msg.sender, secondsToActivate, sessionEndsAt, userIsWhitelisted, cost);
    }

    function deactivate() external {
        require(isActive, "Device not active");
        // Allow manual deactivation by current user or when session expires
        require(msg.sender == lastActivatedBy || block.timestamp >= sessionEndsAt, "Not authorized");

        isActive = false;
        emit DeviceDeactivated(lastActivatedBy, lastUserWasWhitelisted);
    }
    
    function forceDeactivate() external onlyOwner {
        require(isActive, "Device not active");
        isActive = false;
        emit DeviceDeactivated(lastActivatedBy, lastUserWasWhitelisted);
    }

    function getDeviceInfo(address user) external view returns (
        uint256 _feePerSecond,
        bool _isActive,
        address _lastActivatedBy,
        uint256 _sessionEndsAt,
        address _token,
        bool _isWhitelisted,
        uint256 _timeRemaining,
        string memory _tokenName,
        string memory _tokenSymbol,
        uint8 _tokenDecimals
    ) {
        _feePerSecond = whitelist[user] ? whitelistFeePerSecond : feePerSecond;
        _isActive = isActive && block.timestamp < sessionEndsAt;
        _lastActivatedBy = lastActivatedBy;
        _sessionEndsAt = sessionEndsAt;
        _token = token;
        _isWhitelisted = whitelist[user];
        _timeRemaining = sessionEndsAt > block.timestamp ? sessionEndsAt - block.timestamp : 0;
        _tokenName = tokenName;
        _tokenSymbol = tokenSymbol;
        _tokenDecimals = tokenDecimals;
    }

    function getDeviceDetails() external view returns (
        string memory _deviceName,
        string memory _deviceDescription,
        bool _useNativeToken,
        bool _lastUserWasWhitelisted,
        uint256 _whitelistFeePerSecond
    ) {
        _deviceName = deviceName;
        _deviceDescription = deviceDescription;
        _useNativeToken = useNativeToken;
        _lastUserWasWhitelisted = lastUserWasWhitelisted;
        _whitelistFeePerSecond = whitelistFeePerSecond;
    }

    function getUserWhitelistInfo(address user) external view returns (
        string memory _whitelistName,
        bool _isWhitelisted,
        uint256 _applicableFee
    ) {
        _whitelistName = whitelistNames[user];
        _isWhitelisted = whitelist[user];
        _applicableFee = whitelist[user] ? whitelistFeePerSecond : feePerSecond;
    }

    function setFee(uint256 _fee, uint256 _whitelistFee) external onlyOwner {
        feePerSecond = _fee;
        whitelistFeePerSecond = _whitelistFee;
        emit FeeChanged(_fee, _whitelistFee);
    }

    function setWhitelistFee(uint256 _fee) external onlyOwner {
        whitelistFeePerSecond = _fee;
        emit FeeChanged(feePerSecond, _fee);
    }

    function setToken(address _token) external onlyOwner {
        token = _token;
        
        // Update token type
        useNativeToken = (_token == address(0));
        
        if (useNativeToken) {
            tokenName = "Ether";
            tokenSymbol = "ETH";
            tokenDecimals = 18;
        } else {
            // Update token information
            try IERC20(token).name() returns (string memory name) {
                tokenName = name;
            } catch {
                tokenName = "Unknown Token";
            }
            
            try IERC20(token).symbol() returns (string memory symbol) {
                tokenSymbol = symbol;
            } catch {
                tokenSymbol = "UNK";
            }
            
            try IERC20(token).decimals() returns (uint8 decimals) {
                tokenDecimals = decimals;
            } catch {
                tokenDecimals = 18;
            }
        }
    }

    function setWhitelist(address user, bool status, string memory name) external onlyOwner {
        bool wasWhitelisted = whitelist[user];
        whitelist[user] = status;
        
        if (status) {
            whitelistNames[user] = name;
            if (!wasWhitelisted) {
                whitelistAddresses.push(user);
                whitelistCount++;
            }
        } else {
            delete whitelistNames[user];
            if (wasWhitelisted) {
                // Remove from array (expensive operation, but whitelist should be small)
                for (uint i = 0; i < whitelistAddresses.length; i++) {
                    if (whitelistAddresses[i] == user) {
                        whitelistAddresses[i] = whitelistAddresses[whitelistAddresses.length - 1];
                        whitelistAddresses.pop();
                        whitelistCount--;
                        break;
                    }
                }
            }
        }
        
        emit WhitelistUpdated(user, status, name);
    }

    function setDeviceInfo(string memory _name, string memory _description) external onlyOwner {
        deviceName = _name;
        deviceDescription = _description;
        emit DeviceInfoUpdated(_name, _description);
    }

    function getWhitelistInfo() external view returns (
        address[] memory addresses,
        string[] memory names,
        uint256 count
    ) {
        addresses = whitelistAddresses;
        names = new string[](whitelistAddresses.length);
        
        for (uint i = 0; i < whitelistAddresses.length; i++) {
            names[i] = whitelistNames[whitelistAddresses[i]];
        }
        
        count = whitelistCount;
    }

    function transferOwnership(address newOwner) external onlyOwner {
        owner = newOwner;
    }
    
    function withdrawFees() external onlyOwner {
        if (useNativeToken) {
            uint256 balance = address(this).balance;
            require(balance > 0, "No ETH to withdraw");
            payable(owner).transfer(balance);
        } else {
            uint256 balance = IERC20(token).balanceOf(address(this));
            require(balance > 0, "No fees to withdraw");
            IERC20(token).transfer(owner, balance);
        }
    }
}
