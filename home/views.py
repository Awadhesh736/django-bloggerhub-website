from django.shortcuts import render,HttpResponse,redirect
from  home.models import Contact,Yourblog
from django.contrib import messages
from django.core.mail import send_mail 

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post
# Create your views here.
def home(request):
    return render(request, 'home/home.html')
    
def about(request):
    
    return render(request, 'home/about.html')
   
def contact(request):
    
    if request.method =='POST':
       name = request.POST['name']
       email = request.POST['email']
       phone = request.POST['phone']
       content = request.POST['content']
       

       if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
           messages.error(request, 'please fill the form correctly')
       else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your messege has been sent.")
      
       contact = Contact(name=name, email=email, phone=phone, content=content)
       contact.save()
      
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query)>80:
        allPosts = Post.objects.none()
    else:
         allPostsTitle = Post.objects.filter(title__icontains=query)
         allPostsContent = Post.objects.filter(content__icontains=query)
         allPosts = allPostsTitle.union(allPostsContent)
        
    if allPosts.count() == 0:
        messages.warning(request, 'No search results found.')
    
    params = {'allPosts': allPosts, 'query':query}
    return render(request, 'home/search.html', params )

# Authentication APIs
def handleSignup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # check for errorneous inputs
        if len(username) > 10:
            messages.error(request, "Your username must be under 10 characters.")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "Username only should contain number and alphabets.")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('home')

        #create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your Bloggers-Hub account has been created successfully.")
        return redirect('home')



    else:
        return HttpResponse('404 -  Not Found')


def handleLogin(request):
    
    loginusername = request.POST['loginusername']
    loginpassword = request.POST['loginpassword']

    user = authenticate(username=loginusername, password=loginpassword)
    if user is not None:
        login(request, user)
        messages.success(request, "successfully Logged in")
        return redirect('home')
    else:
        messages.error(request, "Invalid credential")   

def handleLogout(request):
    logout(request)
    messages.success(request, "successfully logged out") 
    return redirect('home')

def yourblog(request):
    if request.method =='POST':
       author = request.POST['author']
       blogy = request.POST['blogy']
       photo = request.POST['photo']
       print(blogy, photo, author)

       if len(author)<2 or len(blogy)<70 :
           messages.error(request, 'please fill it properly')
       else:
            yourblog = Yourblog(blogy=blogy, photo=photo, author=author)
            yourblog.save()
            messages.success(request, "Your messege has been sent.")

       yourblog = Yourblog(blogy=blogy, photo=photo, author=author)
       yourblog.save()
       
       
       
       
    return render(request, 'home/yourblog.html')
    
   
    
    
    