from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world.")


def detail(request, title):
    return HttpResponse(f'Details for the book: {title}')


def results(request, title):
    return HttpResponse(f'Results for book search by title: {title}')