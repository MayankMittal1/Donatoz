from django.db.models.query_utils import PathInfo
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
        transanctions=Transaction.objects.filter(organization=organization).order_by('-timestamp')[0:10]
        return render(request,'dashboard_orgo.html',{'instance':organization,'transactions':transanctions})
    else:
        return redirect('/index')

def dashboardSearch(request):
    if request.session.has_key('email') and request.session['type']=='organization':
        organization=get_object_or_404(Organization,email=request.session["email"])
        year=request.GET.get('year')
        month=request.GET.get('month')
        transanctions=Transaction.objects.filter(organization=organization).filter(timestamp__year=year).filter(timestamp__month=month).order_by('-timestamp')[0:10]
        return render(request,'dashboard_orgo.html',{'instance':organization,'transactions':transanctions})
    else:
        return redirect('/index')

def filter(request,id):
    if request.session.has_key('email') and request.session['type']=='user':
        year=request.GET.get('year')
        month=request.GET.get('month')
        user=get_object_or_404(User,email=request.session["email"])
        organization=get_object_or_404(Organization,id=id)
        if organization in user.organizations.all():
            transanctions=Transaction.objects.filter(organization=organization,type='debit').filter(timestamp__year=year).filter(timestamp__month=month).order_by('-timestamp')
            return render(request,'view_ex.html',{'instance':user,'transactions':transanctions,'organization':organization})
        else:
            return redirect('/home')
       
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
        organization.balance=organization.balance+int(amount)
        organization.save()
        user.organizations.add(organization)
        user.save()
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

def addTransaction(request):
    if request.session.has_key('email') and request.session['type']=='organization':
        if request.method=="POST":
            description=request.POST.get('desc')
            type=request.POST.get('type')
            image=request.FILES.get('image')
            amount=request.POST.get('amount')
            organization=get_object_or_404(Organization,email=request.session['email'])
            if type=='credit':
                organization.balance=organization.balance+int(amount)
            else:
                organization.balance=organization.balance-int(amount)
            organization.save()
            Transaction.objects.create(type=type,organization=organization,amount=amount,invoice=image,description=description)
            return redirect('/dashboard')
        else:
            return render(request,'additem.html')
    else:
        return redirect('/index')

def profileO(request):
    if request.session.has_key('email') and request.session['type']=='organization':
        organization=get_object_or_404(Organization,email=request.session["email"])
        return render(request,'profileo.html',{'instance':organization})
    else:
        return redirect('/index')

def profileD(request):
    if request.session.has_key('email') and request.session['type']=='user':
        user=get_object_or_404(User,email=request.session["email"])
        return render(request,'profiledonor.html',{'instance':user})
    else:
        return redirect('/index')

def updatePassword(request):
    if request.session.has_key('email') and request.session['type']=='organization':
        user=get_object_or_404(Organization,email=request.session['email'])
        oldpass=request.POST.get('old_pass')
        newpass=request.POST.get('new_pass')
        if user.password==oldpass:
            user.password=newpass
            user.save()
            return JsonResponse({'updated':'1','message':'Password Updated successfully'})
        else:
            return JsonResponse({'updated':'0','message':'Old Password dosent match'})

    elif request.session.has_key('email') and request.session['type']=='user':
        user=get_object_or_404(User,email=request.session['email'])
        oldpass=request.POST.get('old_pass')
        newpass=request.POST.get('new_pass')
        if user.password==oldpass:
            user.password=newpass
            user.save()
            return JsonResponse({'updated':'1','message':'Password Updated successfully'})
        else:
            return JsonResponse({'updated':'0','message':'Old Password dosent match'})

    else:
        return redirect('/index')

def updateProfileImage(request):
    if request.session.has_key('email') and request.session['type']=='organization':
        user=get_object_or_404(Organization,email=request.session['email'])
        image=request.FILES.get('image')
        user.image=image
        user.save()
        return JsonResponse({'image':user.image.url})

    elif request.session.has_key('email') and request.session['type']=='user':
        user=get_object_or_404(User,email=request.session['email'])
        image=request.FILES.get('image')
        user.image=image
        user.save()
        return JsonResponse({'image':user.image.url})

    else:
        return redirect('/index')

def updateInfo(request):
    if request.session.has_key('email') and request.session['type']=='organization':
        user=get_object_or_404(Organization,email=request.session['email'])
        address=request.POST.get('address')
        pincode=request.POST.get('pincode')
        about=request.POST.get('about')
        phone=request.POST.get('phone')
        user.address=address
        user.pincode=pincode
        user.about=about
        user.phonenumber=phone
        user.save()
        return JsonResponse({'address':address,'pincode':pincode,'phone':phone,'about':about})

    elif request.session.has_key('email') and request.session['type']=='user':
        user=get_object_or_404(User,email=request.session['email'])
        firstName=request.POST.get('first_name')
        lastName=request.POST.get('last_name')
        phone=request.POST.get('phone')
        user.lastName=lastName
        user.firstName=firstName
        user.phonenumber=phone
        user.save()
        return JsonResponse({'firstName':firstName,'lastName':lastName,'phone':phone})
        
    else:
        return redirect('/index')

def viewEx(request,id):
    if request.session.has_key('email') and request.session['type']=='user':
        user=get_object_or_404(User,email=request.session["email"])
        organization=get_object_or_404(Organization,id=id)
        if organization in user.organizations.all():
            transactions=Transaction.objects.filter(organization=organization,type='debit').order_by('-timestamp')[0:10]
            return render(request,'view_ex.html',{'instance':user,'transactions':transactions,'organization':organization})
        else:
            return redirect('/home')
    else:
        return redirect('/index')
