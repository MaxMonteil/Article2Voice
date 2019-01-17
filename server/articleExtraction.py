from newspaper import Article


def extract_article(url):
    article = Article(url=url, language='en')
    article.download()
    article.parse()

    return {
            'title': article.title,
            'text': article.text
            }


def main():
    print(extract_article(
        'https://m.signalvnoise.com/the-company-isnt-a-family/'
        ))


if __name__ == '__main__':
    main()
