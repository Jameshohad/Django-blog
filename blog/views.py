from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from rest_framework import viewsets

from .models import Post
from .forms import NewUserForm, CommentForm
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    context_object_name = 'post_list'


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)


    comments = post.comments.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must log in before posting a comment.")
            return redirect('login')

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    return render(
        request,
        'post_detail.html',
        {
            'post': post,
            'comments': comments,
            'comment_form': comment_form,
        }
    )


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()

    return render(
        request=request,
        template_name="register.html",
        context={"register_form": form}
    )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(
        request=request,
        template_name="login.html",
        context={"login_form": form}
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


#  Cookie test 
def cookie_session(request):
    request.session.set_test_cookie()
    return HttpResponse("<h1>Test cookie has been set.</h1>")


def cookie_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        return HttpResponse("<h1>Your browser accepts cookies.</h1>")
    else:
        return HttpResponse("<h1>Your browser does not accept cookies.</h1>")


#  Session demo 
def create_session(request):
    request.session['name'] = 'username'
    request.session['password'] = 'password123'
    return HttpResponse("<h1>Session is set.</h1>")


def access_session(request):
    response = "<h1>Session data:</h1>"

    if request.session.get('name'):
        response += f"<p>Name: {request.session.get('name')}</p>"

    if request.session.get('password'):
        response += f"<p>Password: {request.session.get('password')}</p>"
        return HttpResponse(response)
    else:
        return redirect('/session/create/')


def delete_session(request):
    try:
        del request.session['name']
        del request.session['password']
    except KeyError:
        pass

    return HttpResponse("<h1>Session data cleared.</h1>")