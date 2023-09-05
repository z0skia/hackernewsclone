import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Story, Vote, Comment
from .forms import StoryForm, CommentForm

def home(request):
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    stories = Story.objects.filter(created_at__gte=date_from).order_by('-number_of_votes')[0:30]

    return render(request, 'home.html', {'stories':stories})

def newest(request):
    stories = Story.objects.all()[0:200]

    return render(request, 'newest.html', {'stories':stories})

def story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.story = story
            comment.created_by = request.user
            comment.save()

            return redirect('story', story_id=story_id)
    else:
        form = CommentForm()

    return render(request, 'detail.html', {'story': story,'form':form})

@login_required
def vote(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    next_page = request.GET.get('next_page', '')

    if story.created_by != request.user and not Vote.objects.filter(created_by=request.user, story=story):
        vote = Vote.objects.create(story=story, created_by=request.user)

    if next_page == 'story':
        return redirect('story', story_id=story_id)
    else: 
        return redirect('home')


@login_required
def submit(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)

        if form.is_valid():
            story = form.save(commit=False)
            story.created_by = request.user
            story.save()

            return redirect('home')
    
    else:
        form = StoryForm()
    
    return render(request, 'submit.html', {'form':form})


