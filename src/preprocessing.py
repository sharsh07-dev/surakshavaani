import librosa
import numpy as np
import soundfile as sf
from .config import *

def load_and_fix_length(file_path):
    """Loads audio, resamples to 16kHz, and fixes duration to 3s."""
    try:
        # Load audio with native sampling rate first, then resample
        y, sr = librosa.load(file_path, sr=SAMPLE_RATE)
        
        # Trim silence (Top-dB 20 is standard for speech)
        y, _ = librosa.effects.trim(y, top_db=20)
        
        # Fix Length (Pad or Truncate)
        if len(y) > SAMPLES_PER_TRACK:
            y = y[:SAMPLES_PER_TRACK]
        else:
            padding = SAMPLES_PER_TRACK - len(y)
            offset = padding // 2
            y = np.pad(y, (offset, SAMPLES_PER_TRACK - len(y) - offset), 'constant')
            
        return y
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def extract_features(y):
    """
    Generates Log-Mel Spectrogram from audio signal.
    
    NOTE: Multi-feature extraction (MFCC, Spectral Contrast, Chroma) is available
    but requires retraining the model. See extract_features_enhanced() below.
    """
    # Compute Mel Spectrogram
    mel_spectrogram = librosa.feature.melspectrogram(
        y=y, 
        sr=SAMPLE_RATE, 
        n_fft=N_FFT, 
        hop_length=HOP_LENGTH, 
        n_mels=N_MELS
    )
    
    # Convert to Log-scale (dB)
    log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
    
    # Add channel dimension for CNN input (Height, Width, Channel)
    return log_mel_spectrogram[..., np.newaxis]


def extract_features_enhanced(y):
    """
    Enhanced multi-feature extraction for better emotion discrimination.
    Combines Mel-Spectrogram, MFCC, Spectral Contrast, and Chroma features.
    
    ⚠️ REQUIRES RETRAINING: This produces 4-channel output.
    Use this after retraining the model with the new architecture.
    """
    # Feature 1: Log-Mel Spectrogram (captures overall spectral energy)
    mel_spectrogram = librosa.feature.melspectrogram(
        y=y, 
        sr=SAMPLE_RATE, 
        n_fft=N_FFT, 
        hop_length=HOP_LENGTH, 
        n_mels=N_MELS
    )
    log_mel = librosa.power_to_db(mel_spectrogram, ref=np.max)
    
    # Feature 2: MFCC (captures vocal tract shape - crucial for emotion)
    mfcc = librosa.feature.mfcc(
        y=y,
        sr=SAMPLE_RATE,
        n_mfcc=40,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH
    )
    
    # Feature 3: Spectral Contrast (distinguishes anger's sharp vs fear's trembling)
    spectral_contrast = librosa.feature.spectral_contrast(
        y=y,
        sr=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH
    )
    
    # Feature 4: Chroma (pitch class - anger is more sustained, fear is erratic)
    chroma = librosa.feature.chroma_stft(
        y=y,
        sr=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH
    )
    
    # Resize all features to match mel-spectrogram dimensions (128 x time_steps)
    target_frames = log_mel.shape[1]
    
    # Pad MFCC to 128 dimensions
    mfcc_padded = np.pad(mfcc, ((0, N_MELS - mfcc.shape[0]), (0, 0)), mode='constant')
    
    # Resize spectral contrast and chroma
    spectral_contrast_resized = np.resize(spectral_contrast, (N_MELS, target_frames))
    chroma_resized = np.resize(chroma, (N_MELS, target_frames))
    
    # Stack features as separate channels (like RGB in images)
    # Shape: (128, time_steps, 4)
    combined_features = np.stack([
        log_mel,
        mfcc_padded[:, :target_frames],
        spectral_contrast_resized,
        chroma_resized
    ], axis=-1)
    
    return combined_features

def augment_audio(y):
    """Applies random augmentations for robustness."""
    aug_choice = np.random.choice(['noise', 'pitch', 'speed', 'none'], p=[0.3, 0.3, 0.2, 0.2])
    
    if aug_choice == 'noise':
        noise = np.random.randn(len(y))
        y = y + 0.005 * noise
    elif aug_choice == 'pitch':
        steps = np.random.uniform(-2, 2)
        y = librosa.effects.pitch_shift(y, sr=SAMPLE_RATE, n_steps=steps)
    elif aug_choice == 'speed':
        rate = np.random.uniform(0.9, 1.1)
        y = librosa.effects.time_stretch(y, rate=rate)
        if len(y) > SAMPLES_PER_TRACK:
            y = y[:SAMPLES_PER_TRACK]
        else:
            y = np.pad(y, (0, SAMPLES_PER_TRACK - len(y)), 'constant')
            
    return y