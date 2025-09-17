#!/usr/bin/env python3
# T2-style PIN scan with fast ticking beeps, robust backends

import os, sys, time, random, math, wave, struct, tempfile, shutil, subprocess, platform
from time import monotonic
import winsound, time

for _ in range(20):
    winsound.Beep(1350, 25)   # 1350 Hz, 25 ms
    time.sleep(0.06)

# ====== Tuning ======
BEEP_EVERY_N_CHARS = 3     # play a tick every N digits
BEEP_MIN_INTERVAL  = 0.03  # rate-limit ticks (~33/s)
DELAY_SEC          = 0.0   # no sleep per char
HEADER_WAIT_ANYKEY = True  # any key (no Enter)
TICK_FREQ_HZ       = 1400  # fallback sine tone
TICK_MS            = 12    # 8–20 ms feels “electronic”
# ====================

SYSTEM = platform.system()

# -------- Windows: WAV-in-memory (asynchronous) --------
_win_wav_bytes = None
def _make_wav_bytes(freq=TICK_FREQ_HZ, ms=TICK_MS, rate=44100):
    import io
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(rate)
        frames = int(rate * (ms/1000.0))
        for i in range(frames):
            val = int(32767 * math.sin(2*math.pi*freq*(i/rate)))
            wf.writeframes(struct.pack("<h", val))
    return buf.getvalue()

def _play_windows_async_wavmem():
    global _win_wav_bytes
    try:
        import winsound
        if _win_wav_bytes is None:
            _win_wav_bytes = _make_wav_bytes()
        # SND_MEMORY + SND_ASYNC
        winsound.PlaySound(_win_wav_bytes, winsound.SND_MEMORY | winsound.SND_ASYNC)
        return True
    except Exception:
        return False

# -------- POSIX players --------
PLAYER = shutil.which("paplay") or shutil.which("aplay") or shutil.which("afplay") or shutil.which("ffplay") or shutil.which("play")
def _play_posix_async_tempwav():
    # create one tiny temp WAV once per process
    if not hasattr(_play_posix_async_tempwav, "tmp"):
        fd, path = tempfile.mkstemp(suffix=".wav"); os.close(fd)
        with wave.open(path, "wb") as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(44100)
            frames = int(44100 * (TICK_MS/1000.0))
            for i in range(frames):
                val = int(32767 * math.sin(2*math.pi*TICK_FREQ_HZ*(i/44100)))
                wf.writeframes(struct.pack("<h", val))
        _play_posix_async_tempwav.tmp = path
        import atexit
        atexit.register(lambda: os.path.exists(path) and os.remove(path))
    path = _play_posix_async_tempwav.tmp
    try:
        if PLAYER.endswith("ffplay"):
            args = [PLAYER, "-nodisp", "-autoexit", "-loglevel", "quiet", path]
        else:
            args = [PLAYER, path]
        subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

# -------- Beeper facade --------
_last_beep = 0.0
def tick():
    global _last_beep
    now = monotonic()
    if now - _last_beep < BEEP_MIN_INTERVAL:
        return
    _last_beep = now

    if SYSTEM == "Windows":
        if _play_windows_async_wavmem():
            return
    else:
        if PLAYER and _play_posix_async_tempwav():
            return
    # last resort
    sys.stdout.write("\a"); sys.stdout.flush()

# -------- Console helpers --------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_key():
    if os.name == 'nt':
        import msvcrt; msvcrt.getch()
    else:
        import tty, termios
        fd = sys.stdin.fileno(); old = termios.tcgetattr(fd)
        try: tty.setraw(fd); sys.stdin.read(1)
        finally: termios.tcsetattr(fd, termios.TCSADRAIN, old)

# -------- Program --------
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
    print("Strike a key when ready ...")
    if HEADER_WAIT_ANYKEY: wait_key()
    else: input()
    tick()

def scan_pin():
    pos = 38
    cnt = 0
    pin_code = str(random.randint(1000, 9999))

    print("\n\n12345678901234567890123457890123456780")
    while pos >= 5:
        for _ in range(5):
            line = ''.join(str(random.randint(0, 9)) for _ in range(pos))
            for i, ch in enumerate(line):
                sys.stdout.write(ch)
                if i % BEEP_EVERY_N_CHARS == 0:
                    tick()
            sys.stdout.write("\n"); sys.stdout.flush()
            if DELAY_SEC: time.sleep(DELAY_SEC)
        pos -= 1 if cnt & 1 else 2
        cnt += 1

    for _ in range(10):
        print(pin_code)
    print(f"\nPIN IDENTIFICATION NUMBER: {pin_code}\n\na>")
    user_input = input().strip()

    if user_input == pin_code:
        print("\nACCESS GRANTED\nDISPENSING FUNDS...\n")
        for _ in range(3): tick(); time.sleep(0.05)
    else:
        print("\nACCESS DENIED\nSECURITY ALERT TRIGGERED\n")
        for _ in range(3): tick(); time.sleep(0.05)

def main():
    print_pin_header()
    scan_pin()

if __name__ == "__main__":
    main()
