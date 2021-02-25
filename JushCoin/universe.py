import base64
import json
from typing import Any, Dict
import block.blockChain as blockChain
import block.block as block

JushCoinSig = "1f60deedb323271b360bbcb58743f120904a00ca7b4b37ac81120c7c32c16ef4"


class Universe:
    """
        Universe: Class of the world of JushCoin

        Attributes:
    """

    def __init__(self, name: str):
        # Universe Storage
        self.supply = 10000000
        self.reward = 32
        self.split = 1024

        # Universe confirmed transactions
        self.totalConfirmedTransactions = 0

        # Universe blockchains
        self.blockChains = dict({})
        self.unconfirmedBlockChains = dict({})

        # Universe Info
        self.nextID = 0
        self.name = name

    def save(self):
        """
        save: Save Universe as bas64
        """

        self.unconfirmedBlockChains = dict({})  # Clear unconfirmedBlockChains
        universe = base64.b64encode(json.dumps(str(self.__dict__), sort_keys=True).encode())

        # Overwrite
        with open(f"JC_WORLD_{self.name}.txt", "wb") as f:
            f.write(universe)

    def load(self, filename: str):
        """
        load: Load universe

        Args:
            filename (str): Filename of the universe.
        """

        with open(filename, "rb") as f:
            txt = f.read()
            universe = base64.b64decode(txt.decode()).decode().split("\"")[1]
            universe = universe.replace("\'", "\"")
            universe = json.loads(universe)

            # Load attributes
            for keys in universe.keys():
                if keys in self.__dict__.keys():
                    self.__setattr__(keys,  universe[keys])

    def splitReward(self):
        """
        splitReward: Split reward accordingly.
        """

        if self.totalConfirmedTransactions % self.split == 0:
            self.reward /= 2

    def addChain(self, chain: blockChain):
        """
        addChain: Add new blockchain into confirmed transactions.

        Args:
            chain (blockChain): Chain class.
        """

        chain.confirmed = True
        self.totalConfirmedTransactions += 1

        # Base64 encode
        self.blockChains[str(self.nextID)] = base64.b64encode(str(json.dumps(str(chain.__dict__), sort_keys=True)).encode()).decode()
        self.splitReward()
        self.nextID += 1

        # Clear blockchain out of unconfirmedBlockChains
        deleteList = []

        for key in self.unconfirmedBlockChains.keys():
            if self.unconfirmedBlockChains[key].confirmed == True:
                deleteList.append(key)

        for i in deleteList:
            del self.unconfirmedBlockChains[i]

    def newChain(self, minerAddress: str):
        """
        newChain: Geneate new chain.

        Args:
            minerAddress (str): Address of the miner who made the chain.

        Returns:
            int: ID of the new chain.
        """
        newID = str(len(self.unconfirmedBlockChains))
        self.unconfirmedBlockChains[newID] = blockChain.BlockChain(self, minerAddress, newID)
        return newID

    def mineChain(self, chainID: str, blocks: int, load: bool = False, block: block = block) -> Any:
        """
        mineChain: Mine a specific chain.

        Args:
            chainID (str): ID of the chain
            blocks (int): How many blocks to mine in the blockchain.
            load (bool, optional): Specification whether to load an existing block or not. Defaults to False.

        Returns:
            any: Returns either the session or new transaction.
        """

        chainID = str(chainID)
        ret = [None, None]
        totalReward = 0

        # Load or Create new block.
        new_block = block if load else None

        if chainID in self.unconfirmedBlockChains.keys():

            block = self.unconfirmedBlockChains[chainID]

            # Mine x blocks in the blockchain.
            for _ in range(blocks):
                ret[1] = block.mine(load=load, block=new_block)
                totalReward += block.reward
                load = False

                if ret != False and ret != True:
                    break

            self.addChain(block)
            ret[0] = self.transaction(block.miner, totalReward, f"Mined in blockchain and earned {totalReward} Jush Coins.")
        return ret[0], ret[1]

    def continueSession(self, blockInfo: Dict[str, Any], minerAddress: str, blocks: int):
        """
        continueSession: Continue the session loaded from the account.

        Args:
            blockInfo (block): Block class.
            minerAddress (str): Address of the miner.
            blocks (int): How many blocks to mine.

        Returns:
            any: Depends.
        """

        chain = blockChain.BlockChain(self, minerAddress, "")
        sessionBlock = blockChain.createDummyBlock(chain)
        index = str(blockInfo["index"])
        sessionBlock.index = index

        for key in blockInfo:
            if key in sessionBlock.__dict__.keys():
                setattr(sessionBlock, key, blockInfo[key])

        self.unconfirmedBlockChains[index] = chain
        return self.mineChain(index, blocks, load=True, block=sessionBlock)

    def restartUniverse(self):
        """
        restartUniverse: Restart the universe, reset all attribute.
        """

        print("Restarting Universe...")
        self.supply = 10000000
        self.reward = 80
        self.split = 1024
        self.totalConfirmedTransactions = 0
        self.blockChains = dict({})

    def transaction(self, address: str, amount: int, *args: str):
        """
        transaction: Process transaction

        Args:
            address (str): Address of the receiver.
            amount (int): Amount of JushCoin the send.
        """

        with open("accounts.json", "r+") as f:
            accounts = json.loads(f.read())

            # Clear file
            f.seek(0)
            f.truncate()

            for name in accounts:
                if accounts[name]["address"] == address:
                    accounts[name]["balance"] += amount
                    newLog = list(accounts[name]["transactionLog"])
                    newLog.append(*args)
                    accounts[name]["transactionLog"] = newLog

                    f.write(json.dumps(accounts))
