from bs4 import BeautifulSoup
import requests

# TODO language handling
class NewsScraper:
    """
    A class for scraping news articles from Google News.

    Methods:
        get_news(num=5): Retrieves the latest news articles.

    Example:
        news_scraper = NewsScraper()
        num_articles, news_result = news_scraper.get_news()
        print(f"Top {num_articles} News Articles:\n\n{news_result}")

    """
    
    @staticmethod
    def get_news(num = 5):
        page = requests.get(f"https://news.google.com/home")
        parsed_page = BeautifulSoup(page.text, 'html.parser')
        news = parsed_page.find_all("article")[:num]
        result = ""
        for item in news:
            time = item.find("time").get_text()
            title = item.find("h4").get_text()
            result += title if len(title) <= 100 else title[:97] + "..."
            result += "\n"
            result += time + "\n"
            result += "-"*100 + "\n"

        return (len(news),result)

