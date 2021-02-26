from typing import Any
import block.block as block
import hashlib
import base64
import json

JushCoinSig = "1f60deedb323271b360bbcb58743f120904a00ca7b4b37ac81120c7c32c16ef4"


class BlockChain:
    def __init__(self, universe: Any,  miner: str, newID: str):
        """
        __init__: Init new blockchain.

        Args:
            universe (Any): Universe class.
            miner (str): Miner address.
            newID (str): ID of the blockchain.
        """

        self.confirmed = False
        self.miner = miner  # Address
        self.chain = dict({})  # Unconfirmed Transactions

        self.difficulty = 8
        self.reward = 0

        self.limit = universe.supply
        self.split = universe.reward
        self.chainID = newID

        self.createGenesis()

    @property
    def lastBlock(self):
        """
        lastBlock: Get last block.

        Returns:
            self: self
        """

        try:
            lastKey = list(self.chain.keys())[-1]
            last = self.chain[int(lastKey)]
        except IndexError:
            last = "No Genesis"

        return last

    def createGenesis(self):
        """
        createGenesis: Create Genesis block.
        """

        if len(self.chain.keys()) == 0:
            hash = block.Block(self.miner, self, "0").getInfo()["hash"]
            self.chain[0] = hashlib.sha256(str(hash).encode()).hexdigest()

    def getChain(self):
        """
        getChain Returns self but encoded as base64.

        Returns:
            str: Base64 encode.
        """

        return base64.b64encode(str(json.dumps(self.__dict__, sort_keys=True)).encode())

    def verify(self, block: block.Block, hash: str) -> bool:
        """
        verify: Verify block.

        Args:
            block (block): Block
            hash (str): hash of the block.

        Returns:
            bool: Returns whether it meets the criteria.
        """

        if block.mined:
            rewardHash = hashlib.sha256(str(block.reward).encode()).hexdigest()

            difficulty = hash.startswith("0"*self.difficulty)
            checkReward = rewardHash == hash[66:]

            return bool(difficulty and checkReward)

        return False

    def addBlock(self, block: block.Block, hash: str, verifiedHash: str) -> bool:
        """
        addBlock: Add block to the confirmed chains.

        Args:
            block (block): Block.
            hash (str): Hash of the block.
            verifiedHash (str): Verified hash.

        Returns:
            bool: True if verified, False if unable to mine block.
        """
        if self.verify(block, hash):
            self.chain[len(self.chain)] = verifiedHash
            print(f"1 Block Mined.\n\tReward: {block.reward}\n\tNonce: {block.nonce}")
            return True

        print("Unable to add block.")
        return False

    def proofWork(self, block: block.Block) -> Any:
        """
        proofWork: Proof of work algorithm.

        Args:
            block (block): block.Block to be mined.

        Returns:
            Any: Returns block hash or "Save Session".
        """

        computedHash = block.computeHash()
        blockHash = ""

        print("Highest Difficulty Achieved: ", block.highestDifficulty)
        print("Mining...")

        try:
            while not self.verify(block, blockHash):
                block.mined = True
                computedHash = block.computeHash()

                blockHash = computedHash+"74"+hashlib.sha256(str(block.reward).encode()).hexdigest()

                if len(blockHash)-len(blockHash.lstrip("0")) > block.highestDifficulty:
                    block.highestDifficulty = len(blockHash)-len(blockHash.lstrip("0"))
                    print(f"Mining Block: \n\tID: {block.index}\n\tNonce: {block.nonce}\n\tHash: {blockHash[:self.difficulty]}\n\tHighest Difficulty: {block.highestDifficulty}")

                block.nonce += 1

            return blockHash
        except KeyboardInterrupt:
            print("Save Session...")
            return "Save Session"

    def mine(self, load: bool = False, **kwargs) -> Any:
        if load:
            newBlock = kwargs["block"]
        else:
            newBlock = block.Block(self.miner, self, str(len(self.chain.keys())))

        proof = self.proofWork(newBlock)

        if proof == "Save Session":
            session = newBlock.__dict__
            return session

        elif proof != False:
            # Generate Verified Hash
            lastBlockHash = newBlock.lastBlock
            blockSignature = newBlock.blockSignature

            verifiedBlockHash = hashlib.sha256(str(lastBlockHash + blockSignature).encode()).hexdigest()

            self.addBlock(newBlock, proof, verifiedBlockHash)
            self.reward += newBlock.reward
            return True

        print("Unable to mine block.")
        return False


def createDummyBlock(chain: BlockChain):
    """
    createDummyBlock Create Dummy Block using chain.

    Args:
        chain (BlockChain): Blockchain

    Returns:
        block: block.Blockclass
    """
    return block.Block("", chain, "")
