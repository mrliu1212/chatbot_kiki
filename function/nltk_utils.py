import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer

# Download the 'punkt' tokenizer for tokenization
# This is only required for the first-time usage
nltk.download("punkt")

class OneHotEncoder:
    def __init__(self) -> None:
        """
    OneHotEncoder class for tokenizing and creating a bag of words representation.

    Attributes:
        stemmer (PorterStemmer): NLTK Porter Stemmer for word stemming.
        ignore_letters (list): List of characters to ignore during tokenization.

    Methods:
        tokenize(sentence): Tokenizes a sentence using NLTK's word_tokenize.
        stem(word): Stems a word using NLTK's Porter Stemmer.
        bag_of_words(pattern_sentence, words): Creates a bag of words representation for a pattern sentence.

    """
        # Initialize the Porter Stemmer for word stemming
        self.stemmer = PorterStemmer()

        # Define characters to be ignored during tokenization
        self.ignore_letters = [',', '.', '!', '?']

    def tokenize(self, sentence):
        """
        Tokenizes a sentence using NLTK's word_tokenize.

        Args:
            sentence (str): Input sentence to be tokenized.

        Returns:
            list: List of tokens extracted from the input sentence.

        """
        return nltk.word_tokenize(sentence)

    def stem(self, word):
        """
        Stems a word using NLTK's Porter Stemmer.

        Args:
            word (str): Input word to be stemmed.

        Returns:
            str: Stemmed version of the input word.

        """
        return self.stemmer.stem(word.lower())

    def bag_of_words(self, pattern_sentence, words):
        """
        Creates a bag of words representation for a pattern sentence.

        Args:
            pattern_sentence (list): List of tokens from a pattern sentence.
            words (list): List of unique words in the entire dataset.

        Returns:
            numpy.ndarray: Bag of words representation for the pattern sentence.

        """
        # Initialize a zero-filled array for the bag of words
        bag = np.zeros(len(words), dtype=np.float32)

        # Stem the words in the pattern sentence
        pattern_sentence = [self.stem(w) for w in pattern_sentence]

        # Fill the bag of words based on the presence of words in the pattern sentence
        for i, word in enumerate(words):
            if word in pattern_sentence:
                bag[i] = 1.00

        return bag
