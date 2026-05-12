# Lich King Orders

```
Cryptography

Difficulty: Trywialne (32 rozwiazania)
Author: Jakub Rawski

King Arthas, the centuries-exiled ruler of the undead, has awakened in his Icecrown citadel.
Instead of marching openly upon the realms of the living, however, he has begun sending magical impulses-encrypted messages-to his dormant agents stationed in Alliance cities and garrisons.
If Arthas's minions receive their full instructions, an unstoppable undead uprising will erupt from the heart of the kingdom.
Your task is to decipher his message and save Azeroth from the undead plague.
```
Plik zawiera zaszyfrowana wiadomosc, zajrzyjmy do niego (to zwykly .txt)

Zawartosc pliku:

```
#------------------------------#
#--GARKB{Wifjkdfliev_ylexvij}--#
#------------------------------#
```

Zakladajac ze pierwsze 5 znakow to "PJATK" sprobojmy szyfru Cezara:

```
    G-P mod 26 = 7-16 mod 26 = -9 mod 26 -> 26-9 = 17 # Przesuwamy o 17 w lewo
```

Odszyfrowanie wyglada nastepujco: `PJATK{Frostmourne_hungers}` 