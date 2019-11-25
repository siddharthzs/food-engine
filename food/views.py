from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from food.models import Food
from food.forms import SignUpForm , FoodForm

from food.google import process
from food.amazon import peak
from mlmodel import predictfood



def signup(request):
    if request.method == 'POST':
        print(request.POST['username'])
        a = {'username' : request.POST['username'] , 'email':request.POST['email'],'password1':request.POST['password1'],
                          'password2':request.POST['password2']}
        form = SignUpForm(a)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
        return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def foods(request):
    if request.method == 'POST':
        name = request.POST['food_name']
        s = Food.objects.create(name=name , user=request.user)
        return redirect('home')
    else:
        form = FoodForm()
        a = Food.objects.filter(user_id = request.user.id)
        return render(request, 'food.html', {'form': form , 'food': a})

def foods_delete(request , id):
    s = Food.objects.get(id=id)
    s.delete()
    return redirect('home')

def home(request ):
    a = Food.objects.filter(user_id=request.user.id)
    form = FoodForm()
    return render(request,'home.html',{'user':request.user.username ,'form': form ,'food':a,'detail':process('food') ,'rate':0})
    #return render(request, 'home.html',{'user':request.user.username ,'form': form ,'food':a ,'rate':0})

def particular_food(request ,id):
    a = Food.objects.get(id=id)
    s = Food.objects.filter(user_id=request.user.id)
    form = FoodForm()
    return render(request,'home.html',{'user':request.user.username ,'form': form ,'food':s ,'detail':process(a.name)  ,'rate':0})
    #return render(request, 'home.html', {'user':request.user.username ,'form': form , 'food': s,'rate':0 })

def search(request  ):
    if request.method == 'POST':
        name = request.POST['query']
        a = Food.objects.filter(user_id=request.user.id)
        form = FoodForm()
        b = predictfood(peak(name))
        return render(request, 'home.html',
                      {'user': request.user.username, 'form': form, 'food': a, 'detail': "",'rate':b})

