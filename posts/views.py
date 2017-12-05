from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404

def random(request):
    return render(request, 'random.html')

def post_create(request):
    if not request.user.is_staff:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Awesome, you just added a blog post!")
        return redirect("more:list")
    context = {
        "form": form
    }
    return render(request, 'post_create.html', context)

def post_update(request, post_id):
    item = Post.objects.get(id=post_id)
    form = PostForm(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        form.save()
        messages.info(request, "Hey, you just changed a blog post!")
        return redirect("more:detail", post_id=item.id)
    context = {
        "form": form,
        "item":item,
    }
    return render(request, 'post_update.html', context)

def post_delete(request, post_id):
    Post.objects.get(id=post_id).delete()
    messages.warning(request, "Noooooooooo!")
    return redirect("more:list")

def some_function(request):
    some_dictionary = {
        "some_key": "with a random value",
    }
    return render(request, "something.html", some_dictionary)


def post_list(request):
    objects = Post.objects.all()
    # objects = Post.objects.all().order_by('title', 'id')
    paginator = Paginator(objects, 5)

    number = request.GET.get('page')

    try:
        objects = paginator.page(number)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    context = {
        "post_items": objects,
    }
    return render(request, "list.html", context)

def post_detail(request, post_id):
    # item = Post.objects.get(id=1000)
    item = get_object_or_404(Post, id=post_id)
    context = {
        "item": item,
    }
    return render(request, "detail.html", context)

