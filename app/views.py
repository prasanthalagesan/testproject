from django.shortcuts import render
from app.models import *

# Create your views here.

def home(request):
    one = User.objects.values('id', 'username')
    print(one)
    return render(request, 'home.html')