from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import auth, messages
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import get_user_model
from checkout.views import Transaction, LineItem
from home.views import home
from menu.views import menu

#Import login_required annotations
from django.contrib.auth.decorators import login_required

# Start of views.


""" This is the logout function """
def logout(request):
    auth.logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect(home)

    
""" This is the user login function """
def login(request):
    if request.method == "POST":
        #This will populate the login request with the user input into the login form
        login_form = UserLoginForm(request.POST)
        
        #If the login form input is valid
        if login_form.is_valid():
            #check if the user name and password match
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            #If user exists, user will be logged in
            if user:
                auth.login(user=user, request=request)
                return redirect(reverse('menu'))
            else:
                messages.error(request, "Username or password is incorrect")
                form = UserLoginForm()
                return render(request, 'accounts/login.template.html', {
                'form': form
                })
    else:
        form = UserLoginForm()
        return render(request, 'accounts/login.template.html', {
            'form': form
        })


""" This is to ensure that user login is required in order for profile page to be accessible """ 
""" Under this view, the transactions which user has made will be filtered and displayed under the Order History page """
@login_required
def order_history(request):
    transaction = Transaction.objects.filter(owner=request.user.id)
    User = get_user_model()
    user = User.objects.get(email=request.user.email)
    return render(request, "accounts/order_history.template.html", {
        'user': user,
        'transaction': transaction
    })


""" This is the user registration function """    
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            #check if the username and password matches
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            #if the user is successfully created, log the user into their account
            if user:
                #log user in
                auth.login(user=user, request=request)
                messages.success(request, "Registration successful")
            else:
                messages.error(request, "Registration failed")
            
            return redirect(reverse('home'))
            
        else:
            register_form = UserRegistrationForm()
            return render(request, "accounts/register.template.html", {
                'form': form
            })
    else:   
        register_form = UserRegistrationForm()
        return render(request, "accounts/register.template.html", {
            'form': register_form
        })


    