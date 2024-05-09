from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import BookTitle, Book
from django.views.generic import ListView, FormView
from .forms import BookTitleForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
import string

# Create your views here.




class  BookTitleListView(FormView,ListView):
    # model = BookTitle

    template_name = 'books/main.html'
    context_object_name = 'qs'
    form_class = BookTitleForm
    # success_url=reverse_lazy('books:main')
    i_instance = None
    def get_success_url(self):
        return self.request.path
    def get_queryset(self):
        parameter = self.kwargs.get('letter') if self.kwargs.get('letter') else 'a'
        return BookTitle.objects.filter(title__startswith=parameter) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        letters = list(string.ascii_uppercase)
        context['letters'] = letters
        selected_letter = self.kwargs.get('letter') if self.kwargs.get('letter') else 'a'
        print('selected_letter',selected_letter)
         
        return context
    
    def form_valid(self,form):
        self.i_instance  = form.save()
        messages.add_message(self.request, messages.INFO, f"Book title: {self.i_instance.title} has been created  ")
        return super().form_valid(form)
# def book_title_list_view(request):
#     qs = BookTitle.objects.all() 
#     return render(request, 'books/main.html', {'qs':qs})
    def form_invalid(self,form):
            print(form.errors)    
            self.object_list  = self.get_queryset()
            messages.add_message(self.request, messages.ERROR , form.errors)
            return super().form_invalid(form)
    



class BookListView(ListView):
     template_name = 'books/detail.html'
     paginate_by  = 1
     def get_queryset(self):
          title_slug = self.kwargs.get('slug')
          return Book.objects.filter(title__slug=title_slug)
     

# def book_title_detail_view(request, **kwargs):
#     slug= kwargs.get('slug')
#     obj = BookTitle.objects.get(slug=slug)
#     return  render(request, 'books/detail.html',{'obj':obj})
