try:
    import sys
    sys.path.append("../JushCoin/")
except:
    exit()

import user
import universe
import json

# Username and Password
username = "Example"
password = "Example"

# Create user
example = user.user()
example.createAccount(username, password)

# Create Universe
world_example = universe.Universe("Foo")

# Restart Universe
# world_example.restartUniverse()

# Mine 1 block
amount_to_mine = 1

# Create Chain
chain_id = world_example.newChain(example.address)
result = world_example.mineChain(chain_id, amount_to_mine)

# In case if keyboard interrupt exception is raised
if type(result) == dict:
    example.session = json.dumps(result)

# After Mining, save results to account
example.save()

# Save World
world_example.save()
