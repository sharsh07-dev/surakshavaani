import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, GlobalAveragePooling2D, Multiply, Reshape, Input
from tensorflow.keras.optimizers import Adam
from .config import N_MELS

def create_surakshavaani_cnn(input_shape):
    """
    Enhanced CNN model with multi-feature input and attention mechanism.
    Optimized for distinguishing between similar emotions (Anger vs Fear).
    Input Shape: (N_MELS, Time_Steps, 4) - 4 channels for different features
    """
    inputs = Input(shape=input_shape)
    
    # Block 1 - Initial feature extraction
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
    x = BatchNormalization()(x)
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.25)(x)

    # Block 2 - Deeper feature learning
    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.25)(x)

    # Block 3 - High-level patterns
    x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.3)(x)
    
    # Block 4 - Fine-grained emotion features
    x = Conv2D(512, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.3)(x)
    
    # Attention Mechanism - Focus on discriminative features
    # This helps the model focus on the differences between anger and fear
    attention = GlobalAveragePooling2D()(x)
    attention = Dense(512, activation='relu')(attention)
    attention = Dense(x.shape[-1], activation='sigmoid')(attention)
    attention = Reshape((1, 1, x.shape[-1]))(attention)
    x = Multiply()([x, attention])
    
    # Global pooling and classification
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    
    x = Dense(256, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.4)(x)
    
    # Output Layer (8 Classes: Neutral, Calm, Happy, Sad, Angry, Fear, Disgust, Surprise)
    outputs = Dense(8, activation='softmax')(x)
    
    model = Model(inputs=inputs, outputs=outputs)

    # Compile with a lower learning rate for stability
    optimizer = Adam(learning_rate=0.0001)
    
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model