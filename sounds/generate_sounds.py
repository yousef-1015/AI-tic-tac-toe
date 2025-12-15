# This script generates simple sound effects using pygame
import pygame
import numpy as np
import os
import wave as wave_module

pygame.mixer.init(frequency=44100, size=-16, channels=1)

def generate_tone(frequency, duration, volume=0.5, fade_out=True):
    """Generate a simple tone"""
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    wave = np.sin(2 * np.pi * frequency * t) * volume * 32767
    
    if fade_out:
        fade = np.linspace(1, 0, n_samples)
        wave = wave * fade
    
    wave = wave.astype(np.int16)
    return wave

def save_wav(filename, wave_data):
    """Save numpy array as WAV file"""
    with wave_module.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)
        f.writeframes(wave_data.tobytes())

# Generate click sound (short high tone)
click = generate_tone(800, 0.08)
save_wav("click.wav", click)

# Generate win sound (ascending tones)
win = np.concatenate([
    generate_tone(523, 0.15),  # C
    generate_tone(659, 0.15),  # E
    generate_tone(784, 0.3),   # G
])
save_wav("win.wav", win)

# Generate lose sound (descending tones)
lose = np.concatenate([
    generate_tone(392, 0.15),  # G
    generate_tone(330, 0.15),  # E
    generate_tone(262, 0.3),   # C
])
save_wav("lose.wav", lose)

# Generate draw sound (two same tones)
draw = np.concatenate([
    generate_tone(440, 0.2),
    generate_tone(440, 0.2),
])
save_wav("draw.wav", draw)

print("Sound files generated!")
