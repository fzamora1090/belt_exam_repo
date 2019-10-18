from django.db import models
import re
from datetime import datetime
from .models import *




#VALIDATION USER CLASS/basic_validator
class UserManager(models.Manager):
    def basic_validator(self, postData):

        errors = {}

        if len(postData['first_name']) < 2:
           errors['first_name'] = "First name should be longer than 2 characters"


        if len(postData['last_name']) < 2:
           errors['last_name'] = "Last name should be longer than 2 characters"
        
        #checking the fomrmat of the entered email!!
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")

        #matching the passwords
        if postData['password'] != postData['password_confirm']:
            errors['passwordMatch'] = "Passwords do not match!"
        
        if len(postData['password']) < 8:
            errors['passwordLength'] = "Password should be longer than 8 characters"

        return errors

#login valid
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")

        # if postData['password'] != postData['password']:
        #             errors['passwordMatch'] = "Passwords do not match!"
                
        if len(postData['password']) < 8:
            errors['password'] = "Login invalid"



        return errors





#item VALIDATOR INFO
class ItemManager(models.Manager):
    def basic_validator(self, postData):

        errors = {}

        if len(postData['item_name']) < 3:
           errors['item_name'] = "Item name must be longer than 3 characters."


        if len(postData['description']) < 3:
           errors['description'] = "Description should be longer than 3 characters"

        return errors


# classes!!

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=150)

    #ONE TO MANY
    #liked_items list of items liked by user

    #items_uploaded list of items uplaoded by user

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #PASS VALIDATION MANAGER
    objects = UserManager()


class Item(models.Model):
    item_name = models.CharField(max_length=50)
    desc = models.TextField(max_length=100)

    #ONE to MANY  item uploaded by and for user: items_uploaded
    uploaded_by = models.ForeignKey(User, related_name='items_uploaded')
    #user who uplaoded the item

    #MANY to MANY Relationship!!!
    users_who_liked = models.ManyToManyField(User, related_name="liked_items")
    #list of users who like a given item User: liked_items
    # likes = len(item.users_who_liked.values())
    likeCount = models.IntegerField(default=False)

    isGranted = models.BooleanField(default=False)
    date_granted = models.DateTimeField(auto_now=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #PASSING BOOK VALIDATION
    objects = ItemManager()
