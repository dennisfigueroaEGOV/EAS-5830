// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "./BridgeToken.sol";
import "forge-std/console.sol";

contract Destination is AccessControl {
    bytes32 public constant WARDEN_ROLE = keccak256("BRIDGE_WARDEN_ROLE");
    bytes32 public constant CREATOR_ROLE = keccak256("CREATOR_ROLE");
    mapping(address => address) public underlying_tokens;
    mapping(address => address) public wrapped_tokens;
    address[] public tokens;

    event Creation(address indexed underlying_token, address indexed wrapped_token);
    event Wrap(address indexed underlying_token, address indexed wrapped_token, address indexed to, uint256 amount);
    event Unwrap(address indexed underlying_token, address indexed wrapped_token, address frm, address indexed to, uint256 amount);

    constructor(address admin) {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(CREATOR_ROLE, admin);
        _grantRole(WARDEN_ROLE, admin);
        console.log("Contract deployed with admin:", admin);
    }

    function wrap(address _underlying_token, address _recipient, uint256 _amount) public onlyRole(WARDEN_ROLE) {
        console.log("---------------------------------------------------");
        console.log("Wrap function called");
        console.log("Caller:", msg.sender);
        console.log("Underlying token:", _underlying_token);
        console.log("Recipient:", _recipient);
        console.log("Amount:", _amount);

        address wrappedTokenAddress = underlying_tokens[_underlying_token];
        console.log("Wrapped token address:", wrappedTokenAddress);

        require(wrappedTokenAddress != address(0), "Underlying token not registered");
        console.log("Wrapped token address is valid");

        BridgeToken(wrappedTokenAddress).mint(_recipient, _amount);
        console.log("Minted", _amount, "tokens to", _recipient);

        emit Wrap(_underlying_token, wrappedTokenAddress, _recipient, _amount);
        console.log("Wrap event emitted");
        console.log("---------------------------------------------------");
    }

    function unwrap(address _wrapped_token, address _recipient, uint256 _amount) public {
        console.log("---------------------------------------------------");
        console.log("Unwrap function called");
        console.log("Caller:", msg.sender);
        console.log("Wrapped token:", _wrapped_token);
        console.log("Recipient:", _recipient);
        console.log("Amount:", _amount);

        address underlyingTokenAddress = wrapped_tokens[_wrapped_token];
        console.log("Underlying token address:", underlyingTokenAddress);

        require(underlyingTokenAddress != address(0), "Not a valid wrapped token");
        console.log("Underlying token address is valid");

        BridgeToken(_wrapped_token).burnFrom(msg.sender, _amount);
        console.log("Burned", _amount, "tokens from", msg.sender);

        emit Unwrap(underlyingTokenAddress, _wrapped_token, msg.sender, _recipient, _amount);
        console.log("Unwrap event emitted");
        console.log("---------------------------------------------------");
    }

    function createToken(address _underlying_token, string memory name, string memory symbol) public onlyRole(CREATOR_ROLE) returns(address) {
        console.log("---------------------------------------------------");
        console.log("createToken function called");
        console.log("Caller:", msg.sender);
        console.log("Underlying token:", _underlying_token);
        console.log("Name:", name);
        console.log("Symbol:", symbol);

        BridgeToken newToken = new BridgeToken(_underlying_token, name, symbol, address(this));
        console.log("New BridgeToken created at:", address(newToken));

        newToken.grantRole(newToken.MINTER_ROLE(), address(this));
        console.log("MINTER_ROLE granted to this contract");

        address wrappedTokenAddress = address(newToken);

      console.log("Before update - underlying_tokens[_underlying_token]:", underlying_tokens[_underlying_token]);
      underlying_tokens[_underlying_token] = wrappedTokenAddress;
      console.log("After update - underlying_tokens[_underlying_token]:", underlying_tokens[_underlying_token]);

      console.log("Before update - wrapped_tokens[wrappedTokenAddress]:", wrapped_tokens[wrappedTokenAddress]);
      wrapped_tokens[wrappedTokenAddress] = _underlying_token;
      console.log("After update - wrapped_tokens[wrappedTokenAddress]:", wrapped_tokens[wrappedTokenAddress]);

        tokens.push(wrappedTokenAddress);
        console.log("New token added to tokens array");

        require(underlying_tokens[_underlying_token] == wrappedTokenAddress, "Underlying mapping not updated");
        require(wrapped_tokens[wrappedTokenAddress] == _underlying_token, "Wrapped mapping not updated");
        console.log("Mapping checks passed");

        emit Creation(_underlying_token, wrappedTokenAddress);
        console.log("Creation event emitted");

        console.log("Returning wrapped token address:", wrappedTokenAddress);
        console.log("---------------------------------------------------");
        return wrappedTokenAddress;
    }
}
