from django.shortcuts import render, redirect, get_object_or_404
from .models import Story, Comments, Stydno, NeStydno, Proud
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import CommentsForm, StoryForm


def main(request):
    count = Story.objects.count()
    storys = Story.objects.order_by('-id')
    for story in Story.objects.order_by("date"):
        story.tags.add(str(story.date.strftime('%m/%d/%Y')))
    comments = Comments.objects.order_by("-date")

    context = {'count': count,
               'storys': storys,
               'user': auth.get_user(request),
               'comments': comments,
               }
    return render(request, 'index.html', context)


def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def story_inf(request, id):
    story = get_object_or_404(Story, pk=id)
    return render(request, 'strory_inf.html', {'story': story})


def comments(request, id):
    comments = Comments.objects.filter(story__id=id)
    form = CommentsForm(request.POST)
    story = get_object_or_404(Story, pk=id)
    if request.method == 'POST':
        if form.is_valid():
            new_com = Comments.objects.create(
                story=get_object_or_404(Story, pk=id), user=auth.get_user(request), text=form.cleaned_data['comment'])
            new_com.save()
            return redirect(request.path_info)
    return render(request, 'comments.html',
                  {'comments': comments, 'form': form, 'story': story, 'user': auth.get_user(request)})


def write(request):
    form = StoryForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            new_story = Story.objects.create(title=form.cleaned_data['title'], story=form.cleaned_data['story'])
            new_story.tags.add(form.cleaned_data['tags'])
            new_story.save()
            return redirect('/')
    return render(request, 'write.html', {'form': form})


def styd(request, story_id):
    p_exist = Proud.objects.filter(user=request.user, story=get_object_or_404(Story, pk=story_id)).exists()
    n_exist = NeStydno.objects.filter(user=request.user, story=get_object_or_404(Story, pk=story_id)).exists()
    if not p_exist and not n_exist:
        new_like, created = Stydno.objects.get_or_create(user=request.user, story=get_object_or_404(Story, pk=story_id))
        if not created:
            new_like.delete()
        else:
            new_like.save()
    return redirect('/')


def nestryd(request, story_id):
    s_exist = Stydno.objects.filter(user=request.user, story=get_object_or_404(Story, pk=story_id)).exists()
    p_exist = Proud.objects.filter(user=request.user, story=get_object_or_404(Story, pk=story_id)).exists()
    if not s_exist and not p_exist:
        new_like, created = NeStydno.objects.get_or_create(user=request.user, story=get_object_or_404(Story, pk=story_id))
        if not created:
            new_like.delete()
        else:
            new_like.save()
    return redirect("/")


def proud(request, story_id):
    s_exist = Stydno.objects.filter(user=request.user, story=get_object_or_404(Story, pk=story_id)).exists()
    n_exist = NeStydno.objects.filter(user=request.user, story=get_object_or_404(Story, pk=story_id)).exists()
    if not s_exist and not n_exist:
        new_like, created = Proud.objects.get_or_create(user=request.user, story=get_object_or_404(Story, pk=story_id))
        if not created:
            new_like.delete()
        else:
            new_like.save()

    return redirect("/")
