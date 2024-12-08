from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.

def home(request):
    # get all the records from db
    records = Record.objects.all()
    
    # check to see if logging in 
    if request.method == "POST":
        # get the data entered in the form
        username = request.POST["username"]
        password = request.POST["password"]
        
        # authenticate the user using django's in-built authenticate view function
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login the user using built-in django's login view function
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect("home")
        else:
            messages.success(request, "There was an error logging in, please try again...")
            # redirect to a page
            return redirect("home")
    else:
        # render a template
        return render(request, 'home.html', {
            'records': records
        })

def logout_user(request):
    # logging out the user using the built-in django's logout view function
    logout(request)
    messages.success(request, "You have been logged out")
    # redirect to a page
    return redirect("home")

def register_user(request):
    # check to see if the request method is POST
    if request.method == "POST":
        # create an instance of SignUpForm with user input data
        form = SignUpForm(request.POST)
        # if the form data is valid
        if form.is_valid():
            # save the user in db
            form.save()
            # authenticate and login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            # authenticate the user using django's in-built authenticate view function
            user = authenticate(username=username, password=password)
            # login the user using django's in-built login view function
            login(request, user)
            messages.success(request, "You have successfully registered, welcome")
            # redirect to a page
            return redirect('home')
    else:
        # create an empty instance of Signup form
        form = SignUpForm()
    # render a template
    return render(request, 'register.html', {
        'form': form
    })
    
def customer_record(request, pk):
    # if user is logged in
    if request.user.is_authenticated:
        # get record that match the id from db
        customer_record = Record.objects.get(id=pk)
        # render a template
        return render(request, 'record.html', {
        'customer_record': customer_record
        })
    else:
        messages.success(request, "You must be logged in to view the page...")
        # redirect to a page
        return redirect('home')
    
def delete_record(request, pk):
    # if user is logged in
    if request.user.is_authenticated:
        # get record that match the id from db
        record = Record.objects.get(id=pk)
        # delete the record
        record.delete()
    
        messages.success(request, "Record deleted successfully...")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do this...")
        return redirect('home')
    
def add_record(request):
        # creating an instance of AddRecord form with user input data if the request is post or creating an empty instance of the add record form
        form = AddRecordForm(request.POST or None)
        # if user is logged in
        if request.user.is_authenticated:
            # if the method is post
            if request.method == "POST":
                # if the user input data is valid
                if form.is_valid():
                    # save the record in db
                    add_record = form.save()
                    messages.success(request, "Record added...")
                    return redirect('home')
            # render a template
            return render(request, 'add_record.html', {
                'form': form
            })
        else:
            messages.success(request, "You must be logged in...")
            return redirect('home')

def update_record(request, pk):
    # get the record which matches the id
    current_record = Record.objects.get(id=pk)
    # creating an instance of AddRecord form with the existing data if the record already exists
    form = AddRecordForm(request.POST or None, instance=current_record)
    # if user is logged in
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                # save the record in db
                form.save()
                messages.success(request, "Record has been updated...")
                return redirect('home')
        return render(request, 'update_record.html', {
            'form': form
        })
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')