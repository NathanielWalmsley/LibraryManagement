from django import forms


class SearchForm(forms.Form):
    search_query = forms.CharField(label='Look for books', max_length=50)