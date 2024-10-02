from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from allocation.scripts.alloc_algo import alloc_algorithm


def index(request):

    return HttpResponse("Hello, world. You're at the allocation index.")


def status(request):

    alloc_algorithm()
    return HttpResponse("Check the Terminal!")


