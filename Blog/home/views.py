from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import *
from User.models import *
from django.contrib import messages


    # Create your views here.

def index(request):
    if 'uid' in request.COOKIES and 'email' in request.COOKIES:
        email=request.COOKIES['email']
        uid=request.COOKIES['uid']
        name=request.COOKIES['name']
            
        user=User.objects.get(uid=uid)

        blog_post=Blog.objects.filter(user=user).count

        blogs=Blog.objects.all()

            # Popular posts section 

        popular_posts = Blog.objects.annotate(comment_count=models.Count('blog')).filter(comment_count__gte=3)
            


        context={
                    'email':email,
                    'uid':uid,
                    'name':name,
                    'blog_post':blog_post,
                    'blog':blogs,
                    'popular_posts': popular_posts
                    # 'popular_posts':popular_posts,
                    # 'categories':categories,
                    }   

        return render(request,'Blog/index.html',context)
            # else:
            #     context={
            #         'email':email,
            #         'uid':uid,
            #         'name':name,
            #         'blog_post':blog_post,
            #         'blog':blogs,
            #         # 'popular_posts':popular_posts,
            #         # 'categories':categories,
            #         }   

            #     return render(request,'Blog/index.html',context)

    else:
        blog=Blog.objects.all()
        popular_posts = Blog.objects.annotate(comment_count=models.Count('blog')).filter(comment_count__gte=3)
            
        context={'blog':blog,'popular_posts':popular_posts}
        return render(request,'Blog/index.html',context)


    # def blog(request):
    
def single_blog(request,uid):
    if 'uid' in request.COOKIES and 'email' in request.COOKIES:
        email=request.COOKIES['email']
        uuid=request.COOKIES['uid']
        name=request.COOKIES['name']
            
        user=User.objects.get(uid=uuid)
        
        blog_post=Blog.objects.filter(user=user).count

        blog=Blog.objects.get(uid=uid)

        comments=Comment.objects.filter(blog=blog)
        
        context={
                "blog":blog,"uid":uuid,"user":user,"email":email,'comment':comments,'name':name,
                'blog_post':blog_post
                }
        
        return render(request,'Blog/blog-single.html',context)
        
    else:
            
        blog=Blog.objects.get(uid=uid)
        comments=Comment.objects.filter(blog=blog)
            
        context={
                'blog':blog,
                'comment':comments
                
            }
        return render(request,'Blog/blog-single.html',context)
        # else:
        #     blog=Blog.objects.get(uid=uid)
        #     context={'blog':blog}
        #     return render(request,'Blog/blog-single.html',context)

def categories(request,uid):
    if "uid" and "email" in request.COOKIES:
        uuid=request.COOKIES['uid']
        email=request.COOKIES['email']
        name=request.COOKIES['name']
        user=User.objects.get(uid=uuid)
        blog_post=Blog.objects.filter(user=user).count
        
        blog=Blog.objects.filter(uid=uid)
        context={'blog_post':blog_post,'blog':blog,'uid':uuid,'user':user,'name':name}
        
        return render(request,'Blog/category.html',context)
        
    else:
            
        blog=Blog.objects.get(uid=uid)
            
        context={
                'blog':blog,
                
            }
        return render(request,'Blog/blog-single.html',context)



def search_posts(request):
        
    query = request.POST.get('search')  # Get the search query from the request's GET parameters
    if query:
        search_results = Blog.objects.filter(title__icontains=query)
            
        
    else:
        search_results = []  # Return an empty list if no query is provided
        return render(request, 'Blog/search.html', {'search_results': search_results, 'query': query})

        
        # try:
        
        #     if request.method=='POST':
        #         search=request.POST.get('search')
        #         blog=Blog.objects.filter(title__icontains=search)
                
        #         if blog:

        #             context={'blogs':blog}
        #             return render(request,'blog/search.html',context)
        #         else:
        #             return HttpResponse("no post ")


        #         # else:
        #         #     blog=Blog.objects.all()
        #         #     context={'blogs':blog}
        #         #     return render(request,'blog/search.html',context)
        
        # except Exception as e:
        #     print(e)
        # return render(request,'blog/search.html')






def contact(request):
    return render(request,'Blog/contact.html')

def comment(request,uid):
    if 'uid' in request.COOKIES:
        uuid=request.COOKIES['uid']

        user=User.objects.get(uid=uuid)
        blog=Blog.objects.get(uid=uid)

        blog_comment=blog.comment
            
            

        if request.method=="POST":
        
            name=request.POST.get('name')
            # email=request.POST.get('email')
            # subject=request.POST.get('subject')
            message=request.POST.get("message")

            blog_comment=blog_comment+1
            blog.comment=blog_comment
                # print(blog.comment)
            
            comment=Comment.objects.create(blog=blog,name=name,message=message)
            blog.save()
                
                
            url=f'/single_blog/{uid}'
            return redirect(url)      
    else:
        messages.warning(request,"Please signin")
        return redirect("/user/signin")
        


    # def popular_posts(request):
    #     blog=Blog.objects.all()
    #     # if blog.comment>=2:
            
    #     popular_posts=Blog.objects.filter(comment=2)

    #     # comment=Comment.objects.all()
    #     # if comment.blog==3:
    #     #     blog=Comment.objects.filter(blog=comment)
            

    #     context={"popular_posts":popular_posts}
    #     return render(request,'Blog/index.html',context)