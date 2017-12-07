from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Country, Place, Post

def index(request):
    context = {
        'places': Place.objects.all(),
        'latest': Post.objects.order_by("-pub_date")[:3],
        'popular': Post.objects.filter(popular=True),
        'featured': Post.objects.filter(featured=True),
    }

    return render(request, 'blogs/index.html', context)

def blog(request, place_id):
    p = get_object_or_404(Place, pk=place_id)
    context = {
        'places': Place.objects.all(),
        'posts': p.post_set.all(),
    }

    return render(request, 'blogs/blog.html', context)