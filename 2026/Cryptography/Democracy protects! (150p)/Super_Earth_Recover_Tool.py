import os
import time
from concurrent.futures import ProcessPoolExecutor
from time import sleep

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import random
import sys
import os
import threading

KEYS = {
    'w': '↑',
    'a': '←',
    's': '↓',
    'd': '→',
}

# ================== CONFIGURATION ==================
received_key =
known_key =
ciphertext_hex =
target =
# ================== PARAMS ==================

ct_full = bytes.fromhex(ciphertext_hex)
first_block = ct_full[:16]
NUM_CORES = os.cpu_count() # USE 100% power of managed democracy
#NUM_CORES = 4 # USE 4 of managed democracy
CHUNK_SIZE = 1_000_000

def show_intro():
    print("#" + "─" * 20 + "Super Earth Recover Tool" + "─" * 20 + "#")
    sleep(1)
    print("""                                                                                                                                          
                                     ##                                     
                                    ####                                    
                                   ######                                   
                                 #  #### ##                                 
                                 #  #### ##                                 
                                ##  # ## ##                                 
                               ##############                               
                           ########### ##########                           
                        #########         #####  ###                        
                      ##########           ###########                      
                    #####  ###              ############                    
                   ####    ###   #         ##############                   
                  ####### # #  ####        ###############                  
                 #  #####   ######       #  ###############                 
                ##     #   ######           ################                
                #                     #  ###################                
             #  #                    ### ###################  #             
             # ##                  ## ####################### #             
          #  # ##              ##  ## #################### ## #  #          
          #  # ##               # ############ ########### ## #  #          
           # #  #               ##############  ########## # ## #           
           #  # ##           ####  # #### ############# #### #  #           
           ## #  ##          #        ##### ########     ## ## ##           
            #  #  #       #########        #########     #  #  #            
             #  #  ##    ################### ######    ##  #  #             
              #  #  ##   ####################  ##     ##  #  #              
               #  ## ###  ########################  ### ##  #               
                ##  ## ###   ###################  ### ##  ##                
                  ##  ##  ####    ################  ##  ##                  
                   ###  ###  ##################  ###  ##                    
                      ###  #####            #####  ###                      
                         ###    ############   ####                         
                            ###    ############                             
                          ##                    ##                          
                         #                        #                         
                               #            #                               
                    ##   ##   ###   ####   ###    ##  ##                    
                                    #  #                                                                                                                                                                                 
    """)
    sleep(1)
    print("#"+"─"*20+"All rights reserved"+"─"*20+"#")
    print("To confirm that you are not an automaton, run the panel:")
    print("Controls:  w=↑  a=←  s=↓  d=→")
    print("  Input keys to verify that you are citizen of Super Earth:")
# ============= PANEL ======================
def random_sequence(length: int) -> list[str]:
    return [random.choice(list(KEYS.values())) for _ in range(length)]


def _make_getch():
    """Returns the appropriate single-keypress reader for the current platform."""
    if sys.platform == 'win32':
        import msvcrt, ctypes

        try:
            msvcrt.kbhit()
            stdin_is_real_tty = sys.stdin.isatty()
        except Exception:
            stdin_is_real_tty = False

        if stdin_is_real_tty:
            def getch():
                ch = msvcrt.getwch()
                if ch in ('\x00', '\xe0'):  # special keys send two bytes
                    msvcrt.getwch()
                    return ''
                return ch
        else:
            # PyCharm / no TTY on Windows → poll via GetAsyncKeyState
            import time
            WASD_VK = {'w': 0x57, 'a': 0x41, 's': 0x53, 'd': 0x44}
            prev_state = {k: False for k in WASD_VK}

            def getch():
                while True:
                    for char, vk in WASD_VK.items():
                        pressed = bool(ctypes.windll.user32.GetAsyncKeyState(vk) & 0x8000)
                        if pressed and not prev_state[char]:
                            prev_state[char] = True
                            return char
                        if not pressed:
                            prev_state[char] = False
                    time.sleep(0.01)

        return getch

    else:
        # Linux / macOS: open /dev/tty directly, bypassing stdin entirely
        import tty, termios

        def getch():
            tty_fd = os.open('/dev/tty', os.O_RDWR)
            old = termios.tcgetattr(tty_fd)
            try:
                tty.setcbreak(tty_fd)
                return os.read(tty_fd, 1).decode('utf-8', errors='ignore')
            finally:
                termios.tcsetattr(tty_fd, termios.TCSADRAIN, old)
                os.close(tty_fd)

        return getch


def arrow_challenge(length: int) -> None:
    """
    Generates a random arrow sequence and requires the Citizen to reproduce it
    using W A S D keys.
    - One wrong key immediately resets the round (same sequence).
    - On a correct full sequence the function returns immediately, no Enter needed.
    Controls:  w=↑  a=←  s=↓  d=→
    Works on: Linux, macOS, Windows (cmd/PowerShell/Terminal), PyCharm (Win/Linux).
    No external dependencies required.
    100% Freedom
    """

    getch = _make_getch()
    sequence = random_sequence(length)

    def print_header():
        print("─" * 60)
        print("   " + "  ".join(sequence))
        print("  ", end="", flush=True)

    while True:
        print_header()
        failed = False

        for expected in sequence:
            while True:
                key = getch().lower()
                if key in ('\x03', '\x04'):  # Ctrl+C / Ctrl+D
                    print("\n\n  Aborted.")
                    return
                if key in KEYS:
                    break

            arrow = KEYS[key]
            print(arrow, end=" ", flush=True)

            if arrow != expected:
                print(f"\n  authentication failed:")
                failed = True
                sleep(1)
                break

        if failed:
            continue

        print("\n  Authentication successful: \n" + "─" * 60)
        sleep(1)
        return


# ===================================================
def crack_chunk(start_val, end_val):
    key_template = bytearray(known_key + b'\x00\x00\x00\x00')
    aes_algo = algorithms.AES
    ecb_mode = modes.ECB()

    for i in range(start_val, end_val):
        key_template[12] = (i >> 24) & 0xFF
        key_template[13] = (i >> 16) & 0xFF
        key_template[14] = (i >> 8) & 0xFF
        key_template[15] = i & 0xFF

        cipher = Cipher(aes_algo(bytes(key_template)), ecb_mode)
        decryptor = cipher.decryptor()

        if decryptor.update(first_block).startswith(target):
            return key_template.hex()
    return None


def main():
    total_keys = 4294967296
    print(f"--- Booting up ---")
    sleep(1)
    print(f"--- Harvesting data ---")
    sleep(1)
    print(f"--- Please confirm specification and recources: ---")
    print(f"--- nuber of cores: {NUM_CORES} ---")
    arrow_challenge(5)
    sleep(1)
    print(f"--- known prefix of message: {target} ---")
    arrow_challenge(5)
    sleep(1)
    print(f"--- known part of key: {known_key} ---")
    arrow_challenge(5)
    sleep(1)
    print(f"--- known ciphertext: {ciphertext_hex} ---")
    arrow_challenge(5)
    sleep(1)
    print(f"--- Please confirm running the recovery tool ---")
    arrow_challenge(32)
    sleep(1)
    print(f"--- Confirm status: APPROVED ---")
    sleep(3)
    start_time = time.time()
    last_checkpoint = -1
    print(f"--- Searching missing part of key: {known_key}... ---")

    with ProcessPoolExecutor(max_workers=NUM_CORES) as executor:
        futures = []
        for chunk_start in range(0, total_keys, CHUNK_SIZE):
            futures.append(executor.submit(crack_chunk, chunk_start, chunk_start + CHUNK_SIZE))
            if len(futures) > NUM_CORES * 2:
                current_f = futures.pop(0)
                res = current_f.result()
                if res:
                    print(f"\n\nFreedom delivery! : {res}")
                    sleep(1)
                    recovered_key = bytes.fromhex(res)
                    cipher = AES.new(recovered_key, AES.MODE_ECB)
                    ciphertext = bytes.fromhex(ciphertext_hex)
                    plaintext_padded = cipher.decrypt(ciphertext)
                    # Prove to yourself that you have the strength and the courage to be free
                    print(f"--- Finalizing for key {res} ---")
                    arrow_challenge(710)
                    try:
                        plaintext = unpad(plaintext_padded, 16)
                        print("Flag:", plaintext.decode())
                    except ValueError:
                        print("Democracy somehow failed.")
                    os._exit(0)

                # Stats
                checked = chunk_start
                elapsed = time.time() - start_time
                speed = checked / elapsed / 1_000_000 if elapsed > 0 else 0

                progress_pct = (checked / total_keys) * 100
                elapsed_str = f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d}"

                print(
                    f"\rProgress: {progress_pct:5.2f}% | "
                    f"Speed: {speed:4.2f} M/s | "
                    f"Elapsed: {elapsed_str}",
                    end="", flush=True
                )

                current_checkpoint = int(progress_pct // 10)
                if current_checkpoint > last_checkpoint:
                    last_checkpoint = current_checkpoint
                    # Confirming that process goes smooth
                    # Liberty knows no bounds
                    # If you don't want to wait how prosperity of Super Earth works, remove code below
                    time.sleep(1)
                    print("\n--- Confirm progres: ---")
                    arrow_challenge(8)


if __name__ == "__main__":
    show_intro()
    arrow_challenge(12)
    main()