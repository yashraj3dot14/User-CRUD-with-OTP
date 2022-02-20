from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import MyCustomUser
from django.contrib.auth import authenticate,login,logout

from twilio.rest import Client
import os
import random
# Create your views here.
OTP = 0
def signup(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request,'app/signup.html', {'form': form})
    else:
        form = UserForm(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        mobile = request.POST['mobile']
        sec_email = request.POST['sec_email']
        if form.is_valid():
            user = MyCustomUser.objects.create_user(
                username= username, email =email,
                password= password,first_name= first_name,
                last_name= last_name, mobile= mobile, sec_email= sec_email
            )

            user.save()
    return render(request,'app/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print('username: ',username)
        print('password: ',password)
        #user = authenticate(username= username, password= password)

        myuser = MyCustomUser.objects.get(username= username)
        #print('myuser: ', myuser)
        if myuser.check_password(password):
            print('login success')
            return render(request, 'app/otp_verify.html')
        else:
            print('Login failed')
            return redirect('signin/')

        '''
        if user:
            login(request, user)
            return render(request, 'app/index.html')
        else:
            return redirect('signin/')
        '''
    return render(request, 'app/login.html')

def random_number():
    rand_num = random.randint(1, 10000)
    OTP = rand_num
    return rand_num

def otp_generate(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        client = Client('#####', '#####')

        message = client.messages.create(
            body="Your OTP is: "+str(random_number()),
            to=mobile,
            from_ = '+100000000'
        )

        print('message sid: ',message.sid)
        print('Usr mobile: ',mobile)
        return redirect('app/verify_otp/')
    return render(request, 'app/otp_verify.html')

def otp_login(request):
    if request.method == 'POST':
        #print('username: ',username)
        #print('password: ',password)
        #user = authenticate(username= username, password= password)

        user_otp = request.POST['otp']
        print('OTP: ',OTP)
        if user_otp == OTP:
            login(request)
            print('login success')
            return render(request, 'app/index.html')
        else:
            messages.error(request, 'Invalid Otp')
            return render(request, 'app/otp_verify.html')
    return render(request, 'app/insert_otp.html')

