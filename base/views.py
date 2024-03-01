from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.http import HttpResponse

from .models import Room,Topic,message,User
from .forms import Roomform,Userform,myusercreationsform
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import myusercreationsform

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ""
    rooms=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics=Topic.objects.all()[0:3]
    room_count=rooms.count()
    Room_Message=message.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms,'topics':topics,'room_count':room_count,"Room_Message":Room_Message}
    return render(request,'base/home.html',context)


def logout_page(request):
    logout(request)
    return redirect('home')



def login_form(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"user doesn't exsit")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'user name or password not crroect')
    context={'page':page}
    return render(request,'base/Login_Reg.html',context)

def user_profile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    Room_Message=user.message_set.all()
    topics=Topic.objects.all()
    context={"user":user,"rooms":rooms,"Room_Message":Room_Message,"topics":topics}
    return render(request,'base/user_profile.html',context)

def register_page(request):
    form=myusercreationsform()
    if request.method=="POST":
        form=myusercreationsform(request.POST)
        if form .is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
             messages.error(request,"user or possword not croorct during register")
    
    context={"form":form}
    return render(request,'base/Login_Reg.html',context)



def room(request,pk):
    ro=Room.objects.get(id=pk,)
    room_messages=ro.message_set.all()
    participents=ro.participents.all()
    if request.method=='POST':
        Message=message.objects.create(
            user=request.user,
            room=ro,
            body=request.POST.get("body")
        )
        ro. participents.add(request.user)
        return redirect('room',pk=ro.id)
    context={"ro":ro,'room_messages':room_messages,'participents': participents}
    return render(request,'base/room.html',context)



@ login_required(login_url='login')
def creat_form(request):
    form=Roomform()
    topics=Topic.objects.all()
    if request.method=="POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            Host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'))
        # form=Roomform(request.POST)
        # form.save()
        # if form.is_valid() ==True:
        #     room=form.save(commit=False)
        #     room.Host=request.user
        #     room.save()
        return redirect('home')
    context={'form':form,'topics':topics}
    return render(request,'base/Form.html',context)


@ login_required(login_url='login')
def update_room(request,pk):
    room=Room.objects.get(id=pk)
    form=Roomform(instance=room)
    topics=Topic.objects.all()
    if request.user != room.Host:
        return redirect('home')
    if request.method=="POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        # form =Roomform(request.POST,instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')
    context={"form":form,'topics':topics,'room':room}
    return render(request,'base/Form.html',context)


@ login_required(login_url='login')
def delete_room(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.Host:
        return redirect('home')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete_form.html',{'obj':room})


@ login_required(login_url='login')
def delete_message(request,pk):
    Mess=message.objects.get(id=pk)
    if request.user != Mess.user:
        return HttpResponse("you are not allowed delete message")
    if request.method=="POST":
        Mess.delete()
        return redirect('home')
    return render(request,'base/delete_form.html',{'obj':Mess})




@ login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=Userform(instance=user)
    if request.method =='POST':
        form=Userform(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_pro',pk=user.id)
    else:
        messages.error(request,"data is not valid")
    return render(request,'base/edit-user.html',{'form':form})
def topicList(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ""
    topics=Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})
def activity(request):
    Room_Message=message.objects.all()
    return render(request,'base/activity.html',{'Room_Message':Room_Message})