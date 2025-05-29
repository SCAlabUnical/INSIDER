# views.py
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.shortcuts import render

# Define API to manage a GET request
@api_view(['GET'])
def homepage(request):
    # Render home.html
    return render(request, 'home.html')

# Define API to manage a GET request for the documentation
@api_view(['GET'])
def docs(request):
    # Render documentation.html
    return render(request, 'docs.html')