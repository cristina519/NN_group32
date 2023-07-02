import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Masking
import glob
from keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences


def create_model(input_shape, output_shape):
    # Create a sequential model
    model = Sequential()
    # Add a masking layer to handle variable-length sequences
    model.add(Masking(mask_value=0.0, input_shape=(input_shape[0], input_shape[1])))
    # Add dense layers with ReLU activation
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    # Add a dense output layer with softmax activation
    model.add(Dense(output_shape, activation='softmax'))
    return model


def train_model(model, x_train, y_train, num_epochs=5):
    # Compile the model with categorical cross-entropy loss, Adam optimizer, and accuracy metric
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Train the model with the given training data for the specified number of epochs
    model.fit(x_train, y_train, epochs=num_epochs, batch_size=32)


def generate_sequence(model, initial_sequence, num_bars, num_beats):
    generated_sequence = []
    current_input = np.array(initial_sequence).reshape(-1)
    for _ in range(num_bars):
        # Predict the next output based on the current input
        output = model.predict(current_input.reshape(1, -1))
        # Transform the predicted output using a hypothesis function
        generated_output = transform_hypothesis(output[0])
        generated_sequence.append(generated_output)

        # Update the current input with the generated output
        current_input = np.concatenate((current_input[num_beats:], generated_output))
    return generated_sequence


def transform_hypothesis(hypothesis_vector, threshold=0.5, scaling_factor=4):
    transformed_vector = []
    for value in hypothesis_vector:
        # Apply sigmoid transformation to the values
        value = 1 / (1 + np.exp(-scaling_factor * (value - threshold)))
        transformed_vector.append(value)

    transformed_vector = np.array(transformed_vector)
    # Convert the transformed values to binary based on the threshold
    transformed_vector = np.where(transformed_vector >= threshold, 1, 0)
    return transformed_vector


def generate_drum_patterns(model, initial_input, num_patterns, num_beats):
    generated_patterns = []
    current_input = np.array(initial_input)

    for _ in range(num_patterns):
        # Predict the next pattern based on the current input
        output = model.predict(current_input.reshape(1, -1))
        generated_patterns.append(output[0])

        # Update the current input with the generated pattern
        current_input = np.concatenate((current_input[num_beats:], output))

    return generated_patterns


def save_sequence_to_txt(sequence, filename):
    with open(filename, 'w') as file:
        for bar in sequence:
            # Convert each beat to a string and join with spaces
            beat_groups = [str(beat) for beat in bar]
            formatted_bar = ' '.join(beat_groups)
            # Write the formatted bar to the file
            file.write(formatted_bar + '\n')


h = 1
input_shape = (h, 8)
output_shape = 8

# Step 1: Read TXT files and load binary sequences
file_paths = glob.glob('binary_files/*.txt')
sequences = []

for file_path in file_paths:
    with open(file_path, 'r') as file:
        content = file.read().strip()
        # Convert the content to a list of integers
        sequence = list(map(int, content.split(' ')))  # Splitting by space instead of '\n'
        sequences.append(sequence)  # Append each sequence as a separate sample

sequences = np.array(sequences, dtype=object)

x_train = []
y_train = []

# Step 2: Prepare the training data
for i in range(0, len(sequences) - h, h):
    x_train.append(sequences[i:i+h])
    y_train.append(sequences[i+h])

x_train = np.array(x_train, dtype=object).reshape(-1, h, 8)
y_train = np.array(y_train, dtype=object).reshape(-1, 8)

x_train = x_train.astype('float32')
y_train = y_train.astype('float32')

#I think something goes wrong when reading the data

# Step 3: Model Selection
model = create_model(input_shape, output_shape)


# Step 4: Network Training
train_model(model, x_train, y_train)


model.save("drum.h5")


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
