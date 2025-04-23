from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse
from .models import Profile, Post, Comment, Picture
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

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

@login_required
def profile_page(request, id):
    """Shows a profiles page"""
    # Fetch the Profile object based on 'id'
    profile = get_object_or_404(Profile, id = id)
    is_following = request.user.profile.isfollowing(profile)
    posts = profile.posts.all()
    pictures = profile.pictures.all()
    # store it in a 'context dictionary', to give the html
    context = {'profile' : profile, 'posts' : posts, 'pictures' : pictures, 'is_following' : is_following}
    return render(request, 'hubspace/profile.html', context)


def new_post(request, id):
    """Profile adds a new post, containing text, and optional picture"""
    # Fetch the Profile object based on 'id'
    profile = get_object_or_404(Profile, id=id)

    # Handle GET request (display empty form)
    if request.method != 'POST':
        post_form = PostForm()
        context = {'form': post_form, 'profile': profile}
        return render(request, 'hubspace/new_post.html', context)

    # Handle POST request (form submission)
    post_form = PostForm(request.POST, request.FILES)
    if post_form.is_valid():
        # Save the new post (but don't commit yet)
        new_post = post_form.save(commit=False)
        # Associate the new post with the current profile (author)
        new_post.author = profile
        # Save the post
        new_post.save()

        # handle if an Picture instance has been passed in
        image = request.FILES.get('image')
        if image:
            Picture.objects.create(file=image, author=profile, post=new_post,caption=new_post.text)
        # Redirect to the profile page (or wherever you want)
        return HttpResponseRedirect(reverse('hubspace:profile_page', args=[id]))
    else:
        # If the form is invalid, re-render the form with error messages
        return render(request, 'hubspace/new_post.html', {'form': post_form, 'profile': profile})


def new_comment(request, profile_id, post_id):

    # extract important information into variables

    author = get_object_or_404(Profile, id = request.user.profile.id)
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
    
def redirect_to_profile(request):
    profile = request.user.profile
    return redirect('hubspace:profile_page', id = profile.id)

def follow_profile(request, profile_id):
    profile = get_object_or_404(Profile, id = profile_id)
    request.user.profile.follow(profile)
    return redirect(reverse('hubspace:profile_page', args=[profile_id]))

def unfollow_profile(request, profile_id):
    profile = get_object_or_404(Profile, id = profile_id)
    request.user.profile.unfollow(profile)
    return redirect(reverse('hubspace:profile_page', args=[profile_id]))




"""def new_picture(request, id):


    # extract important information into variables

    author = get_object_or_404(Profile, id = request.user.profile.id)


    # Handle GET request (display empty form)
    if request.method != 'POST':
        picture_form = PictureForm()
        context = {'form': picture_form, 'author': author}
        return render(request, 'hubspace/new_picture.html', context)

    # Handle POST request (form submission)
    picture_form = PictureForm(request.POST, request.FILES)
    if picture_form.is_valid():
        # Save the new post (but don't commit yet)
        new_picture = picture_form.save(commit=False)

        # Associate the new post with the current profile (author)
        new_picture.author = author
 
        new_picture.save()
        # Redirect to the profile page (or wherever you want)
        return HttpResponseRedirect(reverse('hubspace:profile_page', args=[id]))
    else:
        # If the form is invalid, re-render the form with error messages
        print(picture_form.errors)
        return render(request, 'hubspace/new_picture.html', {'form': picture_form, 'author': author})
        """
    

def home(request):       
    """Home page. This contains a form for you to make a post, and all the posts made recently by profiles the user is following"""

    # get user profile and get their followed profiles
    active_profile = get_object_or_404(Profile, id = request.user.profile.id)
    followed_profiles = active_profile.following.all()
    
    # get posts from all followed profiles, ordering by datepublished
    posts = Post.objects.filter(author__in=followed_profiles).order_by('-datePublished')
    context = {'posts': posts} 

    # Request if get, so just show the user this html page
    if request.method == 'GET':
        post_form = PostForm()
        context['form'] = post_form
        return render(request, 'hubspace/home.html', context)

    # request is post, so save the user filled form, and redirect to the home page.
    elif request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user.profile
            new_post.save()
            return render(request, 'hubspace/home.html', context)
        
def index(request):
    return render(request, 'hubspace/index.html')

def profile_pictures(request, id):
    profile = get_object_or_404(Profile, id=id)
    pictures = profile.pictures.all()
    context = {'pictures' : pictures, 'profile' : profile}
    return render(request, 'hubspace/profile_picture_set.html', context)

def set_profile_picture(request, profile_id, picture_id):
    profile = get_object_or_404(Profile, id=profile_id)
    picture = get_object_or_404(Picture, id=picture_id)
    profile.profilePicture = picture
    profile.save()
    return redirect(reverse('hubspace:profile_page', args=[profile_id]))