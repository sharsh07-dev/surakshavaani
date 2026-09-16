"""
Emotion Prediction Post-Processor
Improves accuracy by applying acoustic feature-based corrections
to distinguish between commonly confused emotions (especially Anger vs Fear)
"""

import numpy as np
import librosa

def analyze_acoustic_features(y, sr=16000):
    """
    Extract discriminative acoustic features to help distinguish emotions.
    Returns a feature dictionary.
    """
    features = {}
    
    # 1. Pitch Analysis (Anger: sustained high pitch, Fear: erratic pitch)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitch_values.append(pitch)
    
    if len(pitch_values) > 0:
        features['pitch_mean'] = np.mean(pitch_values)
        features['pitch_std'] = np.std(pitch_values)
        features['pitch_range'] = np.max(pitch_values) - np.min(pitch_values)
    else:
        features['pitch_mean'] = 0
        features['pitch_std'] = 0
        features['pitch_range'] = 0
    
    # 2. Energy/Loudness (Anger: consistently loud, Fear: variable)
    rms = librosa.feature.rms(y=y)[0]
    features['energy_mean'] = np.mean(rms)
    features['energy_std'] = np.std(rms)
    features['energy_max'] = np.max(rms)
    
    # 3. Zero Crossing Rate (Anger: higher, Fear: moderate)
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    features['zcr_mean'] = np.mean(zcr)
    
    # 4. Spectral Centroid (Anger: higher frequencies, Fear: mid frequencies)
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    features['spectral_centroid_mean'] = np.mean(spectral_centroids)
    
    return features


def correct_emotion_prediction(predicted_emotion, confidence, audio_signal, sr=16000):
    """
    Post-processes emotion predictions using acoustic features.
    Specifically helps distinguish between Anger and Fear.
    
    Args:
        predicted_emotion: String emotion from model
        confidence: Model confidence (0-1)
        audio_signal: Raw audio numpy array
        sr: Sample rate
    
    Returns:
        corrected_emotion, corrected_confidence
    """
    # Only apply correction for low-medium confidence predictions
    # or when dealing with commonly confused emotions
    if confidence > 0.85:
        return predicted_emotion, confidence
    
    features = analyze_acoustic_features(audio_signal, sr)
    
    # Correction Rules based on acoustic analysis
    
    # RULE 1: Anger vs Fear distinction
    if predicted_emotion in ['fear', 'angry']:
        # Anger characteristics:
        # - High sustained pitch (less variation)
        # - Consistently high energy
        # - Higher zero crossing rate
        # - Higher spectral centroid
        
        anger_score = 0
        fear_score = 0
        
        # Pitch stability (anger is more stable)
        if features['pitch_std'] < 50:  # Low variation
            anger_score += 2
        else:
            fear_score += 2
        
        # Energy consistency (anger is more consistent)
        if features['energy_std'] < 0.02:
            anger_score += 2
        else:
            fear_score += 1
        
        # High energy (both can be high, but anger is more sustained)
        if features['energy_mean'] > 0.05:
            anger_score += 1
            fear_score += 1
        
        # Zero crossing rate (anger tends to be higher)
        if features['zcr_mean'] > 0.1:
            anger_score += 2
        else:
            fear_score += 1
        
        # Spectral centroid (anger has sharper, higher frequencies)
        if features['spectral_centroid_mean'] > 2000:
            anger_score += 2
        else:
            fear_score += 1
        
        # Make correction if scores are significantly different
        if anger_score > fear_score + 2:
            return 'angry', min(confidence + 0.1, 0.95)
        elif fear_score > anger_score + 2:
            return 'fear', min(confidence + 0.1, 0.95)
    
    # RULE 2: Surprise vs Fear (both have sudden changes)
    if predicted_emotion in ['surprise', 'fear']:
        # Surprise: sudden onset, shorter duration of high energy
        # Fear: sustained tension
        
        if features['energy_std'] > 0.03:  # High variation suggests surprise
            if predicted_emotion == 'fear':
                return 'surprise', min(confidence + 0.05, 0.9)
    
    # RULE 3: Sad vs Calm (both low energy)
    if predicted_emotion in ['sad', 'calm']:
        # Sad: slightly higher pitch variation (crying/sobbing)
        if features['pitch_std'] > 30:
            return 'sad', min(confidence + 0.05, 0.9)
        else:
            return 'calm', min(confidence + 0.05, 0.9)
    
    # No correction needed
    return predicted_emotion, confidence
