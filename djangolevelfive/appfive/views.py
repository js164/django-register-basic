from django.shortcuts import render
from appfive.forms import userform,usermodelform
from django.http import HttpResponse
# Create your views here.


from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
     return render(request,'appfive/index.html')

@login_required
def thankyou(request):
    return render(request,'appfive/thankyou.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered=False
    if request.method=='POST':
        user_form=userform(data=request.POST)
        usermodel_form=usermodelform(data=request.POST)

        if user_form.is_valid() and usermodel_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            usermodel=usermodel_form.save(commit=False)
            usermodel.user=user

            if 'profile_pic' in request.FILES:
                usermodel.profile_pic=request.FILES['profile_pic']

            usermodel.save()
            registered=True
        else:
            print(user_form.errors,usermodel.errors)
    else:
        user_form=userform()
        usermodel_form=usermodelform()

    return render(request,'appfive/register.html',{'user_form':user_form,'usermodel_form':usermodel_form,'registered':registered})

def user_login(request):

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('thankyou'))
            else:
                return HttpResponse("Account is not ACTIVE!")
        else:
            print("Someone try to login")
            print("Username: {} & Password: {}".format(username,password))
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request,'appfive/login.html')
