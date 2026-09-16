"""
Creates a minimal placeholder CNN model compatible with the current
preprocessing pipeline (input: Mel-spectrogram with shape [128, 94, 1]).
Run this once if you don't have a trained model yet.
The model will always predict "neutral" until you train a real one.
"""
import os
import numpy as np

def create_placeholder_model():
    try:
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization

        print("🏗️  Building placeholder model architecture...")

        # This must match the output of extract_features() in preprocessing.py
        # Mel-spectrogram: (N_MELS=128, time_steps, 1)
        # time_steps = ceil(SAMPLES_PER_TRACK / HOP_LENGTH) = ceil(48000 / 512) = 94
        INPUT_SHAPE = (128, 94, 1)
        NUM_CLASSES = 8

        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=INPUT_SHAPE),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.25),

            Conv2D(64, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.25),

            Conv2D(128, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.3),

            Flatten(),
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(NUM_CLASSES, activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        os.makedirs("models", exist_ok=True)
        model.save("models/surakshavaani_final.h5")
        print("✅ Placeholder model saved to models/surakshavaani_final.h5")
        print("⚠️  NOTE: This model is untrained and will give random predictions.")
        print("   Train it with train.py after downloading RAVDESS dataset for real results.")
        model.summary()
        return True
    except Exception as e:
        print(f"❌ Error creating model: {e}")
        return False

if __name__ == "__main__":
    create_placeholder_model()
