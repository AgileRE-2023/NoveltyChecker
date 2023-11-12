from django.shortcuts import render

# Create your views here.
def search(request):
    return render(request, 'search/searchpage.html')

def report(request):
    return render(request, 'search/searchreport.html')

def list(request):
    return render(request, 'search/searchlist.html')