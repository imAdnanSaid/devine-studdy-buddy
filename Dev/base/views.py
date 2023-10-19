from django.shortcuts import redirect, render, HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm, MyUserCreationForm, RegisterForm

# Create your views here.

def loginpage(request):

    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Doesnot Exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)

            return redirect('home')

        else:
            messages.error(request, 'Username or password Doesnot Exist')

    if request.user.is_authenticated:
        return redirect('home')
    
    context = locals()

    return render(request, 'base/login_register.html', context)


def registerpage(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')


    context = locals()
    return render(request, 'base/login_register.html', context)


def logoutuser(request):
    logout(request)

    return redirect('home')

def topics(request):
    topics = Topic.objects.all()

    return render(request, 'base/topic_component.html', locals())
    

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q)|Q(description__icontains = q)|Q(name__icontains = q))
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')
    context = locals()


    return render(request, 'base/home.html', context)


def room(request, pk):

    room = Room.objects.get(id=pk)
    participants = room.participants.all()
    room_messages = room.message_set.all().order_by('-created')
    if request.method=='POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)

        return redirect('room', pk = room.id)
    context = locals()
    return render(request, 'base/room.html', context)

def userprofile(request, pk):

    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all().order_by('-created')
    topics = Topic.objects.all()
    context = locals()
    return render(request, 'base/profile.html', context)


@login_required(login_url='/login')
def createroom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room = Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
            )
        room.save()

        return redirect('home')
    context = locals()
    return render(request, 'base/room-form.html', context)




@login_required(login_url='login')
def updateroom(request, pk):

    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    
    # if request.user == room.host:
    #     return HttpResponse('You Are Not Allowed')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect('home')

    context = locals()
    return render(request, 'base/room-form.html', context)


@login_required(login_url='login')
def deleteroom(request, pk):
    room = Room.objects.get(id=pk)
    context = {'obj':room}
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)


def deletemessage(request, pk):
    message = Message.objects.get(id=pk)
    room = Room.objects.get(id=message.room.id)
    context = {'obj':message}
    if request.method == 'POST':
        message.delete()
        return redirect('room', room.id)
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def updateuser(request, pk):
    user = User.objects.get(id=pk)
    form = MyUserCreationForm(instance=user)

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            return redirect('profile' ,user.id)


    context = locals()

    return render(request, 'base/update-user.html', context)

def topicspage(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    topics = Topic.objects.filter(Q(name__icontains=q))

    return render(request, 'base/topics.html', locals())


def activitypage(request):
    room_messages = Message.objects.all().order_by('-created')

    return render(request, 'base/activity.html', locals())