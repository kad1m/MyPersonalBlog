from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm, SignupForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.conf import settings

# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_activate = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account!'
            message = render_to_string(
                'registration/acc_active_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                }
            )
            to_email = form.cleaned_data['email']
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email,])
            return HttpResponse('Please confirm your email address to complete the registration.')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64).decode('utf-8'))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def post_list(request):
    posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(posts_list, 10)
    categories = Category.objects.all()
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/post_list.html', {'posts': posts, 'categories': categories})


def post_detail(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.get(pk=pk)
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        categories = Category.objects.all()
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'categories': categories})


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.image = form.cleaned_data['image']
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    categories = Category.objects.all()
    posts_list = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/post_draft_list.html', {'posts': posts, 'categories': categories})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()

    return redirect('post_list')

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve_comment()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def category_post(request, category):
    categories = Category.objects.all()
    posts_list = Post.objects.filter(category__category=category).filter(published_date__isnull=True).order_by('-published_date')
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/category.html', {'posts': posts, 'category': category, 'categories': categories})