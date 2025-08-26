import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from web3 import Web3
from web3.middleware import geth_poa_middleware


ABI_PATH = "/workspace/dsps/backend/app/services/blockchain/abi/DSPSkillProof.json"


@dataclass
class ChainConfig:
	provider_url: str
	contract_address: str
	private_key: str


class DSPSBlockchainClient:
	def __init__(self, provider_url: str, contract_address: str, private_key: str) -> None:
		self.web3 = Web3(Web3.HTTPProvider(provider_url))
		# Add middleware for testnets like Polygon Mumbai (POA chains)
		self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
		self.contract_address = Web3.to_checksum_address(contract_address)
		self.private_key = private_key
		self.account = self.web3.eth.account.from_key(private_key)
		abi = json.loads(Path(ABI_PATH).read_text())
		self.contract = self.web3.eth.contract(address=self.contract_address, abi=abi)

	@staticmethod
	def from_env() -> "DSPSBlockchainClient":
		provider = os.getenv("WEB3_PROVIDER_URL")
		addr = os.getenv("CONTRACT_ADDRESS")
		pk = os.getenv("CONTRACT_PRIVATE_KEY")
		if not provider or not addr or not pk:
			raise ValueError("WEB3_PROVIDER_URL, CONTRACT_ADDRESS, and CONTRACT_PRIVATE_KEY must be set")
		return DSPSBlockchainClient(provider, addr, pk)

	def add_record(self, user_address: str, skill: str, score: int, timestamp: int) -> str:
		user = Web3.to_checksum_address(user_address)
		nonce = self.web3.eth.get_transaction_count(self.account.address)
		chain_id = self.web3.eth.chain_id
		tx = self.contract.functions.addRecord(user, skill, int(score), int(timestamp)).build_transaction({
			"from": self.account.address,
			"nonce": nonce,
			"chainId": chain_id,
			"gas": 400000,
			"maxFeePerGas": self.web3.to_wei("3", "gwei"),
			"maxPriorityFeePerGas": self.web3.to_wei("1", "gwei"),
		})
		signed = self.account.sign_transaction(tx)
		tx_hash = self.web3.eth.send_raw_transaction(signed.rawTransaction)
		receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
		return tx_hash.hex()

	def get_records(self, user_address: str) -> List[Dict[str, Any]]:
		user = Web3.to_checksum_address(user_address)
		records = self.contract.functions.getRecords(user).call()
		# records is a list of tuples
		return [
			{
				"user": r[0],
				"skill": r[1],
				"score": int(r[2]),
				"timestamp": int(r[3]),
			}
			for r in records
		]