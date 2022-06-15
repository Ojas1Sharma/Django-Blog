import imp
from re import template
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from matplotlib.pyplot import cla
from matplotlib.style import context
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.http import HttpResponse
# Create your views here.

# posts=[
#     {'author':'corey',
#     'title':'blog post 1',
#     'content':'first post content',
#     'date_posted':'aug 27 2022'},
    
#     {'author':'jenney',
#     'title':'blog post 2',
#     'content':'second post content',
#     'date_posted':'feb 23 2020'}



# ]



def home(request):
    # return HttpResponse('<h1> Blog Home </h1>')
    context={
        'posts':Post.objects.all()
    }

    
    return render(request,'blog/home.html',context)


def about(request):
    # return HttpResponse('<h1> Blog About</h1>')
    return render(request,'blog/about.html',{'title':'About'})




# class based view
#list view,detail view, create , update, delete etc
# list view-->home
class PostListView(ListView):
    model=Post
    template_name='blog/home.html'
    # <app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5

class UserPostListView(ListView):
    model=Post
    template_name='blog/user_posts.html'
    # <app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5
    def get_queryset(self):
        user=get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')




class PostDetailView(DetailView):
    model=Post
   
class PostCreateView(LoginRequiredMixin, CreateView):
    model=Post
    fields=['title', 'content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
   
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model=Post
    fields=['title', 'content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
   
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False