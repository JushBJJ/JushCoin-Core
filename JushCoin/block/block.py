import hashlib
import json
import time
import random
from typing import Any, Dict

# Types:
"""
    d0: Donation from creator
    74: Transaction
"""


class Block:
    def __init__(self, miner: str, chain: Any, index: str):
        """
        __init__ Init block.

        Args:
            miner (str): Address of Miner
            chain (Any): Chain Class
            index (str): Block Index/ID
        """
        self.index = index

        self.nonce = 0
        self.highestDifficulty = 0
        self.reward = random.randrange(0, chain.split)

        self.mined = False
        self.miner = miner  # Address

        self.timestamp = time.asctime()+str(time.time())
        self.difficulty = chain.difficulty

        self.lastBlock = chain.lastBlock
        self.blockSignature = "1f60deedb323271b360bbcb58743f120904a00ca7b4b37ac81120c7c32c16ef4"

    def computeHash(self) -> str:
        block = json.dumps(str(self.__dict__), sort_keys=True)
        return hashlib.sha256(block.encode()).hexdigest()

    def getInfo(self) -> Dict[str, Any]:
        info = dict({
            "local index": self.index,
            "timestamp": self.timestamp,
            "reward": self.reward,
            "difficulty": self.difficulty,
            "miner": self.miner,
            "hash": self.computeHash()
        })
        return info
