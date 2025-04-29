import requests

class SearchEngine:
    """
    A class for performing searches using the Wikipedia API.

    Methods:
        search(detail, max_result=5): Searches Wikipedia for the specified detail.

    Example:
        search_engine = SearchEngine()
        search_result = search_engine.search("Python programming language")
        print(search_result)

    """

    #TODO language
    def __init__(self):
        self.url = "https://en.wikipedia.org/w/api.php?"
        self.params = {
            'action': 'query',
            'format': 'json',
            'origin': '*',
            'srlimit': 1,
            'generator': 'search',
            'prop': 'extracts',
            'exintro': True,  # Get only the introduction section
            'explaintext': True,  # Return plain text without HTML
            'inprop': 'url',  # Include the full URL in the result
        }

    
    def search(self, detail, max_result = 5):
        try:
            self.params['gsrsearch'] = detail

            # Use a context manager for better resource management
            with requests.get(url=self.url, params=self.params) as resp:
                resp.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

                data = resp.json()
        
            pages = data['query']['pages']
            response = "\n"

            for i, page_id in enumerate(pages):
                if i >= max_result:
                    break

                page = pages[page_id]
                if i == 0:
                    response += f'Here is what I found: \n{page["extract"][:800]}...\n\n'
                else:
                    response += f'{i}) {page["extract"][:100]}...\n'

            return response
        except:
            return None