from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Book


def index(request):
    first_five_books = Book.objects.order_by('title')[:5]
    context = {'first_five_books': first_five_books}
    return render(request, 'library_catalogue/index.html', context)


def detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'library_catalogue/detail.html', {'book': book})


def results(request, book_id):
    return HttpResponse(f'Results for book search by title: {book_id}')