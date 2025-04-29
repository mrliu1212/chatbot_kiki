# Kiki – AI Chatbot for Students

Kiki is an intelligent chatbot developed to support students, particularly in the field of economics. It provides a conversational interface to assist users with educational and utility-based tasks such as financial calculations, retrieving news, checking stock data, managing personal tasks, and more. Kiki is built using a neural network architecture and natural language processing techniques.

## Features

Kiki is capable of understanding user input and performing the following tasks:

- Solve basic and financial math problems (e.g., Duration, Net Present Value, Future Value)
- Retrieve the latest news using Google News scraping
- Fetch stock summaries using NASDAQ data and Yahoo Finance
- Manage personal to-do tasks (add, view, delete)
- Perform Wikipedia searches
- Provide current date and time information
- Display weather information using Open-Meteo API
- Handle greetings, farewells, and general small talk

## Getting Started

### Prerequisites

Before running the project, install the following Python packages:

```bash
pip install nltk numpy requests bs4
```

Note: `sqlite3` is included by default in Python.

### Running the Chatbot

To start the chatbot, use the following command in your terminal:

```bash
python run.py
```

Make sure your terminal path is set to the root of the Kiki project directory.

- Upon starting, select a language (English or Italian).
- On the first run, Kiki will train its neural network, which may take a few moments.
- The chatbot will then prompt for your name, age, and hobby.
- Once setup is complete, you can begin chatting with Kiki.

## Project Structure

```
├── run.py                # Main program entry point
├── chatbot.py            # Main chatbot logic
├── neural_network.py     # Neural network implementation
├── dataset.py            # Data loading and preprocessing
├── function/             # Functional modules
│   ├── date_time_name.py
│   ├── math.py
│   ├── news.py
│   ├── nltk_utils.py
│   ├── search.py
│   ├── stock.py
│   ├── user_data.py
│   └── weather.py
├── data/
│   ├── nn/               # Neural network weights and biases
│   ├── stock/            # NASDAQ company list CSV
│   └── training/         # Intents and training data (data.json)
├── database/
│   └── chatbot.db        # SQLite database for user info
```

## Example Interactions

- Weather: "What is the weather in Milan?"
- News: "Tell me the latest news."
- Stock: "Show me information about Apple."
- Tasks: "Add a new study plan" or "Delete task 2"
- Time: "What time is it now?"
- Search: "Who is John Maynard Keynes?"
- Math: "Calculate NPV of an investment"
- Exit: "bye" or "exit"

## Beta Features

Several features are in development and may contain bugs:

- Handling language-specific responses
- Identifying and improving unanswered questions
- Enhancing the dataset for better intent classification

## Future Development (Kiki 2.0)

To address more complex interactions and improve performance, future versions of Kiki may implement advanced architectures such as Recurrent Neural Networks (RNN) and Long Short-Term Memory (LSTM) networks. These improvements aim to enhance the chatbot’s capabilities in natural language understanding.

## Theoretical Insights

Kiki’s neural network is trained using backpropagation and utilizes the softmax function in combination with cross-entropy loss. Outputs represent probabilities of various intent tags from the dataset.

## Reference Material

- [Neural Networks – StatQuest with Josh Starmer (Part 1)](https://www.youtube.com/watch?v=xBEh66V9gZo)
- [Softmax and Cross Entropy – StatQuest](https://www.youtube.com/watch?v=M59JElEPgIg)

## License

This project is intended for educational and research purposes.

## Author

Developed by economics students passionate about machine learning and natural language processing.
