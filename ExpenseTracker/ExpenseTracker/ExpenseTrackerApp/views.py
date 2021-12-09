from django.shortcuts import render,redirect,HttpResponse
from django.core.paginator import Paginator, EmptyPage , PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import login as dj_login, authenticate
from .models import Addmoney_info,UserProfile
from django.contrib.auth.models import User
from django.shortcuts import render
# Create your views here.
def signup(req):
    return render(req,"signup.html")
def home(req):
    return render(req,"login.html")


def handleSignup(req):
    if req.method == 'POST':
        uname=req.POST['username']
        fname=req.POST['firstname']
        lname=req.POST['lastname']
        email = req.POST['email']
        profession = req.POST['profession']
        savings = req.POST['savings']
        income = req.POST['income']
        pass1 = req.POST['pass1']
        pass2 = req.POST['pass2']
        profile = UserProfile(Savings=savings,profession=profession,income=income)
        if req.method=='POST':
            try:
                user_exists=User.objects.get(username=req.POST['username'])
                messages.error(req,"Username is already taken, Try something else")
                return redirect("/signup/")
            except User.DoesNotExist:
                if len(uname)>15:
                    messages.error(req, "Username must be max 15 character")
                    return redirect("/signup/")
                if not uname.isalnum():
                    messages.error(req, " Username should only contain letters and numbers, Please try again")
                    return redirect("/signup/")
                if pass1 != pass2:
                    messages.error(req, " Password do not match, Please try again")
                    return redirect("/signup/")

        user = User.objects.create_user(uname, email, pass1)
        user.fist_name = fname
        user.last_name = lname
        user.email = email
        user.save()

        profile.user=user
        profile.save()
        messages.success(req,"Your acc was created successfully")
        return redirect("/")

def handleLogin(req):
    if req.method== 'POST' :
        loginuname=req.POST['username']
        loginpassword1=req.POST['password']
        user= authenticate(username=loginuname,password=loginpassword1)
        if user is not None:
            dj_login(req,user)
            req.session['is_logged']=True
            user=req.user.id
            req.session['user_id']=user
            messages.success(req, 'Successfully Login')
            return redirect('/index')
        else:
            messages.error(req,"Invalid Creadentials ,PLease try again")
            return redirect('/')
    return HttpResponse('404 Not Found')

def index(req):
    if req.session.has_key('is_logged'):
        user_id = req.session["user_id"]
        user = User.objects.get(id=user_id)
        addmoney_info = Addmoney_info.objects.filter(user=user).order_by('-Date')
        paginator = Paginator(addmoney_info , 4)
        page_number = req.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {
            # 'add_info' : addmoney_info,
           'page_obj' : page_obj
        }

        return render(req, 'index.html', context)