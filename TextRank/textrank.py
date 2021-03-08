from gensim.summarization.summarizer import summarize
from newspaper import Article
import feedparser

url = 'http://rss.etnews.com/Section901.xml'
#news = Article(url, language='ko')
#news.download()
#news.parse()
#print(news.text)
#print(summarize(news.text))

parse = feedparser.parse(url)
print(url,"complete")
dic=[]
for p in parse.entries:
    dic.append({'title':p.title, 'link' : p.link})
    print(p)

print(dic[0]["title"])