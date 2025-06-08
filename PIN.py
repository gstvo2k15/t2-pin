"""PIN identification hacking simulation, adapted from Atari Portfolio C++ demo.
   Inspired by Terminator 2 ATM hacking scene.
"""

import os
import random
import time
import sys

DELAY_SEC = 0.02  # 20 ms

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_pin_header():
    """Print the program header and wait for user input."""
    clear_screen()
    print(
        "PPPPP  IIIIIII   N    N\n"
        "P   PP    I      NN   N IDENTIFICATION\n"
        "P   PP    I      N N  N\n"
        "PPPPP     I      N  N N   PROGRAM\n"
        "P         I      N   NN\n"
        "P      IIIIIII   N    N\n"
    )
    input("Strike a key when ready ...\a")  # ASCII Bell sound

def scan_pin():
    """Simulate scanning for a PIN number."""
    pos = 38
    cnt = 0
    pin_code = str(random.randint(1000, 9999))

    print("\n\n12345678901234567890123457890123456780")
    while pos >= 5:
        for _ in range(5):
            line = ''.join(str(random.randint(0, 9)) for _ in range(pos))
            print(line)
            sys.stdout.flush()
            time.sleep(DELAY_SEC)

        pos -= 1 if cnt & 1 else 2
        cnt += 1

    for _ in range(10):
        print(pin_code)
    print(f"\nPIN IDENTIFICATION NUMBER: {pin_code}\a\n\na>")

    user_input = input().strip()

    if user_input == pin_code:
        print("\nACCESS GRANTED\nDISPENSING FUNDS...\n")
    else:
        print("\nACCESS DENIED\nSECURITY ALERT TRIGGERED\n")

def main():
    """Main program function."""
    print_pin_header()
    scan_pin()

if __name__ == "__main__":
    main()