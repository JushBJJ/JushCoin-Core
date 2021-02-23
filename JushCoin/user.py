import universe
import hashlib
import json
import os


class user:
    def __init__(self):
        self.id = 0
        self.balance = 0.0
        self.name = ""
        self.transactionLog = []
        self.session = ""
        self.address = ""
        self.password = ""
        self.JushCoinSig = "1f60deedb323271b360bbcb58743f120904a00ca7b4b37ac81120c7c32c16ef4"

    def hash(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def update(self):
        self.load(self.name, self.password)

    def createAccount(self, username, password):
        if os.path.exists("accounts.json"):
            success = False

            with open("accounts.json", "r") as f:
                accounts = json.loads(f.read())
                hashedUsername = self.hash(username)

                if hashedUsername not in accounts:
                    self.id = len(accounts)
                    self.address = createAddress(username, self.id)
                    success = True

                else:
                    print("Account already exists.")

            if success:
                self.save()
                return self
            return False
        else:
            with open("accounts.json", "w") as f:
                self.id = 0
                self.address = createAddress(username, self.id)
                self.name = self.hash(username)
                self.password = self.hash(password)

                account = {
                    self.name: self.__dict__
                }
                f.write(json.dumps(account))

            return self

    def fixFile(self):
        if not os.path.exists("accounts.json"):
            with open("accounts.json", "w") as f:
                f.write(json.dumps({}))
        else:
            if os.stat("accounts.json").st_size == 0:
                os.remove("accounts.json")
                self.fixFile()

    def save(self):
        self.fixFile()

        with open("accounts.json", "r+") as f:
            txt = f.read()

            # Clear file
            f.seek(0)
            f.truncate()

            accounts = json.loads(txt)
            accounts[self.name] = self.__dict__
            f.write(json.dumps(accounts))

    def load(self, username, password):
        self.fixFile()

        with open("accounts.json", "r") as f:
            accounts = json.loads(f.read())
            username = self.hash(username)

            if username in accounts:
                if accounts[username]["password"] == self.hash(password):
                    for attrs in accounts[username]:
                        if attrs in accounts[username].keys():
                            self.__setattr__(attrs, accounts[username][attrs])

        return self


def createAddress(username, id):
    JushCoinSig = "1f60deedb323271b360bbcb58743f120904a00ca7b4b37ac81120c7c32c16ef4"
    id = str(id)
    return hashlib.sha256(str(JushCoinSig+username+id).encode()).hexdigest()
