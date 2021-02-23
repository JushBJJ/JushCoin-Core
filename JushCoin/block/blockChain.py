import block.block as block
import hashlib
import base64
import json


class BlockChain:
    def __init__(self, universe,  miner, newID: str):
        self.JushCoinSig = "1f60deedb323271b360bbcb58743f120904a00ca7b4b37ac81120c7c32c16ef4"
        self.confirmed = False
        self.chain = dict({})  # Unconfirmed Transactions
        self.difficulty = 15
        self.limit = universe.supply
        self.split = universe.reward
        self.chainID = newID
        self.miner = miner  # Address
        self.reward = 0

        self.createGenesis()

    @property
    def lastBlock(self):
        try:
            lastKey = list(self.chain.keys())[-1]
            last = self.chain[int(lastKey)]
        except IndexError:
            last = "No Genesis"

        return last

    def createGenesis(self):
        if len(self.chain.keys()) == 0:
            hash = block.Block(self.miner, self, "0").getInfo()["hash"]
            self.chain[0] = hashlib.sha256(str(hash).encode()).hexdigest()

    def getChain(self):
        return base64.b64encode(str(json.dumps(self.__dict__, sort_keys=True)).encode())

    def verify(self, block, hash):
        if block.mined:
            rewardHash = hashlib.sha256(str(block.reward).encode()).hexdigest()

            difficulty = hash.startswith("0"*self.difficulty)
            checkReward = rewardHash == hash[66:]

            return difficulty and checkReward

        return False

    def addBlock(self, block, hash, verifiedHash):
        if self.verify(block, hash):
            self.chain[len(self.chain)] = verifiedHash
            print(f"1 Block Mined.\n\tReward: {block.reward}\n\tNonce: {block.nonce}")
            return True

        print("Unable to add block.")
        return False

    def proofWork(self, block):
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

    def mine(self, load=False, **kwargs):
        if load:
            newBlock = kwargs["block"]
        else:
            newBlock = block.Block(self.miner, self, str(len(self.chain.keys())))

        proof = self.proofWork(newBlock)

        if proof == "Save Session":
            session = json.dumps(newBlock.__dict__)
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


def createDummyBlock(chain):
    return block.Block(None, chain, "")
