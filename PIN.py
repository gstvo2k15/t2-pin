#!/usr/bin/env python3
# T2-style PIN scan with bright tick matched to your MP3: 1425 Hz, 25 ms, every 60 ms

import os, sys, time, random, platform

# ---------- Tick tuning (matched to MP3 high peak) ----------
BEEP_FREQ_HZ       = 850   # bright click component from the MP3
BEEP_MS            = 5      # short tick to keep scrolling fast
CHAR_PERIOD_SEC    = 0.0001  # overall pace per character (~3 ms)
HEADER_WAIT_ANYKEY = True   # any key (not Enter)
# ------------------------------------------------------------

IS_WINDOWS = (platform.system() == "Windows")
if IS_WINDOWS:
    import winsound

def tick():
    if IS_WINDOWS:
        winsound.Beep(BEEP_FREQ_HZ, BEEP_MS)

def clear_screen():
    os.system('cls' if IS_WINDOWS else 'clear')

def wait_key():
    if IS_WINDOWS:
        import msvcrt
        msvcrt.getch()
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def print_pin_header():
    clear_screen()
    print(
        "PPPPP  IIIIIII   N    N\n"
        "P   PP    I      NN   N     IDENTIFICATION\n"
        "P   PP    I      N N  N\n"
        "PPPPP     I      N  N N        PROGRAM\n"
        "P         I      N   NN\n"
        "P      IIIIIII   N    N\n"
    )
    print("Strike a key when ready ...")
    if HEADER_WAIT_ANYKEY:
        wait_key()
    else:
        input()
    tick()

def scan_pin():
    pos = 38
    cnt = 0
    pin_code = str(random.randint(1000, 9999))

    print("\n\n12345678901234567890123457890123456780")
    while pos >= 5:
        for _ in range(5):
            line = ''.join(str(random.randint(0, 9)) for _ in range(pos))
            for ch in line:
                sys.stdout.write(ch)
                sys.stdout.flush()
                tick()
                time.sleep(CHAR_PERIOD_SEC)
            sys.stdout.write("\n")
            sys.stdout.flush()
        pos -= 1 if (cnt & 1) else 2
        cnt += 1

    for _ in range(10):
        print(pin_code)
    print(f"\nPIN IDENTIFICATION NUMBER: {pin_code}\n\na>")
    user_input = input().strip()

    if user_input == pin_code:
        print("\nACCESS GRANTED\nDISPENSING FUNDS...\n")
        if IS_WINDOWS:
            for f, d in ((880, 80), (1200, 80), (1600, 120)):
                winsound.Beep(f, d); time.sleep(0.05)
    else:
        print("\nACCESS DENIED\nSECURITY ALERT TRIGGERED\n")
        if IS_WINDOWS:
            for _ in range(3):
                winsound.Beep(220, 150); time.sleep(0.1)

def main():
    print_pin_header()
    scan_pin()

if __name__ == "__main__":
    main()
