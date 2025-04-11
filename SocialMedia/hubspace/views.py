from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from .models import Profile, Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.

app_name = 'hubspace'

def users(request):
    """Shows a list of profiles using the site"""
    # get list of all profiles from the database
    users_list = Profile.objects.order_by("firstName")
    # store it in a 'context dictionary', to give the html
    context = {"profiles" : users_list}
    # return render
    return render(request, 'hubspace/users.html', context)


def profile_page(request, id):
    """Shows a profiles page"""
    # Fetch the Profile object based on 'id'
    profile = get_object_or_404(Profile, id = id)
    posts = profile.posts.all()
    # store it in a 'context dictionary', to give the html
    context = {'profile' : profile, 'posts' : posts}
    return render(request, 'hubspace/profile.html', context)


def new_post(request, id):
    """Profile adds a new post"""
    # Fetch the Profile object based on 'id'
    profile = get_object_or_404(Profile, id=id)

    # Handle GET request (display empty form)
    if request.method != 'POST':
        post_form = PostForm()
        context = {'form': post_form, 'profile': profile}
        return render(request, 'hubspace/new_post.html', context)

    # Handle POST request (form submission)
    post_form = PostForm(request.POST)
    if post_form.is_valid():
        # Save the new post (but don't commit yet)
        new_post = post_form.save(commit=False)
        # Associate the new post with the current profile (author)
        new_post.author = profile
        # Save the post
        new_post.save()
        # Redirect to the profile page (or wherever you want)
        return HttpResponseRedirect(reverse('hubspace:profile_page', args=[id]))
    else:
        # If the form is invalid, re-render the form with error messages
        return render(request, 'hubspace/new_post.html', {'form': post_form, 'profile': profile})


def new_comment(request, profile_id, post_id):

    # extract important information into variables

    author = get_object_or_404(Profile, id=profile_id)
    post = get_object_or_404(Post, id = post_id)

    # Handle GET request (display empty form)
    if request.method != 'POST':
        comment_form = CommentForm()
        context = {'form': comment_form, 'author': author, 'post' : post}
        return render(request, 'hubspace/new_comment.html', context)

    # Handle POST request (form submission)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        # Save the new post (but don't commit yet)
        new_comment = comment_form.save(commit=False)

        # Associate the new post with the current profile (author)
        new_comment.author = author
        new_comment.post = post
        new_comment.save()
        # Redirect to the profile page (or wherever you want)
        return HttpResponseRedirect(reverse('hubspace:profile_page', args=[profile_id]))
    else:
        # If the form is invalid, re-render the form with error messages
        return render(request, 'hubspace/new_comment.html', {'form': comment_form, 'author': author, 'post' : post})
