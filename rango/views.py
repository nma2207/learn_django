from .forms import CategoryForm
from .forms import PageForm
from .forms import UserForm
from .forms import UserProfileForm

from .models import Category
from .models import Page
from .models import UserProfile

from .bing_search import run_query

from datetime import datetime


from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect





def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits

    print('visits',visits)
    response = render(request, 'rango/index.html', context_dict)

    return response

def about(request):
    return render(request, "rango/about.html", {})

def category(request, category_name_slug):

    context_dict = {}
    #category_name_slug = "Python"

    try:
        category = Category.objects.get(slug = category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category = category)

        context_dict['pages'] = pages

        context_dict['category'] = category

        context_dict['category_name'] = category.name
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit = True)

            return index(request)
        else:
            print(form.error)
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if cat:
                page = form.save(commit = False)
                page.category = cat
                page.views = 0
                page.save()

                return category(request, category_name_slug)
        print(form.errors)

    else:
        form = PageForm()

    context_dict = {'form': form,
                    'category': cat}

    return render(request, 'rango/add_page.html', context_dict)

def regicter(request):

    registered = False
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            pass
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered}

    return render(request, 'rango/register.html', context_dict)


def user_login(request):
    #print("HII")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate( username=username, password=password)
        if user:
            if user.is_active:
                login(request=request, user = user)
                return HttpResponseRedirect('/rango/')

            else:
                return HttpResponse('Yout Rango accout is disabled')
        else:
            print('Invalid login details: {0}, {1}'.format(username, password))
            return HttpResponse("Incalid login")
    else:
        return render(request, 'rango/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


def search(request):
    result_list = []
    if request.method == "POST":
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)
    return render(request, 'rango/search.html', {'result_list':result_list})


def track_url(request):
    page_id = None
    url = '/rango/'

    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']

            try:
                page = Page.objects.get(id = page_id)
                page.views = page.views + 1
                page.save()
                url = page.url

            except:
                pass
    return redirect(url)


def profile(requset):
    current_user = requset.user
    context_dict = {}
    print(current_user.username)
    try:
        user_profile = UserProfile.objects.get(user = current_user)
        context_dict['profile'] = user_profile
    except:
        print("Can't get profile!")
    print(context_dict)
    return render(requset, 'rango/profile.html', context_dict)
