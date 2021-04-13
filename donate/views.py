from .models import Organization, Transaction, User
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
def index(request):
    return render(request, 'templates/index.html')
    
def login_user(request):
        if request.method=='POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
        user = User.objects.filter(email=email, password=password)
        if user:
            request.session['email'] = email
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
        a=User.objects.filter(email=email)
        if a:
            return JsonResponse({'created':'0','message':"User already exists"})
        User.objects.create(firstName=firstName, lastName=lastName, password=password,email=email,phonenumber=phoneNumber)
        return JsonResponse({'created':'1','message':"Signup Successful, Login to continue"})
    else:
        return render(request, 'templates/signup.html')

def registerOrganization(request):
    if request.method=='POST':
        email=request.POST.get('email')
        name = request.POST.get('first_name')
        password = request.POST.get('password')
        phoneNumber = request.POST.get('phone')
        image=request.FILES.get("image")
        description=request.POST.get("description")
        a=Organization.objects.filter(email=email)
        if a:
            return JsonResponse({'created':'0','message':"User already exists"})
        Organization.objects.create(name=name,password=password,email=email,phonenumber=phoneNumber,image=image,description=description)
        return JsonResponse({'created':'1','message':"Registration Successful, Login to continue"})
    else:
        return render(request, 'templates/signup.html')

def dashboard(request):
    if request.session.has_key('email'):
        organization=get_object_or_404(Organization,email=request.session["email"])
        transanctions=Transaction.objects.filter(organization=organization).order_by('-timestamp')
        return render(request,'templates/dashboard.html',{'instance':organization,'transactions':transanctions})
    else:
        return redirect('/index')

def home(request):
    if request.session.has_key('email'):
        user=get_object_or_404(User,email=request.session["email"])
        transanctions=Transaction.objects.filter(user=user).order_by('-timestamp')
        return render(request,'templates/dashboard.html',{'instance':user,'transactions':transanctions})
    else:
        return redirect('/index')