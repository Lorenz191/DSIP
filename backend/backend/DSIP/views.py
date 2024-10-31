from django.shortcuts import render
from django.http import HttpResponse
from ..sentiment_model.SentimentAnalysis import SeAn


def sean_view(request, text):
    sentiment = SeAn().get_sentiment(text)
    return HttpResponse(sentiment[0])
