from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView, ListView
from django.http import HttpResponse

from .models import Book
from .forms import SearchForm


class HomeView(FormView):
    template_name = 'library_catalogue/home.html'
    form_class = SearchForm


def detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'library_catalogue/detail.html', {'book': book})


class SearchResultsView(ListView):
    model = Book
    template_name = 'library_catalogue/results.html'
    
    def get_queryset(self):
        query = self.request.GET.get('search_query')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        )
