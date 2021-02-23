try:
    import sys
    sys.path.append("../JushCoin/")
except:
    exit()


import JushCoin.user as user

# Username and Password
username = "Example"
password = "Example"

# Create user
example = user.user()
example.createAccount(username, password)

# Save User
example.save()

# Load User
example.load(username, password)

# Get Address
print(example.address)
