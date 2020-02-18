from django.shortcuts import HttpResponse, render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from apps.job_app.models import *
import bcrypt

def index(request):
    return render(request, 'job_app/index.html')

def register(request):
    existing_users = User.objects.filter(email=request.POST['email'])

    if existing_users:
        return redirect('/')
    
    if not User.objects.reg_valid(request):
        return redirect('/')
    print('')
    hashed = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
    new_user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=hashed)

    request.session['uid'] = new_user.id
    return redirect('/dashboard')

def login(request):
    existing_users = User.objects.filter(email=request.POST['email'])

    if existing_users:
        user = existing_users[0]

        pw_matched = bcrypt.checkpw(request.POST['password'].encode(),
                                    user.password.encode())
        if pw_matched:
            request.session['uid'] = user.id
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/')
    else:
        messages.error(request, "Invalid credentials")
        messages.error(request, "Please try again")
        return redirect("/")

    return redirect("/dashboard")


def logout(request):
    request.session.clear()
    # print('home')
    return redirect('/')

def dashboard(request):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")



    info={
        'jobs' : Job.objects.all(),
        'user': User.objects.get(id=uid),
        'got': Job.objects.filter(got=False).filter(creater=uid),


    }

    return render(request, 'job_app/dashboard.html',info)

def new(request):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")

    info={
        'user': User.objects.get(id=uid)
    }

    return render(request, 'job_app/new.html',info)

def create_job(request):
    uid = request.session.get("uid")

    # if not uid:
    #     return redirect("/")

    if not Job.objects.job_valid(request):

        return redirect('dashboard/new')

    user = User.objects.get(id=uid)

    job = Job.objects.create(title=request.POST['title'],description=request.POST['description'],location=request.POST['location'],creater=user,got=False)

    return redirect('/dashboard')

def edit_form(request,job_id):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")

    info={
        'user': User.objects.get(id=uid),
        'job': Job.objects.get(id=job_id),
    }

    return render(request, 'job_app/edit_form.html', info)

def editing(request, job_id):

    if not EditJob.objects.edit_valid(request):
        return redirect('/dashboard/edit_form/'+job_id)

    edit_job = Job.objects.get(id=job_id)
    edit_job.title=request.POST['edit_title']
    edit_job.save()

    edit_job = Job.objects.get(id=job_id)
    edit_job.description = request.POST['edit_description']
    edit_job.save()

    edit_job = Job.objects.get(id=job_id)
    edit_job.location = request.POST['edit_location']
    edit_job.save()

    return redirect('/dashboard')


def details(request,job_id):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")

    info={
        'user' : User.objects.get(id=uid),
        'job': Job.objects.get(id=job_id),
    }

    return render(request, 'job_app/details.html', info)

def remove(request,job_id):
    del_job = Job.objects.get(id=job_id)
    del_job.delete()

    return redirect('/dashboard')

