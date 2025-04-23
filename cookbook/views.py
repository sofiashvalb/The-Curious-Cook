from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Count, Q


from .models import User, Category, Card

from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django.conf import settings
from django.utils import translation

def test_translation(request):
    active_language = get_language()
    print(f"Active language: {active_language}")  # Debugging line
    translated = _("Always experimenting with new flavors and adding a twist to classics.")
    return HttpResponse(f"{translated} (Active language: {active_language})")

def set_language(request):
    lang = request.GET.get('language', 'en')
    next_url = request.GET.get('next', '/')
    response = HttpResponseRedirect(next_url)
    
    # Set language
    translation.activate(lang)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response

# Create your views here.

def index(request):   

    cards = Card.objects.all()
    categories = Category.objects.all()

    return render(request, 'cookbook/index.html', {
        "cards":cards,
        "categories":categories
    })

def talk(request):
    categories = Category.objects.all()

    if request.user.is_authenticated:
        name = request.user.username
        email = request.user.email
    else:
        name = ''
        email = ''

    return render(request, 'cookbook/talk.html', {
        "name": name,
        "email": email,
        "categories": categories,
    })

def search(request):
    categories = Category.objects.all()

    if request.method == "POST":
        word = request.POST['search']
        
        # Search similar words in cards.title + cards.categories
        cards = Card.objects.filter(Q(title__icontains=word) | Q(categories__categoryname__icontains=word)).distinct()

        message = None
        if not cards:
            message = "No recipes found for your search. Try exploring the categories for some inspiration"       

    return render(request, 'cookbook/search.html', {
        "cards":cards,
        "word":word,
        "message":message,
        "categories":categories
    })

def recipe(request, card_id): 
    categories = Category.objects.all()
    # Annotate the number of likes and add anon_like in Python
    top_cards = Card.objects.annotate(like_count=Count('liked')).all()

    # Add anon_like to each card’s total likes in Python, and sort
    top_cards = sorted(top_cards, key=lambda card: card.like_count + card.anon_like, reverse=True)[:5]


    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return HttpResponse("Card not found.", status=404)
    
    template_name = 'cookbook/recipes/{}.html'.format(card.filename) 

    # If template file exists
    try:
        return render(request, template_name, {
            "card": card,
            "categories":categories,
            "top_cards": top_cards,

        })
    except:
        return HttpResponse("No matching recipe found.")

def saved(request, user_id):
    user = User.objects.get(id=user_id)
    cards = Card.objects.filter(saved=user)

    categories = Category.objects.all()

    message = None
    if not cards:
        message = "Looks like you have'nt picked recipes to try. What are you waiting for?"

    return render(request, 'cookbook/saved.html', {
        "user":user,
        "cards":cards,
        "message":message,
        "categories":categories
    })

def top(request):
    categories = Category.objects.all()

    # Annotate the number of likes and add anon_like in Python
    top_cards = Card.objects.annotate(like_count=Count('liked')).all()

    # Add anon_like to each card’s total likes in Python, and sort
    top_cards = sorted(top_cards, key=lambda card: card.like_count + card.anon_like, reverse=True)[:5]


    return render(request, 'cookbook/top.html', {
        "top_cards": top_cards,
        "categories":categories
    })

def vote(request, card_id):
    card = Card.objects.get(id=card_id)
    user = request.user

    liked = False

    if user.is_authenticated: 
        if user in card.liked.all():  
            card.liked.remove(user) 
            liked = False
        else:
            card.liked.add(user) 
            liked = True
    else:
        # Anonymous like
        card.anon_like += 1  
        liked = True  

    card.save()

    return JsonResponse({
        'liked': liked,
        'total_likes': card.total_likes,  # Total likes (sum of registered + anonymous)
        
    })

def savedrecipe(request, card_id):
    saved = False
    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return JsonResponse({'error': 'Card not found'}, status=404)

    user = request.user
    if user.is_authenticated:
        print(f"User {user.username} is authenticated")

        if user in card.saved.all():
            card.saved.remove(user)
            saved = False
            print(f"User {user.username} unsaved card {card.title}")
        else:
            card.saved.add(user)
            saved = True
            print(f"User {user.username} saved card {card.title}")

        card.save()  
        print(f"Card saved status: {saved}")
        return JsonResponse({'saved': saved})
    else:
        return JsonResponse({'saved': saved, 'redirect': True})



def category(request, categories_id):
    # Get all categories for the dropdown
    categories = Category.objects.all()

    category_name = get_object_or_404(Category, id=categories_id)
    cards = Card.objects.filter(categories=category_name)

    message = None
    if not cards:
        message = "Looks like the chef is still in the kitchen. Come back soon for fresh recipes!"

    return render(request, 'cookbook/category.html', {
        "categoryName": category_name,  # Pass the category object to the template
        "cards": cards,
        "categories": categories,
        "message": message
    })

def loginuser(request):
    categories = Category.objects.all()

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "cookbook/login.html", {
                "message": "Invalid username and/or password.",
                "categories":categories
            })
    else:
        return render(request, "cookbook/login.html", {
            "categories":categories
        })

def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def registeruser(request):
    categories = Category.objects.all()

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # if password matches 
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "cookbook/register.html", {
                "message": "Passwords must match.",
                "categories":categories
            })

        # create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "cookbook/register.html", {
                "message": "Username already taken.",
                "categories":categories
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cookbook/register.html",{
            "categories": categories
        })




