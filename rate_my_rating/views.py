from django.shortcuts import render

def index(request):
    response = render(request, 'rango/index.html')