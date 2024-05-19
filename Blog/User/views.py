from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from .models import *
import regex as re
from datetime import datetime,timedelta

# Create your views here.
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        user_obj = User.objects.filter(email = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)
            # email regex
        email_condition = "^[a-z]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$"
        if re.search (email_condition,email):
            password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
            if re.match(password_pattern,password):
                if password==cpassword:

                    user_obj = User.objects.create(name=name,email = email ,password=password)
                    messages.success(request, 'Register successfully')
                    return redirect('/user/signin')
                else:
                    messages.warning(request, 'Password and Confirm Password not match.')
                    return HttpResponseRedirect(request.path_info)
                # messages.success(request, 'An email has been sent on your mail.')
                # return HttpResponseRedirect(request.path_info)
            else:
                messages.warning(request,'Use strong password')
                return HttpResponseRedirect(request.path_info)

        else:
            messages.warning(request, 'Invalid email.')
            return HttpResponseRedirect(request.path_info)

    return render(request,'User/signup.html')


def signin(request):
    
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
        
            user_obj = User.objects.get(email = email)
            
            # profile=User.objects.filter(user=user_obj)

            if user_obj:
                # if user_obj.profile.is_email_verified:
                if user_obj.password==password:
                        
                    response= redirect('/')
                    response.set_cookie('email',user_obj.email,expires=datetime.utcnow()+timedelta(days=1))
                    # response.set_cookie('password',user_obj.password,expires=datetime.utcnow()+timedelta(seconds=1))
                    response.set_cookie('uid',user_obj.uid,expires=datetime.utcnow()+timedelta(days=1))
                    response.set_cookie('name',user_obj.name,expires=datetime.utcnow()+timedelta(days=1))
                        
                    return response
        
                        
                else:
                    messages.warning(request, 'Incorrect Password')
                    return HttpResponseRedirect(request.path_info)
                # else:
                #     messages.warning(request, 'Your email is not verify')
                #     return HttpResponseRedirect(request.path_info)
            else:
                messages.warning(request, 'Invalid credentials')
                return HttpResponseRedirect(request.path_info)
    except Exception as e:
        print(e)
        messages.warning(request,'Account not found')
        return HttpResponseRedirect(request.path_info)

    return render(request,'User/login.html')


# Logout

def logout(request):
    response= redirect('/')
    response.delete_cookie('name')
    response.delete_cookie('email')
    response.delete_cookie('uid')
    response.delete_cookie('password')
    return response

def postblog(request):

    if 'uid' in request.COOKIES and 'email' in request.COOKIES:
        email=request.COOKIES['email']
        uid=request.COOKIES['uid']
        name=request.COOKIES['name']
        user=User.objects.get(uid=uid)

        blog_post=Blog.objects.filter(user=user).count
        if request.method=="POST":

            name=request.POST.get("authorName")
            title=request.POST.get("blogTitle")
            category=request.POST.get("blogCategory")
            desc=request.POST.get("blogContent")
            image=request.FILES.get("blogImage")

        # blog=Blog.objects.create(user=user,author_name=user.name,title=title,category=category,content=desc,image=image)

        


            post_blog = Blog.objects.create(user=user,author_name=name,title=title,category=category,content=desc,image=image)
            messages.success(request, "Your blog is post.")
            return HttpResponseRedirect(request.path_info)

        context={
            'email':email,
            'uid':uid,
            'user':user,
            'name':name,
            'blog_post':blog_post,
            # 'blog':blog
            # 'post_blog':post_blog,
            
            }   

        return render(request,'user/postblog.html',context)
    else:
        return HttpResponse("Something went wrong")








############## Faltu #########################
def check(request):
    if 'uid' in request.COOKIES and 'email' in request.COOKIES:
        email=request.COOKIES['email']
        uid=request.COOKIES['uid']
        context={
            'email':email,
            'uid':uid
        }
        return render(request,'User/copy.html',context)

