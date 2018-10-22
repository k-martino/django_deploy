import re

import bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class UserManager(models.Manager):
    @staticmethod
    def user_validator(post_data):
        errors = {}
        # Check for length
        if len(post_data["first_name"]) < 2:
            errors["first_name_len"] = "First name must have at least 2 characters"
        if len(post_data["last_name"]) < 2:
            errors["last_name_len"] = "Last name must have at least 2 characters"
        if len(post_data["email"]) < 2:
            errors["email_len"] = "Email must have at least 2 characters"
        if len(post_data["pw"]) < 8:
            errors["password_len"] = "Password must have at least 8 characters"
        # Make sure names are only letters
        if not post_data["first_name"].isalpha():
            errors["first_name_alpha"] = "First name must only contain letters"
        if not post_data["last_name"].isalpha():
            errors["last_name_alpha"] = "Last name must only contain letters"
        # Make sure email matches format
        if not EMAIL_REGEX.match(post_data["email"]):
            errors["email_format"] = "Invalid email format"
        # Make sure email isn't already in the list
        if User.objects.filter(email=post_data["email"]):
            errors["email_used"] = "Email already in use"
        # Make sure both passwords match
        if post_data["pw"] != post_data["pw_confirm"]:
            errors["pw_match"] = "Passwords do not match"
        return errors

    @staticmethod
    def login_validator(post_data):
        errors = {}
        # Check if email is in the database
        if not User.objects.filter(email=post_data["email"]):
            errors["email_db_check"] = "Invalid credentials"
        # Check for correct password
        else:
            log_user = User.objects.filter(email=post_data["email"])[0]
            if not bcrypt.checkpw(post_data["pw"].encode(), log_user.pw_hash.encode()):
                errors["pw_db_check"] = "Invalid credentials"
        return errors


class JobManager(models.Manager):
    @staticmethod
    def job_validator(post_data):
        errors = {}
        # Checking for length
        if len(post_data["title"]) < 3:
            errors["title"] = "Title must have at least 3 characters"
        if len(post_data["description"]) < 3:
            errors["description"] = "Description must have at least 3 characters"
        if len(post_data["location"]) < 3:
            errors["location"] = "Location must have at least 3 characters"
        # if post_data["category"] == "Other":
        #     if len(post_data["new_category"]) < 3:
        #         errors["category"] = "Category must have at least 3 characters"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Job(models.Model):
    title = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="posted_jobs", on_delete=models.CASCADE)
    accepted_by = models.ForeignKey(User, related_name="accepted_jobs", null=True)
    category = models.ForeignKey(Category, related_name="jobs", null=True)
    desc = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()
