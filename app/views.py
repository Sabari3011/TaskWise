# from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from email.message import  EmailMessage
import ssl
import smtplib
from .models import Tasks

#  open scopes
otp=random.randint(100000,999999)



# send otp to the entererd mail
def sendmail(otp,email):
    sender = "ceeesabarinathan24@gmail.com"
    password = "hzfzzxwirfjopcsm"

    receiver = email
    # receiver=input("enter email id")
    subject = "OTP for TodoWise"
    body = f"<#> {otp} is your TodoWise verification code"

    em=EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['subject'] = subject
    em.set_content(body)


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(sender,password)
        smtp.sendmail(sender,receiver,em.as_string())

    print("sent successfully")


# Create your views here.
def userlogin(req,username,password):
    user=authenticate(req, username =username , password =password)
    if user is not None:
        login(req,user)
        print("user loged in")
    else:
        print("user not valid")

@login_required
def deletetask(req,id):
    Tasks.objects.get(id=id).delete()

    return redirect("/")
    # return HttpResponse(f"deleted {id}")

@login_required
def updatetask(req,id):
    data=Tasks.objects.filter(author_id = req.user.id)
    currenttask=Tasks.objects.get(id=id)
    if req.method =="POST":
        currenttask.task=req.POST['task']
        currenttask.save()
        return redirect ('/')

    return render(req,"update.html",{"data" :data, "current":currenttask})

@login_required
def complete(req,id):
    db=Tasks.objects.get(id=id)
    
    if db.completed:
        db.completed=False
        db.save()
    else:
        db.completed=True
        db.save()
    return redirect ('/')

@login_required
def home(req):
    print(req.user.id)

    finished=Tasks.objects.filter(author_id = req.user.id).filter(completed= False ).count()
    if req.method =="POST":
        db=Tasks()
        # inst=db.save(commit=False)
        db.author=req.user
        db.task=req.POST['task']
        db.save()
        data=Tasks.objects.filter(author_id = req.user.id)
        return redirect("/")
    else:
        data=Tasks.objects.filter(author_id = req.user.id)
        return render(req,"home.html",{"data" :data,"finished":finished})

# generate a random otp 
def generateotp (email):
    global otp
    otp=random.randint(100000,999999)
    sendmail(otp,email)
    print(otp)

# otp page , reg user ,login user

def sendotp(req,email,valid):
    if valid==0:
        error={"err":"please enter a correct OTP"}
    else:
        error={"err":""}
    if req.method =="POST":
        userotp=req.POST['otp']
        print("user" ,userotp)
        if otp != int(userotp) :
            return redirect(f"/otp/{email}/0")
        else:
            useremail=email
            username=email
            password="sabari123"
            try:
                
                newuser=User.objects.create_user(username,useremail,password)
                newuser.save()
                userlogin(req,username,password)
                
            except:
                userlogin(req,username,password)
            return redirect("/") 
    # if(req.method =="GET"):
    #     return redirect("login")                   
    print(email)
    return render(req,"otp.html",error)

# get email from the user
def getemail(req):
    if req.method =="POST":
        email=req.POST['email']
        print(req.POST['email']) 
        # print(otp)
        generateotp(email)
        # print(req.POST['otp'])   
        # sendotp(req,email)
        
        return redirect(f"/otp/{email}/1")
    return render(req,"login.html")


@login_required
def logoutUser(req):
    logout(req)
    return redirect("/login")

