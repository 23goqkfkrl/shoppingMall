from django.shortcuts import render
from items.models import Post

# Create your views here.
def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_posts':recent_posts
        }
    )

def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )

def company(request):
    return render(
        request,
        'single_pages/company.html'
    )