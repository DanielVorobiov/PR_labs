from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from . import reading
from .forms import SendMail, Login
from .sending import sendMail
from .models import User


def login(request):
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            if mail != User.objects.all().values_list('email', flat=True)[0] and password == User.objects.all().values_list('password', flat=True)[0]:
                print("Incorrect Email")
            elif mail == User.objects.all().values_list('email', flat=True)[0] and password != User.objects.all().values_list('password', flat=True)[0]:
                print("Incorrect Password")
            elif mail != User.objects.all().values_list('email', flat=True)[0] and password != User.objects.all().values_list('password', flat=True)[0]:
                print("Incorect Login and Password")
            elif mail == User.objects.all().values_list('email', flat=True)[0] and password == User.objects.all().values_list('password', flat=True)[0]:
                return redirect('/message.html')

    else:
        form = Login()
        print("failed to login")
    return render(request, "index.html", {'form': form})


def receives(request):
    context = {}
    context['mail_1'] = [reading.email_subject_list[0],
                         reading.email_from_list[0], reading.email_body_list[0]]
    context['mail_2'] = [reading.email_subject_list[1],
                         reading.email_from_list[1], reading.email_body_list[1]]
    context['mail_3'] = [reading.email_subject_list[2],
                         reading.email_from_list[2], reading.email_body_list[2]]
    context['mail_4'] = [reading.email_subject_list[3],
                         reading.email_from_list[3], reading.email_body_list[3]]
    print(reading.email_subject_list,
          reading.email_from_list, reading.email_body_list)
    return render(request, "receives.html", context)


def message(request):
    if request.method == "POST":
        form = SendMail(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            if len(request.FILES) != 0:
                if request.FILES['docfile'].size < 2097152:
                    sendMail(email, subject, body, request.FILES['docfile'])
                    print("The mail was sent with a file")
                else:
                    print("Your file is too big, sorry")
            else:
                sendMail(email, subject, body, "")
                print("The mail was sent a file")
        else:
            print("Form is invalid")
    else:
        form = SendMail()
        print("failed to send mail")
    return render(request, "message.html", {'form': form})
