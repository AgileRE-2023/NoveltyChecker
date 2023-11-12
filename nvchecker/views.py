from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'nvchecker/landingpage.html')

def about(request):
    return render(request, 'nvchecker/about.html')