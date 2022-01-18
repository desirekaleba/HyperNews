from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
import json
import itertools
from datetime import datetime
import random

news = []


# Create your views here.
def load_json_file():
    global news
    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        news = json.load(json_file)


def simple_date_fun(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")


def dump_json_file():
    with open(settings.NEWS_JSON_PATH, 'r+') as json_file:
        json.dump(news, json_file)


def search_news(phrase):
    searched_news = []
    for i in news:
        if phrase in i.get("title"):
            searched_news.append(i)
    return searched_news


def sort_news(_news):
    _news.sort(key=lambda x: x['created'], reverse=True)
    sorted_news = [{'date': date, 'values': list(news)} for date, news in
                   itertools.groupby(_news, lambda x: simple_date_fun(x['created']))]
    return sorted_news


class NewsView(View):
    def get(self, request, *args, **kwargs):
        search = request.GET.get('q')
        load_json_file()
        sorted_news = sort_news(news)
        context = {'news': sorted_news}

        if search:
            searched_news = search_news(search)
            sorted_searched_news = sort_news(searched_news)
            context['news'] = sorted_searched_news
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


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        news_title = request.POST.get('title')
        news_text = request.POST.get('text')
        load_json_file()
        news.append({"created": str(datetime.today().strftime('%Y-%m-%d %H:%M:%S')), "text": news_text,
                     "title": news_title, "link": int(str.zfill(str(random.randint(000000000, 999999999)), 9))})
        dump_json_file()
        return redirect('/news/')
