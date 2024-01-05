from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def signin(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        pass1=request.POST.get('password')
        

        user = authenticate(request, username=uname, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('search')
        else:
            return render(request, 'accounts/signin.html', {'error': 'Invalid Credentials'})
    return render(request, 'accounts/signin.html')

def signup(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password')
        pass2=request.POST.get('confirmation_password')

        

        if uname == '' or email == '' or pass1 == '' or pass2 == '':
            return render(request, 'accounts/signup.html', {'error':'Please fill all the fields'})
        
        if pass1 != pass2:
            return render(request, 'accounts/signup.html', {'error':'Passwords do not match'})
        
        if User.objects.filter(username=uname).exists():
            return render(request, 'accounts/signup.html', {'error':'Username already exists'})

        else:
            my_user=User.objects.create_user(username=uname, email=email, password=pass1)

            # print(uname, email, pass1, pass2)
            return redirect('signin')
    
    return render(request, 'accounts/signup.html')