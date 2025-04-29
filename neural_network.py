import json
import os
import numpy as np


class NeuralNetwork:
    def __init__(self, n_inputs, n_neurons, n_outputs, filename=None):
        # Initialize neural network components
        self.layer1 = LayerDense(n_inputs, n_neurons)
        self.activation1 = ActivationReLU()
        self.layer2 = LayerDense(n_neurons, n_outputs)
        self.activation2 = ActivationSoftmax()
        self.loss_function = LossCategoricalCrossentropy()
        self.is_trained = False

        # Load the model from a file if a filename is provided
        if filename:
            self.load_from_file(filename)

    def load_from_file(self, filename):
        # Load model data from a JSON file
        fn = os.path.join(os.getcwd(), f"{filename}.json")
        if os.path.exists(fn):
            with open(fn, 'rt') as file:
                try:
                    json_data = json.load(file)
                    self.parse_json_data(json_data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
        else:
            print('New file is loaded.')

    def parse_json_data(self, json_data):
        try:
            # Extract layer weights and biases from JSON data
            layer1_data = json_data['data'][0]['layer1'][0]
            layer2_data = json_data['data'][1]['layer2'][0]

            if (
                np.shape(self.layer1.weight) == np.shape(np.array(layer1_data['weights'], dtype="float64")) and
                np.shape(self.layer1.bias) == np.shape(np.array(layer1_data['bias'], dtype="float64")) and
                np.shape(self.layer2.weight) == np.shape(np.array(layer2_data['weights'], dtype="float64")) and
                np.shape(self.layer2.bias) == np.shape(np.array(layer2_data['bias'], dtype="float64"))
            ):
                # Update the neural network with loaded weights and biases
                self.layer1.weight = np.array(layer1_data['weights'], dtype="float64")
                self.layer1.bias = np.array(layer1_data['bias'], dtype="float64")

                self.layer2.weight = np.array(layer2_data['weights'], dtype="float64")
                self.layer2.bias = np.array(layer2_data['bias'], dtype="float64")

                print('File loaded')
                self.is_trained = True
            else:
                print("Neural network has not been trained yet")
        except (KeyError, IndexError) as e:
            print(f"Error parsing JSON data: {e}")

    """
    The neural network's output is a list with a length matching that of the tags in data.json. 
    Each element in the list represents the percentage probability associated with its corresponding tag.
    Further information see chatbot Kiki documentation
    """
    def predict(self, question):
        # Perform forward propagation for prediction
        self.layer1.forward(question)
        self.activation1.forward(self.layer1.output)
        self.layer2.forward(self.activation1.output)
        self.activation2.forward(self.layer2.output)
        return self.activation2.output

    def train(self, inputs, outputs, num_epochs, filename=None, learning_rate=0.005, loss_rate=0.05, wait=20):
        """
        Train the neural network.

        Parameters:
        - inputs: Input data for training
        - outputs: Actual outputs for training
        - num_epochs: Number of training epochs
        - filename: Name of the file to save the trained model (optional)
        - learning_rate: Learning rate for gradient descent
        - loss_rate: Loss threshold for early stopping
        - wait: Patience for early stopping

        """
        if self.is_trained:
            print('Data has already been trained')
            return

        patience_counter = 0
        prev_loss = float('inf')
        losses = []

        for epoch in range(num_epochs):
            # Forward propagation
            self.layer1.forward(inputs)
            self.activation1.forward(self.layer1.output)
            self.layer2.forward(self.activation1.output)
            self.activation2.forward(self.layer2.output)

            # Loss calculation
            current_loss = self.loss_function.calculate(self.activation2.output, outputs)
            losses.append(current_loss)

            # Print progress bar
            self.print_progress_bar(loss_rate, current_loss, prefix='Training', suffix=f'Loss: {round(current_loss * 100, 2)}%')

            # Early stopping check
            if patience_counter >= wait or current_loss <= loss_rate:
                print('\nTraining complete')
                break
            
            if current_loss >= prev_loss and epoch != 0:
                patience_counter += 1
            else:
                patience_counter = 0

            prev_loss = current_loss

            # Backpropagation
            d_loss_respect_activation = self.loss_function.backward(self.activation2.output, outputs)
            d_activation_respect_layer = self.activation2.backward(outputs)

            d_loss_respect_activation = self.layer2.backward(
                d_loss_respect_activation, d_activation_respect_layer, outputs, True, learning_rate)

            d_activation_respect_layer = self.activation1.backward()
            self.layer1.backward(
                d_loss_respect_activation, d_activation_respect_layer, outputs, False, learning_rate)

        # Save the trained model if a filename is provided
        if filename:
            self.save_model_to_json(filename)

    def save_model_to_json(self, filename):
        # Save the model weights and biases to a JSON file
        fn = os.path.join(os.getcwd(), f"{filename}.json")

        layer1_data = {
            "weights": self.layer1.weight.tolist(),
            "bias": self.layer1.bias.tolist(),
        }
        layer2_data = {
            "weights": self.layer2.weight.tolist(),
            "bias": self.layer2.bias.tolist(),
        }

        model_data = {
            "data": [
                {"layer1": [layer1_data]},
                {"layer2": [layer2_data]}
            ]
        }

        with open(fn, 'w') as file:
            json.dump(model_data, file, indent=4)

        print(f'{filename}.json has been created')

    def print_progress_bar(self, iteration, total, prefix='', suffix='', length=50, fill='█'):
        # Print a progress bar with a fixed distance between elements
        percent = ("{0:.2f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        fixed_spacing = " " * 10
        print(f'{prefix} |{bar}| {percent if float(percent) <= 100 else 100}% {suffix}', fixed_spacing, end="\r")


class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        # Initialize dense layer with random weights and zero biases
        self.weight = 0.1 * np.random.randn(n_inputs, n_neurons)
        self.bias = np.zeros((1, n_neurons))

    def forward(self, inputs):
        # Perform forward propagation for the dense layer
        self.inputs = inputs
        self.output = np.dot(inputs, self.weight) + self.bias

    def backward(self, d_loss_respect_activation, d_activation_respect_layer, actual_output, get_derivative=False, learning_rate=0.005):
        """
        Perform backward propagation for the dense layer using chain rule.

        Parameters:
        - d_loss_respect_activation (numpy.ndarray): Gradient of the loss with respect to the layer's activation.
        - d_activation_respect_layer (numpy.ndarray): Gradient of the layer's activation with respect to its output.
        - actual_output (numpy.ndarray): True output labels.
        - get_derivative (bool): Flag indicating whether to compute the derivative.
        - learning_rate (float): Learning rate for weight and bias updates.

        Returns:
        - numpy.ndarray or None: If get_derivative is True, returns the gradient of the loss with respect to the layer's weights.
        Otherwise, returns None.

        Note:
        - The method updates the layer's weights and biases using the provided gradients and learning rate.
        
        Further detail see chatbot Kiki documentation
        """
        
        # Perform backward propagation for the dense layer using chain rule
        d_layer_respect_weight = self.inputs
        d_loss_respect_layer = d_loss_respect_activation * d_activation_respect_layer

        d_loss_respect_bias = np.sum(d_loss_respect_layer, axis=0)
        d_loss_respect_weight = np.dot(d_layer_respect_weight.T, d_loss_respect_layer)

        if get_derivative:
            d_layer_respect_activation = self.weight.T
            res = np.dot(d_loss_respect_layer, d_layer_respect_activation)
        else:
            res = None

        self.update(d_loss_respect_bias, d_loss_respect_weight, learning_rate)
        return res

    def update(self, d_loss_respect_bias, d_loss_respect_weight, learning_rate):
        # Update layer weights and biases
        step_size = d_loss_respect_bias.dot(learning_rate)
        self.bias = np.subtract(self.bias, step_size)

        step_size = d_loss_respect_weight.dot(learning_rate)
        self.weight = np.subtract(self.weight, step_size)


class ActivationReLU:
    def forward(self, inputs):
        # Forward pass: apply ReLU activation
        self.inputs = inputs
        self.output = np.maximum(0, inputs)

    def backward(self):
        # Backward pass: compute derivative of ReLU activation
        d_activation_respect_layer = np.zeros_like(self.inputs)
        for i, inp in enumerate(self.inputs):
            for j in range(len(self.inputs[0])):
                if inp[j] > 0:
                    d_activation_respect_layer[i, j] = 1
                else:
                    d_activation_respect_layer[i, j] = 0

        return d_activation_respect_layer


class ActivationSoftmax:
    def forward(self, inputs):
        # Forward pass: apply Softmax activation
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilities

    def backward(self, actual_output):
        # Backward pass: compute derivative of Softmax activation
        d_activation_layer = np.zeros_like(self.output)

        for i, p in enumerate(self.output):
            correct_output = p[actual_output[i]]
            for j in range(len(self.output[0])):
                if j == actual_output[i]:
                    d_activation_layer[i, j] = correct_output * (1 - correct_output)
                else:
                    d_activation_layer[i, j] = -correct_output * p[j]

        return d_activation_layer


class LossCategoricalCrossentropy:
    def forward(self, y_pred, y_true):
        # Forward pass: calculate categorical crossentropy loss
        samples = len(y_pred)
        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)
        correct_confidences = y_pred_clipped[[range(samples)], y_true]
        negative_log_likelihoods = -np.log(correct_confidences)
        return negative_log_likelihoods

    def backward(self, y_pred, y_true):
        # Backward pass: compute derivative of categorical crossentropy loss
        d_loss_respect_activation = np.zeros((len(y_true), 1))
        # Ensure numerical stability
        y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
        # Calculate the derivative for each element in the output vector
        for i in range(len(y_true)):
            d_loss_respect_activation[i] = -1.0 / (y_pred[i, y_true[i]])

        return d_loss_respect_activation

    def calculate(self, output, y):
        # Calculate categorical crossentropy loss
        sample_losses = self.forward(output, y)
        data_loss = np.mean(sample_losses)
        return data_loss
