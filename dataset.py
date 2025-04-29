import json
import numpy as np
import os
from function.nltk_utils import OneHotEncoder

one_hot_encoder = OneHotEncoder()

class Dataset:
    def __init__(self, filename):
        # Initialize the dataset with the provided filename
        self.filename = filename 
        self.json_data = json.loads(open(os.path.join(os.getcwd(),self.filename + '.json'),'rt').read())
        self.words = []
        self.tags = []
        self.documents = []

        self.inputs = []
        self.outputs = []

        self.inputs_size = 0
        self.outputs_size = 0

        # Parse the data and create bags
        self.parse_data()
        self.create_bags()

    def parse_data(self):
        # Parse intent patterns and tags from the loaded JSON data
        for intent in self.json_data['intents']:
            tag = intent['tag']
            self.tags.append(tag)
            for pattern in intent['patterns']:
                word_list= one_hot_encoder.tokenize(pattern)
                self.words.extend(word_list)
                self.documents.append((word_list,tag))

        # Stem words and remove ignored letters
        self.words = [one_hot_encoder.stem(w) for w in self.words if w not in one_hot_encoder.ignore_letters]
        self.words = sorted(set(self.words))
        self.tags = sorted(set(self.tags))

    def create_bags(self):
        # Create bag-of-words representation for inputs and encode outputs
        for (pattern_sentence, tag) in self.documents:
            bag = one_hot_encoder.bag_of_words(pattern_sentence, self.words)
            self.inputs.append(bag)
            label = self.tags.index(tag)
            self.outputs.append(label)

        # Remove duplicates, convert to numpy arrays, and calculate sizes
        self.inputs = np.array(self.inputs)
        self.outputs = np.array(self.outputs)

        self.inputs_size = len(self.inputs[0])
        # self.outputs_size = len(self.outputs)
        self.outputs_size = len(self.tags)
    
    def get_data(self):
        # Return a dictionary containing dataset information
        res = {}
        res['data'] = self.json_data
        res['words'] = self.words
        res['tags'] = self.tags
        res['inputs'] = self.inputs
        res['outputs'] = self.outputs
        res['inputs_size'] = self.inputs_size
        res['outputs_size'] = self.outputs_size
        print(f"{self.filename} is loaded")
        return res
