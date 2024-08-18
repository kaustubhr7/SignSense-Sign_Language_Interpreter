import os
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

DATA_PATH = os.path.join('MP_Data')
# Actions
actions = np.array(['hello', 'thanks', 'iloveyou'])
# Number of sequences
no_sequences = 30
# Sequence length
sequence_length = 30
label_map = {label: num for num, label in enumerate(actions)}

sequences, labels = [], []
for action in actions:
    for sequence in range(no_sequences):
        window = []
        for frame_num in range(sequence_length):
            file_path = os.path.join(DATA_PATH, action, str(sequence), f"{frame_num}.npy")
            if os.path.exists(file_path):
                try:
                    res = np.load(file_path)
                    if res.size == 0:
                        raise ValueError(f"File is empty: {file_path}")
                    window.append(res)
                except (FileNotFoundError, EOFError, ValueError) as e:
                    print(f"Error loading file: {file_path}. Error: {e}")
                    break
            else:
                print(f"File not found: {file_path}")
                break
        if len(window) == sequence_length:
            sequences.append(window)
            labels.append(label_map[action])

X = np.array(sequences)
y = tf.keras.utils.to_categorical(labels, num_classes=len(actions))

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

log_dir = os.path.join('Logs')
tb_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

model = tf.keras.Sequential([
    tf.keras.layers.LSTM(64, return_sequences=True, activation='tanh', input_shape=(sequence_length, X.shape[2])),
    tf.keras.layers.LSTM(128, return_sequences=True, activation='tanh'),
    tf.keras.layers.LSTM(64, return_sequences=False, activation='tanh'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(len(actions), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

model.fit(x_train, y_train, epochs=2000, callbacks=[tb_callback])
model.summary()

# Predicting and evaluating the model
res = model.predict(x_test)

# Print results for the first test sample
print(f"Predicted: {actions[np.argmax(res[0])]}")  # Use res[0] to access the prediction for the first sample
print(f"Actual: {actions[np.argmax(y_test[0])]}")  # Use y_test[0] to access the actual label for the first sample

model.save('action.h5')
