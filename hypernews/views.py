from django.views import View
from django.shortcuts import render
from django.conf import settings
import json


def load_json_file():
    news_group = []
    global news
    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        news = json.load(json_file)
        news.sort(key=lambda x: x['created'])


class MainView(View):
    def get(self, request, *args, **kwargs):
        load_json_file()
        context = {'news': news}
        return render(request, 'hypernews/main.html', context=context)
