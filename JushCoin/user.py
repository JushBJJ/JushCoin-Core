import hashlib
import json
import os

JushCoinSig = "1f60deedb323271b360bbcb58743f120904a00ca7b4b37ac81120c7c32c16ef4"


class user:
    """
    user: User class for Jush Coin

    Attributes:
        ID: Identification Number of the User.
        Balance: Amount of JushCoin the user has.
        Transaction Log: List of messages of each transaction.
        Session: Saved session stored as a string formatted in JSON.

        Name: Account username
        Password: Account Password (Hashed)
        Address: Account Address for transactions.
    """

    def __init__(self):
        # Account Info
        self.id = 0
        self.balance = 0.0
        self.transactionLog = []
        self.session = ""

        # Account Personal Info
        self.name = ""
        self.password = ""
        self.address = ""

    def hash(self, text: str):
        """
        hash: Hashes the text using sha256.

        Args:
            text (string): Text to be hashed.

        Returns:
            string: Hexdigest of text.
        """
        return hashlib.sha256(text.encode()).hexdigest()

    def update(self):
        """
        update: Updates to the latest updated information by loading the user again.
        """

        self.fixFile()

        with open("accounts.json", "r") as f:
            accounts = json.loads(f.read())

            if self.name in accounts:
                if accounts[self.name]["password"] == self.password:
                    for attrs in accounts[self.name]:
                        if attrs in accounts[self.name].keys():
                            self.__setattr__(attrs, accounts[self.name][attrs])
                else:
                    print("Invaild password.")

    def createAccount(self, username: str, password: str):
        """
        createAccount: Creates a new account and stores it into a JSON file.

        Args:
            username (string): Username of the new account.
            password (string): Password of the new account.

        Returns:
            True if account was successfully created.
            False if failed to create account.
        """

        self.fixFile()

        with open("accounts.json", "r+") as f:
            accounts = json.loads(f.read())

            # Check if username is registered.
            if username not in accounts:
                self.id = str(len(accounts))  # Get New ID
                self.address = createAddress(username, self.id)  # Generate Address

                self.name = username
                self.password = self.hash(password)

                # Clear file
                f.seek(0)
                f.truncate()

                # Store account attributes
                accounts[username] = self.__dict__
                f.write(json.dumps(accounts))

            else:
                print("Account already exists.")
                return False

            return True

    def fixFile(self):
        """
        fixFile: Creates accounts.json if it doesn't exist, else, resets the file if there is a json decode error.
        """

        if not os.path.exists("accounts.json"):
            with open("accounts.json", "w") as f:
                f.write(json.dumps({}))
        else:
            if os.stat("accounts.json").st_size == 0:
                os.remove("accounts.json")
                self.fixFile()

    def save(self):
        """
        save: Save account into json file.
        """

        self.fixFile()

        with open("accounts.json", "r+") as f:
            # Gather accounts
            accounts = f.read()

            # Clear file
            f.seek(0)
            f.truncate()

            # Parse and Save attributes into json
            accounts = json.loads(accounts)
            accounts[self.name] = self.__dict__
            f.write(json.dumps(accounts))

    def load(self, username: str, password: str):
        """
        load: Sign in to account.

        Args:
            username (str): Username of the account.
            password (str): Password of the account.
        """
        self.fixFile()

        with open("accounts.json", "r") as f:
            accounts = json.loads(f.read())

            if username in accounts:
                if accounts[username]["password"] == self.hash(password):
                    for attrs in accounts[username]:
                        if attrs in accounts[username].keys():
                            self.__setattr__(attrs, accounts[username][attrs])
                else:
                    print("Invaild password.")

    def deleteUser(self, username: str):
        """
        deleteUser: Delete the user from the json file.

        Args:
            username (str): Username to be deleted.
        """
        self.fixFile()

        with open("accounts.json", "r+") as f:
            accounts = json.loads(f.read())

            # Remove account from dict.
            if username in accounts:
                del accounts[username]
            else:
                print("User not found.")

            # Clear file and rewrite
            f.seek(0)
            f.truncate()

            f.write(json.dumps(accounts))


def createAddress(username: str, user_id: str):
    """
    createAddress: Generate an address of a user.

    Args:
        username (str): Username of the user.
        user_id (str): User ID of the user.

    Returns:
        str: Hexdigest of the signature+username+user_id
    """
    return hashlib.sha256(str(JushCoinSig+username+user_id).encode()).hexdigest()
