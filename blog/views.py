from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Count
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import messages
from taggit.models import Tag
from .models import Post
from .forms import ShareForm,CommentForm
# Create your views here.

def post_list(req,tag_slug=None):
    obj_list  = Post.published.order_by('-pub_date')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        obj_list = Post.published.filter(tags__in=[tag]).order_by('-pub_date')
    paginator = Paginator(obj_list,4)
    page      = req.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts':posts,
        'page':page,
        'tag':tag
    }

    return render(req,'blog/post_list.html',context)

def post_detail(req,slug):
    post = get_object_or_404(Post,slug=slug)
    comments = post.comments.filter(active=True).order_by('-created')
    comment_form = CommentForm(req.POST or None)
    if req.user:
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = req.user.author
            comment.post = post
            comment.save()
            messages.success(req,'Your Comment has been Added!')
            return redirect('blog:detail',slug=post.slug)
    else:
        return HttpResponse('PLz Login First!')
    tags = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=tags).exclude(id=post.id)
    similar_posts =similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-pub_date')
    context = {
        'post':post,
        'comments':comments,
        'comment_form':comment_form,
        'similar_posts':similar_posts,
    }
    return render(req,'blog/post_detail.html',context)

def post_share(req,slug):
    post = get_object_or_404(Post,slug=slug)
    form = ShareForm(req.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        to = form.cleaned_data.get('to')
        comment = form.cleaned_data.get('comment')
        post_url = req.build_absolute_uri(post.get_absolute_url())
        subject = '{} ({}) Recommends you reading {}'.format(name,email,post.title)
        body = 'You can read {} at {}. \n\n {}\'s Comments are: {}'.format(post.title,post_url,name,comment)

        send_mail(subject,body,email,[to],fail_silently=False)
        messages.success(req,'A "{}" share link has been emailed to {} '.format(post.title,to))
        return redirect('blog:share',post.slug)

    return render(req,'blog/post_share.html',{'form':form,'post':post})
