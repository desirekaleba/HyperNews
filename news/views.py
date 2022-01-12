from django.shortcuts import render
from django.views import View
from django.conf import settings
import json
import itertools
from datetime import datetime

# Create your views here.
def load_json_file():
    global news
    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        news = json.load(json_file)

def simple_date_fun(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")

class NewsView(View):
    def get(self, request, *args, **kwargs):
        load_json_file()
        news.sort(key=lambda x: x['created'], reverse=True)
        sorted_news = [{'date': date, 'values': list(news)} for date, news in
                       itertools.groupby(news, lambda x: simple_date_fun(x['created']))]
        context = {'news': sorted_news}
        return render(request, 'news/news.html', context=context)


class SingleNewsView(View):
    def get(self, request, news_id, *args, **kwargs):
        load_json_file()
        global single_news
        for news_i in news:
            if news_i['link'] == news_id:
                single_news = news_i
        context = {'single_news': single_news}
        return render(request, 'news/single_news.html', context=context)
