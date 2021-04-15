from .models import Organization, Transaction, User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings 
from django.core.mail import send_mail
import os


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request,'signin.html')
def signup(request):
    return render(request,'signup.html')

def login_user(request):
        if request.method=='POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
        user = User.objects.filter(email=email, password=password)
        if user:
            request.session['email'] = email
            request.session['type'] = "user"
            return JsonResponse({'login':'1','message':""})
        else:
            return JsonResponse({'login':'0','message':"No such user exists"})

def login_organization(request):
        if request.method=='POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
        user = Organization.objects.filter(email=email, password=password)
        if user:
            request.session['email'] = email
            request.session['type'] = "organization"
            return JsonResponse({'login':'1','message':""})
        else:
            return JsonResponse({'login':'0','message':"No such Organization exists"})

def registerUser(request):
    if request.method=='POST':
        email=request.POST.get('email')
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        password = request.POST.get('password')
        phoneNumber = request.POST.get('phone')
        dob=request.POST.get('dob')
        gender=request.POST.get('gender')
        a=User.objects.filter(email=email)
        if a:
            return JsonResponse({'created':'0','message':"User already exists"})
        User.objects.create(firstName=firstName, lastName=lastName, password=password,email=email,phonenumber=phoneNumber,dob=dob,gender=gender)
        return JsonResponse({'created':'1','message':"Signup Successful, Login to continue"})
    else:
        return render(request, 'templates/signup.html')

def registerOrganization(request):
    if request.method=='POST':
        email=request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        phoneNumber = request.POST.get('phone')
        image=request.FILES.get("image")
        address=request.POST.get('address1')+'\n'+request.POST.get('address2')
        pincode=request.POST.get('pincode')
        a=Organization.objects.filter(email=email)
        if a:
            return JsonResponse({'created':'0','message':"Organization already exists"})
        Organization.objects.create(name=name,password=password,email=email,phonenumber=phoneNumber,image=image,address=address,pincode=pincode)
        return JsonResponse({'created':'1','message':"Registration Successful, Login to continue"})
    else:
        return render(request, 'template/signup.html')

def dashboard(request):
    if request.session.has_key('email') and request.session['type']=='organization':
        organization=get_object_or_404(Organization,email=request.session["email"])
        transanctions=Transaction.objects.filter(organization=organization).order_by('-timestamp')
        return render(request,'templates/dashboard.html',{'instance':organization,'transactions':transanctions})
        
    elif request.session.has_key('email') and request.session['type']=='user':
        user=get_object_or_404(User,email=request.session["email"])
        transanctions=Transaction.objects.filter(user=user).order_by('-timestamp')
        return render(request,'templates/dashboard.html',{'instance':user,'transactions':transanctions})
    else:
        return redirect('/index')


def home(request):
    if request.session.has_key('email') and request.session['type']=='user':
        user=get_object_or_404(User,email=request.session["email"])
        transanctions=Transaction.objects.filter(user=user).order_by('-timestamp')
        sum=0
        for transaction in transanctions:
            sum=sum+transaction.amount
        return render(request,'dashboarddonar.html',{'user':user,'transactions':transanctions,'sum':sum})
    else:
        return redirect('/index')

def donate(request):
    if request.session.has_key('email') and request.session['type']=='user':
        user=get_object_or_404(User,email=request.session["email"])
        organizations=Organization.objects.all()
        return render(request,'donate.html',{'user':user,'organizations':organizations})
    else:
        return redirect('/index')

def transact(request,id):
    if request.session.has_key('email') and request.session['type']=='user':
        amount=request.GET.get('amount')
        user=get_object_or_404(User,email=request.session["email"])
        organizations=Organization.objects.all()
        organization=get_object_or_404(Organization,id=id)
        Transaction.objects.create(type="credit",organization=organization,amount=amount,user=user)
        subject = 'Thank You for Donating'
        message = "Dear {},\n \n Thank you for your generous gift to {}. We are thrilled to have your support. Through your donation we have been able to accomplish our goal and continue working towards betterment of society. You truly make the difference for us, and we are extremely grateful!.\n If you have specific questions about how your gift is being used or our organization as whole, please don’t hesitate to contact us.\n\nSincerely,\n Donatoz".format(user.firstName,organization.name)
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return redirect('/home')
    else:
        return redirect('/index')

def searchOrganization(request):
    if request.session.has_key('email') and request.session['type']=='user':
        q=request.GET.get('q')
        user=get_object_or_404(User,email=request.session["email"])
        organizations=Organization.objects.filter(name__icontains=q)
        return render(request,'donate.html',{'user':user,'organizations':organizations})
    else:
        return redirect('/index')
        
def render_pdf_view(request,id):
    if request.session.has_key('email') and request.session['type']=='user':
        instance=get_object_or_404(Transaction,id=id)
        return render(request, 'generate.html',{'instance':instance})
    else:
        return redirect('/index')

def logout(request):
    if request.session.has_key('email'):
        request.session.pop('email')
        request.session.pop('type')
    return redirect('/index')
