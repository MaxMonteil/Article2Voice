from newspaper import Article


def extract_article(url):
    # Initialize article object
    article = Article(
                url=url,
                language='en',
                fetch_images=False
            )
    article.download()
    article.parse()

    return {
                'title': article.title,
                'text': article.text
           }
