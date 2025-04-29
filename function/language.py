
# beta
class LanguageManager:
    """
    A class to manage language-specific texts.

    Attributes:
        TEXTS (dict): A dictionary containing language-specific texts.
        language (str): The current language.

    Methods:
        __init__(self, language): Initializes the LanguageManager with the specified language.
        get_text(self, key, **kwargs): Retrieves a text for the given key and replaces placeholders with provided values.

    Example:
        manager = LanguageManager('en')
        greeting_message = manager.get_text('GREETING_MESSAGE', name='John')
        print(greeting_message)  # Output: "Hello John! How can I help you?"

    """
    TEXTS = {
        'en': {
            'INTRODUCTION': "Hi! What's your name?: ",
            'NICE_TO_SEE_AGAIN': "Nice to see you again {name}! How can I help you?",
            'WHAT_YOUR_HOBBY': "Which is your hobby?: ",
            'GREETING_MESSAGE': "Hello {name}! How can I help you?",
            'EXIT_CONFIRMATION': "Do you want to exit? (Y/N): ",
            'EXIT_MESSAGE': "Goodbye!",
            'HELP_MESSAGE': "Okay, how can I help you further?",
            'SEARCH_PROMPT': "Could you provide specific details about what you're seeking?: ",
            'SEARCH_ERROR': "I am sorry, I can't find anything...",
            'NO_ANSWER_RESPONSES': [
                "Sorry, can't understand you",
                "Not sure I understand"
            ],
            'MATH_EXPRESSION_PROMPT': "Enter your expression (press 'F' for financial math): ",
            'MATH_CALCULATION_PROMPT': "What do you want to calculate? (press 'D' for for duration, 'N' for NPV, 'F' for future value): ",
            'INVALID_INPUT_MESSAGE': "Invalid input. Please enter valid value.",
            'ERROR_OCCURRED_MESSAGE': "An error occurred",
            'PLAN_LIST_HEADER': "You have {num_items} item(s) of plan: ",
            'PLAN_LIST_CONTENT': "{index}) On {p[2]}: {p[1]}",
            'PLAN_LIST_PROMPT': "press 'D' to delete a plan, 'A' to add a new plan, 'E' to exit: ",
            'ADD_PLAN_PROMPT': "What is the plan?: ",
            'ADD_PLAN_DATE_PROMPT': "When is the plan? (dd/mm/yyyy): ",
            'PLAN_ADDED_MESSAGE': "Plan added!",
            'DELETE_PLAN_PROMPT': "Which item do you want to delete? (press the number): ",
            'PLAN_DELETED_MESSAGE': "{num}) On {item[2]} {item[1]} has been deleted",
            # 'INVALID_PLAN_NUMBER_MESSAGE': "Invalid input. Please enter a valid number.",
            'STOCK_NAME_PROMPT': "Sure! Could you please let me know the name of the company you are looking for?: ",
            'STOCK_NOT_FOUND_MESSAGE': "I can't find the company.",
            'STOCK_SUMMARY_MESSAGE': "For {name} ({symbol}), here is the summary:\n\n{summary}",
            'CURRENT_DATETIME_MESSAGE': "Today is {weekday}, {month} {day}, {year}, at {hour}:{minute}",
            # weather
            'WEATHER_CITY_PROMPT': "Which city are you looking for?: ",
            'WEATHER_INFO_MESSAGE': "Today, in {city} the temperature is from {low_temp} to {high_temp}.\nPrecipitation probability is about {ave_pre}% and wind speed is around {ave_wind} km/h.",
            'WEATHER_EROOR' : "I am sorry, I can't find weather of {city}",
            'NEWS_ITEMS_PROMPT': "How many items of news are you interested to see?: ",
            'NEWS_RESULT_MESSAGE': "Top {num} news:\n\n{news}",
            # duration
            'DURATION_INTEREST_RATE': "Enter the interest rate (in %): ",
            'DURATION_FACE_VALUE': "Enter the face value: ",
            'DURATION_NUM_OF_YEARS': "Enter the number of years: ",
            'DURATION_COUPON_RATE': "Enter the annual coupon rate (in %): ",
            'DURATION_RESULT': "The duration of the investment is: {duration}",
            # npv
            'NPV_INITIAL_INVESTMENT': "Enter the initial investment: ",
            'NPV_NUM_OF_YEARS': "Enter the number of years: ",
            'NPV_COST_OF_CAPITAL': "Enter the cost of capital (in %): ",
            'NPV_CASH_FLOW': "Enter the cash flow in year {num_year}: ",
            'NPV_RESULT': "The NPV of the investment is: {npv}",
            # future value
            'FV_INTEREST_RATE': "Enter the interest rate (in %): ",
            'FV_NUM_OF_YEARS': "Enter the number of years: ",
            'FV_PRESENT_VALUE': "Enter the present value: ",
            'FV_RESULT': "The future value of the investment is: {fv}",
            # expression
            'CALCULATION_RESULT': "The result is {res}",
            # age
            'AGE_PROMPT': "Nice to meet you! How old are you?: ",
            'AGE_INVALID': "Please enter a valid age.",
            # user info
            "USER_INFO_LIST": "You are {name}, {age} years old, you favorite hobby is {hobby}"
        },
        'it': {
            'INTRODUCTION': "Ciao! Come ti chiami?: ",
            'NICE_TO_SEE_AGAIN': "Piacere di rivederti {name}! Come posso aiutarti?",
            'WHAT_YOUR_HOBBY': "Qual'è il tuo hobby?: ",
            'GREETING_MESSAGE': "Ciao {name}! Come posso aiutarti?",
            'EXIT_CONFIRMATION': "Vuoi uscire? (Y/N): ",
            'EXIT_MESSAGE': "Arrivederci!",
            'HELP_MESSAGE': "Va bene, come posso aiutarti ulteriormente?",
            'SEARCH_PROMPT': "Potresti fornire dettagli specifici su ciò che stai cercando?: ",
            'NO_ANSWER_RESPONSES': [
                "Mi dispiace, non riesco a capirti",
                "Non sono sicuro di capire"
            ],
            'MATH_EXPRESSION_PROMPT': "Inserisci la tua espressione (premi 'F' per la matematica finanziaria): ",
            "MATH_EXPRESSION_PROMPT_CHECK_LIST":['f','finanza','mate finanziaria','matematica finanziaria'],
            'MATH_CALCULATION_PROMPT': "Cosa vuoi calcolare? (premi 'D' per durata, 'N' per NPV, 'F' per valore futuro): ",
            'INVALID_INPUT_MESSAGE': "Input non valido. Inserisci valori validi.",
            'ERROR_OCCURRED_MESSAGE': "Si è verificato un errore",
            'PLAN_LIST_HEADER': "Hai {num_items} elemento{'i' if num_items != 1 else ''} di piano: ",
            'PLAN_LIST_CONTENT':"{i+1}) in data {p[2]}: {p[1]}",
            'PLAN_LIST_PROMPT': "premi 'D' per eliminare a plan, 'A' per aggiungere un nuovo elemento, 'E' per uscire:",
            'ADD_PLAN_PROMPT': "Qual è il piano?: ",
            'ADD_PLAN_DATE_PROMPT': "Quando è il piano? (gg/mm/aaaa): ",
            'PLAN_ADDED_MESSAGE': "Piano aggiunto!",
            'DELETE_PLAN_PROMPT': "Quale elemento vuoi eliminare? (premi il numero): ",
            'PLAN_DELETED_MESSAGE': " è stato eliminato",
            # 'INVALID_PLAN_NUMBER_MESSAGE': "Input non valido. Inserisci un numero valido.",
            'STOCK_NAME_PROMPT': "Certo! Potresti dirmi il nome dell'azienda che stai cercando?: ",
            'STOCK_NOT_FOUND_MESSAGE': "Non riesco a trovare l'azienda.",
            'STOCK_SUMMARY_MESSAGE': "Per {name} ({symbol}), ecco il riepilogo:\n\n{summary}",
            'CURRENT_DATETIME_MESSAGE': "Oggi è {weekday}, {day} {month}, {year}, alle {hour}:{minute}",
            # weather
            'WEATHER_CITY_PROMPT': "Quale città stai cercando?: ",
            'WEATHER_INFO_MESSAGE': "Oggi, a {city} la temperatura va da {low_temp} a {high_temp}.\nLa probabilità di precipitazioni è di circa {ave_pre}% e la velocità del vento è di circa {ave_wind} km/h.",
            'WEATHER_EROOR' : "Mi dispiace, non riesco a trovare il meteo di {city}",
            'NEWS_ITEMS_PROMPT': "Quanti articoli di notizie ti interessano?: ",
            'NEWS_RESULT_MESSAGE': "Primi {num} notizie:\n\n{news}",
            # duration
            'DURATION_INTEREST_RATE': "Inserisci il tasso di interesse (in %): ",
            'DURATION_FACE_VALUE': "Inserisci il valore nominale: ",
            'DURATION_NUM_OF_YEARS': "Inserisci il numero di anni: ",
            'DURATION_COUPON_RATE': "Inserisci il tasso cedolare annuale (in %): ",
            'DURATION_RESULT': "La durata dell'investimento è: {duration}",
            # npv
            'NPV_INITIAL_INVESTMENT': "Inserisci l'investimento iniziale: ",
            'NPV_NUM_OF_YEARS': "Inserisci il numero di anni: ",
            'NPV_COST_OF_CAPITAL': "Inserisci il costo del capitale (in %): ",
            'NPV_CASH_FLOW': "Inserisci il flusso di cassa nell'anno {num_year}: ",
            'NPV_RESULT': "Il NPV dell'investimento è: {npv}}",
            # future value
            'FV_INTEREST_RATE': "Inserisci il tasso di interesse (in %): ",
            'FV_NUM_OF_YEARS': "Inserisci il numero di anni: ",
            'FV_PRESENT_VALUE': "Inserisci il valore attuale: ",
            'FV_RESULT': "Il valore futuro dell'investimento è: {fv}",
            # expression
            'CALCULATION_RESULT': "Il risultato è {}",
            # age
            'AGE_PROMPT': "Piacere di conoscerti! Quanti anni hai?: ",
            'AGE_INVALID': "Per favore, inserisci un'età valida.",
            # user info
            "USER_INFO_LIST": "Ti chiami {name}, hai {age} anni, il tuo hobby è {hobby}"

        }
    }

    def __init__(self,language) -> None:
        self.language = language

    def get_text(self, key, **kwargs):
        text = self.TEXTS.get(self.language, {}).get(key, key)
        if isinstance(text,str):
            return text.format(**kwargs)
        else:
            return text