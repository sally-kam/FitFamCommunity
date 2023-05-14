from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, PostForm, CommentForm, EditProfileForm
from .models import Profile, Comment
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
import requests
import json
import uuid
import boto3
import os
# Create your views here.
# iDY/ohuCxpLGD4yb3YtGVA==1LV8KxQR4T6PSsMs
# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def food_calorie_counter(request):
    if request.method == 'POST':
        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(api_url + query, headers={'X-Api-Key': 'iDY/ohuCxpLGD4yb3YtGVA==1LV8KxQR4T6PSsMs'})
        try:
            food = json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            food = "Search Error!"
            print(e)
        return render(request, 'resources/food_calorie_counter.html', {'food': food})
    else:
        return render(request, 'resources/food_calorie_counter.html', {'query': 'Enter a valid query'})



class ProfileDetail(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profile/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Return the profile of the currently logged-in user
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        posts = user.posts.all()  # Retrieve all posts belonging to the user
        context['posts'] = posts
        context['comment_form'] = CommentForm()
        return context





class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['liked'] = False

        if self.request.user.is_authenticated:
            user = self.request.user

            # Loop over the posts and check if the user has liked each post
            for post in context['posts']:
                if post.likes.filter(id=user.id).exists():
                    post.liked = True

        return context
      


class SignUp(generic.CreateView):
  form_class = SignUpForm
  success_url = reverse_lazy('posts_index')
  template_name = 'registration/signup.html'

  def form_valid(self, form):
      response = super().form_valid(form)
      print(form.cleaned_data)
      Profile.objects.create(
         user=self.object, 
         date_of_birth=form.cleaned_data['date_of_birth'], 
         bio=form.cleaned_data['bio'])
      print("self.object", self.object)
      login(self.request, self.object)
      return response

  def form_invalid(self, form):
      return self.render_to_response(self.get_context_data(form=form, error_message='Invalid sign up - try again'))


class EditProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'registration/edit_profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('profile_detail')

    def form_valid(self, form):
        # Get the profile instance
        profile = form.instance

        # Handle file upload and storage logic here
        profile_pic = self.request.FILES.get('profile_pic', None)
        if profile_pic:
            s3 = boto3.client('s3')
            # Generate a unique key for the file
            key = uuid.uuid4().hex[:6] + profile_pic.name[profile_pic.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(profile_pic, bucket, key)
                # Build the full URL for the uploaded file
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                # Assign the URL to the profile_pic field
                profile.profile_pic = url
            except Exception as e:
                print('An error occurred uploading file to AWS S3')
                print(e)

        # Save the profile instance
        return super().form_valid(form)



class EditSettings(LoginRequiredMixin, UpdateView):
  model = User
  template_name = 'registration/edit_settings.html'
  fields = ['username', 'first_name', 'last_name', 'email']
  success_url = reverse_lazy('profile_detail') 

def get_object(self, queryset=None):
        return self.request.user

def form_valid(self, form):
        response = super().form_valid(form)
        # Perform any additional processing or redirect logic
        return response

class EditPassword(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/edit_password.html'
    success_url = reverse_lazy('profile_detail')

   

class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['liked'] = False

        post = self.object
        user = self.request.user
        context['liked'] = post.likes.filter(id=user.id).exists()

        return context




class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  form_class = PostForm

class PostDelete(LoginRequiredMixin, DeleteView):
  model = Post
  success_url = '/posts'

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('posts_index'))

@login_required
def like_post2(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(reverse('posts_detail', kwargs={'pk': pk}))

def like_post3(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(reverse('profile_detail'))



class CommentCreate(LoginRequiredMixin,CreateView):
   model = Comment
   form_class = CommentForm


   def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.user = self.request.user  
        return super().form_valid(form)

   def get_success_url(self):
        return reverse_lazy('posts_index')
   
class CommentCreate2(LoginRequiredMixin,CreateView):
   model = Comment
   form_class = CommentForm


   def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.user = self.request.user  
        return super().form_valid(form)

   def get_success_url(self):
        return reverse_lazy('posts_detail', kwargs={'pk': self.kwargs['pk']})
   
class CommentCreate3(LoginRequiredMixin,CreateView):
   model = Comment
   form_class = CommentForm


   def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.user = self.request.user  
        return super().form_valid(form)

   def get_success_url(self):
        return reverse_lazy('profile_detail')
   



class CommentDelete(LoginRequiredMixin, DeleteView):
  model = Comment
  success_url = reverse_lazy('posts_index')

class CommentDelete2(LoginRequiredMixin, DeleteView):
  model = Comment

  def get_success_url(self):
        post_pk = self.kwargs['post_pk']  # retrieve the post pk from the URL
        return reverse('posts_detail', kwargs={'pk': post_pk})
  
class CommentDelete3(LoginRequiredMixin, DeleteView):
  model = Comment

  def get_success_url(self):
        post_pk = self.kwargs['post_pk']  # retrieve the post pk from the URL
        return reverse('profile_detail')


# def unlike_post(request, pk):
#    post = get_object_or_404(Post, pk=pk)
#    post.likes.remove(request.user)
#    return redirect('post_detail', pk=pk)
# class CommentUpdate(LoginRequiredMixin, UpdateView):
#   model = Comment
#   form_class = CommentForm
