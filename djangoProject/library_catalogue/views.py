from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Book


def index(request):
    first_five_books = Book.objects.order_by('title')[:5]
    context = {'first_five_books': first_five_books}
    return render(request, 'library_catalogue/index.html', context)


def detail(request, title):
    book = get_object_or_404(Book, title=title)
    return render(request, 'library_catalogue/detail.html', {'book': book})


def results(request, title):
    return HttpResponse(f'Results for book search by title: {title}')