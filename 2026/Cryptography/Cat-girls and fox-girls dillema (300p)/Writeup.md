# Cat-girls and fox-girls dillema

```
Cryptography

Difficulty: Srednie (3 rozwiazania)
Author: Jakub Rawski

In the city of Kivotos, cat girls and fox girls lived in discord because of shape of their ears.
Both factions experienced persecution because of this,
so the GSC decided to introduce a law that would equalize the quarreling citizens
and resolve the inequalities resulting from the differences in ear shape.
Unfortunately, a group of cybercriminals, who valued their sense of superiority
more than harmony, attacked the city's servers and encrypted the signed law
leaving with Ransomware called "punishment For Equality".
Your task is to recover the Free Ears Act
and reconcile the city's quarreling citizens with the law.
```
Dostajemy manifest w postaci pliku punishmentForEquality.py oraz zaszyfrowany plik .secretActs.zip.ears

Zawartosc skryptu:

```
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
```

Widzimy ze szyfrowanie dotyczny tylko plikow a nie folderow, sprobojmy usunac suffix

```
    .secretActs.zip.ears -> .secretActs.zip -zip-> .secretActs.zip
```
po rozpakowaniu widzimy nastepujace pliki:
- catSnack.png.ears
- EqualizationOfStatusAndRights.pdf.ears
- foxSnack.jpg.ears
- KivotosCivicFestival.docx.ears
- LunchBreak.docx.ears
- publicTransport.docx.ears
- SleepHygiene.docx.ears
- snackDistribution.docx.ears

Gdy sprobujemy zajrzec do srodka, plik bedzie nierozczytywalny:
(np dla naszego pliku: - EqualizationOfStatusAndRights.pdf )
```
9C AB 28 81 D3 95 C0 E2 56 13 7F 16 E9 05 EC 23 B3 CA 4C F7 DE CB 8C BF 56 13 66 9F 73 E4 20 5E DC D4 2F A6 8A C5 82 BA 3C 36 0A C2 3B D5 2A 0E 8B DB 5C E7 AC 8B A2 B4 35 7E 72 D3 30 99 79 01 EA 8F 1E B2 9D D0 BA A7 3E 7C 08 CC 33 C4 79 1C 81 DB 5C E7 AC 8B A3 B4 29 72 13 CD 3A DF 65 12
```
to co widzimy NIE JEST naglowkiem PDF.

Przyjrzyjmy sie jeszcze raz plikowi punishmentForEqualitya dokladnie metodzie destroy():
```
def destroy(file: Path, key: bytes) -> None:
    with open(file, "rb") as f:
        oryginal = f.read()

    encrypted = bytes(e ^ a for e, a in zip(oryginal, cycle(key)))

    with open(f"{file}.ears", "wb") as f:
        f.write(encrypted) #create encrypted file

    print(f"Encrypted {file.name}")
    file.unlink() #delete oryginal file
```

do szyfrowania jest uzywamy XOR!
jako ze znamy dlugosc klucza:
```
    key = os.urandom(16)
```
wystarczy XORowac zaszyfrowany plik z oryginalem by dostac klucz!
w pliku sa 2 zdjecia:
- foxSnack.jpg.ears
- catSnack.png.ears

przyjrzyjmy sie naglowkowi catSnack.png.ears:
```
30 AB 22 80 F3 AE F4 DF 5B 19 5A AE 15 F8 1D 7C B9 FB 68 C7 FE A4 E8 D5 53 1B 5A A3 5C D7 B9 83 44 FB 6D 88 F4 C7 8F 97 03 19 5B EC 56 DA 2C 43
```
jako ze hacker nie usunal suffixu wiemy ze to jest plik png ktory posiada nastepujacy naglowek:
```
 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # Magic bytes
        0x00, 0x00, 0x00, 0x0D,                         # Len of chunck IHDR
        0x49, 0x48, 0x44, 0x52                          # "IHDR"
```
zXORujmy i zobaczymy nasz klucz:
```
from pathlib import Path

def recover_key(file: Path) -> bytes:
    ciphertext = file.read_bytes()[:16]

    #  16 bytes PNG
    known_header = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # Magic bytes
        0x00, 0x00, 0x00, 0x0D,                         # Len of chunck IHDR
        0x49, 0x48, 0x44, 0x52                          # "IHDR"
    ])

    # XOR ciphertext ^ known_header => key
    key = bytes(c ^ h for c, h in zip(ciphertext, known_header))
    return key


if __name__ == "__main__":
    enc_file = Path("secretActs/catSnack.png.ears")

    key = recover_key(enc_file)
    print("hex:", key.hex(" "))
```
Wynik to `hex: b9 fb 6c c7 fe a4 ee d5 5b 19 5a a3 5c b0 59 2e`

nastepnie uzyjmy tego klucza by rozszyfrowac zawartosc folderu:
```
import os
from pathlib import Path
from itertools import cycle

TARGET_DIR = Path("./secretActs/")

KEY = bytes.fromhex("b9 fb 6c c7 fe a4 ee d5 5b 19 5a a3 5c b0 59 2e")

def decrypt(file: Path, key: bytes) -> None:
    with open(file, "rb") as f:
        ciphertext = f.read()
    # Similar as encrypt, but order is changed
    plaintext = bytes(c ^ k for c, k in zip(ciphertext, cycle(key)))

    out_file = file.with_suffix("")
    with open(out_file, "wb") as f:
        f.write(plaintext)

    print(f"Decrypted {file.name} -> {out_file.name}")




if __name__ == "__main__":
    print(f"Using key: {KEY.hex(' ')}\n")

    print("Decrypting files...")
    for file in TARGET_DIR.rglob("*.ears"):
        if file.is_file():
            decrypt(file, KEY)
```
Udalo nam sie: pliki sa odczytywane! Wystarczy tylko wejsc do pliku EqualizationOfStatusAndRights.pdf
i poszukac flagi:
```
...
Art. 9. The Act shall enter into force on the day of its official promulgation.

President of the General Student Council: PJATK{kiv070s_in_p34c3_0nc3_4g4in}
```
Wiec flaga to : `PJATK{kiv070s_in_p34c3_0nc3_4g4in}` 