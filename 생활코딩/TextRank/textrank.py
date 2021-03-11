from gensim.summarization.summarizer import summarize
from newspaper import Article

url = ' '
news = Article(url, language='ko')
news.download()
news.parse()
print(news.text)

print(summarize(news.text))