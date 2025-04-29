# Import necessary libraries and modules
import datetime
import json
import random
import numpy as np
from function.nltk_utils import OneHotEncoder
from function.search import SearchEngine
from function.date_time_name import DateTimeName
from function.weather import WeatherForecast
from function.user_data import UserData
from function.stock import YahooStockScraper
from function.news import NewsScraper
from function.math import Calculator
from function.language import LanguageManager

# Instantiate necessary objects
one_hot_encoder = OneHotEncoder()
stock_scraper = YahooStockScraper()
wikipedia = SearchEngine()

# Define the Chatbot class
class Chatbot:
    def __init__(self, neural_networks, json_data, words, tags, error_threshold=0.8, language="en", filename = None):
        # Initialize Chatbot with neural networks, JSON data, words, tags, error threshold, and language
        self.nn = neural_networks
        self.json_data = json_data
        self.words = words
        self.tags = tags
        self.error_threshold = error_threshold
        self.user = UserData()
        global text_manager
        text_manager = LanguageManager(language)
        self.language = language

        # beta
        self.filename = filename


    def run(self):
        # Main method to run the chatbot
        self.introduction()
        response_handler = ResponseHandler()
        noanswer_list = {}

        while True:
            # Get user input, encode it, and get a response
            prediction, message = self.encode_input()
            response, current_tags = self.get_response(prediction)

            # Handle different scenarios based on tags in the response
            if 'goodbye' in current_tags:
                if response_handler.handle_goodbye():
                    # beta
                    choice = input("would you like to help us to improve the data? (Y/N): ")
                    if choice.lower() == "y":
                        response_handler.handle_improve_data(noanswer_list, self.tags, self.json_data, self.filename)

                    break
                else:
                    continue

            if 'search' in current_tags:
                response_handler.handle_search()

            elif 'datetime' in current_tags:
                response_handler.print_current_datetime()

            elif 'math' in current_tags:
                response_handler.handle_math()

            elif 'weather' in current_tags:
                response_handler.handle_weather()

            elif "planning" in current_tags:
                response_handler.handle_plan(self.user)

            elif "stock" in current_tags:
                response_handler.handle_stock()

            elif "news" in current_tags:
                response_handler.handle_news()

            elif "user_info" in current_tags:
                response_handler.handle_user_info(self.user)

            elif not response or 'noanswer' in current_tags:
                noanswer_list[message] = prediction[0]
                response_handler.handle_no_answer()

            # beta
            elif 'improve' in current_tags:
                response_handler.handle_improve_data(noanswer_list, self.tags, self.json_data, self.filename)
                        
            else:
                print(Chatbot.kiki_response(str(response)))

    def introduction(self):
        # Method to handle the introduction and user information
        name = input(Chatbot.kiki_response("INTRODUCTION"))
        response = self.user.check_name(name)
        if response:
            print(Chatbot.kiki_response("NICE_TO_SEE_AGAIN", name=name))
        else:
            age = self.get_user_age()
            hobby = input(Chatbot.kiki_response("WHAT_YOUR_HOBBY"))
            data = {
                'Name': name,
                'Age': age,
                'hobby': hobby
            }
            self.user.save_data("Users", data)
            print(Chatbot.kiki_response("GREETING_MESSAGE", name=name))

    def get_response(self, prediction):
        # Method to get the appropriate response based on predictions
        response = None
        current_tags = []
        for i, r in enumerate(prediction[0]):
            if r > self.error_threshold:
                for intent in self.json_data['intents']:
                    if intent['tag'] == self.tags[i]:
                        current_tags.append(intent['tag'])
                        response = random.choice(intent['responses'])
                        break

        return response, current_tags

    def encode_input(self):
        """
        Method to encode user input for processing.

        Returns:
            int: The predicted category for the user input.
        """
        # Method to encode user input for processing
        message_list = []
        message = input(f'{self.user.name}: ')
        # word tokenizing
        word_list = one_hot_encoder.tokenize(message)
        message_list.extend(word_list)
        # word stemming
        message_list = [one_hot_encoder.stem(w) for w in message_list if w not in one_hot_encoder.ignore_letters]
        bag = one_hot_encoder.bag_of_words(message_list, self.words)
        prediction = self.nn.predict(np.array(bag))

        return prediction, message

    @staticmethod
    def kiki_response(key, **kwargs):
        # Static method to format Kiki's response
        return f'\033[35m{"Kiki:" } {text_manager.get_text(key,**kwargs)}\033[0m'

    @staticmethod
    def get_user_age():
        # Static method to get and validate user age
        while True:
            try:
                age = int(input(Chatbot.kiki_response("AGE_PROMPT")))
                if 0 < age < 150:  # Assuming a reasonable age range
                    return age
                else:
                    print(Chatbot.kiki_response("AGE_INVALID"))
            except ValueError:
                print(Chatbot.kiki_response("AGE_INVALID"))

# Define the ResponseHandler class
class ResponseHandler:
    @staticmethod
    def handle_user_info(user):
        user_info = user.show_user_info()[0]
        print(Chatbot.kiki_response("USER_INFO_LIST", name=user_info[1], age=user_info[2], hobby = user_info[3]))


    # beta
    # TODO add a specific class
    @staticmethod
    def handle_improve_data(noanswer_list, tags, json_data, filename):
        """
        This method handles the improvement of data by interacting with the user to confirm or correct tags for unanswered questions.

        :param noanswer_list: A dictionary containing unanswered questions and corresponding predictions.
        :param tags: A list of tags.
        :param json_data: The JSON data structure containing intents, patterns, and responses.
        :param filename: The name of the file to which the updated JSON data will be written.
        """
        print("This is the beta version of the data improving function...")
        
        # Check if there are no unanswered questions
        if not noanswer_list:
            return

        next = True
        # Iterate over unanswered questions and predictions
        for question, prediction in noanswer_list.items():
            # Identify the top three possible tags based on prediction
            possible_tags_list = sorted(range(len(prediction)), key=lambda sub: prediction[sub],reverse=True)[:3]
            
            # Ask the user to confirm if the question belongs to one of the possible tags
            for possible_tag in possible_tags_list:
                choice = input(f"Is '{question}' a type of {tags[possible_tag]}? (Y/N): ")
                if choice.lower() == "y":
                    # If confirmed, add the pattern to the corresponding intent
                    ResponseHandler.add_pattern_to_intent(json_data, tags[possible_tag], question)
                    next = False
                    break
            
            if next:
                # Display the current tags
                for i, tag in enumerate(tags,start=1):
                    print(f'{i}) {tag}')
                
                # Prompt the user to indicate the correct tag for the question or add a new tag
                while True:
                    choice = input(f"Indicate the correct 'tag' for question '{question}' "
                                "\n(press the number of the item, or press 'N' to add a new tag): ")

                    try:
                        if 1 <= int(choice) <= len(tags):
                            # If a number is entered, add the pattern to the corresponding intent
                            ResponseHandler.add_pattern_to_intent(json_data, tags[int(choice) - 1], question)
                            break
                        else:
                            print("The value is incorrect.")
                    except ValueError:
                        if choice.lower() == 'n':
                            # If 'N' is entered, add a new tag
                            ResponseHandler.add_new_tag(json_data, tags, question, filename)
                            break
                        else:
                            print("Invalid input. Please enter a number or 'N'.")

        print("Thank you!")
        # Write the updated JSON data back to the file
        with open(filename + ".json", 'w') as file:
            file.write(json.dumps(json_data))

    # Beta
    @staticmethod
    def add_pattern_to_intent(json_data, tag, question):
        """
        Add a pattern to the intent with the specified tag in the given JSON data.

        :param json_data: The JSON data structure containing intents, patterns, and responses.
        :param tag: The tag of the intent to which the pattern will be added.
        :param question: The question pattern to be added.
        """
        for intent in json_data['intents']:
            if intent['tag'] == tag:
                intent['patterns'].append(question)
                break

    # Beta
    @staticmethod
    def add_new_tag(json_data, tags, question, filename):
        """
        Add a new tag, along with a pattern and user-defined responses, to the given JSON data.

        :param json_data: The JSON data structure containing intents, patterns, and responses.
        :param tags: A list of tags.
        :param question: The question pattern associated with the new tag.
        :param filename: The name of the file to which the updated JSON data will be written.
        """
        new_tag = input("Enter the name of the new tag: ")
        num_response = int(input("How many responses do you want to create?: "))
        response = []

        # Collect user-defined responses
        for i in range(num_response):
            res = input(f"Enter the response {i + 1}: ")
            response.append(res)

        # Create a new data structure for the new tag
        new_data = {
            "tag": new_tag,
            "patterns": [question],
            "responses": response
        }

        # Append the new data to the intents list in the JSON data
        json_data['intents'].append(new_data)


    @staticmethod
    def handle_goodbye():
        # Method to handle the user's goodbye input
        exit_choice = input(Chatbot.kiki_response("EXIT_CONFIRMATION"))
        if exit_choice.lower() == 'y':
            print(Chatbot.kiki_response("EXIT_MESSAGE"))
            return True
        else:
            print(Chatbot.kiki_response("HELP_MESSAGE"))
            return False

    @staticmethod
    def handle_search():
        # Method to handle user search input
        detail = input(Chatbot.kiki_response("SEARCH_PROMPT"))
        result = wikipedia.search(detail)
        if result:
            print(Chatbot.kiki_response(result))
        else:
            print(Chatbot.kiki_response("SEARCH_ERROR"))

    @staticmethod
    def handle_no_answer():
        # Method to handle scenarios with no valid response
        msg = random.choice(text_manager.get_text("NO_ANSWER_RESPONSES"))
        print(Chatbot.kiki_response(msg))

    @staticmethod
    def handle_math():
        """
        Handles mathematical calculations based on user input.

        This method prompts the user for a mathematical expression or formula,
        performs the corresponding calculation, and prints the result.

        The supported calculations include duration, net present value (NPV),
        future value (FV), and generic arithmetic expressions.

        """
        # Method to handle mathematical calculations
        expr = input(Chatbot.kiki_response("MATH_EXPRESSION_PROMPT"))
        if expr.lower() == "f":
            formula = input(Chatbot.kiki_response("MATH_CALCULATION_PROMPT")).lower()
            if formula == 'd':
                try:
                    interest = float(input(Chatbot.kiki_response("DURATION_INTEREST_RATE"))) / 100
                    face_value = float(input(Chatbot.kiki_response("DURATION_FACE_VALUE")))
                    time = int(input(Chatbot.kiki_response("DURATION_NUM_OF_YEARS")))
                    coupon_rate = float(input(Chatbot.kiki_response("DURATION_COUPON_RATE"))) / 100
                    duration = Calculator.calculate_duration(interest, face_value, time, coupon_rate)
                    print(Chatbot.kiki_response("DURATION_RESULT", duration=round(duration, 2)))
                except (ValueError, ZeroDivisionError):
                    print(Chatbot.kiki_response("INVALID_INPUT_MESSAGE"))
                except Exception as e:
                    print(Chatbot.kiki_response("ERROR_OCCURRED_MESSAGE"))
            elif formula == 'n':
                try:
                    initial_investment = float(input(Chatbot.kiki_response("NPV_INITIAL_INVESTMENT")))
                    time = int(input(Chatbot.kiki_response("NPV_NUM_OF_YEARS")))
                    cost_capital = float(input(Chatbot.kiki_response("NPV_COST_OF_CAPITAL"))) / 100
                    cash_flow = [float(input(Chatbot.kiki_response("NPV_CASH_FLOW", num_year=i + 1))) for i in
                                 range(time)]
                    npv = Calculator.calculate_npv(initial_investment, time, cost_capital, cash_flow)
                    print(Chatbot.kiki_response("NPV_RESULT", npv=round(npv, 2)))
                except (ValueError, ZeroDivisionError):
                    print(Chatbot.kiki_response("INVALID_INPUT_MESSAGE"))
                except Exception as e:
                    print(Chatbot.kiki_response("ERROR_OCCURRED_MESSAGE"))
            elif formula == 'f':
                try:
                    interest = float(input(Chatbot.kiki_response("FV_INTEREST_RATE"))) / 100
                    time = int(input(Chatbot.kiki_response("FV_NUM_OF_YEARS")))
                    pv = float(input(Chatbot.kiki_response("FV_PRESENT_VALUE")))
                    fv = Calculator.calculate_fv(interest, time, pv)
                    print(Chatbot.kiki_response("FV_RESULT", fv=round(fv, 2)))
                except (ValueError, ZeroDivisionError):
                    print(Chatbot.kiki_response("INVALID_INPUT_MESSAGE"))
                except Exception as e:
                    print(Chatbot.kiki_response("ERROR_OCCURRED_MESSAGE"))
        else:
            try:
                print(Chatbot.kiki_response("CALCULATION_RESULT", res=eval(expr)))
            except:
                print(Chatbot.kiki_response("ERROR_OCCURRED_MESSAGE"))

    @staticmethod
    def handle_plan(user):
        """
        Handles user planning input, allowing users to view, add, and delete plans.

        Args:
        - user (UserData): The UserData instance associated with the current user.

        """
        # Method to handle user planning input
        list_plan = user.show_plan()
        num_items = str(len(list_plan))
        print(Chatbot.kiki_response("PLAN_LIST_HEADER", num_items=num_items))

        for i, p in enumerate(list_plan):
            print(Chatbot.kiki_response("PLAN_LIST_CONTENT", index=i + 1, p=p))
        status = input(Chatbot.kiki_response("PLAN_LIST_PROMPT"))

        if status.lower() == 'a':
            desc = input(Chatbot.kiki_response("ADD_PLAN_PROMPT"))
            while True:
                date = input(Chatbot.kiki_response("ADD_PLAN_DATE_PROMPT"))
                try:
                    # Attempt to convert the input to a datetime object
                    date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
                    break  # Break the loop if the conversion is successful
                except ValueError:
                    print(Chatbot.kiki_response("INVALID_INPUT_MESSAGE"))
            if user.add_plan(desc, date):
                print(Chatbot.kiki_response("PLAN_ADDED_MESSAGE"))

        if status.lower() == 'd':
            num = int(input(Chatbot.kiki_response("DELETE_PLAN_PROMPT")))
            if 1 <= num <= len(list_plan):
                item = list_plan[num - 1]
                if user.delete_plan(item):
                    response = Chatbot.kiki_response("PLAN_DELETED_MESSAGE", num=num, item=item)
                else:
                    response = Chatbot.kiki_response("ERROR_OCCURRED_MESSAGE")
                print(response)
            else:
                print(Chatbot.kiki_response("INVALID_INPUT_MESSAGE"))

    @staticmethod
    def handle_stock():
        # Method to handle user stock-related input
        name = input(Chatbot.kiki_response("STOCK_NAME_PROMPT"))

        # First attempt to get stock information
        symbol, response = stock_scraper.get_stock(name)

        if response:
            # Display the summary
            # response = f'For {name} ({symbol}), here is the summary:\n\n' + response
            print(Chatbot.kiki_response("STOCK_SUMMARY_MESSAGE", name=name, symbol=symbol, summary=response))
        else:
            print(Chatbot.kiki_response("STOCK_NOT_FOUND_MESSAGE"))

    @staticmethod
    def print_current_datetime():
        # Method to print the current date and time
        d = datetime.datetime.now()
        print(Chatbot.kiki_response("CURRENT_DATETIME_MESSAGE", weekday=DateTimeName.get_weekday(d.weekday()),
                                    month=DateTimeName.get_month(d.month), day=d.day, year=d.year, hour=d.hour,
                                    minute=d.minute))

    @staticmethod
    def handle_weather():
        # Method to handle user weather-related input
        # TODO prediction for the week
        wf = WeatherForecast()
        city = input(Chatbot.kiki_response('WEATHER_CITY_PROMPT'))
        high_temp, low_temp, ave_pre, ave_wind = wf.get_weather(city)
        if high_temp or low_temp or ave_pre or ave_wind:
            print(Chatbot.kiki_response("WEATHER_INFO_MESSAGE", city=city, low_temp=low_temp, high_temp=high_temp,
                                        ave_pre=round(ave_pre, 2), ave_wind=round(ave_wind, 2)))
        else:
            print(Chatbot.kiki_response("WEATHER_EROOR",city=city))

    @staticmethod
    def handle_news():
        # Method to handle user news-related input
        num = int(input(Chatbot.kiki_response("NEWS_ITEMS_PROMPT")))
        num, news = NewsScraper.get_news(num)
        print(Chatbot.kiki_response("NEWS_RESULT_MESSAGE", num=num, news=news))

