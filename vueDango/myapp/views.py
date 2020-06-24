from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from . import models
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json
@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = models.Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

@require_http_methods(["GET"])
def show_books(request):
    response = {}
    try:
        books = models.Book.objects.all().values()
        print(books)
        response['list'] = list(books)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
