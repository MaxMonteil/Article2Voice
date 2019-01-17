"""Newspaper abstraction to return text extracted from given URL."""
from newspaper import Article


def extract_article(url):
    """Parses the article at the given URL and returns text and title."""
    # Initialize article object
    article = Article(
                url=url,
                language='en',
                fetch_images=False)
    article.download()
    article.parse()

    return {
                'title': article.title,
                'text': article.text
           }
