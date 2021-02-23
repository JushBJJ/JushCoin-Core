import base64
import json
import block.blockChain as blockChain
import json
import base64


class Universe:
    def __init__(self, name):
        self.supply = 10000000
        self.reward = 32
        self.split = 1024
        self.totalConfirmedTransactions = 0
        self.blockChains = dict({})
        self.unconfirmedBlockChains = dict({})
        self.nextID = 0
        self.name = name
        self.JushCoinSig = "1f60deedb323271b360bbcb58743f120904a00ca7b4b37ac81120c7c32c16ef4"

    def save(self):
        self.unconfirmedBlockChains = dict({})
        universe = base64.b64encode(json.dumps(str(self.__dict__), sort_keys=True).encode())

        with open(f"JC_WORLD_{self.name}.txt", "wb") as f:
            f.write(universe)

    def load(self, filename):
        with open(filename, "rb") as f:
            txt = f.read()
            universe = base64.b64decode(txt.decode()).decode().split("\"")[1]
            universe = universe.replace("\'", "\"")
            universe = json.loads(universe)

            for keys in universe.keys():
                if keys in self.__dict__.keys():
                    self.__setattr__(keys,  universe[keys])

    def splitReward(self):
        if self.totalConfirmedTransactions % self.split == 0:
            self.reward /= 2

    def addChain(self, chain):
        chain.confirmed = True
        self.totalConfirmedTransactions += 1
        self.blockChains[str(self.nextID)] = base64.b64encode(str(json.dumps(str(chain.__dict__), sort_keys=True)).encode()).decode()
        self.splitReward()

        self.nextID += 1
        deleteList = []
        for key in self.unconfirmedBlockChains.keys():
            if self.unconfirmedBlockChains[key].confirmed == True:
                deleteList.append(key)

        for i in deleteList:
            del self.unconfirmedBlockChains[i]

    def newChain(self, minerAddress):
        newID = str(len(self.unconfirmedBlockChains))
        self.unconfirmedBlockChains[newID] = blockChain.BlockChain(self, minerAddress, newID)
        return newID

    def mineChain(self, chainID, blocks, load=False, **kwargs):
        chainID = str(chainID)
        saveSession = False
        session = ""

        new_block = kwargs["block"] if load else None

        if chainID in self.unconfirmedBlockChains.keys():
            totalReward = 0
            block = self.unconfirmedBlockChains[chainID]

            for _ in range(blocks):
                ret = block.mine(load=load, block=new_block)
                load = False

                if ret != False and ret != True:
                    saveSession = True
                    session = ret
                    break

                totalReward += block.reward

            if saveSession:
                self.transaction(block.miner, totalReward, f"Mined in blockchain and earned {totalReward} Jush Coins.")
                return json.loads(session)

            self.addChain(block)

            return self.transaction(block.miner, totalReward, f"Mined in blockchain and earned {totalReward} Jush Coins.")

    def continueSession(self, chainInfo, minerAddress, blocks):
        chain = blockChain.BlockChain(self, minerAddress, "")
        block = blockChain.createDummyBlock(chain)
        index = str(chainInfo["index"])

        for key in chainInfo:
            if key in block.__dict__.keys():
                setattr(block, key, chainInfo[key])

        self.unconfirmedBlockChains[index] = chain
        return self.mineChain(index, blocks, load=True, block=block)

    def restartUniverse(self):
        print("Restarting Universe...")
        self.supply = 10000000
        self.reward = 80
        self.split = 1024
        self.totalConfirmedTransactions = 0
        self.blockChains = dict({})

    def transaction(self, address, amount, *args):
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
