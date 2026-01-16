"""
Crypto Wallet Handler Module
Manages wallet operations for Ethereum and Solana
"""

import os
import logging
from typing import Dict, Any, Optional
from decimal import Decimal

logger = logging.getLogger(__name__)


class WalletHandler:
    """Handles crypto wallet operations for ETH and SOL"""

    def __init__(self):
        """Initialize wallet handlers"""
        self.eth_wallet = None
        self.sol_wallet = None
        self.enabled = False

        try:
            # Initialize Ethereum wallet
            try:
                from web3 import Web3

                # Get configuration
                eth_rpc = os.getenv('ETH_RPC_URL', 'https://eth.llamarpc.com')
                eth_private_key = os.getenv('ETH_PRIVATE_KEY')

                if eth_private_key:
                    self.w3 = Web3(Web3.HTTPProvider(eth_rpc))

                    # Load account from private key
                    self.eth_account = self.w3.eth.account.from_key(eth_private_key)
                    self.eth_address = self.eth_account.address

                    logger.info(f"✅ Ethereum wallet initialized: {self.eth_address[:10]}...")
                    self.eth_wallet = True
                else:
                    logger.warning("⚠️  ETH_PRIVATE_KEY not set. Ethereum wallet disabled.")
                    self.eth_wallet = False

            except ImportError:
                logger.warning("web3.py not installed. Ethereum wallet disabled.")
                self.eth_wallet = False
            except Exception as e:
                logger.error(f"Error initializing Ethereum wallet: {e}")
                self.eth_wallet = False

            # Initialize Solana wallet
            try:
                from solders.keypair import Keypair
                from solana.rpc.api import Client

                sol_rpc = os.getenv('SOL_RPC_URL', 'https://api.mainnet-beta.solana.com')
                sol_private_key = os.getenv('SOL_PRIVATE_KEY')

                if sol_private_key:
                    self.sol_client = Client(sol_rpc)

                    # Load keypair from private key (base58 encoded)
                    import base58
                    private_key_bytes = base58.b58decode(sol_private_key)
                    self.sol_keypair = Keypair.from_bytes(private_key_bytes)
                    self.sol_address = str(self.sol_keypair.pubkey())

                    logger.info(f"✅ Solana wallet initialized: {self.sol_address[:10]}...")
                    self.sol_wallet = True
                else:
                    logger.warning("⚠️  SOL_PRIVATE_KEY not set. Solana wallet disabled.")
                    self.sol_wallet = False

            except ImportError:
                logger.warning("solana-py not installed. Solana wallet disabled.")
                self.sol_wallet = False
            except Exception as e:
                logger.error(f"Error initializing Solana wallet: {e}")
                self.sol_wallet = False

            self.enabled = self.eth_wallet or self.sol_wallet

            if not self.enabled:
                logger.info("💡 Using mock wallet mode")

        except Exception as e:
            logger.error(f"Error initializing wallet handler: {e}")
            self.enabled = False

    def get_eth_balance(self) -> Optional[float]:
        """Get Ethereum balance in ETH"""
        if not self.eth_wallet:
            return None

        try:
            balance_wei = self.w3.eth.get_balance(self.eth_address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            logger.debug(f"ETH balance: {balance_eth}")
            return float(balance_eth)

        except Exception as e:
            logger.error(f"Error getting ETH balance: {e}")
            return None

    def get_sol_balance(self) -> Optional[float]:
        """Get Solana balance in SOL"""
        if not self.sol_wallet:
            return None

        try:
            response = self.sol_client.get_balance(self.sol_keypair.pubkey())
            balance_lamports = response.value
            balance_sol = balance_lamports / 1_000_000_000  # Convert lamports to SOL
            logger.debug(f"SOL balance: {balance_sol}")
            return balance_sol

        except Exception as e:
            logger.error(f"Error getting SOL balance: {e}")
            return None

    def get_status(self) -> Dict[str, Any]:
        """Get overall wallet status"""
        status = {
            'enabled': self.enabled,
            'eth': {
                'enabled': bool(self.eth_wallet),
                'address': self.eth_address[:10] + "..." if self.eth_wallet else None,
                'balance': None
            },
            'sol': {
                'enabled': bool(self.sol_wallet),
                'address': self.sol_address[:10] + "..." if self.sol_wallet else None,
                'balance': None
            },
            'total_value_usd': 0.0
        }

        # Get balances
        if self.eth_wallet:
            status['eth']['balance'] = self.get_eth_balance()

        if self.sol_wallet:
            status['sol']['balance'] = self.get_sol_balance()

        # Mock USD value calculation (in production, fetch from price API)
        if status['eth']['balance']:
            status['total_value_usd'] += status['eth']['balance'] * 3000  # Mock ETH price

        if status['sol']['balance']:
            status['total_value_usd'] += status['sol']['balance'] * 100  # Mock SOL price

        return status

    def send_eth(self, to_address: str, amount_eth: float) -> Optional[str]:
        """
        Send Ethereum

        Args:
            to_address: Recipient address
            amount_eth: Amount in ETH

        Returns:
            Transaction hash if successful
        """
        if not self.eth_wallet:
            logger.error("Ethereum wallet not enabled")
            return None

        try:
            # Build transaction
            amount_wei = self.w3.to_wei(amount_eth, 'ether')

            transaction = {
                'to': to_address,
                'value': amount_wei,
                'gas': 21000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.eth_address),
                'chainId': self.w3.eth.chain_id
            }

            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.eth_account.key)

            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

            logger.info(f"✅ Sent {amount_eth} ETH to {to_address}")
            logger.info(f"   TX: {tx_hash.hex()}")

            return tx_hash.hex()

        except Exception as e:
            logger.error(f"Error sending ETH: {e}")
            return None

    def send_sol(self, to_address: str, amount_sol: float) -> Optional[str]:
        """
        Send Solana

        Args:
            to_address: Recipient address
            amount_sol: Amount in SOL

        Returns:
            Transaction signature if successful
        """
        if not self.sol_wallet:
            logger.error("Solana wallet not enabled")
            return None

        try:
            from solders.pubkey import Pubkey
            from solders.transaction import Transaction
            from solders.system_program import TransferParams, transfer
            from solders.message import Message

            # Convert SOL to lamports
            amount_lamports = int(amount_sol * 1_000_000_000)

            # Create transfer instruction
            transfer_ix = transfer(
                TransferParams(
                    from_pubkey=self.sol_keypair.pubkey(),
                    to_pubkey=Pubkey.from_string(to_address),
                    lamports=amount_lamports
                )
            )

            # Get recent blockhash
            recent_blockhash = self.sol_client.get_latest_blockhash().value.blockhash

            # Create transaction
            message = Message.new_with_blockhash(
                [transfer_ix],
                self.sol_keypair.pubkey(),
                recent_blockhash
            )
            transaction = Transaction([self.sol_keypair], message, recent_blockhash)

            # Send transaction
            response = self.sol_client.send_transaction(transaction)
            tx_signature = str(response.value)

            logger.info(f"✅ Sent {amount_sol} SOL to {to_address}")
            logger.info(f"   TX: {tx_signature}")

            return tx_signature

        except Exception as e:
            logger.error(f"Error sending SOL: {e}")
            return None

    def get_transaction_history(self, chain: str = 'eth', limit: int = 10) -> list:
        """
        Get transaction history

        Args:
            chain: 'eth' or 'sol'
            limit: Number of transactions

        Returns:
            List of transactions
        """
        # This is a simplified version
        # In production, you'd query blockchain APIs or indexers
        logger.info(f"Transaction history not implemented yet for {chain}")
        return []


class MockWalletHandler(WalletHandler):
    """Mock wallet handler for testing"""

    def __init__(self):
        """Initialize mock wallet"""
        self.enabled = True
        self.eth_wallet = True
        self.sol_wallet = True
        self.eth_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
        self.sol_address = "DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK"

        # Mock balances
        self.mock_eth_balance = 0.5
        self.mock_sol_balance = 10.0

        logger.info("✅ Mock wallet handler initialized")

    def get_eth_balance(self) -> float:
        """Mock ETH balance"""
        return self.mock_eth_balance

    def get_sol_balance(self) -> float:
        """Mock SOL balance"""
        return self.mock_sol_balance

    def send_eth(self, to_address: str, amount_eth: float) -> str:
        """Mock ETH send"""
        logger.info(f"[MOCK] Would send {amount_eth} ETH to {to_address}")
        return "0x" + "1" * 64

    def send_sol(self, to_address: str, amount_sol: float) -> str:
        """Mock SOL send"""
        logger.info(f"[MOCK] Would send {amount_sol} SOL to {to_address}")
        return "5" * 88


if __name__ == "__main__":
    # Test wallet handler
    logging.basicConfig(level=logging.INFO)

    wallet = MockWalletHandler()
    status = wallet.get_status()
    print(f"Wallet status: {status}")
