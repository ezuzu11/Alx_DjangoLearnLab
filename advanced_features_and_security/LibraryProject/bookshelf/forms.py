from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title.isalnum():
            raise forms.ValidationError("Title should only contain alphanumeric characters.")
        return title
