import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Masking
import glob
from keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences

model = model.compile(Model1.h5)
# Step 5: Autonomous Generation
initial_sequence = [[1,1,1,0,1,0,1,0], [1,1,1,1,1,1,1,1], [1,1,1,1,1,1,1,1], [1,1,1,1,1,0,1,0], [1,1,1,1,0,1,1,1], [1,1,1,1,1,1,1,1], [1,1,1,1,1,1,0,1]]
initial_sequence = np.array(initial_sequence).reshape(-1, h, 8)  # Reshape initial sequence to match the model input shape
num_bars = 8
num_beats = 3
generated_sequence = generate_sequence(model, initial_sequence, num_bars, num_beats)

# Step 6: Decision-making Algorithm
transformed_sequence = [transform_hypothesis(bar) for bar in generated_sequence]

# Step 7: Feedback Loop
initial_input = np.array(initial_sequence).reshape(-1, h, 8)  # Reshape initial sequence to match the model input shape
num_patterns = 32
generated_patterns = generate_drum_patterns(model, initial_input, num_patterns, num_beats)
save_sequence_to_txt(generated_sequence, "generated.txt")
