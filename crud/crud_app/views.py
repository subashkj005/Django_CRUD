from django.shortcuts import render, redirect
from . models import custom_user
from django.views.decorators.cache import never_cache
import time

# Create your views here.

@never_cache
def user_login(request):
    if 'username' in request.session:
        username = request.session['username']
        user = custom_user.objects.get(username = username)

        if user.is_superuser:
            return redirect('adminHome')
        else:
            return redirect('userHome')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = custom_user.objects.get(username=username, password=password)

            if user is not None:
                if not user.is_superuser:
                    request.session['username'] = username
                    return redirect('userHome')
                else:
                    return render(request, 'user_login.html', {'user404': 'Please use admin login'})

        except custom_user.DoesNotExist:
            return render(request, 'user_login.html', {'user404': 'Wrong credentials'})

    return render(request, 'user_login.html')
@never_cache
def admin_login(request):
    if 'username' in request.session:
        username = request.session['username']
        user = custom_user.objects.get(username=username)

        if user.is_superuser:
            return redirect('adminHome')
        else:
            return redirect('userHome')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = custom_user.objects.get(username=username, password=password)

            if user is not None:
                if user.is_superuser:
                    request.session['username'] = username
                    return redirect('adminHome')
                else:
                    return render(request, 'user_login.html', {'user404': 'Please use user login'})

        except custom_user.DoesNotExist:
            return render(request, 'user_login.html', {'user404': 'Invalid Password or Username'})
    return render(request, 'admin_login.html')

@never_cache
def admin_home(request):
    if 'username' in request.session:
        username = request.session['username']
        user = custom_user.objects.get(username = username)

        if user.is_superuser:
            search = request.POST.get('search')

            if search:
                userDatas = custom_user.objects.filter(username__istartswith = search)
            else:
                userDatas = custom_user.objects.filter(is_superuser = False)
            return render(request, 'admin_home.html', {'datas': userDatas})
    return redirect('userlogin')

@never_cache
def user_home(request):
    if 'username' in request.session:
        username = request.session['username']
        user = custom_user.objects.get(username=username)

        if not user.is_superuser:
            return render(request, 'user_home.html')
        else:
            return redirect('adminHome')
    return redirect('userlogin')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('confirm-password')

        if password == cpassword:
            if custom_user.objects.filter(username = username).exists():
                return render(request, 'signup.html',{'pw_error': 'username already exist'})
            if custom_user.objects.filter(email = email).exists():
                return render(request, 'signup.html', {'taken': 'Email already registered' })
            else:
                custom_user(first_name=name, username=username,password=password, email=email).save()
                return render(request, 'signup.html', {'taken': 'Success'})
        else:
            return render(request, 'signup.html', {'taken': 'Password incorrect'})
    return render(request, 'signup.html')

def edit_user(request, id):
    if 'username' in request.session:
        user = custom_user.objects.get(id=id)
        return render(request, 'edit_user.html', {'user': user})

def update_data(request, id):
    user = custom_user.objects.get(id=id)

    if request.method == 'POST':
        user.first_name = request.POST.get('name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        return redirect('adminHome')

    return redirect(request, 'editUser', {'user': user})

def add_user(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password == confirm_password:
            if custom_user.objects.filter(username=username).exists():
                return render(request, 'add_user.html', {'error': 'Username already exists'})
            if custom_user.objects.filter(email=email):
                return render(request, 'add_user.html', {'error': 'Email already registered'})
            else:
                custom_user(first_name=name, username=username, email=email, password=password).save()
                return redirect('adminHome')
        else:
            return render(request, 'add_user.html', {'error': 'Password mismatch'})
    return render(request, 'add_user.html')

def delete_user(requset, id):
    user = custom_user.objects.get(id = id)
    user.delete()
    return redirect('adminHome')


@never_cache
def logout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('userlogin')