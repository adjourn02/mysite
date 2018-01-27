from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from blogs.forms import ContactForm
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Country, Place, Post

def index(request):
    context = {
        'latest': Post.objects.order_by("-pub_date")[:3],
        'popular': Post.objects.filter(popular=True),
        'featured': Post.objects.filter(featured=True),
    }

    return render(request, 'blogs/index.html', context)

def blog(request, post_slug):
    p = get_object_or_404(Post, slug=post_slug)
    try:
        next_post = Post.objects.get(id=p.id+1)
    except Post.DoesNotExist:
        next_post = Post.objects.get(id=p.id-1)
    context = {
        'latest': Post.objects.order_by("-pub_date")[:3],
        'post': p,
        'post_slug': p.slug,
        'next_post': next_post,
    }

    return render(request, 'blogs/blog.html', context)

def contact(request):
    latest = Post.objects.order_by("-pub_date")[:3]
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                sender = from_email+"<"+from_email+">"
                send_mail(subject, message, sender, ['thelostjuanderer@gmail.com'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            form = ContactForm()
            return render(request, 'blogs/contact.html', {'latest':latest,'form': form,'flash': "email sent successfully!",})
        else:
            return render(request, 'blogs/contact.html', {'latest': latest, 'form': form, 'flash': "some fields are incomplete or incorrect",})			

    return render(request, 'blogs/contact.html', {'latest':latest,'form': form,})
