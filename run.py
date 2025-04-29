from neural_network import NeuralNetwork
from dataset import Dataset
from chatbot import Chatbot

def train_and_run_chatbot(language, data_path, nn_filename, chatbot_filename):
    dataset = Dataset(data_path)
    json_data = dataset.get_data()

    nn = NeuralNetwork(n_inputs=json_data['inputs_size'], n_neurons=100, n_outputs=json_data['outputs_size'], filename=nn_filename)
    nn.train(inputs=json_data['inputs'], outputs=json_data['outputs'], num_epochs=10000, filename=nn_filename, learning_rate=0.005, loss_rate=0.01)

    # chatbot_filename beta, need to do improvement
    chat = Chatbot(neural_networks=nn, json_data=json_data['data'], words=json_data['words'], tags=json_data['tags'], error_threshold=0.7, language=language, filename=chatbot_filename)
    chat.run()

def main():
    ENGLISH = 'E'
    ITALIAN = 'I'
    
    while True:
        lang = input("Which language do you speak? (press '{}' for English, '{}' for Italian): ".format(ENGLISH, ITALIAN))

        if lang.lower() == ENGLISH.lower():
            train_and_run_chatbot('en', 'data/training/en/data', 'data/nn/en/data', 'data/training/en/data')
            break
        elif lang.lower() == ITALIAN.lower():
            train_and_run_chatbot('it', 'data/training/it/data', 'data/nn/it/data', 'data/training/it/data')
            break
        else:
            print('Please press the correct letter.')

main()
