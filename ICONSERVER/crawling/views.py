from .models import Post
from django.shortcuts import render

def index(request):
    a = 20190217
    posts = list(Post.objects.filter(date=a))
    return render(request, 'crawling/index.html', {'posts' : posts})