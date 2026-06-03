from __future__ import annotations
import sys
from pathlib import Path
import wave
import struct
import math


def generate_sine_wav(
    path: Path,
    duration: float = 2.0,
    freq: float = 440.0,
    volume: float = 0.3,
    rate: int = 44100,
):
    path = Path(path)
    nframes = int(duration * rate)
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        for i in range(nframes):
            t = i / rate
            val = int(volume * 32767.0 * math.sin(2 * math.pi * freq * t))
            data = struct.pack("<h", val)
            wf.writeframesraw(data)
        wf.writeframes(b"")


def ensure_alarm_wav(path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        generate_sine_wav(path)
    return path


def play_alarm(path: Path, duration: float = 5.0):
    path = ensure_alarm_wav(path)
    # Try simpleaudio if available
    try:
        import simpleaudio as sa  # type: ignore

        wave_read = sa.WaveObject.from_wave_file(str(path))
        play = wave_read.play()
        play.wait_done()
        return
    except Exception:
        pass

    # On Windows use winsound
    if sys.platform.startswith("win"):
        try:
            import winsound

            winsound.PlaySound(str(path), winsound.SND_FILENAME)
            return
        except Exception:
            pass

    # Fallback: terminal bell
    print("\a", end="", flush=True)
