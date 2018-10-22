import bcrypt
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import *


# render
def index(request):
    if 'logged_in' in request.session and 'user_id' in request.session:
        context = {
            'jobs': Job.objects.all(),
            'accepted_jobs': Job.objects.filter(accepted_by_id=request.session["user_id"]),
            'available_jobs': Job.objects.filter(accepted_by_id__isnull=True),
        }
        return render(request, 'exam/dashboard.html', context)
    else:
        return render(request, "exam/index.html")


def new_job(request):
    if 'logged_in' in request.session and 'user_id' in request.session:
        context = {
            'categories': Category.objects.all(),
        }
        return render(request, "exam/new_job.html", context)
    else:
        return redirect(index)


def view_job(request, job_id):
    if 'logged_in' in request.session and 'user_id' in request.session:
        context = {
            'job': Job.objects.get(id=job_id),
        }
        return render(request, 'exam/view_job.html', context)
    else:
        return redirect(index)


def edit_job(request, job_id):
    if 'logged_in' in request.session and 'user_id' in request.session:
        context = {
            'job': Job.objects.get(id=job_id),
            'categories': Category.objects.all(),
        }
        return render(request, 'exam/edit_job.html', context)
    else:
        return redirect(index)


# process & redirect
def register(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags="signup_errors")
        return redirect("/")
    else:
        user = User.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            pw_hash=bcrypt.hashpw(request.POST["pw"].encode(), bcrypt.gensalt()),
        )
        request.session["user_id"] = user.id
        request.session["logged_in"] = True
        request.session['first_name'] = user.first_name
        return redirect(index)


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags="login_errors")
        return redirect("/")
    else:
        user = User.objects.get(email=request.POST["email"])
        request.session["user_id"] = user.id
        request.session["logged_in"] = True
        request.session['first_name'] = user.first_name
        return redirect(index)


def logout(request):
    request.session.clear()
    return redirect(index)


def process_job(request):
    if request.method == "POST":
        errors = Job.objects.job_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags="job_errors")
            return redirect(new_job)
        else:
            title = request.POST["title"]
            desc = request.POST["description"]
            location = request.POST["location"]
            posted_by = User.objects.get(id=request.session["user_id"])
            # if request.POST["category"] == "Other":
            #     category = Category.objects.create(name=request.POST("new_category"))
            # else:
            #     category = Category.objects.filter(name=request.POST["category"])[0]
            job = Job.objects.create(
                title=title,
                desc=desc,
                location=location,
                posted_by=posted_by,
                # category_id=category.id,
            )
            return redirect(index)


def process_edit(request):
    if request.method == "POST":
        errors = Job.objects.job_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags="job_errors")
            return redirect(edit_job)
        else:
            job = Job.objects.get(id=request.POST["job_id"])
            job.title = request.POST["title"]
            job.desc = request.POST["description"]
            job.location = request.POST["location"]
            # if request.POST["category"] == "Other":
            #     category = Category.objects.create(name=request.POST("new_category"))
            # else:
            #     category = Category.objects.filter(name=request.POST["category"])[0]
            job.save()
            return redirect(index)


def accept(request, job_id):
    job = Job.objects.get(id=job_id)
    job.accepted_by_id = request.session["user_id"]
    job.save()
    return redirect(index)


def give_up(request, job_id):
    job = Job.objects.get(id=job_id)
    job.accepted_by_id = None
    job.save()
    return redirect(index)


def destroy(request, job_id):
    b = Job.objects.get(id=job_id)
    b.delete()  # deletes that particular record
    return redirect(index)
