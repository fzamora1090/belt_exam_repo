from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime
from datetime import date
import datetime

#NOW datetime for adding time
from datetime import date
today = date.today()

# Create your views here.
def index(request):



    return render(request, 'belt_exam_app/index.html')


def register(request):
    print("POST DATA REG:", request.POST )

#VALIDATION FOR REGISTRATION FORM
    errors = User.objects.basic_validator(request.POST)
    print(errors)

    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')

    else:
#HASHING PASSWORD
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print(pw_hash)

        #if email does not exist alrady then okay if it exists throw ERROR
        if request.POST['email'] not in User.objects.filter(email=request.POST['email']):
        #CREATING new user WITH pw_hash!!
            new_user = User.objects.create(first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        email=request.POST['email'],
                                        password=pw_hash)

            print("USER CREATED --------", new_user)

            # Setting user EMAIL iN SESSION
            print('-------EMAIL AND ID IN SESSION:', new_user.email, new_user)
            request.session['email'] = new_user.email
            request.session['id'] = new_user.id

            return redirect('/wishes')

        else:
            messages.error(request, 'Email already in use')





def login(request):
    print("POST DATA LOGIN:", request.POST )


    #VALIDATION FOR LOGIN FORM
    errors = User.objects.login_validator(request.POST)
    print(errors)

    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')

    else:
        #matching user info with queried user list to find USER AND SET SESSION
        matched_user_list = User.objects.filter(email=request.POST['email'])

        if len(matched_user_list) > 0 and matched_user_list[0].email == request.POST['email']:
            request.session['email'] = matched_user_list[0].email

            return redirect('/wishes')

        else:
            # pymsgbox.alert(text='User Not Found', title='Fail!', button='Ok')
            messages.error(request, "No user found!")

            return redirect('/')


def wishes (request):
    #matching User with the email provided in SESSION and passing the user info in CONTEXT
    user = User.objects.get(email=request.session['email'])

    #query for all users and all liekd books by user
    allUsers = User.objects.all()
    likedItem = user.liked_items.filter(users_who_liked=user.id)
    allItems = Item.objects.all()

    for item in allItems:
        if item.isGranted == True:
            if len(item.users_who_liked.all()) < 0:
                item.likeCount = 0
            else:
                item.likeCount = len(item.users_who_liked.all())

    context = {
        'item.likeCount': item.likeCount,
        'user': user,
        'alUsers': allUsers,
        'allItems': allItems,
        'likedItems': user.liked_items.filter(users_who_liked=user.id),

    }

    return render(request, 'belt_exam_app/wishes.html', context)



def wishes_edit(request, id):
    item = Item.objects.get(id=id)
    user = User.objects.get(email=request.session['email'])

    context = {
        'user': user,
        'item': item
    }


    return render(request, 'belt_exam_app/edit_wishes.html', context)


def update(request, id):
    print('UPDATE DATA`````````', request.POST)
    item = Item.objects.get(id=id)

    item.item_name = request.POST['item_name']
    item.desc = request.POST['description']
    item.save()

    return redirect('/wishes')



def new_wish(request):
    user = User.objects.get(email=request.session['email'])

    context ={
        'user': user,
    }

    return render(request, 'belt_exam_app/new_wish.html', context)




def make_wish(request):
    #VAL for items
    if 'email' not in request.session:
        messages.error(request, 'Please log in')
        
        return redirect('/')
    
    else: 
        #matching User with the email provided in SESSION and passing the user info in CONTEXT
        print('ADDING ITEM DATA', request.POST)

        errors = Item.objects.basic_validator(request.POST)
        print(errors)

        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/newWish')

        else:
            this_user = User.objects.get(email=request.session['email'])
            print(this_user.first_name)

            #creating item!! with many to many and one to many relationship (uploaded_by)
            new_item = Item.objects.create(item_name=request.POST['item_name'],
                                            desc=request.POST['description'],
                                            uploaded_by=this_user,
                                            likeCount=0
                                            )

            new_item.users_who_liked.add(this_user)


            #BOOK Created 
            print('BOOK CREATED---------:', new_item)

            context = {
                'allItems': Item.objects.all(),
                'user': this_user,
                'newItem': new_item,
            }
            
            print(this_user.liked_items.values())

            return redirect('/wishes', context)


def granted(request, id):

    item = Item.objects.get(id=id)
    user = User.objects.get(email=request.session['email'])

    item.isGranted = True
    item.date_granted = today
    item.save()

    print(item.isGranted)
    print(item.date_granted)

    return redirect('/wishes')

def add_liked_item(request, id):
    item = Item.objects.get(id=id)
    user = User.objects.get(email=request.session['email'])
    print(item.likeCount)
    item.likeCount += 1
    print(item.likeCount)

    #addtoFAVS
    item.users_who_liked.add(user)

    return redirect('/wishes')


def unlike(request, id):
    item = Item.objects.get(id=id)
    user = User.objects.get(email=request.session['email'])
    item.likeCount = item.likeCount - 1
    print(item.likeCount)

    user.liked_items.remove(item)


    return redirect('/wishes')


def remove_item(request, id):
    
    item = Item.objects.get(id=id)

    item.delete()

    
    return redirect('/wishes')



def stats(request, id):
    user = User.objects.get(email=request.session['email'])

    #query for all users and all liekd books by user
    allUsers = User.objects.all()
    likedItems = user.liked_items.filter(users_who_liked=user.id)
    allItems = Item.objects.all()
    grantedCount = 0
    grantUserCount = 0
    notGrantUserCount = 0
    
    for item in allItems:
        if item.isGranted == True:
            grantedCount = grantedCount + 1
    
    for item in likedItems:
        if item.isGranted == True:
            grantUserCount = grantUserCount + 1
    
    for item in likedItems:
        if item.isGranted == False:
            notGrantUserCount = notGrantUserCount + 1





    #passing db query data in context to front end
    context = {
        'grantedCount': grantedCount,
        'grantUserCount': grantUserCount,
        'notGrantUserCount': notGrantUserCount,

        'user': user,
        'alUsers': allUsers,
        'allItems': Item.objects.all(),
        'likedItem': user.liked_items.filter(users_who_liked=user.id)
    }

    return render(request, 'belt_exam_app/stats.html', context)

def logout(request):
    request.session.clear()

    return redirect('/')
