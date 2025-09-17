import os, sys, time, random
import math, wave, struct, tempfile, shutil, subprocess, platform

DELAY_SEC = 0.02  # 20 ms

def beep(freq=440, ms=200):
    dur = ms / 1000.0
    rate = 44100
    frames = int(rate * dur)

    # Crear WAV mono 16-bit en /tmp
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        with wave.open(path, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(rate)
            for i in range(frames):
                val = int(32767 * math.sin(2 * math.pi * freq * (i / rate)))
                wf.writeframes(struct.pack("<h", val))

        system = platform.system()

        if system == "Windows":
            try:
                import winsound
                winsound.PlaySound(path, winsound.SND_FILENAME)
                return
            except Exception:
                # Fallback a PowerShell
                subprocess.call(["powershell", "-NoProfile", "-Command",
                                 f"[console]::beep({freq},{ms})"])
                return

        # Linux/WSL/macOS: escoger reproductor disponible
        for player in ("paplay", "aplay", "ffplay", "play", "afplay"):
            exe = shutil.which(player)
            if not exe:
                continue
            if player == "ffplay":
                subprocess.call([exe, "-nodisp", "-autoexit", path],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.call([exe, path],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return

        # Último recurso: BEL (probablemente silencioso)
        sys.stdout.write("\a")
        sys.stdout.flush()
    finally:
        try:
            os.remove(path)
        except OSError:
            pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_pin_header():
    clear_screen()
    print(
        "PPPPP  IIIIIII   N    N\n"
        "P   PP    I      NN   N IDENTIFICATION\n"
        "P   PP    I      N N  N\n"
        "PPPPP     I      N  N N   PROGRAM\n"
        "P         I      N   NN\n"
        "P      IIIIIII   N    N\n"
    )
    input("Strike a key when ready ...")
    beep(880, 120)

def scan_pin():
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
    print(f"\nPIN IDENTIFICATION NUMBER: {pin_code}\n\na>")

    user_input = input().strip()

    if user_input == pin_code:
        print("\nACCESS GRANTED\nDISPENSING FUNDS...\n")
        beep(523, 120); time.sleep(0.05); beep(659, 120); time.sleep(0.05); beep(784, 180)
    else:
        print("\nACCESS DENIED\nSECURITY ALERT TRIGGERED\n")
        for _ in range(3):
            beep(220, 150); time.sleep(0.1)

def main():
    print_pin_header()
    scan_pin()

if __name__ == "__main__":
    main()
