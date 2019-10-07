from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/latest_posts.html')
def latest_posts(count=5):
    latest_posts = Post.published.order_by('-pub_date')[:count]
    return {'latest_posts':latest_posts}

@register.simple_tag
def popular_posts(count=5):
    return Post.published.annotate(
                    total_comments=Count('comments')
                ).order_by('-total_comments','-pub_date')[:count]
