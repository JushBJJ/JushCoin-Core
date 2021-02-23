import os

# Clean up unnecessary files.
file_filter = [
    "*.json",
    "JC_*"
]

for file in file_filter:
    os.remove(f"JushCoin/{file}")
    os.remove(f"examples/{file}")
