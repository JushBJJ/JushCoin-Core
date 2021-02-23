import hashlib
import json
import time
import random

# Types:
"""
    d0: Donation from creator
    74: Transaction
"""


class Block:
    def __init__(self, miner, chain, index: str):
        self.index = index
        self.timestamp = time.asctime()+str(time.time())
        self.nonce = 0
        self.mined = False
        self.difficulty = chain.difficulty
        self.miner = miner  # Address
        self.reward = random.randrange(0, chain.split)
        self.lastBlock = chain.lastBlock
        self.highestDifficulty = 0

        self.blockSignature = "1f60deedb323271b360bbcb58743f120904a00ca7b4b37ac81120c7c32c16ef4"

    def computeHash(self):
        block = json.dumps(str(self.__dict__), sort_keys=True)
        return hashlib.sha256(block.encode()).hexdigest()

    def getInfo(self):
        info = dict({
            "local index": self.index,
            "timestamp": self.timestamp,
            "reward": self.reward,
            "difficulty": self.difficulty,
            "miner": self.miner,
            "hash": self.computeHash()
        })
        return info
