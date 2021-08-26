from django.core import paginator
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import UserDetailsModel
from django.core.paginator import Page, Paginator, EmptyPage, PageNotAnInteger
import json
from django.http import JsonResponse
from django.views.generic import (
    CreateView, DetailView, ListView,
    UpdateView, TemplateView, View
)

#User details search in realtime
def search_userdetails(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        users = UserDetailsModel.objects.filter(fname__istartswith=search_str)
        data = users.values()
        return JsonResponse(list(data), safe=False)

#User registration
def sample(request):
    if request.method =='POST': 
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        mname = request.POST.get("mname")
        dateofbirth = request.POST.get("dateofbirth")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        country = request.POST.get("country")
        state = request.POST.get("state", default = None)
        file = request.FILES['file']

        UserDetailsModel(fname=fname, lname=lname, mname=mname, dateofbirth=dateofbirth, email=email, gender=gender, country=country, state=state, file=file).save()
        messages.info(request, 'User details saved successfully')
        return redirect('/')
    return render(request, 'sample.html')

#Admin Register
def register(request): 
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password1)
                user.save();
                messages.info(request, 'User created')
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('register')
    else:
        return render(request, 'register.html')

#Admin Login
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('adminpage')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

#Admin Logout
def logout(request):
    auth.logout(request)
    return redirect('/')

#Home Page
def home(request):
    return render(request, 'home.html')

#Admin home page
def adminpage(request):
    userdata = UserDetailsModel.objects.all().order_by('-created')
    count= UserDetailsModel.objects.all().count()

    page = request.GET.get('page', 1)
    paginator = Paginator(userdata, 4)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    user = {
        "userdata": userdata,
        "count": count,
        "users": users,
    }
    return render(request, 'adminpage.html', user)   


class UserDetailView(DetailView):
    model = UserDetailsModel
    template_name = "userdetails.html"

def UserDetailDeleteView(request, pk):
    userdata = UserDetailsModel.objects.get(pk=pk)
    userdata.delete()
    return redirect(adminpage)


def export_excel(request):
    try:
        userdetail = list(UserDetailsModel.objects.all().values())
        return JsonResponse({'status': '1', 'userdetail': userdetail})
    except Exception as e:
            return JsonResponse({'status': '0', 'data': str(e)})

